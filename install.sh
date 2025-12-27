#!/bin/bash

# Gemonade Installer
# Sets up symlinks and initial configuration for the Gemonade framework.

GEMONADE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="$HOME/bin"
CONFIG_FILE="$HOME/.gemonade_config"

echo "💎 Installing Gemonade Framework..."

# 0. Prerequisite Check
echo "🔍 Checking dependencies..."
MISSING_DEPS=0

if ! command -v node &> /dev/null; then
    echo "⚠️  Node.js is not installed."
    MISSING_DEPS=1
fi

if ! command -v python3 &> /dev/null; then
    echo "⚠️  Python 3 is not installed."
    MISSING_DEPS=1
fi

if ! command -v gemini &> /dev/null; then
    echo "⚠️  Google Gemini CLI (@google/gemini-cli) is not installed."
    echo "   Install it via: npm install -g @google/gemini-cli"
    MISSING_DEPS=1
fi

if [ $MISSING_DEPS -eq 1 ]; then
    echo "❌ Missing dependencies detected. Please install them and run this script again."
    exit 1
else
    echo "✅ Dependencies found."
fi

# 1. Create directory for symlinks if it doesn't exist
mkdir -p "$BIN_DIR"

# 2. Symlink the gemonade launcher
echo "🔗 Linking 'gemonade' command to ~/bin/gemonade"
ln -sf "$GEMONADE_ROOT/bin/gemonade" "$BIN_DIR/gemonade"
chmod +x "$GEMONADE_ROOT/bin/gemonade"

# 3. Initialize default config if missing
if [ ! -f "$CONFIG_FILE" ]; then
    echo "📝 Creating default config at ~/.gemonade_config"
    cat <<EOF > "$CONFIG_FILE"
# Gemonade User Configuration
# Defaulting to self-contained mode (knowledge inside gemonade folder)
G_KNOWLEDGE_DIR="$GEMONADE_ROOT/knowledge"
GEMONADE_RETENTION_DAYS="30"
EOF
fi

# 4. Ensure directory structure exists
mkdir -p "$GEMONADE_ROOT/knowledge/sessions"
mkdir -p "$GEMONADE_ROOT/packages/installed"
mkdir -p "$GEMONADE_ROOT/packages/local"

# 4. Success Message
echo ""
echo "✅ Gemonade Installation Complete!"
echo "-------------------------------------------------------"
echo "To get started:"
echo "1. Ensure ~/bin is in your PATH."
echo "   Run this command now: export PATH=\"\$HOME/bin:\$PATH\""
echo "   (Add that line to your ~/.bashrc to make it permanent)"
echo "2. Run 'gemonade list' to see available personas."
echo "3. Run 'gemonade sys' to meet your framework administrator."
echo "-------------------------------------------------------"
