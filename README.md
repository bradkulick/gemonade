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
*   **Python 3.x** (Strict Requirement: The Core CLI is Python-based)
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

**Common Flags:**
*   `--project=<name>`: Define the project context. (e.g., `gemonade coder --project=my-app`)
*   `--scope=<mode>`: Set memory visibility scope.
    *   `project` (Default): Strict isolation. Can only see sessions from the current project.
    *   `persona`: Can see sessions from *any* project within the current persona.
    *   `global`: "God Mode". Can see any session from any persona.

**Common Commands:**
```bash
gemonade list                  # List available Gems (Core, Installed, Local)
gemonade search <term>         # Search GitHub for community Gems
gemonade install <url|path>    # Install a Gem from a Git URL or local folder
gemonade uninstall <gem>       # Remove an installed Gem
gemonade update <gem>          # Update a Gem and re-hydrate its dependencies
gemonade sys                   # Chat with the System Architect
```

**Examples:**
```bash
gemonade search innspect       # Find the 'innspect' gem
gemonade install bradkulick/gem-innspect
gemonade innspect              # Launch it
```

### 3. The Gemonade Stand (Squeezing New Gems)
You don't need to write code to create or manage a Gem. Just ask the System Administrator to handle the "squeezing" for you.

```bash
gemonade sys
> "Make me a stock ticker gem."
> "I want to publish my 'thm' gem to GitHub."
> "Graduate my 'scaffolder' gem into a native extension."
```

**The Architect Workflow:**
1.  **Consultation:** `sys` will ask clarifying questions about your goal.
2.  **Architecture:** It proposes a stack and ensures the tool fits the CLI environment.
3.  **Fabrication:** It scaffolds the `gem.json`, `persona.md`, and `requirements.txt` for you.
4.  **Lifecycle Management:** Once your Gem is mature, `sys` can **Publish** your Gem to the world or **Graduate** it into a native Gemini CLI Extension.

### 4. Bottling & Distribution (Publishing & Graduation)
For those who prefer direct CLI control over the "bottling" process, Gemonade includes a full release engineering suite.

**A. Publishing to the World**
Publish your Local Gem to GitHub so others can find it via `gemonade search`.
1.  Navigate to your gem folder: `cd packages/local/my-gem`
2.  Run the publisher: `python3 ../../../tools/publish.py`
    *   Handles semantic versioning (bumps `gem.json`).
    *   Creates Git tags and release commits.
    *   Tags the repo with `gemonade-gem` for discovery.

**B. Graduation (The Incubator)**
Turn your Gem into a native, permanent Gemini CLI Extension.
1.  Run the incubator: `python3 tools/gem_2_extension.py packages/local/my-gem`
2.  Your gem is compiled into a native extension format in the `graduates/` folder.
3.  Install it permanently: `gemini install extension graduates/my-gem`

### 5. Testing & Verification
Gemonade includes a comprehensive test suite to ensure stability and security.

**Running the Tests:**
To verify the framework's core logic, safety barriers, and lifecycle management:
```bash
python3 -m unittest discover tests
```
The suite covers:
*   **Runtime Logic:** Verifies context detection and scope enforcement.
*   **Security:** Confirms path traversal attacks are blocked.
*   **Lifecycle:** Tests the full install/uninstall loop.
*   **Dependency Management:** Verifies virtual environment creation logic.

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
*   **Naming Convention:** Gem names must be alphanumeric (allowing `.`, `_`, `-`) and contain NO spaces or slashes. This is strictly enforced for security.

### D. Proactive Evolution ("The Pull Request")
Gemonade is designed to be self-improving. If a persona identifies a limitation in its own instructions or tools, it is authorized to draft a "Pull Request"—a proposed code change that the user can accept to permanently upgrade the system's capabilities.