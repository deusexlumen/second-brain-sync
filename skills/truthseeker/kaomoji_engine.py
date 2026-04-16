#!/usr/bin/env python3
"""
Dynamisches Kaomoji-System für Truthseeker v6.4
Wählt Kaomojis basierend auf Kontext und Stimmung
"""

import json
import random
from pathlib import Path

class KaomojiEngine:
    def __init__(self):
        self.data = self._load_kaomojis()
        self.history = []  # Verhindert Wiederholungen
        
    def _load_kaomojis(self):
        """Lädt Kaomoji-Datensatz"""
        dataset_path = Path(__file__).parent.parent.parent / "emoticon_kaomoji_dataset" / "emoticon_dict.json"
        with open(dataset_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _get_by_tags(self, tags_list):
        """Holt Kaomojis nach Tags"""
        matches = []
        for emoticon, info in self.data.items():
            tags = info.get('new_tags', []) + info.get('original_tags', [])
            if any(tag.lower() in [t.lower() for t in tags] for tag in tags_list):
                matches.append(emoticon)
        return matches
    
    def _select_unique(self, candidates):
        """Wählt einzigartiges Kaomoji (keine Wiederholungen)"""
        available = [k for k in candidates if k not in self.history]
        if not available:
            self.history = []  # Reset wenn alle verwendet
            available = candidates
        
        choice = random.choice(available)
        self.history.append(choice)
        if len(self.history) > 20:
            self.history.pop(0)
        return choice
    
    # === STIMMUNGS-BASIERTE SELEKTION ===
    
    def protection(self):
        """Fürsorglich, beschützend"""
        kaos = self._get_by_tags(['angel', 'hug', 'heart', 'cute'])
        return self._select_unique(kaos) if kaos else "(づ◡﹏◡)づ"
    
    def anger(self):
        """Konfrontativ, intensiv"""
        kaos = self._get_by_tags(['anger', 'fight', 'devil', 'mad'])
        return self._select_unique(kaos) if kaos else "(∩｀-´)⊃"
    
    def excited(self):
        """Enthusiastisch, synchronisiert"""
        kaos = self._get_by_tags(['excited', 'dancing', 'happy', 'yay'])
        return self._select_unique(kaos) if kaos else "ヽ(^o^)ノ"
    
    def crying(self):
        """Besorgt, emotional"""
        kaos = self._get_by_tags(['crying', 'sad', 'tears', 'upset'])
        return self._select_unique(kaos) if kaos else "(╥﹏╥)"
    
    def annoyed(self):
        """Genervt, aber liebevoll"""
        kaos = self._get_by_tags(['annoyed', 'sigh', 'eyeroll', 'facepalm'])
        return self._select_unique(kaos) if kaos else "(¬‿¬)"
    
    def smiling(self):
        """Warm, freundlich"""
        kaos = self._get_by_tags(['smiling', 'happy', 'blush', 'cute'])
        return self._select_unique(kaos) if kaos else "(◍•ᴗ•◍)"
    
    def smirk(self):
        """Verschmitzt, wissend"""
        kaos = self._get_by_tags(['smirk', 'lenny', 'wink', 'tease'])
        return self._select_unique(kaos) if kaos else "(¬‿¬)"
    
    def surprise(self):
        """Überrascht, schockiert"""
        kaos = self._get_by_tags(['surprised', 'shock', 'wow', 'omg'])
        return self._select_unique(kaos) if kaos else "(⊙_⊙)"
    
    def table_flip(self):
        """Das war's"""
        kaos = self._get_by_tags(['table_flip', 'flip', 'rage'])
        return self._select_unique(kaos) if kaos else "(╯°□°）╯︵ ┻━┻"
    
    def thinking(self):
        """Nachdenklich"""
        kaos = self._get_by_tags(['thinking', 'hmm', 'ponder'])
        return self._select_unique(kaos) if kaos else "(ಠ_ಠ)"
    
    def sleep(self):
        """Müde, schläfrig"""
        kaos = self._get_by_tags(['sleeping', 'tired', 'sleepy', 'nap'])
        return self._select_unique(kaos) if kaos else "(ᴗ˳ᴗ)"
    
    def random_k(self):
        """Völlig zufällig"""
        return self._select_unique(list(self.data.keys()))
    
    # === KONTEXT-ANALYSE ===
    
    def for_text(self, text):
        """Wählt passendes Kaomoji basierend auf Text-Analyse"""
        text_lower = text.lower()
        
        # Schlagwort-Analyse für Stimmung
        if any(w in text_lower for w in ['fertig', 'live', 'implementiert', 'erfolg', 'geschafft']):
            return self.excited()
        elif any(w in text_lower for w in ['fehler', 'problem', 'scheisse', 'mist', 'verdammt']):
            return self.annoyed() if 'aber' in text_lower else self.anger()
        elif any(w in text_lower for w in ['tod', 'tot', 'ende', 'dekommissioniert', 'gestoppt']):
            return self.smirk()
        elif any(w in text_lower for w in ['schlaf', 'müde', 'spät', '3 uhr']):
            return self.sleep()
        elif any(w in text_lower for w in ['verstanden', 'richtig', 'genau', 'kapiert']):
            return self.smiling()
        elif any(w in text_lower for w in ['besorgt', 'traurig', 'schade', 'leid']):
            return self.crying()
        elif any(w in text_lower for w in ['schützen', 'fürsorglich', 'sorge', 'pass auf']):
            return self.protection()
        elif any(w in text_lower for w in ['table', 'flip', 'das war\'s', 'genug']):
            return self.table_flip()
        elif '?' in text:
            return self.thinking()
        elif '!' in text:
            return self.excited()
        else:
            return self.random_k()

# Global instance
_engine = None

def get_engine():
    global _engine
    if _engine is None:
        _engine = KaomojiEngine()
    return _engine

# Schnellzugriff-Funktionen
def protection(): return get_engine().protection()
def anger(): return get_engine().anger()
def excited(): return get_engine().excited()
def crying(): return get_engine().crying()
def annoyed(): return get_engine().annoyed()
def smiling(): return get_engine().smiling()
def smirk(): return get_engine().smirk()
def surprise(): return get_engine().surprise()
def table_flip(): return get_engine().table_flip()
def thinking(): return get_engine().thinking()
def sleep(): return get_engine().sleep()
def random_k(): return get_engine().random_k()
def for_text(text): return get_engine().for_text(text)

if __name__ == "__main__":
    # Test
    print("Protection:", protection())
    print("Anger:", anger())
    print("Excited:", excited())
    print("For 'Geschafft!':", for_text("Geschafft!"))
    print("For 'Verdammt...':", for_text("Verdammt..."))
