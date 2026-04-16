#!/bin/bash
# Check Imagen Rate Limits

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLIENT="$SCRIPT_DIR/imagen_client.py"

python3 "$CLIENT" "check" --check-limits
