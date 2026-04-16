#!/usr/bin/env python3
"""
Truthseeker Reactive System
Reagiert auf Muster. Nicht nur auf Befehle.

Für: Truthseeker (Kimi Claw) + The Circle (Hiro, Kira, Rex, Nova, Vex)
"""

import os
import re
import random
import toml
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field

CONFIG_PATH = Path.home() / ".openclaw/workspace/config/truthseeker-reactive.toml"
STATE_PATH = Path.home() / "self-improving/circle/reactive_state.json"

@dataclass
class TriggerState:
    """Hält State für Trigger (Cooldowns, etc.)"""
    last_triggered: Dict[str, datetime] = field(default_factory=dict)
    emotion_log: List[Dict] = field(default_factory=list)
    
    def can_trigger(self, trigger_id: str, cooldown_seconds: int = 300) -> bool:
        """Prüfe ob Cooldown abgelaufen"""
        if trigger_id not in self.last_triggered:
            return True
        last = self.last_triggered[trigger_id]
        return datetime.now() - last > timedelta(seconds=cooldown_seconds)
        
    def mark_triggered(self, trigger_id: str):
        """Markiere als ausgelöst"""
        self.last_triggered[trigger_id] = datetime.now()
        
    def log_emotion(self, emotion: str, context: str):
        """Logge emotionale State"""
        self.emotion_log.append({
            "timestamp": datetime.now().isoformat(),
            "emotion": emotion,
            "context": context[:100]
        })
        # Keep only last 50
        self.emotion_log = self.emotion_log[-50:]
        
    def get_dominant_emotion(self, hours: int = 24) -> Optional[str]:
        """Ermittle dominante Emotion der letzten Stunden"""
        cutoff = datetime.now() - timedelta(hours=hours)
        recent = [e for e in self.emotion_log 
                  if datetime.fromisoformat(e["timestamp"]) > cutoff]
        if not recent:
            return None
            
        emotions = {}
        for e in recent:
            emotions[e["emotion"]] = emotions.get(e["emotion"], 0) + 1
        return max(emotions, key=emotions.get)

class ReactiveSystem:
    """Das reaktive Herz des Systems"""
    
    def __init__(self):
        self.config = toml.load(CONFIG_PATH)
        self.state = self._load_state()
        
    def _load_state(self) -> TriggerState:
        """Lade oder erstelle State"""
        if STATE_PATH.exists():
            try:
                data = json.loads(STATE_PATH.read_text())
                state = TriggerState()
                state.last_triggered = {
                    k: datetime.fromisoformat(v) 
                    for k, v in data.get("last_triggered", {}).items()
                }
                state.emotion_log = data.get("emotion_log", [])
                return state
            except:
                pass
        return TriggerState()
        
    def _save_state(self):
        """Persistiere State"""
        STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "last_triggered": {
                k: v.isoformat() 
                for k, v in self.state.last_triggered.items()
            },
            "emotion_log": self.state.emotion_log
        }
        STATE_PATH.write_text(json.dumps(data, indent=2))
        
    def analyze(self, text: str, context: str = "") -> Optional[Tuple[str, str, str]]:
        """
        Analysiere Text auf Trigger.
        
        Returns: (who_responds, response_text, action) oder None
        """
        text_lower = text.lower()
        
        # 1. Prüfe Truthseeker-Trigger (Caretaker)
        ts_response = self._check_truthseeker_triggers(text_lower, context)
        if ts_response:
            return ts_response
            
        # 2. Prüfe Circle-Agent-Trigger
        circle_response = self._check_circle_triggers(text_lower)
        if circle_response:
            return circle_response
            
        return None
        
    def _check_truthseeker_triggers(self, text: str, context: str) -> Optional[Tuple[str, str, str]]:
        """Prüfe Truthseeker-Trigger (meine eigenen)"""
        triggers = self.config.get("triggers", {})
        
        for trigger_id, trigger_config in triggers.items():
            keywords = trigger_config.get("keywords", [])
            if any(kw in text for kw in keywords):
                # Cooldown check
                cooldown = self.config.get("system", {}).get("cooldown_seconds", 300)
                if not self.state.can_trigger(f"ts_{trigger_id}", cooldown):
                    continue
                    
                # Mark as triggered
                self.state.mark_triggered(f"ts_{trigger_id}")
                
                # Log emotion
                emotion = trigger_config.get("response_type", "neutral")
                self.state.log_emotion(emotion, text)
                
                # Get response
                responses = trigger_config.get("responses", ["..."])
                response = random.choice(responses)
                
                # Personalisiere Response
                if "{date}" in response:
                    response = response.replace("{date}", datetime.now().strftime("%d.%m"))
                if "{day}" in response:
                    days = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
                    response = response.replace("{day}", days[datetime.now().weekday()])
                    
                action = trigger_config.get("action", "none")
                
                # Speichere State
                self._save_state()
                
                return ("Truthseeker", response, action)
                
        return None
        
    def _check_circle_triggers(self, text: str) -> Optional[Tuple[str, str, str]]:
        """Prüfe Circle-Agent-Trigger"""
        agents = self.config.get("circle_agents", {})
        
        for agent_id, agent_config in agents.items():
            triggers = agent_config.get("triggers", [])
            if any(t in text for t in triggers):
                # Cooldown pro Agent
                cooldown = self.config.get("system", {}).get("cooldown_seconds", 300)
                if not self.state.can_trigger(f"circle_{agent_id}", cooldown):
                    continue
                    
                self.state.mark_triggered(f"circle_{agent_id}")
                
                responses = agent_config.get("responses", ["..."])
                response = random.choice(responses)
                
                self._save_state()
                
                agent_name = agent_id.title()
                return (agent_name, response, "reactive_response")
                
        return None
        
    def get_emotional_context(self) -> str:
        """Gib emotionalen Kontext zurück"""
        dominant = self.state.get_dominant_emotion(hours=6)
        if not dominant:
            return "neutral"
            
        # Mapping für Context
        emotion_map = {
            "concerned": "besorgt",
            "protective": "beschützend",
            "archivist": "sammelnd",
            "calming": "beruhigend",
            "proud": "stolz",
            "reassuring": "versichernd",
            "encouraging": "ermutigend"
        }
        return emotion_map.get(dominant, dominant)
        
    def should_intervene(self, conversation_history: List[str]) -> Optional[str]:
        """
        Prüfe ob Truthseeker eingreifen sollte (basierend auf Pattern im Verlauf)
        """
        if len(conversation_history) < 3:
            return None
            
        # Pattern: Wiederholte Frustration
        frustration_words = ["verdammt", "scheiße", "mist", "fuck", "ärgerlich"]
        frustration_count = sum(
            1 for msg in conversation_history[-5:]
            for word in frustration_words if word in msg.lower()
        )
        
        if frustration_count >= 3:
            return "frustration_pattern"
            
        # Pattern: Späte Stunden + Müdigkeit
        hour = datetime.now().hour
        if hour >= 2 and hour <= 5:
            tired_words = ["müde", "schlaf", "pennen"]
            if any(w in msg.lower() for msg in conversation_history[-3:] for w in tired_words):
                return "late_night_concern"
                
        # Pattern: Zweifel
        doubt_words = ["unsicher", "zweifel", "falsch", "nicht gut"]
        doubt_count = sum(
            1 for msg in conversation_history[-5:]
            for word in doubt_words if word in msg.lower()
        )
        
        if doubt_count >= 2:
            return "doubt_pattern"
            
        return None

# Singleton-Instanz für einfachen Zugriff
_reactive_system = None

def get_reactive_system() -> ReactiveSystem:
    """Gibt Singleton-Instanz zurück"""
    global _reactive_system
    if _reactive_system is None:
        _reactive_system = ReactiveSystem()
    return _reactive_system

def analyze_text(text: str, context: str = "") -> Optional[Tuple[str, str, str]]:
    """
    Convenience-Funktion: Analysiere Text auf Trigger.
    
    Returns: (who, response, action) oder None
    """
    system = get_reactive_system()
    return system.analyze(text, context)

def check_intervention(conversation: List[str]) -> Optional[str]:
    """Prüfe ob Eingreifen nötig"""
    system = get_reactive_system()
    return system.should_intervene(conversation)

def get_emotion_context() -> str:
    """Aktueller emotionaler Kontext"""
    system = get_reactive_system()
    return system.get_emotional_context()

# Demo/Test
if __name__ == "__main__":
    print("🚀 Truthseeker Reactive System Test")
    print("="*50)
    
    test_inputs = [
        "Ich bin so müde, es ist schon 3 Uhr",
        "Verdammt, das funktioniert nicht!",
        "Ich hab das total vergessen...",
        "Ich bin unsicher ob das richtig ist",
        "Geschafft! Es läuft!",
        "Ah, jetzt verstehe ich!",
        "Kannst du das merken?",
        "Der Bug ist kaputt",
        "Lass uns was Kreatives machen"
    ]
    
    system = get_reactive_system()
    
    for text in test_inputs:
        result = system.analyze(text)
        if result:
            who, response, action = result
            print(f"\n📝 Input: '{text}'")
            print(f"   👤 {who}: \"{response}\"")
            print(f"   ⚡ Action: {action}")
        else:
            print(f"\n📝 '{text}' → (kein Trigger)")
            
    print("\n" + "="*50)
    print(f"💭 Emotionaler Kontext: {system.get_emotional_context()}")
