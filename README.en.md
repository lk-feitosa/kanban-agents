<div align="center">

<img src="assets/avatar.jpg" alt="Kanban Logo" width="120" style="border-radius: 18px; box-shadow: 0 8px 24px rgba(0,0,0,0.5); object-fit: cover;" onerror="this.src='assets/logo.png'" />

# kanban-agents

**Lightweight, native, project-isolated kan.bn-style minimalist agile board for the Maestri Spatial Development Workspace.**

🌐 **[Português](README.md)** | **[English](README.en.md)**

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-3776AB.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Multiplatform](https://img.shields.io/badge/platform-Windows%20|%20Linux%20|%20macOS-informational.svg?style=flat-square)](#quick-start)
[![Zero Docker](https://img.shields.io/badge/docker-zero%20containers-success.svg?style=flat-square)](#key-features)
[![Zero Auth](https://img.shields.io/badge/auth-zero%20login-purple.svg?style=flat-square)](#key-features)
[![Theme: kan.bn](https://img.shields.io/badge/theme-kan.bn%20pure%20dark-252525.svg?style=flat-square)](#key-features)

</div>

---

## 🌟 Overview

`kanban-agents` is a minimalist, responsive task management application designed specifically to operate as an embedded **Portal** node within the **Maestri Canvas** or directly in a **dedicated window on a secondary monitor** for individual developer workflows and autonomous agent tracking.

Inspired by the clean aesthetic of **kan.bn**, `kanban-agents` runs via an ultra-lightweight native Python HTTP server (< 20 MB RAM footprint), saving state atomically and deterministically directly into the **`.kanban/board.json`** file in your active workspace root — zero Docker overhead, zero external database, and zero redundant enterprise SaaS clutter.

```text
┌────────────────────────────────────────────────────────────────────────┐
│                            MAESTRI CANVAS                              │
│                                                                        │
│   [ Terminal 1: Minerva    ] ──┐                                       │
│   [ Terminal 2: Team CODES ] ──┼── (Atomic Read & Write) ────────┐     │
│   [ Terminal 3: Agy        ] ──┘                                 │     │
│                                                                  ▼     │
│   [ Active Workspace       ] ─────── [.kanban/board.json] ───────┤     │
│                                                                  │     │
│   [ Portal / Ext Monitor   ] <────── http://127.0.0.1:3334 ──────┘     │
│     ├── Agile Columns (Backlog, To Do, In Progress, Review, Done)      │
│     ├── Rapid Task Creation Modal ("Create another" batch flow)        │
│     ├── Full Task Detail View (Breadcrumbs, Checklists, Logs & Tags)   │
│     └── Sprint Lifecycle & 1-Click Automated Archiving                 │
└────────────────────────────────────────────────────────────────────────┘
```

---

## ✨ Key Features

- **🎨 Minimalist Black & Grey Design (kan.bn Aesthetic)**:
  - Strict neutral high-contrast dark palette: Canvas at `#141414`, columns at `#1c1c1c`, and elevated cards at `#252525` with hover at `#2e2e2e`.
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

### Opening as a Portal in Maestri Canvas:

In any Maestri terminal or in Minerva's terminal:
```bash
maestri portal create http://localhost:3334 "Kanban"
```

---

## 💻 Usage

In any terminal inside your Maestri workspace, run:

```bash
python kanban.py
```

The server:
1. Resolves the active project's root folder (via Git or Maestri environment).
2. Atomically loads or initializes `.kanban/board.json`.
3. Allocates a free port (default `3334`) and publishes it to `.maestri/ports.json`.
4. Opens the Portal node inside the Maestri Canvas (or in your default browser if requested).

### Command Line Options

```text
Usage: python kanban.py [OPTIONS]

Options:
  --porta INT        HTTP server port (default: 3334, with intelligent auto-fallback)
  --projeto PATH     Root path of the project to bind (default: auto-detected via git/maestri)
  --sem-portal       Start server without spawning a Portal node in Maestri
  --navegador        Automatically open Kanban in your default browser
  -h, --help         Show help message and exit
```

### Secondary Monitor Usage (Dedicated App Mode)

If you want to keep the Kanban board **permanently visible on a secondary monitor** without taking up 3D canvas space in Maestri while retaining full workspace connectivity:

1. **Start bound to a specific workspace (without opening a portal node):**
   ```bash
   python kanban.py --projeto "S:\DEV\your-project" --sem-portal --navegador
   ```
   The daemon binds to that specific directory's `.kanban/board.json`, registers the port, and launches your browser.

2. **Open as a Native WebApp (borderless window without address bar or tabs):**
   - In **Microsoft Edge**:
     ```cmd
     msedge --app=http://localhost:3334
     ```
   - In **Google Chrome**:
     ```cmd
     chrome --app=http://localhost:3334
     ```
   - In **Brave**:
     ```cmd
     brave --app=http://localhost:3334
     ```
   - Drag the window to your secondary monitor and press `F11` for continuous borderless screen (ideal as an ambient project task radar).

3. **If Kanban is already running inside Maestri:**
   - The local server is already running on the active port (default `http://localhost:3334`).
   - Simply open that URL directly on your secondary monitor (or via `msedge --app=http://localhost:3334`).
   - You can close the Portal card inside the Maestri 3D canvas to reclaim space: **the background daemon remains alive**, continuously serving and updating your secondary screen.

4. **Bi-Directional Real-Time Sync:**
   - When you or your agents (Minerva, Claude Code, Codex) add, move, or complete tasks via file or API, your dedicated screen updates seamlessly via lightweight polling (4s) with zero page reload and absolute horizontal/vertical scroll preservation.

---

## 🛠️ How It Works

### 1. Atomic Workspace Detection
`kanban.py` dynamically resolves the active project directory using `MAESTRI_PROJECT_DIR`, parent Git repositories, or standard workspace conventions.

### 2. Format of `.kanban/board.json`
The active board is stored deterministically in the workspace root:

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
      "descricao": "Agile principles and workflow specifications",
      "prioridade": "alta",
      "agente": "Minerva",
      "dataVencimento": "13º nov",
      "etiquetas": [
        { "nome": "ARROW", "cor": "teal" }
      ],
      "checklist": [
        { "texto": "Define WIP limits", "concluido": true },
        { "texto": "Map value stream", "concluido": false }
      ]
    }
  ]
}
```

### 3. Sprint Lifecycle & Archiving
When clicking **"Finalize Sprint"**:
- Cards in the **Done** column are bundled under the active sprint and appended to `sprints_arquivadas`.
- The Done column is cleared on the active board.
- The sprint counter increments automatically (e.g., `Sprint 1` ➔ `Sprint 2`).
- All deliverables remain auditable in the archived sprints modal.

### 4. Smart Port Manager & Collision Fallback
If port `3334` is occupied by another process, `kanban.py` probes sequentially until finding an open port. The bound port is idempotently recorded to `.maestri/ports.json` for zero-configuration discovery.

---

## 📡 REST API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` or `/index.html` | Visual Kanban board and sprint history |
| `GET` | `/health` | Healthcheck and active port indicator |
| `GET` | `/api/kanban` | Returns current board state JSON (`.kanban/board.json`) |
| `POST` | `/api/kanban` | Atomically updates board state |
| `POST` | `/api/kanban/arquivar` | Archives completed cards, resets Done, advances sprint |
| `GET` | `/api/kanban/sprints` | Returns history of archived sprints |

---

## 📂 Repository Structure

```text
kanban-agents/
├── 📁 assets/                 <-- Branding, avatar, and logos
├── 📁 publico/                <-- Modern web UI (Vanilla JS + Pure kan.bn Dark CSS)
│   ├── 📁 assets/             <-- Static media assets
│   └── 📄 index.html          <-- Kanban board, creation modal, detail view & sprints
├── 📄 kanban.py               <-- Native HTTP server, port manager, CLI flags & REST API
├── 📄 iniciar-kanban.bat      <-- Interactive launcher for Windows
├── 📄 iniciar-silencioso.vbs  <-- 100% background silent launcher (no console window)
├── 📄 README.md               <-- Complete documentation in Portuguese
├── 📄 README.en.md            <-- Full documentation in English
└── 📄 .gitignore              <-- Git exclusion rules
```

---

## 🔒 Security & Privacy

- **100% Local Execution**: The server binds strictly to `127.0.0.1` (localhost). No task descriptions, comments, or telemetry leave your machine.
- **Atomic Disk Writes**: State files are saved using atomic replacement (write to temp file then atomic rename), preventing corrupted JSON files even during power loss.
- **Full Data Ownership**: Your board data resides inside your project repository. You control whether `.kanban/` is committed to Git.

---

## 📄 License & Credits

Distributed under the **MIT** License.

Inspired by [kan.bn](https://kan.bn) and built as an integral part of the **Minerva & Maestri** productivity ecosystem.
