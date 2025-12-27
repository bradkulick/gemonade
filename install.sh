#!/bin/bash

# Geode Installer
# Sets up symlinks and initial configuration for the Geode framework.

GEODE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="$HOME/bin"
CONFIG_FILE="$HOME/.geode_config"

echo "💎 Installing Geode Framework..."

# 1. Create directory for symlinks if it doesn't exist
mkdir -p "$BIN_DIR"

# 2. Symlink the geode launcher
echo "🔗 Linking 'geode' command to ~/bin/geode"
ln -sf "$GEODE_ROOT/bin/geode" "$BIN_DIR/geode"
chmod +x "$GEODE_ROOT/bin/geode"

# 3. Initialize default config if missing
if [ ! -f "$CONFIG_FILE" ]; then
    echo "📝 Creating default config at ~/.geode_config"
    cat <<EOF > "$CONFIG_FILE"
# Geode User Configuration
# Defaulting to self-contained mode (knowledge inside geode folder)
G_KNOWLEDGE_DIR="$GEODE_ROOT/knowledge"
GEODE_RETENTION_DAYS="30"
EOF
fi

# 4. Ensure directory structure exists
mkdir -p "$GEODE_ROOT/knowledge/sessions"
mkdir -p "$GEODE_ROOT/packages/installed"
mkdir -p "$GEODE_ROOT/packages/local"

# 4. Success Message
echo ""
echo "✅ Geode Installation Complete!"
echo "-------------------------------------------------------"
echo "To get started:"
echo "1. Ensure ~/bin is in your PATH."
echo "   Run this command now: export PATH=\"\$HOME/bin:\$PATH\""
echo "   (Add that line to your ~/.bashrc to make it permanent)"
echo "2. Run 'geode list' to see available personas."
echo "3. Run 'geode sys' to meet your framework administrator."
echo "-------------------------------------------------------"
