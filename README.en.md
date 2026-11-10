<div align="center">

<img src="assets/logo.png" alt="Kanban for Maestri" width="150" style="border-radius: 18px; box-shadow: 0 8px 24px rgba(0,0,0,0.4);" />

# kanban-agents

**Lightweight, native, project-isolated Trello-style agile board for Maestri Spatial Development Workspace.**

🌐 **[Português](README.md)** | **[English](README.en.md)**

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-3776AB.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Multiplatform](https://img.shields.io/badge/platform-Windows%20|%20Linux%20|%20macOS-informational.svg?style=flat-square)](#quick-start)
[![Zero Docker](https://img.shields.io/badge/docker-zero%20containers-success.svg?style=flat-square)](#key-features)
[![Zero Auth](https://img.shields.io/badge/auth-zero%20login-purple.svg?style=flat-square)](#key-features)

</div>

---

## 🌟 Overview

`kanban-agents` is a minimalist, responsive Trello-style task management application designed specifically to operate as an embedded **Portal** node within the **Maestri Canvas** or in any local web browser.

Unlike heavy enterprise tools that require Docker containers (such as kan.bn or Taiga) and cloud authentication overhead, `kanban-agents` runs via an ultra-lightweight native Python HTTP server (< 20 MB RAM footprint), saving state atomically and deterministically directly into the **`.kanban/board.json`** file in your active workspace root.

```text
┌─────────────────────────────────────────────────────────────────┐
│                        MAESTRI CANVAS                           │
│                                                                 │
│   [ Terminal: Minerva ] ──(reads & updates)─┐                   │
│   [ Terminal: Team CODES ]                  │                   │
│                                             ▼                   │
│   [ Portal: Kanban ] <── http://127.0.0.1:3334 ── [.kanban/]    │
│            │                                                    │
│            └───(Finalize Sprint)──► [.kanban/sprints.json]      │
└─────────────────────────────────────────────────────────────────┘
```

---

## ✨ Key Features

- **🏁 Sprint Lifecycle & Automated Archiving**:
  - **"Finalize Sprint & Archive"** button: instantly moves all completed tasks from the **Done** column to the permanent sprint history.
  - **Board Cleansing**: empties the Done column for the upcoming sprint, keeping your workspace clean and focused.
  - **"📦 Archived Sprints"** tab: review past sprints, delivery metrics, and completion timestamps at any time.

- **⚡ Zero Hardware Overhead (No Docker & No Database Engine)**:
  - No need to run Docker Desktop or configure PostgreSQL.
  - Instant startup in milliseconds with memory usage under 20 MB.

- **🖱️ Smooth Drag & Drop with Anti-Flicker & Scroll State Locking**:
  - Drag cards freely across columns (**Backlog**, **To Do**, **In Progress**, **Review**, **Done**).
  - JSON diffing engine: only re-renders the DOM upon genuine data changes, keeping vertical and horizontal scroll positions locked even during active polling.

- **✅ Interactive Checklists on Cards**:
  - Check and uncheck deliverable items directly on the card face with a single click.
  - Dynamic progress bar with live percentage calculation.

- **📁 Complete Workspace Isolation**:
  - Every project root maintains its own independent `.kanban/board.json`.
  - Switching projects in Maestri automatically updates the Kanban board to reflect that specific workspace.

- **🔌 Intelligent Dual-Stack Port Manager (Anti-Collision)**:
  - Defaults to port **`3334`**. If occupied by an external application, it jumps automatically to `3335`, `3336`... and records the active binding in `.maestri/ports.json`.

- **🛡️ Silent Auto-Heal via Minerva**:
  - If portals are refreshed or the machine is rebooted, Minerva can trigger the launcher silently (`iniciar-silencioso.vbs`) in the background without popups or console windows.

---

## 🚀 Quick Start

### On Windows:

Run via command prompt or double-click:
```cmd
cd S:\DEV\kanban-agents
iniciar-kanban.bat
```

Or run **silently in background** (no console window):
```cmd
wscript iniciar-silencioso.vbs
```

### On Linux or macOS:

```bash
cd ~/DEV/kanban-agents
python3 kanban.py
```

### Open as Portal on Maestri Canvas:

From any terminal in Maestri or the Minerva orchestrator:
```bash
maestri portal create http://localhost:3334 "Kanban"
```

---

## 💻 Command Line Options

```text
Usage: python kanban.py [OPTIONS]

Options:
  --porta INT        Server HTTP port (default: 3334, with smart auto-fallback)
  --projeto PATH     Active project root directory (default: auto-detected via git/maestri)
  --sem-portal       Starts the HTTP server without auto-opening a Portal node in Maestri
  -h, --help         Shows help message and exits
```

---

## 🛠️ How It Works

### 1. Workspace Resolution
`kanban.py` dynamically resolves the active project folder via the `MAESTRI_PROJECT_DIR` environment variable, parent Git directories, or standard workspace paths.

### 2. Format of `.kanban/board.json`
The board state is stored deterministically in the project root:

```json
{
  "versao": 2,
  "workspace": "S:\\DEV\\my-project",
  "titulo": "Kanban: my-project",
  "sprint_atual": "Sprint 1",
  "sprints_arquivadas": [],
  "colunas": [
    { "id": "col-backlog", "titulo": "Backlog", "cor": "#64748b" },
    { "id": "col-todo", "titulo": "To Do", "cor": "#38bdf8" },
    { "id": "col-progresso", "titulo": "In Progress", "cor": "#fbbf24" },
    { "id": "col-revisao", "titulo": "Review", "cor": "#a855f7" },
    { "id": "col-concluido", "titulo": "Done", "cor": "#22c55e" }
  ],
  "cartoes": [
    {
      "id": "card-01",
      "colunaId": "col-todo",
      "titulo": "KB-001: Implement JWT Authentication",
      "descricao": "Token generation and security middleware",
      "prioridade": "alta",
      "agente": "Back-End Specialist",
      "etiquetas": ["backend", "auth"],
      "checklist": [
        { "texto": "Define user database schema", "concluido": true },
        { "texto": "Implement POST /auth/login endpoint", "concluido": false }
      ]
    }
  ]
}
```

---

## 📡 REST API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` or `/index.html` | Visual board interface and sprint history |
| `GET` | `/health` | Health check endpoint and active port |
| `GET` | `/api/kanban` | Returns active board JSON state (`.kanban/board.json`) |
| `POST` | `/api/kanban` | Atomically persists board updates |
| `POST` | `/api/kanban/arquivar` | Archives completed tasks, cleans up Done column, and advances sprint |
| `GET` | `/api/kanban/sprints` | Returns the history of all archived sprints |

---

## 📂 Repository Structure

```text
kanban-agents/
├── 📁 assets/                 <-- Ecosystem visual identity and logo
├── 📁 publico/                <-- Modern web UI (Vanilla JS + Dark Theme CSS)
│   └── 📄 index.html          <-- Kanban board, drag & drop, and sprint viewer
├── 📄 kanban.py               <-- Native HTTP server, anti-collision, and REST API
├── 📄 iniciar-kanban.bat      <-- Interactive Windows batch launcher
├── 📄 iniciar-silencioso.vbs  <-- Silent background Windows launcher (no window)
├── 📄 README.md               <-- Full documentation in Portuguese
├── 📄 README.en.md            <-- Full documentation in English
└── 📄 .gitignore              <-- Git exclusion rules
```

---

## 📄 License

Distributed under the **MIT** license. Official component of the **Minerva & Maestri** ecosystem.
