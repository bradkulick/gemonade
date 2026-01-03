#!/usr/bin/env python3
import os
import json
import subprocess
import argparse
import sys
import shutil
from pathlib import Path

def run_command(command, cwd=None, check=True):
    """Runs a shell command and returns the output."""
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            check=check,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Stderr: {e.stderr}")
        if check:
            sys.exit(1)
        return None

def check_git_clean(gem_path):
    """Checks if the git repository is clean."""
    status = run_command("git status --porcelain", cwd=gem_path)
    if status:
        print("❌ Error: Git working directory is not clean. Please commit or stash changes.")
        sys.exit(1)

def load_manifest(manifest_path):
    with open(manifest_path, 'r') as f:
        return json.load(f)

def save_manifest(manifest_path, data):
    with open(manifest_path, 'w') as f:
        json.dump(data, f, indent=2)
        f.write('\n') # Add trailing newline

def bump_version(current_version, bump_type):
    major, minor, patch = map(int, current_version.split('.'))
    if bump_type == 'major':
        major += 1
        minor = 0
        patch = 0
    elif bump_type == 'minor':
        minor += 1
        patch = 0
    elif bump_type == 'patch':
        patch += 1
    return f"{major}.{minor}.{patch}"

def sync_github_metadata(gem_path, data):
    """Syncs gem.json description and topics to GitHub."""
    print("🔄 Syncing metadata to GitHub...")
    # Check if gh is installed
    if shutil.which("gh") is None:
        print("⚠️  Warning: GitHub CLI ('gh') not found. Skipping metadata sync.")
        return

    # Check if repo has a remote
    remotes = run_command("git remote", cwd=gem_path, check=False)
    if not remotes:
        print("⚠️  Warning: No git remote configured. Skipping GitHub sync.")
        return

    try:
        # 1. Ensure Topic
        cmd_topic = "gh repo edit --add-topic gemonade-gem"
        run_command(cmd_topic, cwd=gem_path, check=False)

        # 2. Sync Description
        description = data.get("description", "")
        if description:
            # Escape double quotes for shell safety
            safe_desc = description.replace('"', '\\"')
            cmd_desc = f'gh repo edit --description "{safe_desc}"'
            run_command(cmd_desc, cwd=gem_path, check=False)
            
        print("   ✅ Synced gem.json metadata (description & topics) to GitHub.")
    except Exception as e:
        print(f"   ⚠️  Failed to sync metadata: {e}")

def main():
    parser = argparse.ArgumentParser(description="Publish a Gemonade Gem (Version Bump + Git Release).")
    parser.add_argument("gem_path", help="Path to the Gem directory", default=".")
    args = parser.parse_args()

    gem_path = Path(args.gem_path).resolve()
    manifest_path = gem_path / "gem.json"

    if not manifest_path.exists():
        print(f"❌ Error: No gem.json found at {gem_path}")
        sys.exit(1)

    # 1. Check Git Status
    check_git_clean(gem_path)

    # 2. Version Bump
    data = load_manifest(manifest_path)
    current_version = data.get("version", "0.0.0")
    name = data.get("name", "unknown")
    
    print(f"📦 Publishing Gem: {name}")
    print(f"   Current Version: {current_version}")
    
    print("\nSelect version bump:")
    print("1) Patch (x.x.N+1)")
    print("2) Minor (x.N+1.0)")
    print("3) Major (N+1.0.0)")
    print("4) Cancel")
    
    choice = input("Enter choice [1-4]: ").strip()
    
    if choice == '1':
        new_version = bump_version(current_version, 'patch')
    elif choice == '2':
        new_version = bump_version(current_version, 'minor')
    elif choice == '3':
        new_version = bump_version(current_version, 'major')
    else:
        print("Aborted.")
        sys.exit(0)
        
    print(f"\n🚀 Bumping version to: {new_version}")
    
    # 3. Write new version
    data['version'] = new_version
    save_manifest(manifest_path, data)
    
    # 4. Git Operations
    print("💾 Committing and Tagging...")
    tag_name = f"v{new_version}"
    commit_msg = f"chore: release {tag_name}"
    
    run_command(f"git add gem.json", cwd=gem_path)
    run_command(f'git commit -m "{commit_msg}"', cwd=gem_path)
    run_command(f"git tag {tag_name}", cwd=gem_path)
    
    print("☁️  Pushing to remote...")
    run_command("git push", cwd=gem_path)
    run_command("git push --tags", cwd=gem_path)

    # 5. Enforce Findability & Metadata Sync
    sync_github_metadata(gem_path, data)

    print(f"\n✅ Published {name} {tag_name} successfully!")

if __name__ == "__main__":
    main()
