import asyncio
import os
import json
from datetime import datetime

def check_logs():
    log_file = "/root/.openclaw/workspace/truthseeker-voice/truthseeker_live.log"
    target_channel = "1476262394563920006"
    
    try:
        with open(log_file, 'r') as f:
            lines = f.readlines()
            
        # Suche nach Messages
        for line in lines[-50:]:
            if "Message" in line or target_channel in line:
                print(f"[LOG] {line.strip()}")
                
        # Suche nach Errors
        for line in lines[-20:]:
            if "error" in line.lower() or "exception" in line.lower():
                print(f"[ERROR] {line.strip()}")
                
    except Exception as e:
        print(f"Fehler beim Lesen: {e}")

check_logs()
