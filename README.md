# Geode: The Stateful, Persona-Driven Gemini CLI Framework

Geode is an architectural wrapper that transforms the [Google Gemini CLI](https://www.npmjs.com/package/@google/gemini-cli) into a stateful, modular operating environment. It enables the creation of specialized AI "Personas" (Gems) that possess long-term memory, local system access, and the ability to self-evolve.

## 🚀 Why Geode?
Standard AI interactions are stateless. Geode introduces a "Memory Bank" and a "Personality Engine" to the CLI, enabling:

*   **Deep Context:** Every session is automatically recorded to a structured Knowledge Base.
*   **Modular Identity:** Switch instantly between specialized personas (e.g., `sys`, `coding`, `network`) with a single command.
*   **Unified Packages:** Community and local personas are treated as standardized packages that can bundle their own tools and knowledge.
*   **Local Power:** Operates within your shell, allowing direct interaction with local files, tools, and private network devices.

## 🛠️ Quick Start

### Prerequisites
Geode is a wrapper around existing tools. Ensure you have the following installed:
*   **Python 3.x** (for session management)
*   **Node.js & npm**
*   **Google Gemini CLI:**
    ```bash
    npm install -g @google/gemini-cli
    ```

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
geode help
# 💡 Pro Tip: To create new personas or understand how this framework works,
#             run 'geode sys' to chat with the Geode Expert.
```

**Examples:**
```bash
geode sys      # Launch the framework administrator
geode general  # Launch the general knowledge partner
geode thm      # Launch a local private persona (if created)
```

### 3. Creating New Personas
Just ask the system admin!
```bash
geode sys
> "Create a new persona for cooking called 'chef'. It should be terse and focus on French cuisine."
```
*Note: New personas are created as packages in `packages/local/`.*

## 🧠 Core Philosophy

### A. The "Geode" Metaphor
A Geode is a protective shell containing distinct, valuable crystals. Similarly, this framework provides the "Shell" (launcher, logging, configuration) that protects and organizes your "Gems" (Personas).

### B. Unified Package Architecture
Geode treats every identity as a "Package"—a folder containing the persona's prompt, tools, and blueprints.
*   **Core:** Immutable system identities (`sys`, `general`).
*   **Installed:** Community packages downloaded from external sources.
*   **Local:** Your private, site-specific identities.

### C. Proactive Evolution ("The Pull Request")
Geode is designed to be self-improving. If a persona identifies a limitation in its own instructions or tools, it is authorized to draft a "Pull Request"—a proposed code change that the user can accept to permanently upgrade the system's capabilities.