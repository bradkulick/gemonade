# Geode V2 Roadmap & Strategy

This document tracks high-level architectural considerations and features deferred for future versions of the Geode framework.

## 1. Tool Governance & Persona Boundaries
Currently, all Geode personas share access to a flat `~/gemini_tools` directory. In V2, we should consider:
- **Shadow Tooling:** If a persona wants to modify a tool, it should create a local copy first to prevent "collateral damage" to other personas.
- **Sys-Admin Review:** The `sys` persona could act as a code reviewer, deciding when a persona-specific tool improvement should be "merged" into the global toolset.
- **Immutable Core:** Mark specific critical tools as read-only for certain personas.

## 2. Distribution & Packaging
- **Deployment Strategy:** Introduce an "End User" installation mode that copies files to `~/.local/share/geode` instead of symlinking to a git repo.
- **Environment Management:** Use `package.json` or a Python `venv` to strictly manage the version of the underlying `google-gemini-cli`.
- **Extension Wrapper:** Explore wrapping Geode logic into a formal Gemini CLI Extension (`gemini-extension.json`).

## 3. Advanced Memory & Context
- **RAG Integration:** Beyond just reading the "last session," integrate local vector search to allow Geode to query its entire session history across all personas.
- **Blueprint Lifecycle:** Logic for the `sys` persona to proactively identify when blueprints (like network maps) are outdated based on recent tool outputs.

## 4. Automation & Maintenance
- **Native Task Runner:** Replace the background Bash cleanup with a native Python-based task manager for more granular control.
- **Update Notifications:** Alert the user when the `google-gemini-cli` npm package has an update available.
