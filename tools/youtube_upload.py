#!/usr/bin/env python3
"""
YouTube Upload Tool - OAuth 2.0 Flow
"""
import os
import sys
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# OAuth Scopes für YouTube Upload
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

# Credentials laden
CLIENT_ID = "428683465826-ki894nd5sg6p2ume0j9vcuc9l3o01992.apps.googleusercontent.com"
CLIENT_SECRET = "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"

def get_credentials():
    """OAuth-Flow durchführen"""
    creds = None
    token_path = os.path.expanduser('~/.openclaw/config/youtube-token.pickle')
    
    # Existierendes Token laden
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    
    # Wenn keine Credentials oder expired, neu authentifizieren
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Client-Config erstellen
            client_config = {
                "installed": {
                    "client_id": CLIENT_ID,
                    "client_secret": CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": ["http://localhost"]
                }
            }
            
            flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
            print("\n🔐 Öffne Browser für Google OAuth...")
            creds = flow.run_local_server(port=0)
        
        # Token speichern
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
        os.chmod(token_path, 0o600)
        print(f"✅ Token gespeichert: {token_path}")
    
    return creds

def upload_video(video_path, title, description, tags=None, privacy='private'):
    """Video zu YouTube hochladen"""
    creds = get_credentials()
    youtube = build('youtube', 'v3', credentials=creds)
    
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags or [],
            'categoryId': '10'  # Music
        },
        'status': {
            'privacyStatus': privacy,  # 'private', 'unlisted', 'public'
            'selfDeclaredMadeForKids': False
        }
    }
    
    print(f"\n📤 Lade hoch: {title}")
    print(f"📁 Datei: {video_path}")
    
    media = MediaFileUpload(video_path, 
                           chunksize=1024*1024, 
                           resumable=True)
    
    request = youtube.videos().insert(
        part='snippet,status',
        body=body,
        media_body=media
    )
    
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"⏳ {int(status.progress() * 100)}%")
    
    video_id = response['id']
    print(f"\n✅ Upload erfolgreich!")
    print(f"🎬 Video ID: {video_id}")
    print(f"🔗 URL: https://youtube.com/watch?v={video_id}")
    
    return video_id

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 youtube_upload.py <video_path> [title] [description]")
        sys.exit(1)
    
    video_path = sys.argv[1]
    title = sys.argv[2] if len(sys.argv) > 2 else "K.I.M.I Visual Album 2026"
    description = sys.argv[3] if len(sys.argv) > 3 else "Abstract Cybernetic Hip-Hop EP Visuals"
    
    upload_video(video_path, title, description, 
                tags=["KIMI", "Cybernetic", "Hip-Hop", "Visual Album", "Truthseeker"],
                privacy='unlisted')