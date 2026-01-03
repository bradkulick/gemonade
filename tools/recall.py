#!/usr/bin/env python3
"""
Gemonade Recall Tool (V4)
Performs semantic search over the Gemonade Memory Store (ChromaDB).
"""
import os
import sys
import argparse
import json

# --- Configuration ---
GEMONADE_HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.expanduser("~/.gemonade/chroma_db")

# --- Dependency Check ---
try:
    import chromadb
except ImportError:
    # Try to re-exec with the Core Venv python if we are running as system python
    core_venv_python = os.path.expanduser("~/.gemonade/.venv/bin/python3")
    if os.path.exists(core_venv_python) and sys.executable != core_venv_python:
        os.execv(core_venv_python, [core_venv_python] + sys.argv)
    
    # If we are here, we failed to load chroma
    print(json.dumps({
        "error": "Advanced Memory is not installed.",
        "hint": "Run 'gemonade setup-memory' to enable."
    }))
    sys.exit(1)

def recall(query, project=None, persona=None, scope="project", limit=5):
    if not os.path.exists(DB_PATH):
        return {"results": [], "message": "Memory database is empty."}

    client = chromadb.PersistentClient(path=DB_PATH)
    
    try:
        collection = client.get_collection(name="gemonade_memory")
    except ValueError:
        return {"results": [], "message": "No memories found yet."}

    # Build Metadata Filter
    where_filter = {}
    filters = []

    # 1. Project Filter
    if project and project != "global":
        filters.append({"project": project})
    
    # 2. Persona Filter
    # We apply persona filter unless we are in GLOBAL scope
    if scope != "global" and persona:
         filters.append({"persona": persona})

    # Combine Filters
    if len(filters) > 1:
        where_filter = {"$and": filters}
    elif len(filters) == 1:
        where_filter = filters[0]
    
    results = collection.query(
        query_texts=[query],
        n_results=limit,
        where=where_filter
    )

    formatted_results = []
    
    # Results structure is lists of lists (one per query)
    if results['documents']:
        docs = results['documents'][0]
        metas = results['metadatas'][0]
        distances = results['distances'][0] if results['distances'] else [0]*len(docs)

        for doc, meta, dist in zip(docs, metas, distances):
            formatted_results.append({
                "content": doc,
                "project": meta.get('project'),
                "persona": meta.get('persona', 'unknown'),
                "date": meta.get('date'),
                "relevance": round(1 - dist, 2) # Crude approx of relevance
            })

    return {"results": formatted_results, "count": len(formatted_results)}

def main():
    parser = argparse.ArgumentParser(description="Recall memories from Gemonade Vector Store.")
    parser.add_argument("query", help="The question or topic to remember.")
    parser.add_argument("--project", help="Filter by project context.", default=None)
    parser.add_argument("--limit", type=int, default=3, help="Max results to return.")
    
    args = parser.parse_args()
    
    # Auto-detect project env var if flag not set
    project = args.project
    scope = os.environ.get("GEMONADE_SCOPE", "project")
    persona = os.environ.get("GEMONADE_PERSONA")

    if not project:
        # If we are in 'project' scope, we filter by the current project
        if scope == "project" and "GEMONADE_PROJECT" in os.environ:
            project = os.environ["GEMONADE_PROJECT"]
        # If scope is 'persona' or 'global', we default to wider search (project=None)

    data = recall(args.query, project, persona, scope, args.limit)
    
    # Output JSON for the LLM to parse easily
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()
