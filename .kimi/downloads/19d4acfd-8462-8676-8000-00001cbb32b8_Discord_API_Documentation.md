# Discord Developer API - Strukturierte Dokumentation

> Zusammenfassung der Discord API-Dokumentation (Interactions, Gateway, Resources, Voice)

---

## Inhaltsverzeichnis

1. [Interactions](#1-interactions)
2. [Gateway](#2-gateway)
3. [Ressourcen](#3-ressourcen)
4. [Voice Connections](#4-voice-connections)
5. [Discord Social SDK](#5-discord-social-sdk)
6. [Community Ressourcen](#6-community-ressourcen)

---

## 1. Interactions

### 1.1 Übersicht

Interactions sind die Grundlage für interaktive Discord-Features. Es gibt zwei Empfangsmethoden:

| Methode | Beschreibung |
|---------|-------------|
| **Gateway** | WebSocket-Verbindung für Echtzeit-Events |
| **HTTP Webhook** | POST-Requests an konfigurierte Endpoint-URL |

> **Wichtig:** Diese Methoden sind **mutually exclusive** - nur eine kann verwendet werden.

### 1.2 Interaction-Typen

| Typ | Value | Beschreibung |
|-----|-------|-------------|
| `PING` | 1 | Verbindungstest |
| `APPLICATION_COMMAND` | 2 | Slash-/User-/Message-Commands |
| `MESSAGE_COMPONENT` | 3 | Button-Click, Select Menu |
| `APPLICATION_COMMAND_AUTOCOMPLETE` | 4 | Autocomplete-Vorschläge |
| `MODAL_SUBMIT` | 5 | Modal-Formular-Submit |

### 1.3 Interaction Context Types

| Typ | Value | Beschreibung |
|-----|-------|-------------|
| `GUILD` | 0 | Server-Kontext |
| `BOT_DM` | 1 | DM mit Bot-User |
| `PRIVATE_CHANNEL` | 2 | Gruppen-DM oder DM mit anderen Usern |

### 1.4 Application Command Typen

- **Slash Commands** (`CHAT_INPUT`) - `/` im Chat
- **User Commands** - Rechtsklick auf User → Apps
- **Message Commands** - Rechtsklick auf Nachricht → Apps
- **Entry Point Commands** - Activity Launcher

### 1.5 Interaction Objekt Struktur

```json
{
  "id": "snowflake",
  "application_id": "snowflake",
  "type": 2,
  "data": {},
  "guild_id": "snowflake?",
  "channel_id": "snowflake?",
  "member": {},
  "user": {},
  "token": "string",
  "version": 1,
  "message": {},
  "app_permissions": "string",
  "locale": "string",
  "guild_locale": "string",
  "entitlements": [],
  "authorizing_integration_owners": {},
  "context": 0,
  "attachment_size_limit": 0
}
```

### 1.6 Callback Types (Antworten)

| Name | Value | Beschreibung |
|------|-------|-------------|
| `PONG` | 1 | Ping-Acknowledgement |
| `CHANNEL_MESSAGE_WITH_SOURCE` | 4 | Nachricht als Antwort |
| `DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE` | 5 | "Denke nach..." Loading-State |
| `DEFERRED_UPDATE_MESSAGE` | 6 | Später bearbeiten (nur Components) |
| `UPDATE_MESSAGE` | 7 | Original-Message bearbeiten |
| `APPLICATION_COMMAND_AUTOCOMPLETE_RESULT` | 8 | Autocomplete-Vorschläge |
| `MODAL` | 9 | Modal öffnen |
| `LAUNCH_ACTIVITY` | 12 | Activity starten |

### 1.7 Message Components

**Verfügbare Components:**
- Buttons (verschiedene Styles)
- String Select Menus
- User/Role/Mentionable/Channel Select
- Text Input (nur in Modals)
- Text Display, Label, File Upload
- Radio/Checkbox Groups

### 1.8 Security (HTTP Interactions)

**Erforderliche Header-Validierung:**
- `X-Signature-Ed25519` - Ed25519 Signatur
- `X-Signature-Timestamp` - Timestamp

**Python-Beispiel:**
```python
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))
signature = request.headers["X-Signature-Ed25519"]
timestamp = request.headers["X-Signature-Timestamp"]
body = request.data.decode("utf-8")

try:
    verify_key.verify(f'{timestamp}{body}'.encode(), bytes.fromhex(signature))
except BadSignatureError:
    abort(401, 'invalid request signature')
```

---

## 2. Gateway

### 2.1 Übersicht

Der Gateway ist eine persistente WebSocket-Verbindung für:
- Echtzeit-Events (Messages, Voice State, etc.)
- State-Management
- Voice-Verbindungen

### 2.2 Verbindungs-Lebenszyklus

```
1. Get Gateway URL → 2. Connect → 3. Hello (heartbeat_interval)
→ 4. Heartbeat starten → 5. Identify → 6. Ready → 7. Events empfangen
```

### 2.3 Gateway Opcodes

| Opcode | Name | Beschreibung |
|--------|------|-------------|
| 0 | `DISPATCH` | Event empfangen |
| 1 | `HEARTBEAT` | Heartbeat senden |
| 2 | `IDENTIFY` | Authentifizierung |
| 6 | `RESUME` | Verbindung wiederherstellen |
| 7 | `RECONNECT` | Neu verbinden |
| 9 | `INVALID_SESSION` | Session ungültig |
| 10 | `HELLO` | Initialer Handshake |
| 11 | `HEARTBEAT_ACK` | Heartbeat bestätigt |

### 2.4 Gateway Intents

Intents sind Bitwise-Values zur Steuerung empfangener Events.

**Standard Intents:**
| Intent | Value | Events |
|--------|-------|--------|
| `GUILDS` | `1 << 0` | Guild/Channel/Thread Events |
| `GUILD_MEMBERS` | `1 << 1` | Member Add/Update/Remove |
| `GUILD_MODERATION` | `1 << 2` | Ban/Audit Log |
| `GUILD_EXPRESSIONS` | `1 << 3` | Emojis/Stickers/Soundboard |
| `GUILD_INTEGRATIONS` | `1 << 4` | Integration Events |
| `GUILD_WEBHOOKS` | `1 << 5` | Webhook Updates |
| `GUILD_INVITES` | `1 << 6` | Invite Create/Delete |
| `GUILD_VOICE_STATES` | `1 << 7` | Voice State Updates |
| `GUILD_PRESENCES` | `1 << 8` | Presence Updates |
| `GUILD_MESSAGES` | `1 << 9` | Message Events |
| `GUILD_MESSAGE_REACTIONS` | `1 << 10` | Reactions |
| `GUILD_MESSAGE_TYPING` | `1 << 11` | Typing Indicator |
| `DIRECT_MESSAGES` | `1 << 12` | DM Events |
| `DIRECT_MESSAGE_REACTIONS` | `1 << 13` | DM Reactions |
| `DIRECT_MESSAGE_TYPING` | `1 << 14` | DM Typing |
| `MESSAGE_CONTENT` | `1 << 15` | Message Content (privileged) |
| `GUILD_SCHEDULED_EVENTS` | `1 << 16` | Scheduled Events |

**Privileged Intents** (benötigen Approval für verified Apps):
- `GUILD_PRESENCES`
- `GUILD_MEMBERS`
- `MESSAGE_CONTENT`

### 2.5 Sharding

- **Limit pro Shard:** 2500 Guilds
- **Formel:** `shard_id = (guild_id >> 22) % num_shards`
- **Max Concurrency:** Rate-Limit für gleichzeitige Identifies

### 2.6 Wichtige Gateway Events

**Send Events:**
- `IDENTIFY` - Initialer Handshake
- `RESUME` - Wiederherstellen nach Disconnect
- `HEARTBEAT` - Verbindung aufrechterhalten
- `REQUEST_GUILD_MEMBERS` - Member-Liste anfordern
- `UPDATE_VOICE_STATE` - Voice Channel beitreten/verlassen
- `UPDATE_PRESENCE` - Status ändern

**Receive Events:**
- `READY` - Verbindung erfolgreich
- `MESSAGE_CREATE` - Neue Nachricht
- `MESSAGE_UPDATE` - Nachricht bearbeitet
- `MESSAGE_DELETE` - Nachricht gelöscht
- `GUILD_MEMBER_ADD/REMOVE/UPDATE` - Member-Events
- `INTERACTION_CREATE` - Interaction empfangen
- `VOICE_STATE_UPDATE` - Voice-Status geändert
- `VOICE_SERVER_UPDATE` - Voice-Server-Info

---

## 3. Ressourcen

### 3.1 Channel

**Channel-Typen:**
| Typ | ID | Beschreibung |
|-----|-----|-------------|
| `GUILD_TEXT` | 0 | Textkanal |
| `DM` | 1 | Direktnachricht |
| `GUILD_VOICE` | 2 | Sprachkanal |
| `GROUP_DM` | 3 | Gruppen-DM |
| `GUILD_CATEGORY` | 4 | Kategorie |
| `GUILD_ANNOUNCEMENT` | 5 | Ankündigungskanal |
| `ANNOUNCEMENT_THREAD` | 10 | Thread in Ankündigung |
| `PUBLIC_THREAD` | 11 | Öffentlicher Thread |
| `PRIVATE_THREAD` | 12 | Privater Thread |
| `GUILD_STAGE_VOICE` | 13 | Stage-Channel |
| `GUILD_FORUM` | 15 | Forum-Channel |
| `GUILD_MEDIA` | 16 | Media-Channel |

**Channel-Flags:**
| Flag | Value | Beschreibung |
|------|-------|-------------|
| `PINNED` | `1 << 1` | Thread gepinnt |
| `REQUIRE_TAG` | `1 << 4` | Tag erforderlich |
| `HIDE_MEDIA_DOWNLOAD_OPTIONS` | `1 << 15` | Download-Optionen ausblenden |

### 3.2 Message

**Message-Typen:**
- `DEFAULT` (0), `RECIPIENT_ADD` (1), `RECIPIENT_REMOVE` (2)
- `CALL` (3), `CHANNEL_NAME_CHANGE` (4), `CHANNEL_ICON_CHANGE` (5)
- `CHANNEL_PINNED_MESSAGE` (6), `USER_JOIN` (7)
- `GUILD_BOOST` (8-11), `CHANNEL_FOLLOW_ADD` (12)
- `REPLY` (19), `CHAT_INPUT_COMMAND` (20), `THREAD_STARTER_MESSAGE` (21)
- `CONTEXT_MENU_COMMAND` (23), `AUTO_MODERATION_ACTION` (24)

**Message-Flags:**
| Flag | Value | Beschreibung |
|------|-------|-------------|
| `CROSSPOSTED` | `1 << 0` | Veröffentlicht |
| `IS_CROSSPOST` | `1 << 1` | Crosspost |
| `SUPPRESS_EMBEDS` | `1 << 2` | Embeds unterdrücken |
| `SOURCE_MESSAGE_DELETED` | `1 << 3` | Quelle gelöscht |
| `URGENT` | `1 << 4` | Dringend |
| `HAS_THREAD` | `1 << 5` | Hat Thread |
| `EPHEMERAL` | `1 << 6` | Nur für User sichtbar |
| `LOADING` | `1 << 7` | Loading-State |
| `SUPPRESS_NOTIFICATIONS` | `1 << 12` | Keine Benachrichtigungen |
| `IS_VOICE_MESSAGE` | `1 << 13` | Sprachnachricht |
| `IS_COMPONENTS_V2` | `1 << 15` | Components V2 |

**Wichtig:** Message Content (`content`, `embeds`, `attachments`, `components`) erfordert `MESSAGE_CONTENT` Intent.

### 3.3 User

**User-Flags:**
| Flag | Value | Beschreibung |
|------|-------|-------------|
| `STAFF` | `1 << 0` | Discord Mitarbeiter |
| `PARTNER` | `1 << 1` | Partner |
| `HYPESQUAD` | `1 << 2` | HypeSquad Events |
| `BUG_HUNTER_LEVEL_1` | `1 << 3` | Bug Hunter |
| `HYPESQUAD_HOUSE_*` | `1 << 6-8` | HypeSquad Houses |
| `PREMIUM_EARLY_SUPPORTER` | `1 << 9` | Früher Nitro-Supporter |
| `VERIFIED_BOT` | `1 << 16` | Verifizierter Bot |
| `VERIFIED_DEVELOPER` | `1 << 17` | Verifizierter Developer |

**Premium-Types:**
- `NONE` (0), `NITRO_CLASSIC` (1), `NITRO` (2), `NITRO_BASIC` (3)

### 3.4 Webhook

**Webhook-Typen:**
| Typ | Value | Beschreibung |
|-----|-------|-------------|
| `Incoming` | 1 | Eingehende Webhooks |
| `Channel Follower` | 2 | Channel Following |
| `Application` | 3 | Interactions Webhooks |

**Wichtige Endpunkte:**
- `POST /webhooks/{id}/{token}` - Webhook ausführen
- `PATCH /webhooks/{id}/{token}/messages/{message.id}` - Nachricht bearbeiten
- `DELETE /webhooks/{id}/{token}/messages/{message.id}` - Nachricht löschen

### 3.5 Voice State

```json
{
  "guild_id": "snowflake?",
  "channel_id": "?snowflake",
  "user_id": "snowflake",
  "session_id": "string",
  "deaf": false,
  "mute": false,
  "self_deaf": false,
  "self_mute": true,
  "self_stream?": false,
  "self_video": false,
  "suppress": false,
  "request_to_speak_timestamp": "ISO8601?"
}
```

---

## 4. Voice Connections

### 4.1 Übersicht

Voice-Verbindungen bestehen aus:
1. **Gateway Voice State Update** - Channel beitreten
2. **Voice WebSocket** - Steuerung
3. **UDP-Verbindung** - Audio-Daten

### 4.2 Verbindungs-Ablauf

```
1. Gateway: Voice State Update (Opcode 4)
2. Warte auf: Voice State Update + Voice Server Update Events
3. Verbinde zu Voice WebSocket (wss://endpoint)
4. Sende: Identify (Opcode 0)
5. Empfange: Ready (Opcode 2) - SSRC, IP, Port, Modes
6. IP Discovery über UDP
7. Sende: Select Protocol (Opcode 1)
8. Empfange: Session Description (Opcode 4) - Secret Key
9. Audio-Daten senden/empfangen
```

### 4.3 Voice Gateway Opcodes

| Opcode | Name | Beschreibung |
|--------|------|-------------|
| 0 | `IDENTIFY` | Authentifizierung |
| 1 | `SELECT_PROTOCOL` | Protokoll wählen |
| 2 | `READY` | Verbindung bereit |
| 3 | `HEARTBEAT` | Heartbeat senden |
| 4 | `SESSION_DESCRIPTION` | Session-Details |
| 5 | `SPEAKING` | Sprachstatus |
| 6 | `HEARTBEAT_ACK` | Heartbeat bestätigt |
| 7 | `RESUME` | Verbindung wiederherstellen |
| 8 | `HELLO` | Heartbeat-Interval |
| 9 | `RESUMED` | Wiederhergestellt |

### 4.4 Encryption Modes

| Mode | Status |
|------|--------|
| `aead_aes256_gcm_rtpsize` | Verfügbar (Bevorzugt) |
| `aead_xchacha20_poly1305_rtpsize` | Verfügbar (Erforderlich) |
| `xsalsa20_poly1305_lite_rtpsize` | Deprecated |
| `xsalsa20_poly1305` | Deprecated |

### 4.5 DAVE Protocol (E2EE)

> **Wichtig:** Ab März 1, 2026 wird nur noch E2EE unterstützt!

**Features:**
- End-to-End Encryption für Audio/Video
- MLS (Messaging Layer Security) Group
- Per-sender ratcheted media keys
- AES128-GCM Frame-Verschlüsselung

**Voice Gateway Versions:**
- Version 8 (empfohlen): Buffered Resume, Message Sequencing
- Version 4+: Speaking Status als Bitmask

---

## 5. Discord Social SDK

### 5.1 Voice Chat in Lobbies

**Grundlegende Schritte:**
1. Lobby erstellen/beitreten (`CreateOrJoinLobby`)
2. Voice Call starten (`StartCall`)
3. Teilnehmer verwalten

**C++ Beispiel:**
```cpp
client->CreateOrJoinLobby(lobbySecret, [client](const discordpp::ClientResult& result, uint64_t lobbyId) {
    if (result.Successful()) {
        const auto call = client->StartCall(lobbyId);
        if (call) {
            std::cout << "Voice call started!" << std::endl;
        }
    }
});
```

### 5.2 Voice Controls

**Global (Client):**
- `SetSelfMuteAll(bool)` - Mikrofon stummschalten
- `SetSelfDeafAll(bool)` - Alles stummschalten
- `SetInputVolume(float)` - Mikrofon-Lautstärke
- `SetOutputVolume(float)` - Ausgabe-Lautstärke

**Per-Call (Call):**
- `SetSelfMute(bool)` - Stumm für diesen Call
- `SetSelfDeaf(bool)` - Deaf für diesen Call
- `SetParticipantVolume(userId, volume)` - Teilnehmer-Lautstärke
- `SetVADThreshold(bool, float)` - Voice Activation Threshold

### 5.3 Audio Callbacks

**Custom Audio Processing:**
```cpp
const auto call = client->StartCallWithAudioCallbacks(
    lobbyId,
    // Input callback (received audio)
    [](uint64_t userId, int16_t *data, size_t samplesPerChannel,
       int sampleRate, size_t channels, bool &outShouldMuteData) {
        // Audio verarbeiten
        outShouldMuteData = true; // Discord nicht direkt abspielen
    },
    // Output callback (send audio)
    [](int16_t *data, uint64_t samplesPerChannel, int32_t sampleRate,
       uint64_t channels) {}
);
```

### 5.4 Voice Status

```cpp
const auto callInfo = lobby->GetCallInfoHandle();
if (callInfo) {
    const auto participants = callInfo->GetParticipants();
    for (const auto &participantId : participants) {
        const auto voiceState = callInfo->GetVoiceStateHandle(participantId);
        bool isMuted = voiceState->SelfMute();
        bool isDeafened = voiceState->SelfDeaf();
    }
}
```

---

## 6. Community Ressourcen

### 6.1 Beliebte Libraries

| Name | Sprache |
|------|---------|
| discord.js | JavaScript |
| discord.py | Python |
| JDA | Java |
| Discord.Net | C# |
| DSharpPlus | C# |
| discordgo | Go |
| Serenity | Rust |
| Discord4J | Java |

### 6.2 Interactions Libraries

- **JavaScript:** discord-interactions-js, slash-create
- **Python:** discord-interactions-python, flask-discord-interactions
- **Go:** tempest
- **C#:** Discord.Net.Rest

### 6.3 Tools

- **Permission Calculator:** tools.botforge.org/permissions
- **Intent Calculator:** ziad87.net/intents/
- **OpenAPI Spec:** github.com/discord/discord-api-spec

### 6.4 API Types

- **JavaScript:** discord-api-types
- **Go:** dasgo

---

## Anhänge

### A. Rate Limits

- **Gateway:** 120 Events pro 60 Sekunden pro Connection
- **Identify:** 1000 pro 24 Stunden (global)
- **Request Guild Members:** Neue Rate Limits beachten

### B. API-Versionen

- **Aktuell empfohlen:** API v10
- **Gateway Version:** v8 (empfohlen)
- **Voice Gateway:** v8 (empfohlen)

### C. Wichtige URLs

- **API Base:** `https://discord.com/api/v{version}`
- **Gateway:** `wss://gateway.discord.gg/?v=10&encoding=json`
- **Docs:** https://discord.com/developers/docs
- **Developer Portal:** https://discord.com/developers/applications
