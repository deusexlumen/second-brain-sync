# Truthseeker Voice Skill
# Steuert den Discord Voice Bot über API

name: truthseeker-voice
description: |
  Steuert Truthseeker's Voice-Funktionen (Discord Voice Channel, TTS, bidirektionale Konversation).
  Ermöglicht es, dem Voice Channel beizutreten und zu sprechen.

commands:
  - name: voice_join
    description: Voice Channel beitreten und Konversation starten
    usage: "!voice_join [#channel]"
    
  - name: voice_leave
    description: Voice Channel verlassen
    usage: "!voice_leave"
    
  - name: voice_status
    description: Voice Bot Status prüfen
    usage: "!voice_status"
    
  - name: voice_say
    description: TTS-Nachricht senden (wenn im Voice Channel)
    usage: "!voice_say [Text]"

api:
  host: localhost
  port: 8742
  endpoints:
    health: /health
    status: /status
    speak: /speak
    join: /join
    leave: /leave

process:
  name: truthseeker_voice
  script: ~/.openclaw/workspace/truthseeker-voice/truthseeker_live.py
  log: ~/.openclaw/workspace/truthseeker-voice/truthseeker_live.log
  auto_restart: true
