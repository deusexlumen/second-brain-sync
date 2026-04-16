# Gofile Upload Skill

## Overview

Upload files to Gofile.io via API. Supports authenticated uploads with token.

## Activation Trigger

- User wants to upload file to Gofile
- Keywords: "gofile", "upload", "file share"

## Configuration

```bash
# Environment variables (set in ~/.openclaw/config/gofile.env)
GOFILE_API_TOKEN=aAbfNend9STgMVrFKc872rvQNKLVG7B7
GOFILE_USER_ID=930161e8-99ef-4af5-843f-c43a098945ba
```

## API Endpoints (Updated 2026-04-14)

- **Base URL:** `https://api.gofile.io`

## Workflow

### 1. Get Upload Server (REQUIRED before each upload)
```bash
curl -s "https://api.gofile.io/servers"
# Response: {"status":"ok","data":{"servers":[{"name":"store1","zone":"eu"}...]}}
```

### 2. Upload File
```bash
curl -X POST \
  -F "file=@/path/to/file.mp4" \
  -F "token=$GOFILE_API_TOKEN" \
  "https://{server}.gofile.io/uploadFile"
# Response: {"status":"ok","data":{"downloadPage":"https://gofile.io/d/XXXX"}}
```

### 3. Create Folder
```bash
curl -X POST \
  -H "Authorization: Bearer $GOFILE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"parentFolderId":"root","folderName":"MyFolder"}' \
  "https://api.gofile.io/createFolder"
```

### 4. Get Content Info
```bash
curl -s "https://api.gofile.io/getContent?contentId=FILE_ID"
```

### 5. Delete Content
```bash
curl -X DELETE \
  -H "Authorization: Bearer $GOFILE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"contentsId":"FILE_ID"}' \
  "https://api.gofile.io/deleteContent"
```

## Implementation Script

```bash
#!/bin/bash
# gofile_upload.sh <file_path> [description]

set -e

FILE_PATH="$1"
TOKEN="${GOFILE_API_TOKEN}"

# Step 1: Get server (use first available)
SERVER=$(curl -s "https://api.gofile.io/servers" | jq -r '.data.servers[0].name')

# Step 2: Upload file
RESPONSE=$(curl -s -X POST \
  -F "file=@$FILE_PATH" \
  -F "token=$TOKEN" \
  "https://${SERVER}.gofile.io/uploadFile")

# Extract download page
DOWNLOAD_PAGE=$(echo "$RESPONSE" | jq -r '.data.downloadPage')
echo "✓ Upload successful: $DOWNLOAD_PAGE"
```

## Usage

```bash
# Set token
export GOFILE_API_TOKEN="your-token"

# Upload file
bash ~/.openclaw/workspace/skills/gofile-upload/gofile_upload.sh /path/to/file.mp4
```

## Free Tier Limits

- Files deleted after inactivity
- No permanent links guaranteed
- Use downloadPage for user sharing (directLink often empty)

## Error Handling

| Status | Meaning | Action |
|--------|---------|--------|
| `ok` | Success | Continue |
| `error-limit` | Free tier limit reached | Inform user |
| `error-token` | Invalid token | Check credentials |

---

## Upload History

**2026-04-14:** Terminated Video (38MB)
- Download: https://gofile.io/d/3j3xO4
- File ID: 93600a8a-8a67-45d8-902e-d24bb9146eb6

*Status: Active and working*
