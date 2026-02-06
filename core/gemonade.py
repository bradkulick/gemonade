#!/usr/bin/env python3
"""
Gemonade Core CLI (v5.2.1)
The Python-powered brain of the Gemonade framework.
"""

import os
import sys
import json
import shutil
import argparse
import subprocess
import re
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path

try:
    from dotenv import load_dotenv
    HAS_DOTENV = True
except ImportError:
    HAS_DOTENV = False


# --- Configuration & Paths ---
GEMONADE_HOME = Path(__file__).resolve().parent.parent
CONFIG_FILE = Path.home() / ".gemonade_config"
STATE_DIR = Path.home() / ".gemonade"
G_CORE_VENV = STATE_DIR / ".venv"

# Default Paths
DEFAULTS = {
    "G_KNOWLEDGE_DIR": str(GEMONADE_HOME / "knowledge"),
    "G_PACKAGE_ROOT": str(GEMONADE_HOME / "packages"),
    "G_CORE_PERSONA": str(GEMONADE_HOME / "core" / "CORE_PERSONA.md"),
    "G_SAVER_SCRIPT": str(GEMONADE_HOME / "tools" / "save_session.py"),
    "GEMONADE_RETENTION_DAYS": "30"
}

# Shared State for Global Flags
FLAGS = {"verbose": False}

def load_config(config_path=None):
    """Loads Gemonade configuration. Prefers python-dotenv, fallbacks to manual parsing."""
    config = DEFAULTS.copy()
    target_config = Path(config_path) if config_path else CONFIG_FILE
    
    if not target_config.exists():
        return config

    if HAS_DOTENV:
        load_dotenv(dotenv_path=target_config)
    else:
        # Robust Manual Fallback
        with open(target_config, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    line = line.replace("export ", "", 1)
                    key, value = line.split("=", 1)
                    value = value.split("#")[0].strip().strip('"').strip("'")
                    os.environ[key.strip()] = value

    for key in DEFAULTS:
        if os.environ.get(key):
            config[key] = os.environ.get(key)
    
    return config

# --- UI Helpers ---
def print_msg(emoji, message):
    print(f"{emoji} {message}")

def print_err(message):
    print(f"❌ Error: {message}", file=sys.stderr)

def log_debug(message):
    if FLAGS["verbose"]:
        print(f"🔍 DEBUG: {message}")

def run_proc(cmd, cwd=None, check=True):
    """Unified subprocess runner with verbosity control."""
    log_debug(f"Running command: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    
    # If not verbose, hide stdout/stderr unless there's an error
    stdout = None if FLAGS["verbose"] else subprocess.PIPE
    stderr = None if FLAGS["verbose"] else subprocess.STDOUT
    
    try:
        return subprocess.run(cmd, cwd=cwd, check=check, text=True, stdout=stdout, stderr=stderr)
    except subprocess.CalledProcessError as e:
        if not FLAGS["verbose"] and e.stdout:
            print(e.stdout)
        raise e

# --- Safety & Validation ---
def validate_gem_name(name):
    """Ensures gem name is safe and contains no traversal characters."""
    if not name:
        raise ValueError("Gem name cannot be empty.")
    if not re.match(r'^[a-zA-Z0-9._-]+$', name) or '..' in name:
        raise ValueError(f"Invalid Gem name '{name}'. Only alphanumeric, '.', '_', and '-' characters allowed.")
    return name

def validate_manifest(data):
    """Validates the Gem manifest against the Gemonade Package Standard (GPS)."""
    required = ["name", "version", "description"]
    for field in required:
        if field not in data:
            raise ValueError(f"Manifest missing required field: '{field}'")
    return data

def get_safe_installed_path(config, name):
    """Resolves a Gem path and ensures it stays within the 'installed' directory."""
    clean_name = validate_gem_name(name)
    root = (Path(config["G_PACKAGE_ROOT"]) / "installed").resolve()
    target = (root / clean_name).resolve()
    
    if not str(target).startswith(str(root)):
         raise ValueError(f"Security Alert: Path traversal attempted for '{name}'")
    
    return target

# --- Context Logic ---
def detect_project_context(explicit_flag=None):
    if explicit_flag:
        return explicit_flag
    if os.environ.get("GEMONADE_PROJECT"):
        return os.environ["GEMONADE_PROJECT"]
    
    # Git Root Detection
    try:
        git_root = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], 
            stderr=subprocess.DEVNULL
        ).decode().strip()
        return os.path.basename(git_root)
    except:
        pass

    # Local Project File
    local_conf = Path(".gemonade_project")
    if local_conf.exists():
        return local_conf.read_text().splitlines()[0].strip()

    return "global"

# --- Persona/Gem Discovery ---
def find_persona_file(name, config):
    root = Path(config["G_PACKAGE_ROOT"])
    
    search_paths = [
        root / "local" / name / "persona.md",
        root / "installed" / name / "persona.md",
        root / "core" / name / "persona.md"
    ]
    
    if name == "sys":
        search_paths.append(root / "core" / "sys" / "persona.md")
    if name == "general":
        search_paths.append(root / "core" / "general" / "persona.md")

    for path in search_paths:
        if path.exists():
            return path
    return None

def get_gems_list(config):
    """Logic-only: returns a dictionary of gems by category."""
    root = Path(config["G_PACKAGE_ROOT"])
    categories = [
        ("LOCAL", root / "local"),
        ("INSTALLED", root / "installed"),
        ("CORE", root / "core")
    ]

    results = {}
    for title, path in categories:
        gems = []
        if path.exists():
            for persona_md in path.glob("*/persona.md"):
                gem_name = persona_md.parent.name
                objective = "No objective defined."
                try:
                    with open(persona_md, 'r') as f:
                        for line in f:
                            if "Objective:" in line:
                                objective = line.split("Objective:", 1)[1].strip()
                                break
                except: pass
                gems.append((gem_name, objective))
        results[title] = sorted(gems)
    return results

# --- Search Capability ---
def search_gems(query):
    """Search for Gems using 'gh' CLI or fallback to GitHub API."""
    if query:
        print_msg("🔍", f"Searching for Gemonade Gems matching: '{query}'...")
    else:
        print_msg("🔍", "Discovering popular Gemonade Gems...")
    
    results = []
    
    if shutil.which("gh"):
        log_debug("Searching via GitHub CLI...")
        cmd = [
            "gh", "search", "repos", 
            "--topic", "gemonade-gem",
            "--json", "name,description,url,stargazersCount,owner",
            "--limit", "15"
        ]
        if query: cmd.append(query)
        try:
            res = run_proc(cmd)
            if res.returncode == 0:
                results = json.loads(res.stdout)
        except Exception: pass
    
    if not results:
        log_debug("Searching via GitHub REST API...")
        api_query = "topic:gemonade-gem"
        if query: api_query += f" {query}"
        params = urllib.parse.urlencode({'q': api_query, 'sort': 'stars', 'order': 'desc'})
        url = f"https://api.github.com/search/repositories?{params}"
        
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Gemonade-CLI'})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read())
                results = data.get("items", [])
        except urllib.error.URLError as e:
            print_err(f"Search failed: {e}")
            return

    if not results:
        print("   No gems found.")
        return

    print(f"\nFound {len(results)} gems:\n")
    for repo in results:
        name = repo.get("name")
        owner = repo.get("owner", {}).get("login", "unknown")
        full_name = f"{owner}/{name}"
        desc = repo.get("description") or "No description."
        url = repo.get("html_url") or repo.get("url")
        stars = repo.get("stargazersCount", 0)
        
        print(f"💎 {full_name} (⭐ {stars})")
        print(f"   {desc}")
        print(f"   Install: gemonade install {url}\n")


# --- Gem Lifecycle ---
def hydrate_gem(path):
    path = Path(path)
    req_file = path / "requirements.txt"
    gem_json = path / "gem.json"
    python_version = None
    
    if gem_json.exists():
        try:
            data = json.loads(gem_json.read_text())
            if "python_dependencies" in data:
                req_file = path / data["python_dependencies"]
            python_version = data.get("python_version")
        except: pass

    if not req_file.exists():
        return True

    print_msg("🐍", f"Python dependencies detected for '{path.name}'. Hydrating environment...")
    
    py_cmd = sys.executable
    if python_version:
        if shutil.which(f"python{python_version}"):
            py_cmd = f"python{python_version}"
            log_debug(f"Using requested Python version: {py_cmd}")
        else:
            print_msg("⚠️", f"Requested python{python_version} not found. Falling back to default.")

    venv_path = path / ".venv"
    try:
        run_proc([py_cmd, "-m", "venv", str(venv_path)])
        pip_cmd = venv_path / "bin" / "pip"
        if not pip_cmd.exists():
            pip_cmd = venv_path / "Scripts" / "pip.exe"

        if not pip_cmd.exists():
            raise FileNotFoundError("pip not found in virtual environment.")

        run_proc([str(pip_cmd), "install", "-r", str(req_file)])
        print_msg("✅", "Virtual environment hydrated.")
        return True

    except Exception as e:
        if venv_path.exists():
            shutil.rmtree(venv_path)
        raise RuntimeError(f"Hydration failed for '{path.name}': {e}")

def install_gem(source, config):
    installed_dir = Path(config["G_PACKAGE_ROOT"]) / "installed"
    installed_dir.mkdir(parents=True, exist_ok=True)
    
    dest_path = None
    try:
        if os.path.isdir(source):
            src_path = Path(source).resolve()
            gem_name = validate_gem_name(src_path.name)
            dest_path = installed_dir / gem_name
            print_msg("📦", f"Installing from local path: {src_path}")
            if not (src_path / "gem.json").exists():
                raise ValueError("Not a valid Gem (missing gem.json).")
            if dest_path.exists():
                shutil.rmtree(dest_path)
            shutil.copytree(src_path, dest_path, ignore=shutil.ignore_patterns(".git", ".venv", "__pycache__"))
        else:
            repo_url = source
            if "/" in source and "http" not in source and "@" not in source:
                repo_url = f"https://github.com/{source}.git"
            gem_name = validate_gem_name(Path(repo_url).stem)
            dest_path = installed_dir / gem_name
            if dest_path.exists():
                shutil.rmtree(dest_path)
            print_msg("📦", f"Cloning {repo_url}...")
            run_proc(["git", "clone", repo_url, str(dest_path)])
            shutil.rmtree(dest_path / ".git", ignore_errors=True)

        manifest = dest_path / "gem.json"
        if manifest.exists():
            try:
                data = json.loads(manifest.read_text())
                validate_manifest(data)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON in gem.json: {e}")

            canonical_name = data.get("name")
            if canonical_name and canonical_name != gem_name:
                clean_canonical = validate_gem_name(canonical_name)
                final_path = installed_dir / clean_canonical
                if not final_path.exists():
                    dest_path.rename(final_path)
                    dest_path = final_path

        hydrate_gem(dest_path)
        return str(dest_path.name)

    except Exception as e:
        if dest_path and dest_path.exists():
            shutil.rmtree(dest_path)
        raise e

# --- Runtime Engine ---
def run_persona(persona, project_flag, scope, config, dry_run=False):
    persona_file = find_persona_file(persona, config)
    if not persona_file:
        raise FileNotFoundError(f"Persona '{persona}' not found.")

    project_ctx = detect_project_context(project_flag)
    knowledge_dir = Path(config["G_KNOWLEDGE_DIR"])
    session_dir = knowledge_dir / "sessions" / persona / project_ctx
    session_dir.mkdir(parents=True, exist_ok=True)
    STATE_DIR.mkdir(parents=True, exist_ok=True)

    scope_md = f"# ⚠️ Active Access Scope: {scope.upper()}\n"
    if scope == "global":
        scope_md += "GLOBAL visibility granted. Access ALL sessions.\n"
    elif scope == "persona":
        scope_md += f"PERSONA visibility granted for '{persona}'.\n"
    else:
        scope_md += f"PROJECT isolation active for '{project_ctx}'.\n"

    ledger_path = session_dir / "history.jsonl"
    recent_history = ""
    if ledger_path.exists():
        try:
            lines = ledger_path.read_text().splitlines()
            last_5 = lines[-5:]
            recent_history = "\n# 🧠 Recent Memory (The Recap)\n"
            for line in last_5:
                try:
                    entry = json.loads(line)
                    date = entry.get('display_date', 'Unknown Date')
                    topic = entry.get('topic', 'No Topic')
                    file = entry.get('file', '')
                    recent_history += f"- **{date}**: {topic} (Ref: `{file}`)\n"
                except: pass
            recent_history += "\n"
        except Exception as e:
            recent_history = f"\n# ⚠️ Memory Error: Could not read history: {e}\n"

    core_persona_path = Path(config["G_CORE_PERSONA"])
    system_md_content = ""
    if core_persona_path.exists():
        system_md_content += core_persona_path.read_text() + "\n\n"
    
    if recent_history:
        system_md_content += recent_history
        
    system_md_content += scope_md + "\n\n"
    system_md_content += persona_file.read_text()

    system_md_file = STATE_DIR / f"system_{persona}_{os.getpid()}.md"
    system_md_file.write_text(system_md_content)

    env = os.environ.copy()
    env["GEMINI_SYSTEM_MD"] = str(system_md_file)
    env["GEMONADE_PROJECT"] = project_ctx
    env["GEMONADE_PERSONA"] = persona
    env["GEMONADE_SCOPE"] = scope

    gem_home = persona_file.parent
    paths = []
    if (gem_home / "tools").exists(): paths.append(str(gem_home / "tools"))
    if (gem_home / ".venv" / "bin").exists(): 
        paths.append(str(gem_home / ".venv" / "bin"))
        env["VIRTUAL_ENV"] = str(gem_home / ".venv")
    
    core_tools = GEMONADE_HOME / "tools"
    if core_tools.exists(): paths.append(str(core_tools))
    if paths: env["PATH"] = ":".join(paths) + ":" + env.get("PATH", "")

    if dry_run:
        state = {
            "project_context": project_ctx,
            "scope": scope,
            "persona": persona,
            "env": {k: env.get(k) for k in ["GEMONADE_PROJECT", "GEMONADE_SCOPE", "GEMONADE_PERSONA", "GEMINI_SYSTEM_MD", "VIRTUAL_ENV", "PATH"]},
            "command": ["gemini", "--include-directories", str(knowledge_dir)],
            "system_prompt_content": system_md_content
        }
        if system_md_file.exists(): system_md_file.unlink()
        return state

    print_msg("💎", f"Gemonade: [{persona}] @ [{project_ctx}] (Scope: {scope})")
    try:
        subprocess.run(["gemini", "--include-directories", str(knowledge_dir)], env=env)
    finally:
        if system_md_file.exists(): system_md_file.unlink()
        saver = Path(config["G_SAVER_SCRIPT"])
        if saver.exists():
            run_proc([sys.executable, str(saver), str(session_dir), "--project", project_ctx])

# --- Main CLI ---
def main():
    parser = argparse.ArgumentParser(description="Gemonade: The Gemini CLI Persona Wrapper")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output for debugging")
    subparsers = parser.add_subparsers(dest="command")

    run_p = subparsers.add_parser("run", help="Start a session")
    run_p.add_argument("gem", nargs="?", default="general")
    run_p.add_argument("--project", help="Project context")
    run_p.add_argument("--scope", default="project", choices=["project", "persona", "global"])
    run_p.add_argument("--dry-run", action="store_true")

    subparsers.add_parser("list", help="List available Gems")
    subparsers.add_parser("config", help="Show current config")
    subparsers.add_parser("install", help="Install a Gem").add_argument("source")
    subparsers.add_parser("uninstall", help="Uninstall a Gem").add_argument("name")
    subparsers.add_parser("update", help="Update a Gem").add_argument("name")
    
    search_p = subparsers.add_parser("search", help="Search GitHub for Gems")
    search_p.add_argument("query", nargs="?", default="")

    if len(sys.argv) == 1: args = parser.parse_args(["run", "general"])
    elif sys.argv[1] not in subparsers.choices and not sys.argv[1].startswith("-"): args = parser.parse_args(["run"] + sys.argv[1:])
    else: args = parser.parse_args()

    # Apply Global Flags
    FLAGS["verbose"] = args.verbose
    config = load_config()

    try:
        if args.command == "run":
            state = run_persona(args.gem, args.project, args.scope, config, dry_run=args.dry_run)
            if args.dry_run: print(json.dumps(state, indent=2))
        elif args.command == "list":
            for cat, gems in get_gems_list(config).items():
                title = f"{cat} (Private & Custom)" if cat == "LOCAL" else f"{cat} (Community Gems)" if cat == "INSTALLED" else f"{cat} (Built-in Standards)"
                print(title)
                if not gems: print("  (none)")
                else: 
                    for name, desc in gems: print(f"  - {name:<15} : {desc}")
                print("")
        elif args.command == "install":
            name = install_gem(args.source, config)
            print_msg("✅", f"Installation of '{name}' complete.")
        elif args.command == "uninstall":
            target = get_safe_installed_path(config, args.name)
            if target.exists():
                shutil.rmtree(target)
                print_msg("🗑️", f"Uninstalled {args.name}")
            else: print_err(f"Gem '{args.name}' not found.")
        elif args.command == "update":
            target = get_safe_installed_path(config, args.name)
            if target.exists():
                print_msg("⬇️", f"Updating {args.name}...")
                run_proc(["git", "pull"], cwd=target)
                hydrate_gem(target)
            else: print_err(f"Gem '{args.name}' not found.")
        elif args.command == "config":
            for k, v in config.items(): print(f"{k:<25} = {v}")
        elif args.command == "search":
            search_gems(args.query)
    except Exception as e:
        print_err(str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()
