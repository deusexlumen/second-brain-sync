#!/usr/bin/env python3
"""
YouTube Video Analyzer - Persistent Solution
Supports: Invidious API + YouTube Data API v3
Usage: python3 youtube_analyzer.py <youtube_url>
"""

import sys
import os
import json
import urllib.request
import urllib.error
from urllib.parse import urlparse, parse_qs

# Invidious Instances (fallback list)
INVIDIOUS_INSTANCES = [
    "https://iv.datura.network",
    "https://iv.nboeck.de",
    "https://iv.melmac.space",
    "https://yt.artemislena.eu",
    "https://iv.nboeck.de",
]

def extract_video_id(url):
    """Extract YouTube video ID from various URL formats"""
    parsed = urlparse(url)
    
    # youtu.be/XXXX
    if parsed.netloc == 'youtu.be':
        return parsed.path[1:]
    
    # youtube.com/watch?v=XXXX
    if parsed.netloc in ('www.youtube.com', 'youtube.com'):
        if parsed.path == '/watch':
            return parse_qs(parsed.query).get('v', [None])[0]
        # youtube.com/embed/XXXX
        if parsed.path.startswith('/embed/'):
            return parsed.path.split('/')[2]
        # youtube.com/shorts/XXXX
        if parsed.path.startswith('/shorts/'):
            return parsed.path.split('/')[2]
    
    return None

def try_invidious(video_id):
    """Try to fetch video info from Invidious instances"""
    for instance in INVIDIOUS_INSTANCES:
        try:
            url = f"{instance}/api/v1/videos/{video_id}"
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (compatible; Analyzer/1.0)'
            })
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status == 200:
                    return json.loads(response.read().decode('utf-8'))
        except Exception as e:
            continue
    return None

def try_youtube_api(video_id, api_key):
    """Try to fetch video info from YouTube Data API"""
    try:
        url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails,statistics&id={video_id}&key={api_key}"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                if data.get('items'):
                    return data['items'][0]
    except Exception as e:
        print(f"YouTube API Error: {e}")
    return None

def format_invidious_output(data):
    """Format Invidious response for display"""
    return f"""
**Titel:** {data.get('title', 'N/A')}
**Kanal:** {data.get('author', 'N/A')}
**Beschreibung:** {data.get('description', 'N/A')[:200]}...
**Views:** {data.get('viewCount', 'N/A')}
**Likes:** {data.get('likeCount', 'N/A')}
**Dauer:** {data.get('lengthSeconds', 'N/A')} Sekunden
"""

def format_youtube_output(data):
    """Format YouTube API response for display"""
    snippet = data.get('snippet', {})
    stats = data.get('statistics', {})
    return f"""
**Titel:** {snippet.get('title', 'N/A')}
**Kanal:** {snippet.get('channelTitle', 'N/A')}
**Beschreibung:** {snippet.get('description', 'N/A')[:200]}...
**Views:** {stats.get('viewCount', 'N/A')}
**Likes:** {stats.get('likeCount', 'N/A')}
**Veröffentlicht:** {snippet.get('publishedAt', 'N/A')}
"""

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 youtube_analyzer.py <youtube_url>")
        sys.exit(1)
    
    youtube_url = sys.argv[1]
    video_id = extract_video_id(youtube_url)
    
    if not video_id:
        print(f"Error: Could not extract video ID from {youtube_url}")
        sys.exit(1)
    
    print(f"Analyzing video ID: {video_id}")
    print("=" * 50)
    
    # Try Invidious first (no API key needed)
    print("\nTrying Invidious...")
    invidious_data = try_invidious(video_id)
    if invidious_data:
        print("✓ Invidious success!")
        print(format_invidious_output(invidious_data))
        return
    else:
        print("✗ Invidious failed (all instances unreachable)")
    
    # Try YouTube API if key available
    api_key = os.environ.get('YOUTUBE_API_KEY')
    if not api_key:
        config_path = os.path.expanduser('~/.openclaw/workspace/config/youtube.env')
        if os.path.exists(config_path):
            with open(config_path) as f:
                for line in f:
                    if line.startswith('YOUTUBE_API_KEY='):
                        api_key = line.strip().split('=')[1].strip('"\'')
                        break
    
    if api_key:
        print("\nTrying YouTube Data API...")
        yt_data = try_youtube_api(video_id, api_key)
        if yt_data:
            print("✓ YouTube API success!")
            print(format_youtube_output(yt_data))
            return
        else:
            print("✗ YouTube API failed")
    else:
        print("\nNo YouTube API key found.")
        print("Set YOUTUBE_API_KEY in ~/.openclaw/workspace/config/youtube.env")
    
    print("\n✗ All methods failed")
    print("\nTo fix:")
    print("1. Get YouTube API key: https://developers.google.com/youtube/v3/getting-started")
    print("2. Save to: ~/.openclaw/workspace/config/youtube.env")
    print("   Format: YOUTUBE_API_KEY=your_key_here")

if __name__ == "__main__":
    main()
