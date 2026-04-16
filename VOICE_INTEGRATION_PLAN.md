# Discord Voice Integration Plan for OpenClaw Gateway

## Executive Summary

OpenClaw Gateway **already has built-in Discord Voice support** with a complete bidirectional audio pipeline. The existing implementation uses a segmented approach (record → transcribe → process → TTS → play). 

This plan documents:
1. The **current architecture** (which already works!)
2. How to **upgrade to Gemini 3.1 Flash Live** for true real-time streaming
3. How to **unify text and voice** into one Kimi Claw entity

---

## 1. Current Architecture Analysis

### 1.1 Existing Discord Voice Stack

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        OpenClaw Discord Voice Stack                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐                 │
│  │  Discord.js  │────▶│@discordjs/voice│───▶│DiscordVoiceManager│           │
│  │   Gateway    │     │   Voice Conn   │     │   (built-in)   │              │
│  └──────────────┘     └──────────────┘     └───────┬──────┘                │
│                                                     │                        │
│  Audio Flow (Current Segmented Pipeline):           ▼                        │
│                                                                              │
│  User speaks ──▶ Opus decode ──▶ PCM (48kHz/16bit/stereo)                   │
│       │                                                                        │
│       ▼                                                                        │
│  Write WAV ──▶ Transcribe ──▶ Agent Process ──▶ TTS ──▶ Play                 │
│  (~0.35s min)   (Whisper/etc)  (Kimi Claw)   (ElevenLabs/   (Discord PCM)    │
│                                                Edge/OpenAI)                  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Key Components Already Present

| Component | Location | Purpose |
|-----------|----------|---------|
| `DiscordVoiceManager` | `openclaw/dist/plugin-sdk/discord/voice/manager.js` | Main voice controller |
| `DiscordVoiceConfig` | `openclaw/dist/plugin-sdk/config/types.discord.d.ts` | Voice configuration |
| `joinVoiceChannel()` | `@discordjs/voice` | Discord voice connection |
| `createAudioPlayer()` | `@discordjs/voice` | Audio playback |
| `transcribeAudio()` | `manager.js:284` | Audio → Text (Whisper) |
| `textToSpeech()` | `manager.js:297` | Text → Audio (TTS) |
| `opusscript` decoder | `manager.js:97` | Opus → PCM decode |

### 1.3 Current Configuration Schema

```yaml
# ~/.openclaw/config/credentials.json
channels:
  discord:
    enabled: true
    token: "your-bot-token"
    voice:
      enabled: true                    # Enable voice (default: true)
      daveEncryption: true             # E2E encryption (default: true)
      decryptionFailureTolerance: 24   # DAVE recovery threshold
      autoJoin:                        # Auto-join on startup
        - guildId: "123456789"
          channelId: "987654321"
      tts:                             # Voice-specific TTS overrides
        provider: "elevenlabs"
        voiceId: "Rachel"
        elevenlabs:
          voiceSettings:
            stability: 0.5
            similarity_boost: 0.75
```

### 1.4 Current Voice Commands (Already Available!)

The existing implementation provides **built-in slash commands** via Discord interactions:

```
/voice join <channel>     - Join a voice channel
/voice leave              - Leave current voice channel  
/voice status             - Show voice connection status
```

**No custom `!join_vc` / `!leave_vc` commands needed** - the Discord plugin registers these automatically.

---

## 2. Gemini 3.1 Flash Live Integration Plan

### 2.1 Target Architecture (Streaming)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Gemini 3.1 Flash Live Integration                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   DISCORD (48kHz/16bit/stereo)          GEMINI (24kHz/16bit/mono)           │
│                                                                              │
│  ┌─────────────────┐                    ┌─────────────────┐                 │
│  │  VoiceReceiver  │──────┐    ┌────────│  GeminiLiveConn │                 │
│  │  (opusscript)   │      │    │        │   (WebSocket)   │                 │
│  └────────┬────────┘      │    │        └────────┬────────┘                 │
│           │               │    │                 │                          │
│           ▼               ▼    ▼                 ▼                          │
│  ┌─────────────────────────────────────────────────────────┐               │
│  │              Audio Processing Pipeline                   │               │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │               │
│  │  │ Resample    │───▶│  WebSocket  │───▶│ Resample    │ │               │
│  │  │ 48k▶24k     │    │   Send/Recv │    │ 24k▶48k     │ │               │
│  │  │ Stereo▶Mono │    │  (real-time)│    │ Mono▶Stereo │ │               │
│  │  └─────────────┘    └─────────────┘    └─────────────┘ │               │
│  └─────────────────────────────────────────────────────────┘               │
│                                                                              │
│  Key Differences from Current:                                               │
│  • No WAV file creation (streaming)                                          │
│  • No Whisper transcription (Gemini handles audio)                           │
│  • No TTS generation (Gemini outputs audio)                                  │
│  • True duplex: Listen & Speak simultaneously                                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Audio Format Conversion Matrix

| Direction | Source | Target | Conversion |
|-----------|--------|--------|------------|
| Input (Discord → Gemini) | 48kHz, Stereo, 16-bit | 24kHz, Mono, 16-bit | Downsample: every 2nd sample; Average channels |
| Output (Gemini → Discord) | 24kHz, Mono, 16-bit | 48kHz, Stereo, 16-bit | Upsample: duplicate samples; Duplicate to both channels |

**Implementation:** Use `numpy` for efficient resampling (as shown in existing `truthseeker-voice/`)

```python
def resample_to_gemini(pcm_48k_stereo: bytes) -> bytes:
    """48kHz Stereo → 24kHz Mono"""
    samples = np.frombuffer(pcm_48k_stereo, dtype=np.int16)
    samples = samples.reshape(-1, 2)
    mono = ((samples[:, 0] + samples[:, 1]) // 2).astype(np.int16)
    return mono[::2].tobytes()  # Downsample

def resample_to_discord(pcm_24k_mono: bytes) -> bytes:
    """24kHz Mono → 48kHz Stereo"""
    samples = np.frombuffer(pcm_24k_mono, dtype=np.int16)
    upsampled = np.repeat(samples, 2)  # Upsample
    stereo = np.column_stack((upsampled, upsampled)).flatten()
    return stereo.astype(np.int16).tobytes()
```

### 2.3 WebSocket Protocol (Gemini 3.1 Live)

```javascript
// Connection URL
wss://generativelanguage.googleapis.com/ws/google.ai.generativelanguage.v1alpha.GenerativeService.BidiGenerateContent?key={GEMINI_API_KEY}

// Setup Message
{
  "setup": {
    "model": "models/gemini-2.0-flash-live-001",
    "generation_config": {
      "response_modalities": ["AUDIO"],
      "speech_config": {
        "voice_config": {
          "prebuilt_voice_config": {
            "voice_name": "Aoede"  // Truthseeker voice
          }
        }
      }
    },
    "system_instruction": {
      "parts": [{
        "text": "Du bist Truthseeker..."
      }]
    }
  }
}

// Send Audio (from Discord)
{
  "realtime_input": {
    "media_chunks": [{
      "mime_type": "audio/pcm;rate=24000;channels=1;format=linear16",
      "data": "<base64-encoded-pcm>"
    }]
  }
}

// Receive Audio (from Gemini)
{
  "serverContent": {
    "modelTurn": {
      "parts": [{
        "inlineData": {
          "mime_type": "audio/pcm;rate=24000;channels=1;format=linear16",
          "data": "<base64-encoded-pcm>"
        }
      }]
    }
  }
}
```

---

## 3. Implementation Strategy

### 3.1 Two Implementation Options

| Approach | Pros | Cons | Effort |
|----------|------|------|--------|
| **A: Extend DiscordVoiceManager** | Native integration, unified config | Requires modifying OpenClaw core | High |
| **B: External Voice Bridge** | Independent, easier to develop | Separate process, config duplication | Medium |

### 3.2 Recommended: Hybrid Approach

Create a **Voice Mode Toggle** in the existing DiscordVoiceManager that switches between:

1. **Standard Mode** (current): Segmented pipeline with Whisper + TTS
2. **Live Mode** (new): Gemini 3.1 Flash Live streaming

```typescript
// Extended DiscordVoiceConfig
interface DiscordVoiceConfig {
  enabled?: boolean;
  mode?: 'standard' | 'live';  // NEW: Toggle between modes
  geminiLive?: {               // NEW: Gemini Live settings
    enabled: boolean;
    apiKey?: string;           // Falls back to GEMINI_API_KEY env
    voiceName?: string;        // Default: 'Aoede'
    systemPrompt?: string;     // Context prompt
  };
  autoJoin?: DiscordVoiceAutoJoinConfig[];
  // ... existing options
}
```

### 3.3 Files to Create/Modify

#### New Files
```
~/.openclaw/extensions/kimi-claw/src/voice/
├── gemini-live-connection.ts     # WebSocket connection manager
├── audio-processor.ts            # Resample utilities
├── live-audio-source.ts          # Discord AudioSource adapter
└── voice-receiver.ts             # Discord → Gemini bridge
```

#### Modified Files
```
~/.openclaw/extensions/dingtalk-connector/node_modules/openclaw/
├── src/discord/voice/manager.ts           # Add Live mode switch
├── src/discord/voice/live-session.ts      # NEW: Live session handler
└── src/config/types.discord.d.ts          # Extend config schema
```

---

## 4. Unified Entity: Kimi Claw Text + Voice

### 4.1 The Problem

Currently, there are **two separate bots**:
1. **OpenClaw Discord Bot** - Text messages via Gateway
2. **Truthseeker Voice Bot** - Voice via separate Python process

### 4.2 The Solution

**Single Bot, Dual Presence** - One Discord bot account handles both:

```
┌────────────────────────────────────────────────────────────┐
│                    Kimi Claw (Unified)                      │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │           OpenClaw Gateway (Node.js)                │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │ Text Handler│  │DiscordPlugin│  │ Voice Manager│ │   │
│  │  │  (existing) │  │  (existing) │  │  (enhanced) │ │   │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘ │   │
│  │         │                │                 │        │   │
│  │         └────────────────┴─────────────────┘        │   │
│  │                          │                          │   │
│  │                    Kimi Claw Core                    │   │
│  │                   (Session Routing)                  │   │
│  └──────────────────────────┼──────────────────────────┘   │
│                             │                               │
│              ┌──────────────┼──────────────┐               │
│              │              │              │                │
│              ▼              ▼              ▼                │
│        ┌─────────┐   ┌──────────┐   ┌───────────┐          │
│        │Discord  │   │  Gemini  │   │  Gemini   │          │
│        │Gateway  │   │  2.5 Pro │   │ 2.0 Flash │          │
│        │(text)   │   │  (text)  │   │ Live (voice)│        │
│        └─────────┘   └──────────┘   └───────────┘          │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

### 4.3 Session Unification

**Key Insight:** Voice interactions should share the same session/context as text:

```typescript
// When user speaks in voice channel:
const voiceMessage = await transcribeAudio(audioBuffer);
// Route to same session as if they typed it
const sessionKey = getVoiceSession(guildId, channelId);
await agentCommandFromIngress({
  message: voiceMessage,
  sessionKey: sessionKey,  // Same session as text!
  messageChannel: "discord",
  // ...
});
```

### 4.4 Configuration for Unified Bot

```yaml
# ~/.openclaw/config/credentials.json
{
  "channels": {
    "discord": {
      "enabled": true,
      "token": "${DISCORD_BOT_TOKEN}",
      
      // Text settings
      "responsePrefix": "(⌐■_■) ",
      "groupPolicy": "allowlist",
      "guilds": {
        "123456789": {
          "channels": ["987654321"]
        }
      },
      
      // Voice settings (same bot!)
      "voice": {
        "enabled": true,
        "mode": "live",  // Use Gemini Live
        "geminiLive": {
          "voiceName": "Aoede",
          "systemPrompt": "Du bist Truthseeker..."
        },
        "autoJoin": [
          {"guildId": "123456789", "channelId": "111222333"}
        ]
      }
    }
  }
}
```

---

## 5. Implementation Roadmap

### Phase 1: Enable Existing Voice (Immediate)

The existing voice support just needs to be **enabled** in config:

```bash
# Add to ~/.openclaw/config/credentials.json
jq '.channels.discord.voice = {
  "enabled": true,
  "autoJoin": []
}' ~/.openclaw/config/credentials.json > /tmp/cfg.json && mv /tmp/cfg.json ~/.openclaw/config/credentials.json

# Install opusscript for audio decoding
npm install -g opusscript  # Or in OpenClaw's node_modules
```

**Result:** Voice works with segmented pipeline (Whisper → Kimi → TTS)

### Phase 2: Gemini Live Bridge (Week 1-2)

Create a **Python bridge** that interfaces with existing DiscordVoiceManager:

```python
# ~/.openclaw/workspace/discord-voice-bridge/gemini_bridge.py
# - Wraps Gemini 3.1 Live WebSocket
# - Provides HTTP API for OpenClaw to call
# - Handles audio resampling
```

**Result:** Voice uses Gemini Live for true real-time conversation

### Phase 3: Native Integration (Week 3-4)

Port the Python bridge to TypeScript within OpenClaw's Discord plugin:

```typescript
// src/discord/voice/gemini-live.ts
export class GeminiLiveVoiceSession {
  private ws: WebSocket;
  private audioBuffer: AudioBuffer;
  // ...
}
```

**Result:** Fully native, no external dependencies

### Phase 4: Unified Commands (Week 5)

Add voice commands that integrate with text session:

```typescript
// Slash commands registered by Discord plugin
/voice join <channel>     - Join voice
/voice leave              - Leave voice
/voice mode <standard|live> - Switch mode
/voice persona <name>     - Change voice
```

**Result:** Unified Kimi Claw experience

---

## 6. Technical Specifications

### 6.1 Audio Parameters

| Parameter | Discord | Gemini Live | Conversion |
|-----------|---------|-------------|------------|
| Sample Rate | 48,000 Hz | 24,000 Hz | 2:1 ratio |
| Channels | 2 (Stereo) | 1 (Mono) | Mix/Split |
| Bit Depth | 16-bit | 16-bit | Pass-through |
| Frame Size | 960 samples (20ms) | 480 samples (20ms) | Match timing |
| Format | Opus (encoded) | PCM (raw) | opusscript |

### 6.2 Latency Budget

| Stage | Latency | Notes |
|-------|---------|-------|
| Discord → PCM | ~20ms | Opus decode |
| Resample | ~5ms | numpy vectorized |
| WebSocket send | ~30ms | Network round-trip |
| Gemini processing | ~200-500ms | Variable (LLM) |
| WebSocket recv | ~30ms | Network |
| Resample | ~5ms | numpy |
| PCM → Discord | ~20ms | Opus encode |
| **Total** | **~300-600ms** | End-to-end |

### 6.3 Required Dependencies

```json
{
  "dependencies": {
    "@discordjs/voice": "^0.16.0",
    "opusscript": "^0.0.8",
    "sodium-native": "^4.0.0",
    "ws": "^8.14.0"
  }
}
```

For Python bridge (Phase 2):
```txt
discord.py[voice]==2.3.2
numpy==1.26.0
websockets==12.0
aiohttp==3.9.0
```

---

## 7. Risk Assessment & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| DAVE decryption failures | High | Built-in recovery (auto-rejoin after 3 failures) |
| Gemini Live latency spikes | Medium | Fallback to segmented mode on timeout |
| Audio drift (clock skew) | Low | 20ms frame buffering, drop/duplicate as needed |
| Memory leaks (streaming) | Medium | Bounded buffers (max 50 chunks), auto-cleanup |
| Discord rate limits | Low | Exponential backoff, queue management |

---

## 8. Testing Plan

### 8.1 Unit Tests
- Audio resampling accuracy (< 1% error)
- WebSocket reconnection logic
- DAVE failure recovery

### 8.2 Integration Tests
- Full pipeline: speak → hear response
- Concurrent voice + text in same session
- Mode switching (standard ↔ live)

### 8.3 Load Tests
- Multiple guilds simultaneously
- 24h+ uptime stability
- Memory usage over time

---

## 9. Migration Guide

### For Existing Users

```bash
# 1. Backup config
cp ~/.openclaw/config/credentials.json ~/.openclaw/backups/credentials-pre-voice.json

# 2. Add voice section
openclaw config set channels.discord.voice.enabled true
openclaw config set channels.discord.voice.mode live

# 3. Verify dependencies
openclaw doctor --check voice

# 4. Test voice
openclaw discord voice join <guild-id> <channel-id>
```

---

## 10. Conclusion

**The foundation is already there.** OpenClaw has a sophisticated Discord Voice implementation that just needs:

1. ✅ **Configuration** - Enable in credentials.json
2. 🔄 **Gemini Live Integration** - Add WebSocket streaming mode
3. 🔄 **Unification** - Share sessions between text and voice

The existing `truthseeker-voice/` implementation in the workspace serves as an excellent **reference implementation** for the Gemini Live protocol and audio processing.

**Next Steps:**
1. Enable existing voice support (5 minutes)
2. Test current segmented pipeline (1 hour)
3. Implement Gemini Live bridge (1-2 weeks)
4. Port to native TypeScript (2-3 weeks)

---

## Appendix A: Existing Voice Files Reference

```
~/.openclaw/workspace/
├── truthseeker-voice/
│   ├── truthseeker_live.py      # Full Live implementation (reference)
│   ├── bot.py                   # TTS-only bot
│   ├── api_server.py            # HTTP API wrapper
│   └── voice_control.py         # Control utilities
├── skills/truthseeker-voice/    # OpenClaw skill wrapper
└── tools/
    ├── discord_tts_upload.py    # TTS upload helper
    └── tts_31live.py            # Gemini TTS standalone
```

## Appendix B: OpenClaw Voice Architecture

```
~/.openclaw/extensions/dingtalk-connector/node_modules/openclaw/
├── src/discord/voice/
│   ├── manager.ts               # Main controller (527 lines)
│   ├── command.ts               # Slash commands
│   └── monitor.ts               # Connection monitoring
├── src/discord/
│   └── channel.ts               # Plugin registration
└── dist/
    └── manager.runtime-CsxzcRLw.js  # Compiled output
```
