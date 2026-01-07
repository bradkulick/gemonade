#!/usr/bin/env python3
"""
Gemonade Memory Re-Indexer
Scans existing session logs and backfills the 'history.jsonl' ledger.
"""

import os
import json
import glob
from pathlib import Path
from datetime import datetime

GEMONADE_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = GEMONADE_ROOT / "knowledge" / "sessions"

def index_file(filepath):
    try:
        content = filepath.read_text()
        
        # 1. Extract Date
        # Filename format: session_YYYYMMDD_HHMM.md
        filename = filepath.name
        date_str = "Unknown"
        display_date = "Unknown"
        if filename.startswith("session_"):
            try:
                # session_20251230_1913.md
                dt_part = filename.split("_")[1] # 20251230
                time_part = filename.split("_")[2].split(".")[0] # 1913
                dt = datetime.strptime(f"{dt_part}{time_part}", "%Y%m%d%H%M")
                date_str = dt.strftime('%Y%m%d_%H%M')
                display_date = dt.strftime('%A, %B %d, %Y')
            except: pass

        # 2. Extract Topic
        topic = "Legacy Session"
        
        # Method A: Look for Summary Block
        if "```summary" in content:
            try:
                block = content.split("```summary")[1].split("```")[0]
                lines = block.strip().split('\n')
                goal = next((l.split(':',1)[1].strip() for l in lines if l.upper().startswith("GOAL:")), "")
                outcome = next((l.split(':',1)[1].strip() for l in lines if l.upper().startswith("OUTCOME:")), "")
                if goal or outcome:
                    topic = f"{goal} -> {outcome}"
            except: pass
        
        # Method B: First User Prompt
        if topic == "Legacy Session":
            # Very rough parsing of MD structure
            # ## 👤 User\n\nPrompt...
            parts = content.split("## 👤 User")
            if len(parts) > 1:
                prompt = parts[1].strip().split("\n")[0] # First line of prompt
                if prompt:
                    topic = (prompt[:75] + '...') if len(prompt) > 75 else prompt

        return {
            "date": date_str,
            "display_date": display_date,
            "file": filename,
            "topic": topic
        }

    except Exception as e:
        print(f"Failed to parse {filepath.name}: {e}")
        return None

def main():
    print(f"🧠 Re-indexing session history from: {KNOWLEDGE_DIR}")
    
    # Iterate over all project folders
    # Structure: sessions/{persona}/{project}/*.md
    personas = [d for d in KNOWLEDGE_DIR.iterdir() if d.is_dir() and d.name != "archive"]
    
    total_indexed = 0
    
    for persona_dir in personas:
        for project_dir in persona_dir.iterdir():
            if not project_dir.is_dir(): continue
            
            ledger_path = project_dir / "history.jsonl"
            
            # Find all MD files
            md_files = sorted(project_dir.glob("session_*.md"))
            if not md_files: continue
            
            print(f"   Processing {persona_dir.name}/{project_dir.name} ({len(md_files)} sessions)...")
            
            entries = []
            for md in md_files:
                entry = index_file(md)
                if entry:
                    entries.append(entry)
            
            # Write Ledger (Overwrite mode to ensure clean slate)
            if entries:
                with open(ledger_path, 'w') as f:
                    for e in entries:
                        f.write(json.dumps(e) + "\n")
                total_indexed += len(entries)

    print(f"✅ Re-indexing complete. Processed {total_indexed} sessions.")

if __name__ == "__main__":
    main()
