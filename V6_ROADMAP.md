# Gemonade V6 Roadmap: The "Text-First" Evolution

**Goal:** Eliminate the heavy "Intelligence Pack" (PyTorch/Chroma) entirely by leveraging Gemonade's strongest asset: its clean, structured file system.

## 1. Core Philosophy: "The File IS The Database"
Instead of duplicating data into a vector store (which requires sync, ingest, and heavy libs), we treat the `knowledge/sessions/` directory as the primary database.

## 2. Memory Architecture (The "Recap" Model)

### A. The Auto-Summarizer
**Mechanism:** At the end of every session (`save_session.py`), Gemonade generates a **Structured Recap**.
*   **Trigger:** A final prompt to the LLM: *"Summarize this session in 3 lines: Goal, Outcome, Next Steps."*
*   **Storage:** 
    1.  Appended to the session log header (YAML Frontmatter style).
    2.  Appended to a `knowledge/projects/<project>/RECAP.md` ledger.

### B. Context Injection (The "Catch-Up")
**Mechanism:** When starting a new session:
*   **Action:** Read the last 5 entries from `RECAP.md` for the current project.
*   **Result:** The System Prompt includes:
    > **Recent History:**
    > - 2025-01-01: Refactored Core to Python.
    > - 2025-01-02: Added Smoke Tests.
    > - 2025-01-03: Fixed Path Traversal bug.

## 3. Recall Strategy (Manual Integration)

**Decision:** We explicitly reject a dedicated `recall` command to avoid abstraction layers.
*   **Mechanism:** Users and Personas rely on standard filesystem tools (`grep`, `find`, `list_directory`) to navigate the `knowledge/` base.
*   **Benefit:** Keeps the interface transparent and the codebase minimal.

## 4. The Benefit (Why we are doing this)
1.  **Zero External Dependencies:** No PyTorch, no Embeddings API key, no Cloud cost.
2.  **Privacy:** 100% Local. No text is sent to an embedding API.
3.  **Speed:** `grep` is faster than network calls.
4.  **Resilience:** The "Memory" is just text files. It can be git-committed, read by humans, and never "corrupts."

## 5. Gem Interoperability & Automation (Legacy Backlog)
*   **Shared Blueprints:** Formalize a mechanism for Gems to reference `blueprints/` from other Installed Gems.
*   **Tool Borrowing:** A secure protocol for one Gem to invoke a tool from another Gem's path.
*   **Native Task Runner:** Replace background Bash cleanup with a native Python-based task manager (`gemonade-daemon`).
*   **Update Notifications:** Alert the user when core or Gems have updates available.

## 6. Backlog / Candidate Improvements
*   **Graduate `anki-forge` to Extension:**
    *   **Goal:** Transform it from a "Flashcard Factory" into a "Photographic Memory" (Skill).
    *   **Technical:** Migrate `library.jsonl` to the extension's `state/` directory for global access via `@anki`.
*   **Graceful Uninstall (Data Preservation):**
    *   **Goal:** Upgrade `gemonade uninstall` to prompt users before deleting user-generated data (e.g., `data/`, `*.db`, `*.jsonl`).
    *   **Implementation:** Detect non-code artifacts and prompt: "User data detected. Archive before uninstalling? [Y/n]".
