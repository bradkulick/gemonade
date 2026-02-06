#!/usr/bin/env python3
import json
import glob
import os
import sys
from datetime import datetime
from pathlib import Path

# Add project root to sys.path to allow imports from core
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.gemonade import print_msg, print_err

# Configuration
GEMINI_TMP_DIR = os.path.expanduser("~/.gemini/tmp")

def find_latest_session_log():
    """Finds the most recently modified session-*.json file in the Gemini tmp directories."""
    search_pattern = os.path.join(GEMINI_TMP_DIR, "*", "chats", "session-*.json")
    files = glob.glob(search_pattern)
    if not files:
        return None
    return max(files, key=os.path.getmtime)

def format_message(msg):
    """Formats a single message object into Markdown."""
    text = ""
    if msg['type'] == 'user':
        text += f"\n## 👤 User\n\n{msg.get('content', '')}\n"
    elif msg['type'] == 'gemini':
        if 'thoughts' in msg and msg['thoughts']:
             text += "\n<details><summary>🧠 <i>Thought Process</i></summary>\n\n"
             for t in msg['thoughts']:
                 text += f"- **{t.get('subject')}**: {t.get('description')}\n"
             text += "\n</details>\n"

        if msg.get('content'):
            text += f"\n## 🤖 Gemini\n\n{msg['content']}\n"
        
        if 'toolCalls' in msg and msg['toolCalls']:
            text += "\n### 🛠️ Tools Used\n"
            for tool in msg['toolCalls']:
                name = tool.get('displayName', tool.get('name'))
                args = json.dumps(tool.get('args', {}), indent=2)
                result = tool.get('resultDisplay')
                if not result and 'result' in tool:
                     try:
                         res_data = tool['result']
                         if isinstance(res_data, list) and len(res_data) > 0:
                            res_data = res_data[0]
                         result = res_data.get('functionResponse', {}).get('response', {}).get('output')
                     except:
                         result = str(tool.get('result'))
                
                result_str = str(result)
                if len(result_str) > 2000:
                    result_str = result_str[:2000] + "\n... (truncated)"

                text += f"**{name}**\n"
                text += f"```json\n{args}\n```\n"
                if result_str:
                    text += f"> **Result:**\n> ```\n> {result_str.replace(chr(10), chr(10) + '> ')}\n> ```\n\n"
    return text

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Save Gemini session logs as Markdown.")
    parser.add_argument("dest_dir", help="Directory where the Markdown file will be saved.")
    parser.add_argument("--project", help="The project context for this session.", default="global")
    
    args = parser.parse_args()
    dest_dir = os.path.expanduser(args.dest_dir)
    project_ctx = args.project
    
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir, exist_ok=True)

    log_file = find_latest_session_log()
    if not log_file:
        print_err("No Gemini session logs found in ~/.gemini/tmp/")
        sys.exit(1)

    try:
        with open(log_file, 'r') as f:
            data = json.load(f)
        
        session_id = data.get('sessionId', 'unknown')
        start_time = data.get('startTime', datetime.now().isoformat())
        
        try:
            dt_obj = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            date_str = dt_obj.strftime('%Y%m%d_%H%M')
            display_date = dt_obj.strftime('%A, %B %d, %Y at %I:%M %p')
        except ValueError:
            date_str = datetime.now().strftime('%Y%m%d_%H%M')
            display_date = start_time
        
        filename = f"session_{date_str}.md"
        output_path = os.path.join(dest_dir, filename)

        markdown_content = f"# Gemini Session Log\n"
        markdown_content += f"- **Date:** {display_date}\n"
        markdown_content += f"- **Project:** {project_ctx}\n"
        markdown_content += f"- **ID:** {session_id}\n"
        markdown_content += f"- **Source Log:** `{log_file}`\n"
        markdown_content += f"---\n"

        for msg in data.get('messages', []):
            markdown_content += format_message(msg)

        with open(output_path, 'w') as f:
            f.write(markdown_content)

        print_msg("✅", f"Session saved to: {output_path}")

        # --- V6 Memory Indexing (The Ledger) ---
        topic = "General Session"
        summary_found = False
        for msg in reversed(data.get('messages', [])):
            if msg['type'] == 'gemini':
                content = msg.get('content', '')
                if '```summary' in content:
                    try:
                        block = content.split('```summary')[1].split('```')[0].strip()
                        lines = block.split('\n')
                        goal = ""
                        outcome = ""
                        for line in lines:
                            if line.upper().startswith('GOAL:'): goal = line.split(':', 1)[1].strip()
                            if line.upper().startswith('OUTCOME:'): outcome = line.split(':', 1)[1].strip()
                        
                        if goal or outcome:
                            topic = f"{goal} -> {outcome}"
                            if len(topic) > 100: topic = topic[:97] + "..."
                            print_msg("📚", f"Indexed via Self-Summary: '{topic}'")
                            summary_found = True
                            break
                    except: pass
        
        if not summary_found:
            for msg in data.get('messages', []):
                if msg['type'] == 'user':
                    content = msg.get('content', '').strip()
                    if content:
                        first_line = content.split('\n')[0]
                        topic = (first_line[:75] + '...') if len(first_line) > 75 else first_line
                        print_msg("📚", f"Indexed via First Prompt: '{topic}'")
                        break
        
        ledger_path = os.path.join(dest_dir, "history.jsonl")
        ledger_entry = {
            "date": date_str,
            "display_date": display_date,
            "file": filename,
            "topic": topic
        }
        
        with open(ledger_path, 'a') as f:
            f.write(json.dumps(ledger_entry) + "\n")

    except Exception as e:
        print_err(f"Processing failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()