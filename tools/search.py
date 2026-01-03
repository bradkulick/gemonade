#!/usr/bin/env python3
import subprocess
import argparse
import sys
import json
import shutil

def run_gh_search(query):
    if not shutil.which("gh"):
        print("❌ Error: GitHub CLI ('gh') is not installed.")
        print("   Please install it to use the search feature: https://cli.github.com/")
        sys.exit(1)

    # Construct the search query
    # We use the explicit --topic flag for reliability
    cmd = [
        "gh", "search", "repos", 
        "--topic", "gemonade-gem",
        "--json", "name,description,url,stargazersCount,owner",
        "--limit", "10"
    ]
    
    # Append the user query if provided
    if query:
        cmd.append(query)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error searching GitHub: {e.stderr}")
        return []

def main():
    parser = argparse.ArgumentParser(description="Search for Gemonade Gems on GitHub.")
    parser.add_argument("query", nargs="?", default="", help="Search term (optional)")
    args = parser.parse_args()

    print(f"🔍 Searching for Gemonade Gems matching: '{args.query}'...")
    
    results = run_gh_search(args.query)

    if not results:
        print("   No gems found.")
        print("   (Tip: Try a broader term or check if 'gh' is authenticated)")
        return

    print(f"\nFound {len(results)} gems:\n")
    
    for repo in results:
        name = repo.get("name")
        owner = repo.get("owner", {}).get("login", "unknown")
        full_name = f"{owner}/{name}"
        desc = repo.get("description", "No description provided.")
        url = repo.get("url")
        stars = repo.get("stargazersCount", 0)
        
        print(f"💎 {full_name} (⭐ {stars})")
        print(f"   {desc}")
        print(f"   Install: gemonade install {url}")
        print("")

if __name__ == "__main__":
    main()
