# Geode Architecture & Implementation Guide

This document details the technical implementation of the Geode Framework. It explains how the launcher, memory system, and personas interact to create a stateful AI environment.

## 1. Directory Structure

Geode separates **System Logic** (The Framework) from **User Data** (Knowledge).

### A. The Framework (`geode/`)
This repository contains the immutable logic of the system.
```text
geode/
├── bin/
│   └── geode               # The Launcher (Bash script)
├── core/
│   └── CORE_PERSONA.md     # Universal standards (Inherited by all Personas)
├── personas/               # The Identity Files
│   ├── sys.md              # Framework Administrator
│   └── general.md          # Default Assistant
├── tools/
│   ├── save_session.py     # The Clean Logger
│   └── cleanup_sessions.sh # The Maintenance Script
└── install.sh              # Setup Utility
```

### B. The Knowledge Base (`~/gemini_knowledge/`)
This directory is created in the user's home folder and stores the state.
```text
~/gemini_knowledge/
├── blueprints/             # Static reference files (e.g., Network Maps)
└── sessions/               # The "Memory Bank"
    ├── sys/                # Logs for the Admin persona
    ├── general/            # Logs for the General persona
    └── archive/            # Rotated logs (>30 days old)
```

## 2. Core Components

### A. The Launcher (`bin/geode`)
The `geode` command is the single entry point. It orchestrates the session lifecycle:
1.  **Resolution:** Identifies the requested persona (e.g., `thm`).
2.  **Context Injection:** It dynamically concatenates `core/CORE_PERSONA.md` + `personas/thm.md` into a temporary system prompt (`~/.geode/system_thm_PID.md`).
    *   *Why?* This ensures every persona inherits the Core Standards (Startup protocols, Memory rules) without code duplication.
    *   *Safety:* Uses Process IDs (PID) to allow multiple concurrent Geode sessions in different terminals.
3.  **Execution:** Launches the native `gemini` CLI with the injected system prompt.
4.  **Teardown:** Upon exit, it triggers the Memory Saver.

### B. The Memory Saver (`tools/save_session.py`)
Standard terminal recording (`script`) captures "noise" (spinners, progress bars, backspaces). Geode uses a custom Python hook that:
1.  Parses the internal JSON logs from the Gemini CLI.
2.  Extracts the clean conversation (User Prompt + AI Response).
3.  Formats "Thought Processes" into collapsible HTML/Markdown details.
4.  Saves the clean file to `~/gemini_knowledge/sessions/[persona]/`.

### C. The Maintenance Cycle (`tools/cleanup_sessions.sh`)
To prevent the "active memory" from becoming too large (which slows down reading), Geode includes a **Lazy Maintenance Trigger**:
*   Every time `geode` runs, it checks `~/.geode/last_clean`.
*   If >24 hours have passed, it spawns `cleanup_sessions.sh` in the background.
*   Old sessions (>30 days) are moved to `archive/YYYY-MM/`.

## 3. Workflow & Evolution

### The "System Admin" Persona (`sys`)
Geode includes a built-in "Meta-Persona" called `sys`. It has explicit knowledge of this architecture.
*   **Role:** Architect & Maintainer.
*   **Capabilities:**
    *   It can read and edit the `geode` launcher script.
    *   It can create new files in `personas/`.
    *   It can diagnose issues with `save_session.py`.

### Evolving the System
The intended workflow for upgrading Geode is **User-Led Evolution**:
1.  **Identify Friction:** "Geode is failing to save logs when I use Ctrl+C."
2.  **Consult Admin:** `geode sys` -> "Analyze the launcher script and fix the trap logic."
3.  **Review PR:** The AI proposes the Bash code fix.
4.  **Apply:** The user applies the fix (or uses a tool to write it).
