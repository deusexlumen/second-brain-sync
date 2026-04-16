#!/bin/bash
# Discord-Transcribe-Wrapper
# Nutzt kein exec direkt, sondern liest aus einer Queue

AUDIO_FILE="$1"
if [ -f "$AUDIO_FILE" ]; then
    export GROQ_API_KEY=$(cat /root/.openclaw/workspace/config/groq.env | grep GROQ_API_KEY | cut -d= -f2)
    python3 /root/.openclaw/workspace/tools/audio_transcribe.py "$AUDIO_FILE"
else
    echo "Error: Audio file not found: $AUDIO_FILE"
    exit 1
fi
