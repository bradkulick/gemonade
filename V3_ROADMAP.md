# Gemonade V3 Roadmap & Strategy

This document tracks high-level architectural considerations for the next evolution of the Gemonade framework.

## 🏆 Completed in V2.0 (The Gem Ecosystem)
*   **Unified Package Ecosystem:** Gems are now portable, self-contained directories with `gem.json` manifests.
*   **Isolated Environments:** Dependency hell was solved via per-Gem `.venv` hydration.
*   **Decentralized Distribution:** `gemonade install <url>` allows installing Gems directly from Git.
*   **Sys-Admin Architect:** The `sys` persona now actively enforces standards and scaffolds projects.

---

## 1. Advanced Memory & Context (The "Brain" Upgrade)
Currently, Gemonade reads the "last session" file to maintain context. In V3, we aim to implement **Semantic Memory**.
*   **Local RAG (Retrieval-Augmented Generation):** Implement a lightweight vector store (e.g., `chromadb` or simple cosine similarity) over the `knowledge/sessions/` directory. This would allow Gems to answer: *"What did we discuss about AWS three weeks ago?"*
*   **Cross-Session Context:** Allowing a Gem to pull context from *other* Gems' sessions if authorized (e.g., `sys` diagnosing a crash in `innspect`).

## 2. Gem Interoperability
*   **Shared Blueprints:** Formalize a mechanism for Gems to reference `blueprints/` from other Installed Gems (e.g., a "Network Map" blueprint shared by `innspect` and `sys`).
*   **Tool Borrowing:** A secure protocol for one Gem to invoke a tool from another Gem's path (e.g., `general` asking `innspect` to run a scan).

## 3. Automation & Maintenance
*   **Native Task Runner:** Replace the background Bash cleanup script with a native Python-based task manager (`gemonade-daemon`) for granular control.
*   **Update Notifications:** Alert the user when the core framework or an installed Gem has updates available (using `git fetch` checks).

## 4. Discovery & Publishing
*   **CLI Search:** Implement `gemonade search <term>` to query GitHub for repositories tagged with `gemonade-gem`.
*   **Publishing Assistant:** Upgrade `sys` to handle the full Git lifecycle (init, commit, push) for new Gems.