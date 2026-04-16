#!/usr/bin/env python3
"""
Kaomoji CLI Tool - Dynamische Kaomoji-Auswahl
Usage: kaomoji [mood|for_text "text"]
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/skills/truthseeker')

from kaomoji_engine import KaomojiEngine

def main():
    engine = KaomojiEngine()
    
    if len(sys.argv) < 2:
        # Random
        print(engine.random())
        return
    
    command = sys.argv[1].lower()
    
    if command == "for_text" and len(sys.argv) > 2:
        text = " ".join(sys.argv[2:])
        print(engine.for_text(text))
    elif command == "protection":
        print(engine.protection())
    elif command == "anger":
        print(engine.anger())
    elif command == "excited":
        print(engine.excited())
    elif command == "crying":
        print(engine.crying())
    elif command == "annoyed":
        print(engine.annoyed())
    elif command == "smiling":
        print(engine.smiling())
    elif command == "smirk":
        print(engine.smirk())
    elif command == "surprise":
        print(engine.surprise())
    elif command == "table_flip":
        print(engine.table_flip())
    elif command == "thinking":
        print(engine.thinking())
    elif command == "sleep":
        print(engine.sleep())
    elif command == "random":
        print(engine.random_k())
    else:
        # Treat as text analysis
        text = " ".join(sys.argv[1:])
        print(engine.for_text(text))

if __name__ == "__main__":
    main()
