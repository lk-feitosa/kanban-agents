@echo off
title Kanban Minimalista para Maestri
cd /d "%~dp0"
echo ============================================================
echo   Iniciando Kanban Minimalista para Maestri (Porta 3334)...
echo ============================================================
python kanban.py %*
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [-] Erro ao iniciar. Pressione qualquer tecla para sair.
    pause >nul
)
