# Gemonade: The Refreshingly Stateful Gemini CLI Framework

> **"When the world gives you Gemini, make Gemonade."** 🍋🥤
> *"Squeeze the Gems out of Gemini."*

Gemonade is an architectural wrapper that transforms the [Google Gemini CLI](https://www.npmjs.com/package/@google/gemini-cli) into a stateful, modular operating environment. It enables the creation of specialized AI "Personas" (Gems) that possess long-term memory, local system access, and the ability to self-evolve.

## 🚀 Why Gemonade?

While generic AI wrappers exist, Gemonade is purpose-built for the Google Gemini ecosystem.

1.  **Gemini-Native:** Unlike generic wrappers (like ShellGPT or Fabric) that default to OpenAI, Gemonade is optimized specifically for `@google/gemini-cli`, leveraging its deep integration with Google's models.
2.  **Unified Package Ecosystem:** Personas aren't just text prompts. In Gemonade, a persona is a **Gem**—a portable package containing the prompt (`persona.md`), custom Python tools (`tools/`), metadata (`gem.json`), and isolated dependencies (`.venv`). You can install a community "AWS Expert" package and immediately gain its specific scripts and knowledge without polluting your system Python.
3.  **Local-First State:** Your session history is yours. Gemonade automatically logs every interaction into clean, readable Markdown files in `knowledge/sessions/`. This "Active State" allows you to build a personal knowledge base that remains private and local.

## 🛠️ Quick Start

### Prerequisites
Gemonade is a wrapper around existing tools. Ensure you have the following installed:
*   **Python 3.x** (for session management and tool environments)
*   **Node.js & npm**
*   **Google Gemini CLI:**
    ```bash
    npm install -g @google/gemini-cli
    ```

### 1. Installation
Run the installer to link the `gemonade` command to your path and generate the default config.
```bash
bash install.sh
export PATH="$HOME/bin:$PATH"
```

### 2. Usage
Launch a specific persona (Gemonade will handle the session logging and environment setup automatically).
```bash
gemonade [gem_name]
```

**Common Commands:**
```bash
gemonade list                  # List available Gems (Core, Installed, Local)
gemonade install <url>         # Install a Gem from a Git repository
gemonade uninstall <gem>       # Remove an installed Gem
gemonade update <gem>          # Update a Gem and re-hydrate its dependencies
gemonade sys                   # Chat with the System Architect
```

**Examples:**
```bash
gemonade sys      # Launch the framework administrator
gemonade general  # Launch the general knowledge partner
gemonade innspect # Launch a local private persona (if created)
```

### 3. Creating New Gems (The "Gem Factory")
You don't need to write code to create a Gem. Just ask the System Administrator.

```bash
gemonade sys
> "Make me a stock ticker gem."
```

**The Architect Workflow:**
1.  **Consultation:** `sys` will ask clarifying questions about your goal (e.g., "Do you have an API key?").
2.  **Architecture:** It will propose a stack and ensure the tool fits the CLI environment (e.g., warning against Video/GUI requests).
3.  **Fabrication:** Once approved, it scaffolds the `gem.json`, `persona.md`, and `requirements.txt` for you.

## 🧠 Core Philosophy

### A. The "Gemonade" Metaphor
Just as lemonade transforms simple ingredients into something refreshing, this framework provides the "Mix" (launcher, logging, configuration) that turns the raw Gemini CLI into a complete, flavorful operating system for your AI interactions.

### B. Unified Package Architecture
Gemonade treats every identity as a "Package"—a folder containing the persona's prompt, tools, and blueprints.
*   **Core:** Immutable system identities (`sys`, `general`).
*   **Installed:** Community packages downloaded from external sources (via `gemonade install`).
*   **Local:** Your private, site-specific identities.

### C. The Gemonade Package Standard (GPS)
Every Gem is a self-contained directory governed by a `gem.json` manifest.
*   **Isolation:** Gems that require Python libraries (like `requests` or `scapy`) get their own isolated virtual environment (`.venv`) automatically created at install time.
*   **Portability:** You can zip up a Gem or push it to Git, and anyone else can install it with a single command.

### D. Proactive Evolution ("The Pull Request")
Gemonade is designed to be self-improving. If a persona identifies a limitation in its own instructions or tools, it is authorized to draft a "Pull Request"—a proposed code change that the user can accept to permanently upgrade the system's capabilities.