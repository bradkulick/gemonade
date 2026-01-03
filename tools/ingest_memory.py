#!/usr/bin/env python3
"""
Gemonade Memory Ingester (V4)
Parses the latest session log (Markdown) and ingests it into a local ChromaDB vector store.
"""
import os
import sys
import re
import argparse
import glob
from datetime import datetime

# --- Configuration ---
GEMONADE_HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.expanduser("~/.gemonade/chroma_db")
SESSION_DIR = os.path.join(GEMONADE_HOME, "knowledge", "sessions")

# --- Dependency Check ---
try:
    import chromadb
    from chromadb.config import Settings
except ImportError:
    print("⚠️  Advanced Memory not active (missing chromadb).")
    print("   Run 'gemonade setup-memory' to enable.")
    sys.exit(0)

def find_latest_session_file(persona=None):
    """Finds the most recently modified session markdown file."""
    search_path = SESSION_DIR
    if persona:
        search_path = os.path.join(SESSION_DIR, persona)
    
    # Recursive search for .md files
    files = glob.glob(os.path.join(search_path, "**", "*.md"), recursive=True)
    if not files:
        return None
    return max(files, key=os.path.getmtime)

def parse_markdown_session(file_path):
    """
    Parses a Gemonade Session Markdown file.
    Returns metadata and a list of interaction chunks.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract Header Metadata
    metadata = {
        "source_file": file_path,
        "date": datetime.now().isoformat(),
        "project": "global",
        "id": "unknown"
    }

    # Simple regex parsing for header keys
    date_match = re.search(r'- \*\*Date:\*\* (.*)', content)
    id_match = re.search(r'- \*\*ID:\*\* (.*)', content)
    proj_match = re.search(r'- \*\*Project:\*\* (.*)', content)

    if date_match: metadata["date"] = date_match.group(1).strip()
    if id_match: metadata["id"] = id_match.group(1).strip()
    if proj_match: metadata["project"] = proj_match.group(1).strip()

    # Extract Conversation Chunks (User + Gemini pairs)
    # We split by "## 👤 User" to find interaction blocks
    chunks = []
    
    # Split content by User header
    raw_blocks = re.split(r'\n## 👤 User\n', content)
    
    # Skip the header block (index 0)
    for block in raw_blocks[1:]:
        # block contains User text... then "## 🤖 Gemini"... then Gemini text
        parts = re.split(r'\n## 🤖 Gemini\n', block)
        
        user_text = parts[0].strip()
        gemini_text = ""
        if len(parts) > 1:
            gemini_text = parts[1].strip()
            
            # Clean up tool outputs from gemini text to reduce noise
            # Remove <details> thoughts
            gemini_text = re.sub(r'<details>.*?</details>', '', gemini_text, flags=re.DOTALL)
            # Remove tool blocks (optional, but good for semantic search quality)
            # gemini_text = re.sub(r'### 🛠️ Tools Used.*', '', gemini_text, flags=re.DOTALL)

        if user_text and gemini_text:
            chunks.append({
                "user": user_text,
                "gemini": gemini_text,
                "full_text": f"User: {user_text}\nGemini: {gemini_text}"
            })

    return metadata, chunks

def ingest_session(file_path, project_override=None, persona_override=None):
    print(f"🧠 Ingesting session: {os.path.basename(file_path)}")
    
    # 1. Parse
    meta, chunks = parse_markdown_session(file_path)
    
    if project_override:
        meta["project"] = project_override
    
    # If persona not in file (it currently isn't), use the override
    meta["persona"] = persona_override if persona_override else "unknown"

    if not chunks:
        print("   ⚪ No conversational chunks found.")
        return

    # 2. Init DB
    client = chromadb.PersistentClient(path=DB_PATH)
    
    # We use a single collection for everything, relying on metadata filtering
    collection = client.get_or_create_collection(name="gemonade_memory")

    # 3. Prepare Vectors
    ids = []
    documents = []
    metadatas = []

    for idx, chunk in enumerate(chunks):
        # Create a unique ID for this memory chunk
        chunk_id = f"{meta['id']}_{idx}"
        
        ids.append(chunk_id)
        documents.append(chunk["full_text"])
        metadatas.append({
            "project": meta["project"],
            "persona": meta["persona"],
            "session_id": meta["id"],
            "date": meta["date"],
            "source": meta["source_file"],
            "type": "conversation"
        })

    # 4. Upsert
    try:
        collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )
        print(f"   ✅ Indexed {len(ids)} interactions into Project: '{meta['project']}' (Persona: '{meta['persona']}')")
    except Exception as e:
        print(f"   ❌ Error inserting into ChromaDB: {e}")

def main():
    parser = argparse.ArgumentParser(description="Ingest Gemini session into Vector Memory.")
    parser.add_argument("--file", help="Specific session file to ingest. Defaults to latest.")
    parser.add_argument("--project", help="Override project context.")
    parser.add_argument("--persona", help="Override persona context.")
    
    args = parser.parse_args()
    
    target_file = args.file
    if not target_file:
        target_file = find_latest_session_file()
    
    if not target_file:
        # Silent exit if no files exist yet
        return

    ingest_session(target_file, args.project, args.persona)

if __name__ == "__main__":
    main()
