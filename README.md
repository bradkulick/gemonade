# Geode: The Stateful, Persona-Driven Gemini CLI Framework

Geode is an architectural wrapper that transforms the [Google Gemini CLI](https://www.npmjs.com/package/@google/gemini-cli) into a stateful, modular operating environment. It enables the creation of specialized AI "Personas" (Gems) that possess long-term memory, local system access, and the ability to self-evolve.

## 🚀 Why Geode?
Standard AI interactions are stateless. Geode introduces a "Memory Bank" and a "Personality Engine" to the CLI, enabling:

*   **Deep Context:** Every session is automatically recorded to a structured Knowledge Base.
*   **Modular Identity:** Switch instantly between specialized personas (e.g., `sys`, `coding`, `network`) with a single command.
*   **Local Power:** Operates within your shell, allowing direct interaction with local files, tools, and private network devices.
*   **Self-Healing:** The system includes an admin persona (`sys`) capable of diagnosing errors and rewriting its own code.

## 🛠️ Quick Start

### 1. Installation
Run the installer to link the `geode` command to your path and generate the default config.
```bash
bash install.sh
export PATH="$HOME/bin:$PATH"
```

### 2. Usage
Launch a specific persona (Geode will handle the session logging automatically).
```bash
geode [persona_name]
```

**Listing Available Personas:**
See what personas are available and their objectives:
```bash
geode list
```
*Output:*
```text
Available Geode Personas:
  - general    : Provide high-quality thought partnership across any domain.
  - sys        : Assist the user in managing personas, configuring the environment, and maintaining the Geode framework.
```

**Examples:**
```bash
geode sys      # Launch the framework administrator
geode general  # Launch the general knowledge partner
geode coding   # (If created) Launch a specialized coding partner
```

### 3. Creating New Personas
Just ask the system admin!
```bash
geode sys
> "Create a new persona for cooking called 'chef'. It should be terse and focus on French cuisine."
```

## 🧠 Core Philosophy

### A. The "Geode" Metaphor
A Geode is a protective shell containing distinct, valuable crystals. Similarly, this framework provides the "Shell" (launcher, logging, configuration) that protects and organizes your "Gems" (Personas).

### B. Stateful Memory
Geode automatically captures every interaction in clean Markdown format (stripping out terminal noise) and stores it in `~/gemini_knowledge/sessions/`.
*   **Startup Scan:** When a persona launches, it reviews recent session files to recall past context.
*   **Archives:** The system automatically cleans up and archives logs older than 30 days to keep the active memory fresh.

### C. Proactive Evolution ("The Pull Request")
Geode is designed to be self-improving. If a persona identifies a limitation in its own instructions or tools, it is authorized to draft a "Pull Request"—a proposed code change that the user can accept to permanently upgrade the system's capabilities.
