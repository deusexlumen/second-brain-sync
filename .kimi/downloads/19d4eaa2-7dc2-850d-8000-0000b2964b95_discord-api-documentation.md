# Discord API Dokumentation - Zusammenfassung

> Zusammengestellt aus der offiziellen Discord Developer Dokumentation
> Letzte Aktualisierung: 2026-04-02

---

## Inhaltsverzeichnis

1. [Interactions](#1-interactions)
   - [Overview](#11-overview)
   - [Receiving & Responding](#12-receiving--responding)
   - [Plattform](#13-plattform)
2. [Gateway](#2-gateway)
   - [Gateway Verbindungen](#21-gateway-verbindungen)
   - [Gateway Events](#22-gateway-events)
3. [Voice](#3-voice)
   - [Voice Connections](#31-voice-connections)
   - [Voice Ressourcen](#32-voice-ressourcen)
   - [Discord Social SDK](#33-discord-social-sdk)
4. [Webhooks](#4-webhooks)
5. [Ressourcen](#5-ressourcen)
   - [User](#51-user)
   - [Message](#52-message)
   - [Channel](#53-channel)
6. [Community Resources](#6-community-resources)

---

## 1. Interactions

### 1.1 Overview

**Interaction-Typen:**

| Typ | Beschreibung |
|-----|--------------|
| **Slash Commands** | Über `/` im Chat oder Command Picker erreichbar |
| **Message Commands** | Über Kontextmenü (3 Punkte) → Apps bei Nachrichten |
| **User Commands** | Über Rechtsklick auf User-Profil → Apps |
| **Entry Point Commands** | Primärer Weg zum Starten von Activities |
| **Message Components** | Interaktive Elemente in Nachrichten (Buttons, Select Menus) |
| **Modals** | Popup-Formulare zur Dateneingabe |

**Zwei Wege Interactions zu empfangen:**
1. **Gateway** (WebSocket) - Standard
2. **HTTP Webhook** - Konfigurierbar via Interactions Endpoint URL

**Sicherheitsanforderungen für HTTP Webhooks:**
- `PING` Requests bestätigen (type: 1)
- Request-Header validieren:
  - `X-Signature-Ed25519` (Signatur)
  - `X-Signature-Timestamp` (Zeitstempel)
- Ed25519 Signatur-Verifizierung mit Public Key

### 1.2 Receiving & Responding

#### Interaction Object

| Feld | Typ | Beschreibung |
|------|-----|--------------|
| `id` | snowflake | ID der Interaction |
| `application_id` | snowflake | ID der Anwendung |
| `type` | integer | Interaction-Typ |
| `data` | object | Interaction-Daten |
| `guild_id` | ?snowflake | Guild-Quelle |
| `channel_id` | ?snowflake | Channel-Quelle |
| `member` | ?guild member | Guild-Mitglied (bei Guild-Interactions) |
| `user` | ?user | User (bei DM-Interactions) |
| `token` | string | Token für Antworten |
| `version` | integer | Immer `1` |
| `message` | ?message | Bei Components: Ursprüngliche Nachricht |
| `app_permissions` | string | Berechtigungen der App |
| `locale` | string | Sprache des Users |
| `guild_locale` | string | Guild-Sprache |

#### Interaction Types

| Name | Wert |
|------|------|
| PING | 1 |
| APPLICATION_COMMAND | 2 |
| MESSAGE_COMPONENT | 3 |
| APPLICATION_COMMAND_AUTOCOMPLETE | 4 |
| MODAL_SUBMIT | 5 |

#### Interaction Context Types

| Name | Wert | Beschreibung |
|------|------|--------------|
| GUILD | 0 | Innerhalb von Servern |
| BOT_DM | 1 | DMs mit dem Bot-User |
| PRIVATE_CHANNEL | 2 | Gruppen-DMs und andere DMs |

#### Interaction Callback Types

| Name | Wert | Beschreibung |
|------|------|--------------|
| PONG | 1 | ACK für Ping |
| CHANNEL_MESSAGE_WITH_SOURCE | 4 | Antwort mit Nachricht |
| DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE | 5 | ACK mit Ladezustand |
| DEFERRED_UPDATE_MESSAGE | 6 | Für Components: Später bearbeiten |
| UPDATE_MESSAGE | 7 | Für Components: Nachricht bearbeiten |
| APPLICATION_COMMAND_AUTOCOMPLETE_RESULT | 8 | Autocomplete-Vorschläge |
| MODAL | 9 | Modal öffnen |
| LAUNCH_ACTIVITY | 12 | Activity starten |

**Wichtige Zeitlimits:**
- **3 Sekunden**: Erste Antwort muss gesendet werden
- **15 Minuten**: Token bleibt gültig für Follow-up Nachrichten

#### API Endpoints für Interactions

```
POST /interactions/{interaction.id}/{interaction.token}/callback
GET    /webhooks/{application.id}/{interaction.token}
POST   /webhooks/{application.id}/{interaction.token}
PATCH  /webhooks/{application.id}/{interaction.token}/messages/{message.id}
DELETE /webhooks/{application.id}/{interaction.token}/messages/{message.id}
POST   /webhooks/{application.id}/{interaction.token}/messages/{message.id}
```

### 1.3 Plattform

Interactions können über zwei Modelle empfangen werden:

**Gateway Interactions:**
- Standard für bestehende Gateway-Verbindungen
- Keine zusätzliche Konfiguration nötig
- Interactions kommen über denselben WebSocket wie andere Events

**HTTP Interactions:**
- Interactions Endpoint URL in App-Einstellungen konfigurieren
- POST-Requests von Discord erhalten
- Signatur-Validierung erforderlich
- Skaliert natürlich mit Web-Infrastruktur

---

## 2. Gateway

### 2.1 Gateway Verbindungen

**Lebenszyklus einer Gateway-Verbindung:**

1. **WSS URL abrufen**
   - `GET /gateway` oder `GET /gateway/bot`
   - URL cachen für Reconnects

2. **Verbindung herstellen**
   - URL: `wss://gateway.discord.gg/?v=10&encoding=json`
   - Query-Parameter: `v`, `encoding` (json/etf), `compress` (zlib-stream/zstd-stream)

3. **Hello Event empfangen** (opcode 10)
   - `heartbeat_interval` in ms

4. **Heartbeat starten**
   - Erster Heartbeat: `heartbeat_interval * jitter` (0-1)
   - Danach: Alle `heartbeat_interval` ms
   - Sequence-Nummer (`s`) mitsenden

5. **Identify senden** (opcode 2)
   - Authentication
   - Intents definieren
   - Properties setzen

6. **Ready Event empfangen** (opcode 0)
   - `session_id` und `resume_gateway_url` speichern

**Wichtige Limits:**
- 120 Events pro 60 Sekunden pro Verbindung
- 1000 IDENTIFY Aufrufe pro 24 Stunden
- Payload-Limit: 4096 Bytes

**Encoding & Kompression:**
- **JSON**: Plain-text, optional mit Payload-Kompression
- **ETF**: Binary (Erlang Term Format), schneller aber komplexer
- **Transport-Kompression**: `zlib-stream` oder `zstd-stream`

#### Gateway Intents

**Standard Intents:**
| Intent | Wert | Events |
|--------|------|--------|
| GUILDS | 1 << 0 | GUILD_CREATE, CHANNEL_CREATE, etc. |
| GUILD_MEMBERS | 1 << 1 | GUILD_MEMBER_ADD, UPDATE, REMOVE |
| GUILD_MODERATION | 1 << 2 | GUILD_BAN_ADD, GUILD_AUDIT_LOG_ENTRY_CREATE |
| GUILD_EXPRESSIONS | 1 << 3 | GUILD_EMOJIS_UPDATE, GUILD_STICKERS_UPDATE |
| GUILD_INTEGRATIONS | 1 << 4 | INTEGRATION_CREATE, UPDATE, DELETE |
| GUILD_WEBHOOKS | 1 << 5 | WEBHOOKS_UPDATE |
| GUILD_INVITES | 1 << 6 | INVITE_CREATE, INVITE_DELETE |
| GUILD_VOICE_STATES | 1 << 7 | VOICE_STATE_UPDATE |
| GUILD_MESSAGES | 1 << 9 | MESSAGE_CREATE, UPDATE, DELETE |
| GUILD_MESSAGE_REACTIONS | 1 << 10 | MESSAGE_REACTION_ADD, REMOVE |
| GUILD_SCHEDULED_EVENTS | 1 << 16 | GUILD_SCHEDULED_EVENT_CREATE, etc. |
| AUTO_MODERATION_CONFIGURATION | 1 << 20 | AUTO_MODERATION_RULE_CREATE, etc. |
| AUTO_MODERATION_EXECUTION | 1 << 21 | AUTO_MODERATION_ACTION_EXECUTION |

**Privileged Intents** (müssen im Developer Portal aktiviert werden):
- `GUILD_PRESENCES` (1 << 8)
- `GUILD_MEMBERS` (1 << 1)
- `MESSAGE_CONTENT` (1 << 15)

#### Sharding

**Formel:** `shard_id = (guild_id >> 22) % num_shards`

- Maximum 2500 Guilds pro Shard
- Ab 2500+ Guilds ist Sharding verpflichtend
- `max_concurrency` bestimmt gleichzeitige Shard-Starts

**Rate Limit Key:** `rate_limit_key = shard_id % max_concurrency`

### 2.2 Gateway Events

#### Send Events (Client → Discord)

| Event | Opcode | Beschreibung |
|-------|--------|--------------|
| Identify | 2 | Initialer Handshake |
| Resume | 6 | Verbindung wiederherstellen |
| Heartbeat | 1 | Verbindung am Leben halten |
| Request Guild Members | 8 | Guild-Mitglieder anfordern |
| Update Voice State | 4 | Voice-Channel beitreten/verlassen |
| Update Presence | 3 | Status aktualisieren |
| Request Soundboard Sounds | 31 | Soundboard-Sounds anfordern |

#### Receive Events (Discord → Client)

| Event | Beschreibung |
|-------|--------------|
| **HELLO** (op 10) | Heartbeat-Interval definieren |
| **READY** | Initialer State nach Identify |
| **RESUMED** | Resume erfolgreich |
| **RECONNECT** | Client soll reconnecten |
| **INVALID_SESSION** | Session ungültig |
| **CHANNEL_CREATE/UPDATE/DELETE** | Channel-Änderungen |
| **GUILD_CREATE/UPDATE/DELETE** | Guild-Änderungen |
| **GUILD_MEMBER_ADD/REMOVE/UPDATE** | Mitgliedschafts-Änderungen |
| **MESSAGE_CREATE/UPDATE/DELETE** | Nachrichten-Events |
| **INTERACTION_CREATE** | Interaction empfangen |
| **VOICE_STATE_UPDATE** | Voice-Status Änderung |
| **VOICE_SERVER_UPDATE** | Voice-Server Info |

---

## 3. Voice

### 3.1 Voice Connections

**Aktuelle Version:** Version 8 (empfohlen)
**Deprecated:** Versionen < 4 (nicht mehr unterstützt seit Nov 2024)

#### Verbindungsaufbau

1. **Voice State Update an Gateway senden** (opcode 4)
```json
{
  "op": 4,
  "d": {
    "guild_id": "...",
    "channel_id": "...",
    "self_mute": false,
    "self_deaf": false
  }
}
```

2. **Voice Server Update empfangen**
```json
{
  "t": "VOICE_SERVER_UPDATE",
  "d": {
    "token": "my_token",
    "guild_id": "...",
    "endpoint": "sweetwater-12345.discord.media:2048"
  }
}
```

3. **Voice WebSocket verbinden**
   - `wss://{endpoint}?v=8`
   - Identify senden

4. **Ready empfangen** (opcode 2)
   - SSRC, IP, Port, Verschlüsselungsmodi

5. **UDP-Verbindung aufbauen**
   - IP Discovery durchführen
   - Select Protocol senden

#### Verschlüsselungsmodi

| Modus | Status |
|-------|--------|
| `aead_aes256_gcm_rtpsize` | Verfügbar (Bevorzugt) |
| `aead_xchacha20_poly1305_rtpsize` | Verfügbar (Erforderlich) |
| `xsalsa20_poly1305_lite_rtpsize` | Deprecated |
| `xsalsa20_poly1305` | Deprecated |

#### DAVE Protocol (End-to-End Encryption)

**Wichtig:** Ab 1. März 2026 nur noch E2EE unterstützt!

- Nutzt MLS (Messaging Layer Security) für Schlüsselaustausch
- Audio-Frames werden mit AES128-GCM verschlüsselt
- `max_dave_protocol_version` in Identify angeben
- Bibliothek: [libdave](https://github.com/discord/libdave)

**DAVE Opcodes:**
- 21: DAVE Protocol Prepare Transition
- 22: DAVE Protocol Execute Transition
- 23: DAVE Protocol Transition Ready
- 24: DAVE Protocol Prepare Epoch
- 25: DAVE MLS External Sender Package
- 26: DAVE MLS Key Package
- 27: DAVE MLS Proposals
- 28: DAVE MLS Commit Welcome
- 29: DAVE MLS Announce Commit Transition
- 30: DAVE MLS Welcome
- 31: DAVE MLS Invalid Commit Welcome

#### Speaking

| Flag | Bedeutung | Wert |
|------|-----------|------|
| Microphone | Normale Sprachübertragung | 1 << 0 |
| Soundshare | Kontext-Audio (Video, Screen Share) | 1 << 1 |
| Priority | Priority Speaker | 1 << 2 |

**Wichtig:** Mindestens ein Speaking-Payload vor Sprachdaten senden!

#### Voice Packet Struktur

| Feld | Größe |
|------|-------|
| Version + Flags (0x80) | 1 Byte |
| Payload Type (0x78) | 1 Byte |
| Sequence | 2 Bytes (Big Endian) |
| Timestamp | 4 Bytes (Big Endian) |
| SSRC | 4 Bytes (Big Endian) |
| Encrypted Audio | n Bytes |

### 3.2 Voice Ressourcen

#### Voice State Object

| Feld | Typ | Beschreibung |
|------|-----|--------------|
| `guild_id` | ?snowflake | Guild-ID |
| `channel_id` | ?snowflake | Channel-ID (null = disconnected) |
| `user_id` | snowflake | User-ID |
| `session_id` | string | Session-ID |
| `deaf` | boolean | Server-deafened |
| `mute` | boolean | Server-muted |
| `self_deaf` | boolean | Selbst-deafened |
| `self_mute` | boolean | Selbst-muted |
| `self_stream` | ?boolean | Streaming (Go Live) |
| `self_video` | boolean | Kamera aktiv |
| `suppress` | boolean | Sprachberechtigung entzogen |
| `request_to_speak_timestamp` | ?ISO8601 | Zeitpunkt der Sprechanfrage |

#### Voice Region Object

| Feld | Beschreibung |
|------|--------------|
| `id` | Eindeutige Region-ID |
| `name` | Anzeigename |
| `optimal` | Nächste Region zum Client |
| `deprecated` | Veraltet |
| `custom` | Benutzerdefiniert |

#### API Endpoints

```
GET /voice/regions
GET /guilds/{guild.id}/voice-states/@me
GET /guilds/{guild.id}/voice-states/{user.id}
PATCH /guilds/{guild.id}/voice-states/@me
PATCH /guilds/{guild.id}/voice-states/{user.id}
```

### 3.3 Discord Social SDK

**Voice Chat in Lobbies:**

```cpp
// Lobby beitreten/erstellen
client->CreateOrJoinLobby(lobbySecret, callback);

// Voice Call starten/beitreten
auto call = client->StartCall(lobbyId);

// Mit Audio-Callbacks
auto call = client->StartCallWithAudioCallbacks(
    lobbyId,
    userAudioCallback,    // Eingehende Audio-Daten
    captureAudioCallback  // Ausgehende Audio-Daten
);
```

**Globale Steuerung:**
- `SetSelfMuteAll(bool)` - Mikrofon in allen Calls stummschalten
- `SetSelfDeafAll(bool)` - Alle Calls stummschalten
- `SetInputVolume(float)` - Mikrofon-Lautstärke (0-200%)
- `SetOutputVolume(float)` - Ausgabe-Lautstärke (0-200%)

**Pro-Call Steuerung:**
- `Call::SetSelfMute(bool)` - Stummschalten in diesem Call
- `Call::SetSelfDeaf(bool)` - Deafen in diesem Call
- `Call::SetParticipantVolume(userId, volume)` - Teilnehmer-Lautstärke
- `Call::SetVADThreshold(bool, float)` - Voice Activity Detection

**Empfohlene Limits:**
- Maximal 25 Teilnehmer pro Voice Call
- Bis zu 1.000 Lobby-Mitglieder technisch möglich

---

## 4. Webhooks

### Webhook Object

| Feld | Typ | Beschreibung |
|------|-----|--------------|
| `id` | snowflake | Webhook-ID |
| `type` | integer | Webhook-Typ |
| `guild_id` | ?snowflake | Guild-ID |
| `channel_id` | ?snowflake | Channel-ID |
| `user` | ?user | Ersteller |
| `name` | ?string | Webhook-Name |
| `avatar` | ?string | Avatar-Hash |
| `token` | ?string | Webhook-Token (nur Incoming) |
| `application_id` | ?snowflake | App-ID |
| `url` | ?string | Webhook-URL |

### Webhook Types

| Wert | Name | Beschreibung |
|------|------|--------------|
| 1 | Incoming | Standard-Webhook mit Token |
| 2 | Channel Follower | Intern für Channel Following |
| 3 | Application | Für Interactions |

### API Endpoints

```
POST   /channels/{channel.id}/webhooks
GET    /channels/{channel.id}/webhooks
GET    /guilds/{guild.id}/webhooks
GET    /webhooks/{webhook.id}
GET    /webhooks/{webhook.id}/{webhook.token}
PATCH  /webhooks/{webhook.id}
PATCH  /webhooks/{webhook.id}/{webhook.token}
DELETE /webhooks/{webhook.id}
DELETE /webhooks/{webhook.id}/{webhook.token}

POST   /webhooks/{webhook.id}/{webhook.token}
POST   /webhooks/{webhook.id}/{webhook.token}/slack
POST   /webhooks/{webhook.id}/{webhook.token}/github

GET    /webhooks/{webhook.id}/{webhook.token}/messages/{message.id}
PATCH  /webhooks/{webhook.id}/{webhook.token}/messages/{message.id}
DELETE /webhooks/{webhook.id}/{webhook.token}/messages/{message.id}
```

### Query-Parameter für Execute

| Parameter | Beschreibung |
|-----------|--------------|
| `wait` | Auf Bestätigung warten, Nachricht zurückgeben |
| `thread_id` | In Thread senden |
| `with_components` | Component-Unterstützung aktivieren |

**Hinweis:** Für Forum/Media-Channels entweder `thread_id` oder `thread_name` angeben.

---

## 5. Ressourcen

### 5.1 User

#### User Object

| Feld | Typ | OAuth2 Scope |
|------|-----|--------------|
| `id` | snowflake | identify |
| `username` | string | identify |
| `discriminator` | string | identify |
| `global_name` | ?string | identify |
| `avatar` | ?string | identify |
| `bot` | boolean | identify |
| `mfa_enabled` | boolean | identify |
| `banner` | ?string | identify |
| `accent_color` | ?integer | identify |
| `locale` | string | identify |
| `verified` | boolean | email |
| `email` | ?string | email |
| `flags` | integer | identify |
| `premium_type` | integer | identify |
| `public_flags` | integer | identify |

#### User Flags

| Flag | Wert | Beschreibung |
|------|------|--------------|
| STAFF | 1 << 0 | Discord Mitarbeiter |
| PARTNER | 1 << 1 | Partnered Server Owner |
| HYPESQUAD | 1 << 2 | HypeSquad Events |
| BUG_HUNTER_LEVEL_1 | 1 << 3 | Bug Hunter Stufe 1 |
| HYPESQUAD_ONLINE_HOUSE_1 | 1 << 6 | House Bravery |
| HYPESQUAD_ONLINE_HOUSE_2 | 1 << 7 | House Brilliance |
| HYPESQUAD_ONLINE_HOUSE_3 | 1 << 8 | House Balance |
| PREMIUM_EARLY_SUPPORTER | 1 << 9 | Früher Nitro Supporter |
| VERIFIED_BOT | 1 << 16 | Verifizierter Bot |
| VERIFIED_DEVELOPER | 1 << 17 | Früher verifizierter Bot-Entwickler |

#### Premium Types

| Wert | Name |
|------|------|
| 0 | Keins |
| 1 | Nitro Classic |
| 2 | Nitro |
| 3 | Nitro Basic |

#### API Endpoints

```
GET    /users/@me
GET    /users/{user.id}
PATCH  /users/@me
GET    /users/@me/guilds
GET    /users/@me/guilds/{guild.id}/member
DELETE /users/@me/guilds/{guild.id}
POST   /users/@me/channels
GET    /users/@me/connections
GET    /users/@me/applications/{application.id}/role-connection
PUT    /users/@me/applications/{application.id}/role-connection
```

### 5.2 Message

#### Message Object

| Feld | Typ | Beschreibung |
|------|-----|--------------|
| `id` | snowflake | Nachrichten-ID |
| `channel_id` | snowflake | Channel-ID |
| `author` | user | Autor (kann Webhook sein) |
| `content` | string | Nachrichteninhalt |
| `timestamp` | ISO8601 | Sendezeit |
| `edited_timestamp` | ?ISO8601 | Bearbeitungszeit |
| `tts` | boolean | TTS-Nachricht |
| `mention_everyone` | boolean | @everyone erwähnt |
| `mentions` | user[] | Erwähnte User |
| `mention_roles` | snowflake[] | Erwähnte Rollen |
| `attachments` | attachment[] | Anhänge |
| `embeds` | embed[] | Embeds |
| `reactions` | reaction[] | Reaktionen |
| `pinned` | boolean | Angepinnt |
| `webhook_id` | ?snowflake | Webhook-ID |
| `type` | integer | Nachrichtentyp |
| `flags` | integer | Message Flags |
| `components` | component[] | Komponenten |
| `sticker_items` | sticker item[] | Sticker |
| `poll` | poll | Umfrage |

#### Message Types

| Typ | Wert | Löschbar |
|-----|------|----------|
| DEFAULT | 0 | Ja |
| RECIPIENT_ADD | 1 | Nein |
| RECIPIENT_REMOVE | 2 | Nein |
| CALL | 3 | Nein |
| CHANNEL_NAME_CHANGE | 4 | Nein |
| CHANNEL_PINNED_MESSAGE | 6 | Ja |
| USER_JOIN | 7 | Ja |
| GUILD_BOOST | 8 | Ja |
| REPLY | 19 | Ja |
| CHAT_INPUT_COMMAND | 20 | Ja |
| THREAD_STARTER_MESSAGE | 21 | Nein |
| CONTEXT_MENU_COMMAND | 23 | Ja |
| AUTO_MODERATION_ACTION | 24 | Ja* |
| POLL_RESULT | 46 | Ja |

#### Message Flags

| Flag | Wert | Beschreibung |
|------|------|--------------|
| CROSSPOSTED | 1 << 0 | Veröffentlicht (Channel Following) |
| IS_CROSSPOST | 1 << 1 | Aus anderem Channel |
| SUPPRESS_EMBEDS | 1 << 2 | Keine Embeds anzeigen |
| SOURCE_MESSAGE_DELETED | 1 << 3 | Quelle gelöscht |
| URGENT | 1 << 4 | Dringende Nachricht |
| HAS_THREAD | 1 << 5 | Hat Thread |
| EPHEMERAL | 1 << 6 | Nur für Interacting-User sichtbar |
| LOADING | 1 << 7 | "Denkt nach"-Status |
| SUPPRESS_NOTIFICATIONS | 1 << 12 | Keine Push-Benachrichtigungen |
| IS_VOICE_MESSAGE | 1 << 13 | Sprachnachricht |
| HAS_SNAPSHOT | 1 << 14 | Hat Snapshot (Weiterleitung) |
| IS_COMPONENTS_V2 | 1 << 15 | Component-Driven Nachricht |

### 5.3 Channel

#### Channel Types

| Typ | ID | Beschreibung |
|-----|----|--------------|
| GUILD_TEXT | 0 | Text-Channel |
| DM | 1 | Direktnachricht |
| GUILD_VOICE | 2 | Sprach-Channel |
| GROUP_DM | 3 | Gruppen-DM |
| GUILD_CATEGORY | 4 | Kategorie |
| GUILD_ANNOUNCEMENT | 5 | Ankündigungs-Channel |
| ANNOUNCEMENT_THREAD | 10 | Ankündigungs-Thread |
| PUBLIC_THREAD | 11 | Öffentlicher Thread |
| PRIVATE_THREAD | 12 | Privater Thread |
| GUILD_STAGE_VOICE | 13 | Stage-Channel |
| GUILD_FORUM | 15 | Forum-Channel |
| GUILD_MEDIA | 16 | Media-Channel |

#### Channel Object (Auswahl)

| Feld | Beschreibung |
|------|--------------|
| `id` | Channel-ID |
| `type` | Channel-Typ |
| `guild_id` | Guild-ID |
| `position` | Sortierungsposition |
| `permission_overwrites` | Berechtigungs-Overrides |
| `name` | Channel-Name |
| `topic` | Thema/Beschreibung |
| `nsfw` | Age-restricted |
| `last_message_id` | Letzte Nachricht |
| `bitrate` | Bitrate (Voice) |
| `user_limit` | User-Limit (Voice) |
| `rate_limit_per_user` | Slowmode |
| `parent_id` | Parent-Kategorie |
| `rtc_region` | Voice-Region |
| `video_quality_mode` | Video-Qualität |
| `message_count` | Nachrichtenanzahl (Thread) |
| `member_count` | Mitgliederanzahl (Thread) |
| `thread_metadata` | Thread-Metadaten |
| `default_auto_archive_duration` | Standard-Archivierungsdauer |
| `flags` | Channel-Flags |

#### Video Quality Modes

| Modus | Wert | Beschreibung |
|-------|------|--------------|
| AUTO | 1 | Automatisch |
| FULL | 2 | 720p |

#### API Endpoints

```
GET    /channels/{channel.id}
PATCH  /channels/{channel.id}
DELETE /channels/{channel.id}

GET    /channels/{channel.id}/messages
POST   /channels/{channel.id}/messages

GET    /channels/{channel.id}/messages/{message.id}
PATCH  /channels/{channel.id}/messages/{message.id}
DELETE /channels/{channel.id}/messages/{message.id}

POST   /channels/{channel.id}/messages/{message.id}/crosspost
PUT    /channels/{channel.id}/messages/{message.id}/pin
DELETE /channels/{channel.id}/messages/{message.id}/pin
POST   /channels/{channel.id}/messages/{message.id}/reactions/{emoji}/@me
DELETE /channels/{channel.id}/messages/{message.id}/reactions/{emoji}/@me

GET    /channels/{channel.id}/messages/{message.id}/reactions/{emoji}
DELETE /channels/{channel.id}/messages/{message.id}/reactions

DELETE /channels/{channel.id}/messages/bulk-delete

POST   /channels/{channel.id}/typing

GET    /channels/{channel.id}/pins
DELETE /channels/{channel.id}/pins/{message.id}

POST   /channels/{channel.id}/followers

POST   /channels/{channel.id}/invites
GET    /channels/{channel.id}/invites

POST   /channels/{channel.id}/threads
POST   /channels/{channel.id}/thread-members/@me
DELETE /channels/{channel.id}/thread-members/@me
GET    /channels/{channel.id}/thread-members
```

---

## 6. Community Resources

### Discord-Bibliotheken

| Name | Sprache |
|------|---------|
| discord.js | JavaScript |
| discord.py | Python |
| JDA | Java |
| Discord.Net | C# |
| DSharpPlus | C# |
| discordgo | Go |
| Serenity | Rust |
| discordrb | Ruby |
| D++ | C++ |

### Interactions-Bibliotheken

**JavaScript:**
- discord-interactions-js (offiziell)
- slash-create

**Python:**
- discord-interactions-python (offiziell)
- discord-interactions.py
- flask-discord-interactions

**C#:**
- Discord.Net.Rest
- DSharpPlus.Http.AspNetCore

**PHP:**
- discord-interactions-php (offiziell)

### Tools & Calculator

| Tool | Zweck |
|------|-------|
| BotForge Permissions Calculator | Berechtigungen berechnen |
| ziad87's Intent Calculator | Gateway Intents berechnen |
| discord-api-types | TypeScript-Typen |

### Support

- **Discord Developers Server**: https://discord.gg/discord-developers
- **Bug Reports Social SDK**: https://dis.gd/social-sdk-bug-report

---

## Anhänge

### HTTP API Informationen

**Basis-URL:** `https://discord.com/api/v{version}`

**Aktuelle Versionen:**
- v10 (stable)
- v9 (verfügbar)

**Rate Limiting:**
- Global Rate Limits pro Route
- Retry-After Header bei Limits
- 429 Too Many Requests

**Authentication:**
```
Authorization: Bot {token}
Authorization: Bearer {token}  # OAuth2
```

### Gateway Opcodes

| Opcode | Name | Beschreibung |
|--------|------|--------------|
| 0 | Dispatch | Event |
| 1 | Heartbeat | Heartbeat senden |
| 2 | Identify | Authentifizierung |
| 6 | Resume | Session wiederherstellen |
| 7 | Reconnect | Reconnect anfordern |
| 8 | Request Guild Members | Mitglieder anfordern |
| 9 | Invalid Session | Ungültige Session |
| 10 | Hello | Erste Verbindung |
| 11 | Heartbeat ACK | Heartbeat bestätigt |

### Voice Opcodes

| Opcode | Name |
|--------|------|
| 0 | Identify |
| 1 | Select Protocol |
| 2 | Ready |
| 3 | Heartbeat |
| 4 | Session Description |
| 5 | Speaking |
| 6 | Heartbeat ACK |
| 7 | Resume |
| 8 | Hello |
| 9 | Resumed |
| 13 | Client Disconnect |
| 18 | Client Flags |
| 20 | Sources |
| 21-31 | DAVE Protocol Opcodes |

---

*Diese Dokumentation wurde automatisch aus der offiziellen Discord Developer Dokumentation generiert.*
