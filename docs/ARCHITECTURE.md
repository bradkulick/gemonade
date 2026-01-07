# Gemonade Architecture & Implementation Guide

This document details the technical implementation of the Gemonade Framework. It explains how the launcher, memory system, and package architecture interact to create a stateful AI environment.

## 1. Directory Structure

Gemonade adopts a "Unified Package" architecture, treating all identities—from core system admins to community extensions—as standardized packages called **Gems**.

### A. The Framework (`gemonade/`)
This repository contains the system logic and package definitions.
```text
gemonade/
├── bin/
│   └── gemonade               # The Launcher (Bash Wrapper)
├── core/
│   ├── gemonade.py            # The Core CLI Logic (Python)
│   └── CORE_PERSONA.md        # Universal standards
├── packages/                  # The Identity Packages
│   ├── core/                  # Immutable System Personas (sys, general)
│   ├── installed/             # Community/3rd-Party Gems (Git Clones)
│   └── local/                 # User-Created Private Gems
├── knowledge/                 # The "Active State"
│   └── sessions/              # Session Logs
├── tests/                     # Integration & Unit Test Suite
├── user_tools/                # Global User Scripts
└── tools/                     # System Maintenance Scripts
```

### B. The Gem Model (Package)
Every persona is a self-contained directory within `packages/`.
```text
packages/local/my-gem/
├── gem.json                # The Manifest & Metadata
├── persona.md              # The Identity Prompt
├── requirements.txt        # Python dependencies
├── .venv/                  # Isolated Virtual Environment (Auto-generated)
├── tools/                  # (Optional) Python scripts specific to this persona
└── blueprints/             # (Optional) Reference docs/knowledge
```

## 2. Core Components

### A. The Core CLI (`core/gemonade.py`)
The `gemonade` command is now a thin Bash wrapper that bootstraps the environment and hands off execution to the Python Core (`core/gemonade.py`). This architecture ensures robustness, type safety, and deeper integration.

**Key Responsibilities:**
1.  **Resolution & Priority:** Identifies the requested persona by searching namespaces (`local` > `installed` > `core`).
2.  **Hydration (V2):**
    *   Creates isolated virtual environments (`.venv`) for Gems with dependencies.
    *   Respects `python_version` in `gem.json` to ensure compatibility.
    *   **Auto-Rollback:** Automatically cleans up corrupted environments if hydration fails.
3.  **Context Injection:** Dynamically assembles the System Prompt (Core Standards + Scope Directive + Persona Instructions).
4.  **Tool Discovery:** Prepends the Gem's `tools/` directory and `.venv/bin` to the `$PATH`.
5.  **Execution:** Launches the native `gemini` CLI with the assembled context.

### B. The Memory Saver (`tools/save_session.py`)
Standard terminal recording (`script`) captures "noise". Gemonade uses a custom Python hook that:
1.  Parses the internal JSON logs from the Gemini CLI.
2.  Extracts the clean conversation (User Prompt + AI Response).
3.  Formats "Thought Processes" into collapsible HTML/Markdown details.
4.  Saves the clean file to `knowledge/sessions/[persona]/[project_context]/`.

### C. Memory Access Scopes (V4.1)
Gemonade implements "Contextual Boundaries" to prevent session bleed and ensure data integrity. These boundaries are controlled via the `--scope` flag.

| Mode | Scope | Visibility Boundary | Default Use Case |
| :--- | :--- | :--- | :--- |
| **Project** | `project` | Restricted to `sessions/{persona}/{project_context}/` | Daily development, isolated tasks (Default). |
| **Persona** | `persona` | Access to all projects within the current Persona. | Cross-project reference, library knowledge. |
| **Global** | `global` | Unrestricted access to all sessions across all personas. | System administration, meta-analysis. |

The launcher dynamically injects a "Scope Directive" into the system prompt based on the active mode, guiding the agent's file browsing and retrieval behavior.

## 3. The Gemonade Package Standard (GPS)

To enable distribution via `gemonade install`, a package must contain a `gem.json` manifest in its root.

### Specification
```json
{
  "name": "gem-name",
  "version": "1.0.0",
  "description": "Short description of the capability.",
  "author": "Your Name",
  "python_dependencies": "requirements.txt",
  "python_version": "3.10"  // Optional. Request specific binary.
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

## 5. Lifecycle & Release Engineering

V3 introduced a formal pipeline for moving Gems from local prototypes to production-ready extensions.

### A. The Incubator (Gem-to-Extension)
The `tools/gem_2_extension.py` utility allows Gems to "graduate" into native Gemini CLI Extensions. 
*   **Transformation:** It refactors the Gemonade-specific `persona.md` and `gem.json` into the extension-native `GEMINI.md` and `gemini-extension.json`.
*   **Isolation:** It bundles dependencies and scripts while excluding framework-specific metadata.

### B. Discovery & Publishing
Gemonade treats GitHub as its decentralized package registry.
*   **Search:** `gemonade search` uses a hybrid approach:
    1.  Tries the GitHub CLI (`gh`) for authenticated, rate-limit-friendly queries.
    2.  Falls back to the public GitHub API (via `urllib`) if `gh` is missing.
*   **Publishing:** `tools/publish.py` automates the "bottling" process by handling SemVer version bumps, Git tagging, and applying the `gemonade-gem` topic to the repository for discovery.

## 6. Security & Verification

### A. Safety Barriers
The Python Core implements strict input validation to prevent malicious behavior from imported Gems.
*   **Path Containment:** All `install`, `uninstall`, and `update` operations are strictly confined to the `packages/installed/` directory. Path traversal attempts (e.g., `uninstall ../../etc/passwd`) are detected and blocked.
*   **Naming Conventions:** Gem names are restricted to alphanumeric characters (plus `.`, `_`, `-`) to prevent shell injection or filesystem issues.

### B. The Test Suite
Gemonade includes a comprehensive test suite in `tests/` that verifies the framework's integrity without external side effects.
*   **Structure:**
    *   `test_units.py`: Verifies internal logic (config parsing, validation).
    *   `test_integration.py`: Verifies the CLI lifecycle (install/run/uninstall) using a mock environment.
    *   `test_search.py`: Verifies search logic and fallbacks.
*   **Dry Runs:** The Core CLI supports a `--dry-run` flag that outputs the internal state (context, scope, prompt path) as JSON, allowing tests to verify logic without launching the heavy AI process.