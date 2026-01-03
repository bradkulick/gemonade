#!/usr/bin/env python3
import os
import json
import shutil
import argparse
import sys
from pathlib import Path

def load_gem_manifest(gem_path):
    manifest_path = gem_path / "gem.json"
    if not manifest_path.exists():
        print(f"Error: Not a valid Gem. Missing {manifest_path}")
        sys.exit(1)
    
    with open(manifest_path, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {manifest_path}")
            sys.exit(1)

def create_extension_manifest(gem_data):
    """Maps Gemonade Gem metadata to Gemini Extension metadata."""
    return {
        "name": gem_data.get("name", "unknown-extension"),
        "version": gem_data.get("version", "0.1.0"),
        "description": gem_data.get("description", ""),
        "contextFileName": "GEMINI.md"
    }

def graduate_gem(gem_path, output_dir):
    gem_path = Path(gem_path).resolve()
    gem_data = load_gem_manifest(gem_path)
    gem_name = gem_data.get("name")
    
    # Define target directory
    target_path = Path(output_dir) / gem_name
    
    if target_path.exists():
        print(f"Warning: Target directory {target_path} already exists.")
        overwrite = input("Overwrite? (y/N): ").lower()
        if overwrite == 'y':
            shutil.rmtree(target_path)
        else:
            print("Aborting.")
            sys.exit(0)
    
    print(f"🎓 Graduating '{gem_name}'...")
    print(f"   Source: {gem_path}")
    print(f"   Target: {target_path}")

    # 1. Create Directory
    target_path.mkdir(parents=True, exist_ok=True)

    # 2. Generate gemini-extension.json
    extension_manifest = create_extension_manifest(gem_data)
    with open(target_path / "gemini-extension.json", "w") as f:
        json.dump(extension_manifest, f, indent=2)
    print("   ✅ Generated gemini-extension.json")

    # 3. Transform persona.md -> GEMINI.md
    persona_path = gem_path / "persona.md"
    if persona_path.exists():
        shutil.copy(persona_path, target_path / "GEMINI.md")
        print("   ✅ Transformed persona.md -> GEMINI.md")
    else:
        print("   ⚠️  Warning: No persona.md found. Extension will be brainless.")

    # 4. Copy support files
    # Blacklist of files to NOT copy
    ignore_files = {
        "gem.json", 
        "persona.md", 
        ".venv", 
        "__pycache__", 
        ".git",
        ".DS_Store"
    }
    
    copied_count = 0
    for item in gem_path.iterdir():
        if item.name in ignore_files:
            continue
        
        dest = target_path / item.name
        if item.is_dir():
            shutil.copytree(item, dest, ignore=shutil.ignore_patterns(".venv", "__pycache__", ".git"))
        else:
            shutil.copy2(item, dest)
        copied_count += 1
    
    print(f"   ✅ Copied {copied_count} support files/directories.")

    print(f"\n🎉 Graduation Complete!")
    print(f"To install this extension in Gemini CLI:")
    print(f"  gemini install extension {target_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Graduate a Gemonade Gem into a Gemini CLI Extension.")
    parser.add_argument("gem_path", help="Path to the source Gem (containing gem.json)")
    parser.add_argument("--out", default="graduates", help="Output directory (default: ./graduates)")
    
    args = parser.parse_args()
    
    graduate_gem(args.gem_path, args.out)
