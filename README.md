<div align="center">

<img src="assets/logo.png" alt="Kanban para Maestri" width="150" style="border-radius: 18px; box-shadow: 0 8px 24px rgba(0,0,0,0.4);" />

# kanban-agents

**Quadro ágil nativo, leve e isolado por projeto estilo Trello para o Maestri Spatial Development Workspace.**

🌐 **[Português](README.md)** | **[English](README.en.md)**

[![Licença MIT](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-3776AB.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Multiplataforma](https://img.shields.io/badge/plataforma-Windows%20|%20Linux%20|%20macOS-informational.svg?style=flat-square)](#início-rápido)
[![Zero Docker](https://img.shields.io/badge/docker-zero%20containers-success.svg?style=flat-square)](#destaques)
[![Zero Auth](https://img.shields.io/badge/auth-zero%20login-purple.svg?style=flat-square)](#destaques)

</div>

---

## 🌟 O que é

`kanban-agents` é um gestor de tarefas visual minimalista e funcional estilo Trello, projetado especificamente para operar como um nó de **Portal** integrado no **Maestri Canvas** ou no navegador local.

Diferente de ferramentas corporativas pesadas que demandam contêineres Docker (como kan.bn ou Taiga) e burocracia de autenticação por nuvem, o `kanban-agents` roda com um servidor nativo ultraleve em Python (< 20 MB de RAM), salvando o estado de forma atômica e versionável diretamente no arquivo **`.kanban/board.json`** na raiz do seu projeto ativo.

```text
┌─────────────────────────────────────────────────────────────────┐
│                        MAESTRI CANVAS                           │
│                                                                 │
│   [ Terminal: Minerva ] ──(lê e atualiza)──┐                    │
│   [ Terminal: Team CODES ]                 │                    │
│                                            ▼                    │
│   [ Portal: Kanban ] <── http://127.0.0.1:3334 ── [.kanban/]    │
│            │                                                    │
│            └───(Finalizar Sprint)──► [.kanban/sprints.json]     │
└─────────────────────────────────────────────────────────────────┘
```

---

## ✨ Destaques

- **🏁 Ciclos de Sprint & Arquivamento Automático**:
  - Botão **"Finalizar Sprint & Arquivar"**: arquiva instantaneamente todas as tarefas da coluna **Concluído** no histórico de sprints.
  - **Limpeza do Quadro**: a coluna de concluídos é esvaziada para a próxima sprint, mantendo o ambiente limpo e focado.
  - Aba **"📦 Sprints Arquivadas"** para auditar ciclos passados, métricas de entrega e datas a qualquer momento.

- **⚡ Zero Sobrecarga de Hardware (Sem Docker & Sem Banco de Dados)**:
  - Não consome gigabytes de RAM do Docker Desktop nem requer banco PostgreSQL.
  - Inicialização instantânea em milissegundos com consumo inferior a 20 MB de memória.

- **🖱️ Drag & Drop Fluido com Anti-Flicker & Preservação de Scroll**:
  - Arraste cartões livremente entre as colunas (**Backlog**, **A Fazer**, **Em Progresso**, **Revisão**, **Concluído**).
  - Algoritmo de diffing de JSON: o painel só toca no DOM se houver mudanças reais de dados, mantendo o scroll vertical e horizontal perfeitamente fixo mesmo com polling ativo.

- **✅ Checklists Interativos nos Cartões**:
  - Marque e desmarque subitens de entrega diretamente na face do cartão com 1 clique.
  - Barra de progresso visual colorida com cálculo de porcentagem em tempo real.

- **📁 Isolamento Completo por Workspace**:
  - Cada pasta de projeto possui seu próprio arquivo `.kanban/board.json`.
  - Ao alternar entre projetos no Maestri, o Kanban abre automaticamente o contexto do workspace ativo.

- **🔌 Gerenciador Inteligente de Portas (Anti-Colisão Dual-Stack)**:
  - Opera por padrão na porta **`3334`**. Se estiver ocupada por aplicação externa, salta automaticamente para `3335`, `3336`... e registra a porta ativa em `.maestri/ports.json`.

- **🛡️ Auto-Heal Silencioso pela Minerva**:
  - Se os portais forem recarregados ou o computador for reiniciado, a Minerva pode acionar silenciosamente o launcher (`iniciar-silencioso.vbs`) em segundo plano sem abrir janelas de console.

---

## 🚀 Início Rápido

### No Windows:

Abra o prompt de comando ou execute clicando duas vezes:
```cmd
cd S:\DEV\kanban-agents
iniciar-kanban.bat
```

Ou em **segundo plano silencioso** (sem janela preta):
```cmd
wscript iniciar-silencioso.vbs
```

### No Linux ou macOS:

```bash
cd ~/DEV/kanban-agents
python3 kanban.py
```

### Abrindo como Portal no Maestri Canvas:

Em qualquer terminal do Maestri ou no terminal da Minerva:
```bash
maestri portal create http://localhost:3334 "Kanban"
```

---

## 💻 Opções de Linha de Comando

```text
Uso: python kanban.py [OPÇÕES]

Opções:
  --porta INT        Porta HTTP do servidor (padrão: 3334, com auto-fallback inteligente)
  --projeto CAMINHO  Caminho da raiz do projeto a carregar (padrão: auto-detectado via git/maestri)
  --sem-portal       Inicia o servidor web sem tentar abrir automaticamente o nó de Portal no Maestri
  -h, --help         Exibe a mensagem de ajuda e opções
```

---

## 🛠️ Como Funciona

### 1. Detecção Atômica do Workspace
O `kanban.py` resolve dinamicamente a pasta do projeto ativo através da variável `MAESTRI_PROJECT_DIR`, do diretório Git pai ou de convenções do workspace.

### 2. Estrutura do Arquivo `.kanban/board.json`
O quadro ativo é armazenado de forma determinística e versionável na raiz do projeto:

```json
{
  "versao": 2,
  "workspace": "S:\\DEV\\meu-projeto",
  "titulo": "Kanban: meu-projeto",
  "sprint_atual": "Sprint 1",
  "sprints_arquivadas": [],
  "colunas": [
    { "id": "col-backlog", "titulo": "Backlog", "cor": "#64748b" },
    { "id": "col-todo", "titulo": "A Fazer", "cor": "#38bdf8" },
    { "id": "col-progresso", "titulo": "Em Progresso", "cor": "#fbbf24" },
    { "id": "col-revisao", "titulo": "Revisão", "cor": "#a855f7" },
    { "id": "col-concluido", "titulo": "Concluído", "cor": "#22c55e" }
  ],
  "cartoes": [
    {
      "id": "card-01",
      "colunaId": "col-todo",
      "titulo": "KB-001: Implementar Autenticação JWT",
      "descricao": "Criação de tokens e middleware de segurança",
      "prioridade": "alta",
      "agente": "Back-End Specialist",
      "etiquetas": ["backend", "auth"],
      "checklist": [
        { "texto": "Modelar tabela de usuários", "concluido": true },
        { "texto": "Implementar rota POST /auth/login", "concluido": false }
      ]
    }
  ]
}
```

---

## 📡 Endpoints da API REST

| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/` ou `/index.html` | Interface visual do quadro e histórico de sprints |
| `GET` | `/health` | Status de saúde do serviço e porta ativa |
| `GET` | `/api/kanban` | Retorna o estado JSON do quadro ativo (`.kanban/board.json`) |
| `POST` | `/api/kanban` | Grava atomicamente alterações no quadro ativo |
| `POST` | `/api/kanban/arquivar` | Arquiva tarefas concluídas, limpa o quadro e avança o ciclo de sprint |
| `GET` | `/api/kanban/sprints` | Retorna o histórico de todas as sprints arquivadas |

---

## 📂 Estrutura do Repositório

```text
kanban-agents/
├── 📁 assets/                 <-- Identidade visual e logo do ecossistema
├── 📁 publico/                <-- Interface web moderna (Vanilla JS + CSS Dark)
│   └── 📄 index.html          <-- Quadro Kanban, drag & drop e visualizador de sprints
├── 📄 kanban.py               <-- Servidor HTTP nativo, anti-colisão e API REST
├── 📄 iniciar-kanban.bat      <-- Launcher interativo para Windows
├── 📄 iniciar-silencioso.vbs  <-- Launcher 100% em segundo plano (sem janela)
├── 📄 README.md               <-- Documentação completa em Português
├── 📄 README.en.md            <-- Full documentation in English
└── 📄 .gitignore              <-- Regras de exclusão do Git
```

---

## 📄 Licença

Distribuído sob a licença **MIT**. Parte oficial do ecossistema de produtividade **Minerva & Maestri**.
