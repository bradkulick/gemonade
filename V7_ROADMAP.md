# Gemonade V7 Roadmap: The "Agent Orchestration" Evolution

**Goal:** Transition Gemonade from a persona-driven CLI wrapper into a proactive "Agent OS" capable of automated context resumption, multi-agent collaboration, and rapid identity harvesting.

---

## Pillar 1: Performance & Continuity (The "Synapse" Update)
*Status: Implementing V6 Architectural Goals*

### 1.1 The Auto-Summarizer
**Mechanism:** At session termination, `save_session.py` triggers a background LLM call to produce a 3-line "Context Brief" (Goal, Outcome, Next Steps).
**Storage:** Appended to a project-specific `RECAP.md` ledger.

### 1.2 The Project Catch-Up
**Mechanism:** Upon `gemonade run`, the core reads the latest entries from `RECAP.md` and injects them into the system prompt.
**Rationale:** To reduce context-resumption friction and allow the AI to "hit the ground running" without manual history lookups.

---

## Pillar 2: Identity Integrity (The "Guardrail" Update)
*Status: New Focus on instruction Drift*

### 2.1 Post-Persona Guardrails
**Mechanism:** Move core operational protocols (Rationale-First, Plan-Before-Action) from the prepended `CORE_PERSONA.md` to a **System Footer**.
**Rationale:** Identity-heavy personas often "drift" from core rules. Placing rules in the footer (the last thing the AI reads) ensures the framework's operational standards remain the final authority.

---

## 3. Pillar: The Multi-Agent Layer (The "Round Table")
*Status: Advanced Orchestration*

### 3.1 Multi-Persona Sessions
**Mechanism:** Implement the `--with <persona>` flag (e.g., `gemonade run sys --with thm`).
**Implementation:** The framework assembles a multi-identity prompt. The AI is instructed to act as a "Consultative Board," prefixing responses with the name of the active persona (e.g., `[sys]: ...`, `[thm]: ...`).
**Rationale:** Allows complex tasks (Architecting + Infrastructure) to be handled by specialized expert identities within a single conversational context.

---

## 4. Pillar: The Persona Harvester (The "Cloning" Update)
*Status: Ecosystem Expansion*

### 4.1 Automated Distillation
**Mechanism:** A new specialized tool (or `sys` capability) that takes a transcript (e.g., from the Gemini Web App) or a raw prompt string and "distills" it into a valid Gemonade Gem.
**Rationale:** To leverage the vast library of popular external personas and rapidly ingest them into the Gemonade ecosystem as modular, tool-enabled Gems.

---

## 5. Pillar: The Creator Studio (The "Ecosystem" Update)
*Status: Distribution Optimization*

### 5.1 The `eject` Workflow
**Mechanism:** `gemonade eject <local-gem>`.
**Action:** Automates the creation of a standalone Git repository, standardizes the `gem.json`, and prepares the package for `tools/publish.py`.

### 5.2 Flagship Shared Gems
**Objective:** Develop and release a suite of production-ready Gems to showcase V7 capabilities:
*   **The Ideation Partner:** Specialized in structured brainstorming and business logic.
*   **The Harvester:** The flagship Gem for persona cloning and GPS optimization.

---

## Deferred / Research (V8 Candidates)
*   **Cross-Gem Tool Borrowing:** Requires deep structural ideation on tool-namespace isolation.
*   **The Observatory:** Standardized telemetry provider for real-time sensor integration.
