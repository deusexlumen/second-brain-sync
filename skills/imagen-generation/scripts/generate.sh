#!/bin/bash
# Imagen Generation Script
# Usage: generate.sh "prompt" [options]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLIENT="$SCRIPT_DIR/imagen_client.py"

# Default values
MODEL="generate"
COUNT=1
ASPECT="1:1"
SIZE=""
PERSON_GEN="allow_adult"
OUTPUT="/tmp/imagen-output"

# Parse arguments
PROMPT="$1"
shift

while [[ $# -gt 0 ]]; do
    case $1 in
        --model)
            MODEL="$2"
            shift 2
            ;;
        --count)
            COUNT="$2"
            shift 2
            ;;
        --aspect)
            ASPECT="$2"
            shift 2
            ;;
        --size)
            SIZE="--size $2"
            shift 2
            ;;
        --person-generation)
            PERSON_GEN="$2"
            shift 2
            ;;
        --output)
            OUTPUT="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: generate.sh \"prompt\" [options]"
            echo ""
            echo "Options:"
            echo "  --model [generate|ultra|fast]    Model variant (default: generate)"
            echo "  --count [1-4]                    Number of images (default: 1)"
            echo "  --aspect [1:1|3:4|4:3|9:16|16:9] Aspect ratio (default: 1:1)"
            echo "  --size [1K|2K]                   Image size (ultra/generate only)"
            echo "  --person-generation [dont_allow|allow_adult|allow_all]"
            echo "  --output [path]                  Output directory"
            echo "  --help                           Show this help"
            echo ""
            echo "Examples:"
            echo "  generate.sh \"A cat playing piano\""
            echo "  generate.sh \"Mountain sunset\" --model ultra --count 2"
            echo "  generate.sh \"Portrait\" --aspect 9:16 --model fast"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Run Python client
python3 "$CLIENT" "$PROMPT" \
    --model "$MODEL" \
    --count "$COUNT" \
    --aspect "$ASPECT" \
    $SIZE \
    --person-generation "$PERSON_GEN" \
    --output "$OUTPUT"
