# Gemonade Architecture & Implementation Guide

This document details the technical implementation of the Gemonade Framework. It explains how the launcher, memory system, and package architecture interact to create a stateful AI environment.

## 1. Directory Structure

Gemonade adopts a "Unified Package" architecture, treating all identities—from core system admins to community extensions—as standardized packages called **Gems**.

### A. The Framework Layout
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
│   └── sessions/              # Session Logs & Recaps
├── user_tools/                # Global User Scripts (Git-Ignored)
└── tools/                     # System Maintenance Scripts
```

> **Principle: Repository-Centricity**
> Gemonade uses repo-relative paths to ensure portability and zero-configuration setups across diverse Linux environments. By containing the state, knowledgebase, and tools within the repository, the framework remains functional immediately after a `git clone` without requiring external directory provisioning.

### B. The Gem Model
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

> **Principle: Encapsulation**
> By making every Gem self-contained—including its own isolated virtual environment and tools—we ensure that an identity can be shared between Gemonade installations without conflicting with other personas or system-wide dependencies.

---

## 2. The Core Engine

### A. The Python Core CLI (`core/gemonade.py`)
The `gemonade` command is a thin Bash wrapper that bootstraps the environment and hands off execution to the Python Core.

**Key Responsibilities:**
1.  **Resolution & Priority:** Identifies the requested persona by searching namespaces in order of specificity (`local` > `installed` > `core`).
2.  **Hydration:** Creates isolated virtual environments (`.venv`) for Gems and provides automatic rollback for failed environment builds.
3.  **Context Injection:** Dynamically assembles the System Prompt from Core Standards, Scope Directives, and Persona instructions.
4.  **Tool Discovery:** Prepends Gem-specific `tools/` and `.venv/bin` to the `$PATH` to expose scripts to the AI.

---

## 3. Text-First Memory

Gemonade prioritizes a "Text-First" memory model over complex database abstractions.

### A. The Recap Model (`tools/save_session.py`)
At the end of every session, the system parses the clean conversation, formats thought processes into collapsible details, and appends a structured entry to a `history.jsonl` ledger.

> **Principle: The File IS The Database**
> Gemonade rejects heavy Vector Database dependencies in favor of human-readable text for three reasons:
> 1.  **Zero-Dependency:** No heavy libraries or external API keys are required for memory retrieval.
> 2.  **Privacy:** 100% of the conversation history remains local.
> 3.  **Auditability:** Memory is stored in plain text, making it searchable by standard Linux tools (`grep`, `find`) and verifiable by humans.

---

## 4. Contextual Scoping

To maintain high precision and prevent "hallucination bleed" between unrelated tasks, Gemonade uses the `--scope` flag to set visibility boundaries.

| Mode | Scope | Visibility Boundary | Default? |
| :--- | :--- | :--- | :--- |
| **Project** | `project` | Isolated to `sessions/{persona}/{project_context}/` | **Yes** |
| **Persona** | `persona` | Access to all projects within the current Persona. | No |
| **Global** | `global` | Unrestricted access across all personas. | No |

> **Principle: Domain Isolation**
> Scoping ensures that the AI only retrieves information relevant to the current logical domain, preventing it from incorrectly applying details from one project to another, unless explicitly instructed otherwise.

---

## 5. The Gemonade Package Standard (GPS)

To enable distribution via `gemonade install`, a package must comply with the GPS by containing a `gem.json` manifest in its root.

### A. Manifest Specification
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

### B. Lifecycle Operations
*   **`install <url>`:** Clones the repository, validates the manifest, and hydrates the virtual environment.
*   **`update <name>`:** Synchronizes the local clone with the remote source and refreshes dependencies.
*   **`uninstall <name>`:** Performs a clean removal of the Gem directory and its isolated state.

> **Principle: Automated Lifecycle Management**
> Standardizing the manifest allows the framework to treat personas as managed software packages. This enables automated installation and dependency resolution, effectively turning Gemonade into a package manager for AI capabilities.

---

## 6. Workflow & Extension

### A. The "System Admin" Persona (`sys`)
The built-in `sys` persona acts as the framework's Architect and Meta-Manager. 

**Key Responsibilities:**
1.  **Lifecycle Advisor:** It determines the best architectural fit for a request, deciding when a utility should be a stateless **Extension** vs. a stateful **Gem**.
2.  **Factory Manager:** It scaffolds new local Gems for private prototyping and can upgrade them to shareable, installable Gems or Extensions for community distribution.
3.  **Governance:** It enforces the GPS and ensures framework integrity during system-wide refactors.

### B. Extending vs. Overriding
Gemonade supports two methods for modifying behavior:

1.  **Override (Shadowing):** Higher-priority namespaces (e.g., `local`) can override lower-priority ones (`installed`). For example, creating `packages/local/aws/persona.md` will completely hide `packages/installed/aws/persona.md`. 
    *   **Constraint:** You cannot override `core` packages (e.g., `sys`, `general`) to ensure framework stability.
2.  **Extension (Inheritance):** Personas can import the base logic of other personas using relative paths and then chain additional instructions.
    *   **Implementation Example:**
        ```markdown
        # My General
        {{LOAD: ../../../core/general/persona.md}}
        - **Extra Rule:** Always speak in Haiku.
        ```
    *   *Note:* While Gemonade doesn't have a native macro language, users can manually inherit logic by referencing files or copying base instructions.

---

## 7. Lifecycle: The Incubator Model

Gemonade serves as a rapid-prototyping environment for AI capabilities. 

1.  **The Local Gem:** A persona is created in `packages/local/` (often via `sys`) for rapid prototyping and stateful local use.
2.  **Packaging:** The `sys` persona refines the Gem, ensuring it has a valid `gem.json` and `requirements.txt` for distribution.
3.  **Graduation:** Use `tools/gem_2_extension.py` to convert a mature Gem into a native Gemini CLI Extension.

> **Principle: Pilot vs. Co-Pilot**
> - **Gems (The Pilot):** Best for focused roles requiring long-term memory, deep state, and a distinct identity.
> - **Extensions (The Co-Pilot):** Best for stateless, global utilities that should be available in any conversation via `@` handles.

---

## 8. Security & Verification

### A. Safety Barriers
*   **Path Containment:** All lifecycle operations are strictly confined to the `packages/installed/` directory to prevent unauthorized filesystem access.
*   **Naming Conventions:** Gem names are restricted to safe alphanumeric characters to prevent shell injection.

### B. The Test Suite
The integration and unit tests in `tests/` leverage the `--dry-run` flag to verify the framework's internal state (context, environment, and paths) without executing the heavy AI process.
