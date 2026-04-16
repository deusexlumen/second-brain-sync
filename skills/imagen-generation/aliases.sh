#!/bin/bash
# Imagen Quick Aliases
# Source this file: source ~/.openclaw/workspace/skills/imagen-generation/aliases.sh
# Or add to your ~/.bashrc

IMAGEN_DIR="$HOME/.openclaw/workspace/skills/imagen-generation/scripts"

# Main commands
alias imagen="python3 $IMAGEN_DIR/imagen_client.py"
alias imgen-limits="python3 $IMAGEN_DIR/imagen_client.py 'check' --check-limits"
alias imgen-styles="python3 $IMAGEN_DIR/imagen_client.py 'check' --list-styles"

# Quick shortcuts
alias img="python3 $IMAGEN_DIR/imagen_client.py"
alias img-limits="python3 $IMAGEN_DIR/imagen_client.py 'check' --check-limits"

echo "Imagen aliases loaded!"
echo "Commands: imagen, imgen-limits, imgen-styles, img, img-limits"
