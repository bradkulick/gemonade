# Gemonade: The Refreshingly Stateful Gemini CLI Framework

> **"When the world gives you Gemini, make Gemonade."** 🍋🥤

Gemonade is an architectural wrapper that transforms the [Google Gemini CLI](https://www.npmjs.com/package/@google/gemini-cli) into a stateful, modular operating environment. It enables the creation of specialized AI "Personas" (Gems) that possess long-term memory, local system access, and the ability to self-evolve.

## 🚀 Why Gemonade?

While generic AI wrappers exist, Gemonade is purpose-built for the Google Gemini ecosystem.

1.  **Gemini-Native:** Unlike generic wrappers (like ShellGPT or Fabric) that default to OpenAI, Gemonade is optimized specifically for `@google/gemini-cli`, leveraging its deep integration with Google's models.
2.  **Unified Package Architecture:** Personas aren't just text prompts. In Gemonade, a persona is a **Package**—a portable folder containing the prompt (`persona.md`), custom Python tools (`tools/`), and reference blueprints (`blueprints/`). You can install a community "AWS Expert" package and immediately gain its specific scripts and knowledge.
3.  **Local-First State:** Your session history is yours. Gemonade automatically logs every interaction into clean, readable Markdown files in `knowledge/sessions/`. This "Active State" allows you to build a personal knowledge base that remains private and local.

## 🛠️ Quick Start

### Prerequisites
Gemonade is a wrapper around existing tools. Ensure you have the following installed:
*   **Python 3.x** (for session management)
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
Launch a specific persona (Gemonade will handle the session logging automatically).
```bash
gemonade [persona_name]
```

**Listing Available Personas:**
See what personas are available and their objectives:
```bash
gemonade list
```
*Output:*
```text
Available Gemonade Personas:

LOCAL (Private & Custom)
  - thm        : Manage and optimize the Emerald Hills infrastructure...

INSTALLED (Community Packages)
  - (none)

CORE (Built-in Standards)
  - general    : Provide high-quality thought partnership across any domain.
  - sys        : Assist the user in managing personas and maintaining the framework.
```

**Getting Help:**
```bash
gemonade help
# 💡 Pro Tip: To create new personas or understand how this framework works,
#             run 'gemonade sys' to chat with the Gemonade Expert.
```

**Examples:**
```bash
gemonade sys      # Launch the framework administrator
gemonade general  # Launch the general knowledge partner
gemonade thm      # Launch a local private persona (if created)
```

### 3. Creating New Personas
Just ask the system admin!
```bash
gemonade sys
> "Create a new persona for cooking called 'chef'. It should be terse and focus on French cuisine."
```
*Note: New personas are created as packages in `packages/local/`.*

## 🧠 Core Philosophy

### A. The "Gemonade" Metaphor
Just as lemonade transforms simple ingredients into something refreshing, this framework provides the "Mix" (launcher, logging, configuration) that turns the raw Gemini CLI into a complete, flavorful operating system for your AI interactions.

### B. Unified Package Architecture
Gemonade treats every identity as a "Package"—a folder containing the persona's prompt, tools, and blueprints.
*   **Core:** Immutable system identities (`sys`, `general`).
*   **Installed:** Community packages downloaded from external sources.
*   **Local:** Your private, site-specific identities.

### C. Proactive Evolution ("The Pull Request")
Gemonade is designed to be self-improving. If a persona identifies a limitation in its own instructions or tools, it is authorized to draft a "Pull Request"—a proposed code change that the user can accept to permanently upgrade the system's capabilities.
