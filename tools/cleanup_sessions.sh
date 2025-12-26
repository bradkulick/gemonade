#!/bin/bash

# Geode Session Maintenance Script
# Archives session logs older than a specified retention period.
# Logic: Argument > Env Var > Default (30)

# Configuration
CONFIG_FILE="$HOME/.geode_config"

# 1. Load User Config (for Defaults)
if [ -f "$CONFIG_FILE" ]; then
    source "$CONFIG_FILE"
fi

# 2. Determine Retention Period
# Priority 1: Command line argument
if [ -n "$1" ]; then
    RETENTION_DAYS="$1"
# Priority 2: Environment Variable (from config)
elif [ -n "$GEODE_RETENTION_DAYS" ]; then
    RETENTION_DAYS="$GEODE_RETENTION_DAYS"
# Priority 3: Hard Default
else
    RETENTION_DAYS="30"
fi

# 3. Determine Directories
# Use configured Knowledge Dir or fallback
KNOWLEDGE_ROOT="${G_KNOWLEDGE_DIR:-$HOME/gemini_knowledge}"
SESSION_ROOT="$KNOWLEDGE_ROOT/sessions"
ARCHIVE_ROOT="$SESSION_ROOT/archive/$(date +%Y-%m)"

# 4. Execution
echo "🧹 Geode Cleanup: Moving sessions older than $RETENTION_DAYS days..."
echo "   Source:  $SESSION_ROOT"
echo "   Archive: $ARCHIVE_ROOT"

if [ ! -d "$SESSION_ROOT" ]; then
    echo "❌ Session directory not found: $SESSION_ROOT"
    exit 1
fi

mkdir -p "$ARCHIVE_ROOT"

# Find and Move
# -mindepth 2 ensures we look inside persona subfolders (sessions/thm/*.md) but don't move the folders themselves
find "$SESSION_ROOT" -mindepth 2 -name "*.md" -type f -mtime +$RETENTION_DAYS -exec mv -v {} "$ARCHIVE_ROOT/" \;

echo "✅ Maintenance Complete."