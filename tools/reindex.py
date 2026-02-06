#!/usr/bin/env python3
"""
Gemonade Memory Re-Indexer
Scans existing session logs and backfills the 'history.jsonl' ledger.
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime

# Add project root to sys.path to allow imports from core
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.gemonade import print_msg, print_err

KNOWLEDGE_DIR = PROJECT_ROOT / "knowledge" / "sessions"

def index_file(filepath):
    try:
        content = filepath.read_text()
        filename = filepath.name
        date_str = "Unknown"
        display_date = "Unknown"
        
        if filename.startswith("session_"):
            try:
                parts = filename.split("_")
                dt_part = parts[1]
                time_part = parts[2].split(".")[0]
                dt = datetime.strptime(f"{dt_part}{time_part}", "%Y%m%d%H%M")
                date_str = dt.strftime('%Y%m%d_%H%M')
                display_date = dt.strftime('%A, %B %d, %Y')
            except: pass

        topic = "Legacy Session"
        
        if "```summary" in content:
            try:
                block = content.split("```summary")[1].split("```")[0]
                lines = block.strip().split('\n')
                goal = next((l.split(':',1)[1].strip() for l in lines if l.upper().startswith("GOAL:")), "")
                outcome = next((l.split(':',1)[1].strip() for l in lines if l.upper().startswith("OUTCOME:")), "")
                if goal or outcome:
                    topic = f"{goal} -> {outcome}"
            except: pass
        
        if topic == "Legacy Session":
            parts = content.split("## 👤 User")
            if len(parts) > 1:
                prompt = parts[1].strip().split("\n")[0]
                if prompt:
                    topic = (prompt[:75] + '...') if len(prompt) > 75 else prompt

        return {
            "date": date_str,
            "display_date": display_date,
            "file": filename,
            "topic": topic
        }

    except Exception as e:
        print_err(f"Failed to parse {filepath.name}: {e}")
        return None

def main():
    print_msg("🧠", f"Re-indexing session history from: {KNOWLEDGE_DIR}")
    
    if not KNOWLEDGE_DIR.exists():
        print_err("Knowledge directory not found.")
        return

    personas = [d for d in KNOWLEDGE_DIR.iterdir() if d.is_dir() and d.name != "archive"]
    total_indexed = 0
    
    for persona_dir in personas:
        for project_dir in persona_dir.iterdir():
            if not project_dir.is_dir(): continue
            
            ledger_path = project_dir / "history.jsonl"
            md_files = sorted(project_dir.glob("session_*.md"))
            if not md_files: continue
            
            print(f"   Processing {persona_dir.name}/{project_dir.name} ({len(md_files)} sessions)...")
            
            entries = []
            for md in md_files:
                entry = index_file(md)
                if entry:
                    entries.append(entry)
            
            if entries:
                with open(ledger_path, 'w') as f:
                    for e in entries:
                        f.write(json.dumps(e) + "\n")
                total_indexed += len(entries)

    print_msg("✅", f"Re-indexing complete. Processed {total_indexed} sessions.")

if __name__ == "__main__":
    main()