# Geode Architecture & Implementation Guide

This document details the technical implementation of the Geode Framework. It explains how the launcher, memory system, and package architecture interact to create a stateful AI environment.

## 1. Directory Structure

Geode adopts a "Unified Package" architecture, treating all identities—from core system admins to community extensions—as standardized packages.

### A. The Framework (`geode/`)
This repository contains the system logic and package definitions.
```text
geode/
├── bin/
│   └── geode               # The Launcher (Bash script)
├── core/
│   └── CORE_PERSONA.md     # Universal standards (Inherited by all Personas)
├── packages/               # The Identity Packages
│   ├── core/               # Immutable System Personas (sys, general)
│   ├── installed/          # Community/3rd-Party Personas (Git Ignored)
│   └── local/              # User-Created Private Personas (Git Ignored)
├── knowledge/              # The "Active State"
│   └── sessions/           # Session Logs
├── user_tools/             # Global User Scripts
└── tools/                  # System Maintenance Scripts
```

### B. The Package Model
Every persona is a self-contained directory within `packages/`.
```text
packages/local/my-persona/
├── persona.md              # The Identity Prompt
├── tools/                  # (Optional) Python scripts specific to this persona
└── blueprints/             # (Optional) Reference docs/knowledge
```

## 2. Core Components

### A. The Launcher (`bin/geode`)
The `geode` command is the single entry point. It orchestrates the session lifecycle:

1.  **Resolution & Priority:** Identifies the requested persona by searching namespaces in specific order:
    *   **Local** (`packages/local/`): Highest priority. Allows user overrides.
    *   **Installed** (`packages/installed/`): Community packages.
    *   **Core** (`packages/core/`): Lowest priority. Protected system identities.
    *   *Note:* The `sys` and `general` namespaces are reserved and strictly served from `core`.

2.  **Context Injection:** It dynamically concatenates `core/CORE_PERSONA.md` + `packages/.../persona.md`.

3.  **Tool Discovery:** If the resolved package contains a `tools/` directory, that path is automatically prepended to the environment `$PATH`, granting the persona access to its specific capabilities.

4.  **Execution & Teardown:** Launches the native `gemini` CLI and triggers the Memory Saver upon exit.

### B. The Memory Saver (`tools/save_session.py`)
Standard terminal recording (`script`) captures "noise". Geode uses a custom Python hook that:
1.  Parses the internal JSON logs from the Gemini CLI.
2.  Extracts the clean conversation (User Prompt + AI Response).
3.  Formats "Thought Processes" into collapsible HTML/Markdown details.
4.  Saves the clean file to `knowledge/sessions/[persona]/`.

## 3. Workflow & Extension

### The "System Admin" Persona (`sys`)
Geode includes a built-in "Meta-Persona" called `sys`. It has explicit knowledge of this architecture.
*   **Role:** Architect & Maintainer.
*   **Capabilities:**
    *   It knows how to create new packages in `packages/local/`.
    *   It can diagnose issues with the launcher or tools.

### Extending vs. Overriding
Geode supports two methods for modifying behavior:

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
    *   *Note:* While Geode doesn't have a native macro language yet, users can manually inherit logic by referencing files or copying base instructions.