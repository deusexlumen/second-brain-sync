#!/bin/bash
# Setup script for Gemini Video Analysis Tool
# Run this once to install dependencies

echo "Setting up Gemini Video Analysis Tool..."

# Check if running in venv or system
if [ -n "$VIRTUAL_ENV" ]; then
    echo "Installing in virtual environment..."
    pip install google-genai
else
    echo "Creating virtual environment..."
    mkdir -p ~/.openclaw/venvs
    python3 -m venv ~/.openclaw/venvs/gemini
    source ~/.openclaw/venvs/gemini/bin/activate
    pip install google-genai
    echo "Venv created at ~/.openclaw/venvs/gemini"
fi

echo "Setup complete!"
echo ""
echo "Usage:"
echo "  ~/.openclaw/venvs/gemini/bin/python3 tools/gemini_video_analyze.py <video.mp4> [prompt]"
