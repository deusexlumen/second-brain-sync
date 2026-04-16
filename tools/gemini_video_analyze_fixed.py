#!/usr/bin/env python3
"""
Gemini Video Analysis Tool - FIXED VERSION
Uses Gemini 3.1 Pro Preview with proper error handling
"""

import os
import sys
import time
from google import genai
from google.genai import types

# API Key from config
API_KEY = "AIzaSyDfSX88OXe9BKE1-TaMAcwVAdYseSdH8MQ"

def analyze_video(video_path, prompt_text=None):
    """Analyze a video using Gemini 3.1 Pro Preview"""
    
    client = genai.Client(api_key=API_KEY)
    
    if not prompt_text:
        prompt_text = """Analysiere dieses Video im Detail:

1. Worum geht es im Video? Was ist das Hauptthema?
2. Welches Problem wird gelöst?
3. Welche Technologie/Architektur wird verwendet?
4. Ist es relevant für ein Memory-System für AI Agents?
5. Was sind die Kernpunkte, die man implementieren sollte?

Antworte auf Deutsch, strukturiert und detailliert."""

    print(f"📹 Uploading video: {video_path}")
    print(f"📊 File size: {os.path.getsize(video_path) / (1024*1024):.1f} MB")
    
    try:
        # Upload the video file
        video_file = client.files.upload(file=video_path)
        print(f"✅ Uploaded: {video_file.name}")
        
        # Wait for processing with longer timeout
        print("⏳ Waiting for video processing...")
        max_wait = 300  # 5 minutes
        waited = 0
        
        while waited < max_wait:
            file_info = client.files.get(name=video_file.name)
            state = file_info.state.name if hasattr(file_info.state, 'name') else str(file_info.state)
            
            print(f"  State: {state} ({waited}s)")
            
            if state == "ACTIVE":
                print(f"✅ Video ready after {waited}s")
                break
            elif state == "FAILED":
                print("❌ Video processing failed!")
                return None
                
            time.sleep(10)
            waited += 10
        else:
            print("⏰ Timeout waiting for video processing")
            return None
        
        print("🤖 Analyzing with Gemini 3.1 Flash Lite...")
        
        # Generate content with Gemini 3.1 Flash Lite (my default model)
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",  # Using Flash Lite as specified
            contents=[
                video_file,
                prompt_text
            ],
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_level="high")
            )
        )
        
        return response.text
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 gemini_video_analyze_fixed.py <video_file> [prompt]")
        sys.exit(1)
    
    video_path = sys.argv[1]
    prompt = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(video_path):
        print(f"❌ File not found: {video_path}")
        sys.exit(1)
    
    result = analyze_video(video_path, prompt)
    
    if result:
        print("\n" + "="*60)
        print("📊 ANALYSE ERGEBNIS:")
        print("="*60)
        print(result)
        print("="*60)
    else:
        print("❌ Analysis failed")
        sys.exit(1)
