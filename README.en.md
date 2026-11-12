<div align="center">

<img src="assets/avatar.jpg" alt="Kanban Logo" width="120" style="border-radius: 14px; box-shadow: 0 8px 24px rgba(0,0,0,0.5); object-fit: cover;" onerror="this.src='assets/logo.png'" />

# kanban-agents

**Lightweight, native, project-isolated kan.bn-style minimalist agile board for Maestri Spatial Development Workspace.**

🌐 **[Português](README.md)** | **[English](README.en.md)**

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-3776AB.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Multiplatform](https://img.shields.io/badge/platform-Windows%20|%20Linux%20|%20macOS-informational.svg?style=flat-square)](#quick-start)
[![Zero Docker](https://img.shields.io/badge/docker-zero%20containers-success.svg?style=flat-square)](#key-features)
[![Zero Auth](https://img.shields.io/badge/auth-zero%20login-purple.svg?style=flat-square)](#key-features)

</div>

---

## 🌟 Overview

`kanban-agents` is a minimalist, responsive task management application designed specifically to operate as an embedded **Portal** node within the **Maestri Canvas** or directly in your local browser for individual developer workflows.

Inspired by the clean aesthetic of **kan.bn**, `kanban-agents` runs via an ultra-lightweight native Python HTTP server (< 20 MB RAM footprint), saving state atomically and deterministically directly into the **`.kanban/board.json`** file in your active workspace root — zero Docker overhead, zero external database, and zero redundant enterprise SaaS clutter.

```text
┌─────────────────────────────────────────────────────────────────┐
│                        MAESTRI CANVAS                           │
│                                                                 │
│   [ Terminal: Minerva ] ──(reads & updates)─┐                   │
│   [ Terminal: Team CODES ]                  │                   │
│                                             ▼                   │
│   [ Portal: Kanban ] <── http://127.0.0.1:3334 ── [.kanban/]    │
│            │                                                    │
│            └───(Finalize Sprint)──► [.kanban/board.json]        │
└─────────────────────────────────────────────────────────────────┘
```

---

## ✨ Key Features in this Version

- **🎨 Minimalist Black & Grey Design (kan.bn Aesthetic)**:
  - Neutral high-contrast dark palette: Canvas at `#141414`, columns at `#1c1c1c`, and elevated cards at `#252525` with hover at `#2e2e2e`.
  - Zero bluish/tokyo-night tint, eliminating muddy "black on black" and ensuring crisp surface hierarchy.
  - Consolidated top header (no redundant sidebar) dedicating **100% of the screen width** to your board.
  - 36px modern square logo with profile avatar.

- **⚡ Streamlined Task Creation Modal**:
  - Clean title input, rapid description textarea, and inline action pills (Column, Members, Colored tags with palette, Priority, Checklist, Attachments).
  - Functional **"Create another"** toggle switch for seamless batch card creation without modal dismissals.

- **🔍 Full Task Detail & Activity View**:
  - Click **anywhere on the card** to open the full detail view.
  - Top breadcrumb navigation (`workspace › sprint › ID`).
  - Two-column split layout:
    - **Main (Left):** Editable title, formatted description, interactive checklist, activity history timeline, and comment box.
    - **Sidebar (Right):** Column selector, tags with color dots (*Teal, Blue, Purple, Yellow, Orange, Red, Pink*), priority badge, and **responsible member/agent tag** (without photo avatars on card faces).

- **🏷️ Dot Tags & Agent Text Badges**:
  - Tags with clean colored dot indicators (e.g. `● ARROW`).
  - Assigned agent text badge in the card footer (e.g. `Minerva`, `DevOps`).

- **🏁 Sprint Lifecycle & Automated Archiving**:
  - **"Finalize Sprint"** button: instantly archives completed cards from **Done** into the sprint history.
  - Empties the Done column for the upcoming cycle while keeping your active board focused.
  - **"Archived Sprints"** tab to review previous iterations and deliverables.

- **🖱️ Smooth Drag & Drop with Scroll Preservation**:
  - Drag cards freely across columns (**Backlog**, **To Do**, **In Progress**, **Review**, **Done**).
  - DOM diffing keeps horizontal and vertical scroll positions locked during polling.

- **📁 Isolated Workspace Context**:
  - Every project maintains its own independent `.kanban/board.json`.
  - Switching projects automatically reloads that workspace's local board.

- **🔌 Intelligent Dual-Stack Port Manager**:
  - Defaults to port **`3334`** with automatic collision-free fallback (`3335`, `3336`...) and records bindings to `.maestri/ports.json`.
  - Windows socket conflict fix (`SO_EXCLUSIVEADDRUSE`).

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
  --porta INT        HTTP port (default: 3334, with auto-fallback)
  --projeto PATH     Root path of target project workspace (default: auto-detected)
  --sem-portal       Starts web server without attempting to open Maestri Canvas portal
  -h, --help         Show help and options
```

---

## 🛠️ How It Works

### 1. Atomic Workspace Detection
`kanban.py` dynamically locates the active workspace via `MAESTRI_PROJECT_DIR`, parent Git directories, or workspace conventions.

### 2. State in `.kanban/board.json`
Active board state is persisted deterministically on disk:

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
      "titulo": "TES-3: Understanding Kanban",
      "descricao": "Agile workflow principles and continuous improvement",
      "prioridade": "alta",
      "agente": "Minerva",
      "dataVencimento": "13º nov",
      "etiquetas": [
        { "nome": "ARROW", "cor": "teal" }
      ],
      "checklist": [
        { "texto": "Define WIP limits", "concluido": true },
        { "texto": "Value stream mapping", "concluido": false }
      ]
    }
  ]
}
```

---

## 📡 REST API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` or `/index.html` | Visual Kanban board and sprint archives |
| `GET` | `/health` | Service health status and active port |
| `GET` | `/api/kanban` | Returns current board state JSON (`.kanban/board.json`) |
| `POST` | `/api/kanban` | Atomically persists board updates to disk |
| `POST` | `/api/kanban/arquivar` | Archives completed tasks and advances sprint cycle |
| `GET` | `/api/kanban/sprints` | Returns history of archived sprints |

---

## 📂 Repository Structure

```text
kanban-agents/
├── 📁 assets/                 <-- Brand identity, avatar and logo
├── 📁 publico/                <-- Modern web UI (Vanilla JS + Pure Dark CSS)
│   ├── 📁 assets/             <-- Static assets served by web app
│   └── 📄 index.html          <-- Board, task creation, detail view, archives
├── 📄 kanban.py               <-- Native HTTP server, port collision & REST API
├── 📄 iniciar-kanban.bat      <-- Interactive Windows batch launcher
├── 📄 iniciar-silencioso.vbs  <-- 100% background silent launcher
├── 📄 README.md               <-- Complete documentation in Portuguese
├── 📄 README.en.md            <-- Full documentation in English
└── 📄 .gitignore              <-- Git ignore rules
```

---

## 📄 License

Distributed under the **MIT** license. Official part of the **Minerva & Maestri** ecosystem.
