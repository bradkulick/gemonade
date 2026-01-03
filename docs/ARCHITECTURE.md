# Gemonade Architecture & Implementation Guide

This document details the technical implementation of the Gemonade Framework. It explains how the launcher, memory system, and package architecture interact to create a stateful AI environment.

## 1. Directory Structure

Gemonade adopts a "Unified Package" architecture, treating all identities—from core system admins to community extensions—as standardized packages called **Gems**.

### A. The Framework (`gemonade/`)
This repository contains the system logic and package definitions.
```text
gemonade/
├── bin/
│   └── gemonade               # The Launcher (Bash script)
├── core/
│   └── CORE_PERSONA.md        # Universal standards (Inherited by all Personas)
├── packages/                  # The Identity Packages
│   ├── core/                  # Immutable System Personas (sys, general)
│   ├── installed/             # Community/3rd-Party Gems (Git Clones)
│   └── local/                 # User-Created Private Gems
├── knowledge/                 # The "Active State"
│   └── sessions/              # Session Logs
├── user_tools/                # Global User Scripts
└── tools/                     # System Maintenance Scripts
```

### B. The Gem Model (Package)
Every persona is a self-contained directory within `packages/`.
```text
packages/local/my-gem/
├── gem.json                # (V2) The Manifest & Metadata
├── persona.md              # The Identity Prompt
├── requirements.txt        # (V2) Python dependencies
├── .venv/                  # (V2) Isolated Virtual Environment (Auto-generated)
├── tools/                  # (Optional) Python scripts specific to this persona
└── blueprints/             # (Optional) Reference docs/knowledge
```

## 2. Core Components

### A. The Launcher (`bin/gemonade`)
The `gemonade` command is the single entry point. It orchestrates the session lifecycle:

1.  **Resolution & Priority:** Identifies the requested persona by searching namespaces in specific order: `local` > `installed` > `core`.
2.  **Hydration (V2):** Checks if the Gem has a `.venv` directory.
    *   If yes, it prepends `.venv/bin` to the `$PATH` so `python3` calls use the isolated libraries.
    *   If missing but `requirements.txt` exists, it warns the user or auto-hydrates (depending on command).
3.  **Context Injection:** It dynamically concatenates `core/CORE_PERSONA.md` + `packages/.../persona.md`.
4.  **Tool Discovery:** Prepend `tools/` to the session's `$PATH`.
5.  **Execution:** Launches the native `gemini` CLI.

### B. The Memory Saver (`tools/save_session.py`)
Standard terminal recording (`script`) captures "noise". Gemonade uses a custom Python hook that:
1.  Parses the internal JSON logs from the Gemini CLI.
2.  Extracts the clean conversation (User Prompt + AI Response).
3.  Formats "Thought Processes" into collapsible HTML/Markdown details.
4.  Saves the clean file to `knowledge/sessions/[persona]/`.

## 3. The Gemonade Package Standard (GPS)

To enable distribution via `gemonade install`, a package must contain a `gem.json` manifest in its root.

### Specification
```json
{
  "name": "gem-name",
  "version": "1.0.0",
  "description": "Short description of the capability.",
  "author": "Your Name",
  "python_dependencies": "requirements.txt"  // Optional. Triggers .venv creation.
}
```

### Lifecycle Commands
*   **`install <url>`:** Clones the repo, reads `gem.json`, and runs `python -m venv .venv && pip install -r requirements.txt`.
*   **`update <name>`:** Pulls the latest git changes and re-runs the pip install step.
*   **`uninstall <name>`:** Deletes the package directory (clean removal).

## 4. Workflow & Extension

### The "System Admin" Persona (`sys`)
Gemonade includes a built-in "Meta-Persona" called `sys`. It has explicit knowledge of this architecture.
*   **Role:** Architect & Maintainer.
*   **Capabilities:**
    *   It acts as a "Gem Factory," scaffolding new packages compliant with the GPS.
    *   It performs "Compatibility Checks" to ensure user requests fit the CLI paradigm.

### Extending vs. Overriding
Gemonade supports two methods for modifying behavior:

1.  **Override (Shadowing):**
    *   Creating a package with the same name in a higher-priority namespace (e.g., `packages/local/aws`) completely hides the lower-priority version (`packages/installed/aws`).
    *   *Constraint:* You cannot override `core` packages (`sys`, `general`).

2.  **Extension (Inheritance):**
    *   Create a new package (e.g., `packages/local/my-general`) and reference the original in the prompt:
        ```markdown
        # My General
        {{LOAD: ../../../core/general/persona.md}}
        - **Extra Rule:** Always speak in Haiku.
        ```
    *   *Note:* While Gemonade doesn't have a native macro language yet, users can manually inherit logic by referencing files or copying base instructions.

## 5. Lifecycle & Release Engineering

V3 introduced a formal pipeline for moving Gems from local prototypes to production-ready extensions.

### A. The Incubator (Gem-to-Extension)
The `tools/gem_2_extension.py` utility allows Gems to "graduate" into native Gemini CLI Extensions. 
*   **Transformation:** It refactors the Gemonade-specific `persona.md` and `gem.json` into the extension-native `GEMINI.md` and `gemini-extension.json`.
*   **Isolation:** It bundles dependencies and scripts while excluding framework-specific metadata.

### B. Discovery & Publishing
Gemonade treats GitHub as its decentralized package registry.
*   **Search:** `gemonade search` uses the GitHub CLI (`gh`) to query repositories tagged with the `gemonade-gem` topic.
*   **Publishing:** `tools/publish.py` automates the "bottling" process by handling SemVer version bumps, Git tagging, and applying the `gemonade-gem` topic to the repository for discovery.
