#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kanban Minimalista do Projeto — Servidor Local & Plugin para Maestri.

Servidor HTTP nativo em Python, leve (zero Docker, zero npm), anti-colisão de portas,
integrado diretamente com o arquivo `.kanban/board.json` na raiz do projeto ativo.
Suporta arquivamento de sprints finalizadas e limpeza da coluna de concluídos.
"""

import argparse
import http.server
import json
import os
import re
import socket
import socketserver
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlparse

RAIZ = Path(__file__).resolve().parent
PASTA_PUBLICO = RAIZ / "publico"
PORTA_PADRAO = 3334
FLAGS_SEM_JANELA = getattr(subprocess, "CREATE_NO_WINDOW", 0)

ESTADO = {
    "porta_ativa": PORTA_PADRAO,
    "projeto_dir": None,
}


def localizar_projeto_ativo(caminho_informado=None):
    """Descobre a raiz do projeto ativo."""
    if caminho_informado:
        p = Path(caminho_informado).resolve()
        if p.exists():
            return p

    env_proj = os.environ.get("MAESTRI_PROJECT_DIR") or os.environ.get("PROJECT_DIR")
    if env_proj and Path(env_proj).exists():
        return Path(env_proj).resolve()

    cwd = Path.cwd().resolve()
    for pasta in [cwd, *cwd.parents]:
        if (pasta / ".kanban").exists() or (pasta / ".agents").exists() or (pasta / ".git").exists():
            return pasta

    candidatos = [
        Path("S:/DEV/test-maestri"),
        Path("S:/DEV/minerva-workspace"),
        Path("S:/DEV/agents"),
    ]
    for c in candidatos:
        if c.exists():
            return c

    return cwd


def obter_ou_criar_board(projeto_dir):
    """Lê .kanban/board.json ou cria o quadro inicial limpo."""
    pasta_kanban = projeto_dir / ".kanban"
    pasta_kanban.mkdir(parents=True, exist_ok=True)
    board_path = pasta_kanban / "board.json"

    if board_path.exists():
        try:
            return json.loads(board_path.read_text(encoding="utf-8", errors="ignore"))
        except Exception:
            pass

    nome_proj = projeto_dir.name or "Projeto"
    agora = datetime.now(timezone.utc).isoformat()
    novo_board = {
        "versao": 2,
        "workspace": str(projeto_dir),
        "titulo": f"Kanban: {nome_proj}",
        "atualizadoEm": agora,
        "sprint_atual": "Sprint 1",
        "sprints_arquivadas": [],
        "colunas": [
            {"id": "col-backlog", "titulo": "Backlog", "cor": "#64748b"},
            {"id": "col-todo", "titulo": "A Fazer", "cor": "#38bdf8"},
            {"id": "col-progresso", "titulo": "Em Progresso", "cor": "#fbbf24"},
            {"id": "col-revisao", "titulo": "Revisão", "cor": "#a855f7"},
            {"id": "col-concluido", "titulo": "Concluído", "cor": "#22c55e"},
        ],
        "cartoes": [
            {
                "id": "card-01",
                "colunaId": "col-todo",
                "titulo": "KB-001: Alinhamento de Arquitetura e Escopo",
                "descricao": "Definição de especificações técnicas, ADRs e regras do projeto com a Minerva",
                "prioridade": "alta",
                "agente": "Minerva",
                "etiquetas": ["arquitetura", "planejamento"],
                "sprint": "Sprint 1",
                "criadoEm": agora,
                "checklist": [
                    {"texto": "Definir requisitos e escopo do MVP", "concluido": True},
                    {"texto": "Registrar ADR inicial em docs/adr/", "concluido": False},
                    {"texto": "Recrutar terminais do Team CODES", "concluido": False},
                ],
            }
        ],
    }

    gravar_atomico(board_path, json.dumps(novo_board, ensure_ascii=False, indent=2))
    return novo_board


def salvar_board(projeto_dir, dados):
    """Salva .kanban/board.json de forma atômica."""
    pasta_kanban = projeto_dir / ".kanban"
    pasta_kanban.mkdir(parents=True, exist_ok=True)
    board_path = pasta_kanban / "board.json"

    dados["atualizadoEm"] = datetime.now(timezone.utc).isoformat()
    dados["workspace"] = str(projeto_dir)
    gravar_atomico(board_path, json.dumps(dados, ensure_ascii=False, indent=2))


def arquivar_sprint(projeto_dir, nome_sprint=None):
    """Arquiva todas as tarefas concluídas em uma sprint finalizada e limpa a coluna de concluídos."""
    board = obter_ou_criar_board(projeto_dir)
    cartoes = board.get("cartoes") or []
    sprints_antigas = board.get("sprints_arquivadas") or []

    concluidos = [c for c in cartoes if c.get("colunaId") == "col-concluido"]
    restantes = [c for c in cartoes if c.get("colunaId") != "col-concluido"]

    sprint_nome = nome_sprint or board.get("sprint_atual") or f"Sprint {len(sprints_antigas) + 1}"
    agora = datetime.now(timezone.utc).isoformat()

    registro_sprint = {
        "id": f"sprint-{int(time.time())}",
        "nome": sprint_nome,
        "arquivadaEm": agora,
        "total_tarefas": len(concluidos),
        "tarefas": concluidos,
    }

    sprints_antigas.append(registro_sprint)
    board["sprints_arquivadas"] = sprints_antigas
    board["cartoes"] = restantes

    # Avança contador da sprint atual
    match_num = re.search(r"\d+", sprint_nome)
    if match_num:
        prox_num = int(match_num.group(0)) + 1
        board["sprint_atual"] = re.sub(r"\d+", str(prox_num), sprint_nome)
    else:
        board["sprint_atual"] = f"Sprint {len(sprints_antigas) + 1}"

    salvar_board(projeto_dir, board)
    return registro_sprint


def gravar_atomico(caminho, texto):
    """Grava em arquivo temporário e renomeia para evitar leituras pela metade."""
    caminho = Path(caminho)
    tmp = caminho.with_suffix(".tmp." + str(os.getpid()))
    try:
        tmp.write_text(texto, encoding="utf-8")
        tmp.replace(caminho)
    except Exception:
        if tmp.exists():
            tmp.unlink(missing_ok=True)
        caminho.write_text(texto, encoding="utf-8")


def porta_em_uso(porta):
    """Verifica se a porta está em uso no host."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex(("127.0.0.1", porta)) == 0


def achar_porta_inteligente(porta_base):
    """Retorna porta_base se livre; se ocupada pelo próprio Kanban, reutiliza; senão avança."""
    p = porta_base
    for tentativa in range(30):
        porta_teste = p + tentativa
        if not porta_em_uso(porta_teste):
            return porta_teste
        # Se estiver em uso, verifica se já é o Kanban
        try:
            import urllib.request
            req = urllib.request.Request(f"http://127.0.0.1:{porta_teste}/health")
            with urllib.request.urlopen(req, timeout=1.0) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    if data.get("servico") == "kanban-agents":
                        return porta_teste
        except Exception:
            pass
    return porta_base + 99


class ServidorTCPExclusivo(socketserver.ThreadingTCPServer):
    allow_reuse_address = True

    def server_bind(self):
        if sys.platform == "win32" and hasattr(socket, "SO_EXCLUSIVEADDRUSE"):
            try:
                self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
            except OSError:
                pass
        super().server_bind()


class HandlerKanban(http.server.SimpleHTTPRequestHandler):
    """Handler REST + arquivos estáticos do Kanban Minimalista."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PASTA_PUBLICO), **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        url_parsed = urlparse(self.path)
        caminho = url_parsed.path

        if caminho in ("/", ""):
            self.path = "/index.html"
            return super().do_GET()

        if caminho == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(
                json.dumps(
                    {
                        "status": "ok",
                        "servico": "kanban-agents",
                        "porta": ESTADO["porta_ativa"],
                        "projeto": str(ESTADO["projeto_dir"]),
                    }
                ).encode("utf-8")
            )
            return

        if caminho == "/api/kanban":
            proj = ESTADO["projeto_dir"] or localizar_projeto_ativo()
            board = obter_ou_criar_board(proj)
            corpo = json.dumps(board, ensure_ascii=False, indent=2).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(corpo)
            return

        if caminho == "/api/kanban/sprints":
            proj = ESTADO["projeto_dir"] or localizar_projeto_ativo()
            board = obter_ou_criar_board(proj)
            sprints = board.get("sprints_arquivadas", [])
            corpo = json.dumps(sprints, ensure_ascii=False, indent=2).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(corpo)
            return

        super().do_GET()

    def do_POST(self):
        url_parsed = urlparse(self.path)
        caminho = url_parsed.path

        if caminho == "/api/kanban":
            try:
                tamanho = int(self.headers.get("Content-Length", 0))
                payload_bruto = self.rfile.read(tamanho)
                dados_recebidos = json.loads(payload_bruto.decode("utf-8"))
                proj = ESTADO["projeto_dir"] or localizar_projeto_ativo()
                salvar_board(proj, dados_recebidos)
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(b'{"ok": true}')
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"ok": False, "erro": str(e)}).encode("utf-8"))
            return

        if caminho == "/api/kanban/arquivar":
            try:
                tamanho = int(self.headers.get("Content-Length", 0))
                payload_bruto = self.rfile.read(tamanho) if tamanho > 0 else b"{}"
                corpo = json.loads(payload_bruto.decode("utf-8")) if payload_bruto else {}
                proj = ESTADO["projeto_dir"] or localizar_projeto_ativo()
                nome_sprint = corpo.get("nome_sprint")
                resultado = arquivar_sprint(proj, nome_sprint)
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"ok": True, "arquivado": resultado}, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"ok": False, "erro": str(e)}).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()

    def log_message(self, format, *args):
        pass


def registrar_porta_projeto(projeto_dir, porta):
    """Atualiza .maestri/ports.json com a porta do Kanban."""
    try:
        pasta_maestri = projeto_dir / ".maestri"
        pasta_maestri.mkdir(parents=True, exist_ok=True)
        ports_file = pasta_maestri / "ports.json"
        dados_portas = {}
        if ports_file.exists():
            try:
                dados_portas = json.loads(ports_file.read_text(encoding="utf-8"))
            except Exception:
                pass
        dados_portas["kanban"] = {
            "porta": porta,
            "url": f"http://localhost:{porta}",
            "atualizadoEm": datetime.now(timezone.utc).isoformat(),
        }
        gravar_atomico(ports_file, json.dumps(dados_portas, indent=2))
    except Exception:
        pass


def abrir_portal_maestri(url, titulo="Kanban"):
    """Tenta abrir ou conectar o portal no Maestri Canvas."""
    try:
        from shutil import which
        cli = os.environ.get("MAESTRI_CLI") or which("maestri") or which("maestri.exe")
        if not cli and sys.platform == "win32":
            local_app_data = os.environ.get("LOCALAPPDATA", "")
            if local_app_data:
                c = Path(local_app_data) / "Programs" / "Maestri" / "resources" / "cli" / "maestri.exe"
                if c.exists():
                    cli = str(c)
        if cli:
            subprocess.run(
                [cli, "portal", "create", url, titulo],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=FLAGS_SEM_JANELA,
                timeout=5,
            )
            return True
    except Exception:
        pass
    return False


def main():
    parser = argparse.ArgumentParser(description="Servidor do Kanban Minimalista para Maestri")
    parser.add_argument("--porta", type=int, default=PORTA_PADRAO, help="Porta HTTP (padrão: 3334)")
    parser.add_argument("--projeto", type=str, default=None, help="Caminho da raiz do projeto")
    parser.add_argument("--sem-portal", action="store_true", help="Não tenta abrir portal no Maestri")
    args = parser.parse_args()

    projeto = localizar_projeto_ativo(args.projeto)
    ESTADO["projeto_dir"] = projeto

    porta = achar_porta_inteligente(args.porta)
    ESTADO["porta_ativa"] = porta

    # Garante que o quadro inicial exista
    obter_ou_criar_board(projeto)
    registrar_porta_projeto(projeto, porta)

    print(f"============================================================")
    print(f"  📋 Kanban Minimalista para Maestri")
    print(f"  🌐 URL: http://localhost:{porta}/")
    print(f"  📁 Projeto Ativo: {projeto}")
    print(f"  💾 Dados: {projeto / '.kanban' / 'board.json'}")
    print(f"============================================================")

    url_portal = f"http://localhost:{porta}/"
    if not args.sem_portal:
        abrir_portal_maestri(url_portal, "Kanban")

    try:
        srv = ServidorTCPExclusivo(("0.0.0.0", porta), HandlerKanban)
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n[+] Encerrando Kanban.")
    except Exception as e:
        print(f"[-] Erro fatal no servidor: {e}")


if __name__ == "__main__":
    main()
