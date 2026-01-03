# Gemonade V4 Roadmap: The Intelligent Framework

Following the successful implementation of the Gem Ecosystem and Lifecycle tools in V3, V4 focuses on deepening the intelligence, connectivity, and automation of the framework.

## ✅ Completed: Advanced Memory & Isolation (V4.1)
*   **Semantic Memory (RAG):** Implemented local vector store (`chromadb`) over `knowledge/sessions/`.
*   **Strict Isolation:** Migrated session storage to `sessions/{persona}/{project}/` to prevent bleed.
*   **Access Scopes:** Introduced `--scope` flags (`project`, `persona`, `global`) to control visibility boundaries.
*   **Cross-Session Context:** Enabled via Global Scope or Persona Scope for broad queries.

## 2. Gem Interoperability
*   **Shared Blueprints:** Formalize a mechanism for Gems to reference `blueprints/` from other Installed Gems (e.g., a "Network Map" blueprint shared by `innspect` and `sys`).
*   **Tool Borrowing:** A secure protocol for one Gem to invoke a tool from another Gem's path (e.g., `general` asking `innspect` to run a scan).

## 3. Automation & Orchestration
*   **Native Task Runner:** Replace the background Bash cleanup script with a native Python-based task manager (`gemonade-daemon`) for granular control and scheduling.
*   **Update Notifications:** Alert the user when the core framework or an installed Gem has updates available (using `git fetch` checks).
