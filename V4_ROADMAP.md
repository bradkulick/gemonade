# Gemonade V4 Roadmap: The Intelligent Framework

Following the successful implementation of the Gem Ecosystem and Lifecycle tools in V3, V4 focuses on deepening the intelligence, connectivity, and automation of the framework.

## 1. Advanced Memory & Context (The "Brain" Upgrade)
Currently, Gemonade reads the "last session" file to maintain context. In V4, we aim to implement **Semantic Memory**.
*   **Local RAG (Retrieval-Augmented Generation):** Implement a lightweight vector store (e.g., `chromadb` or simple cosine similarity) over the `knowledge/sessions/` directory. This would allow Gems to answer: *"What did we discuss about AWS three weeks ago?"*
*   **Cross-Session Context:** Allowing a Gem to pull context from *other* Gems' sessions if authorized (e.g., `sys` diagnosing a crash in `innspect`).

## 2. Gem Interoperability
*   **Shared Blueprints:** Formalize a mechanism for Gems to reference `blueprints/` from other Installed Gems (e.g., a "Network Map" blueprint shared by `innspect` and `sys`).
*   **Tool Borrowing:** A secure protocol for one Gem to invoke a tool from another Gem's path (e.g., `general` asking `innspect` to run a scan).

## 3. Automation & Orchestration
*   **Native Task Runner:** Replace the background Bash cleanup script with a native Python-based task manager (`gemonade-daemon`) for granular control and scheduling.
*   **Update Notifications:** Alert the user when the core framework or an installed Gem has updates available (using `git fetch` checks).
