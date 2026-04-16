#!/bin/bash
# Gofile Upload Script
# Usage: gofile_upload.sh <file_path> [optional_description]

set -e

FILE_PATH="$1"
DESCRIPTION="${2:-}"
TOKEN="${GOFILE_API_TOKEN:-aAbfNend9STgMVrFKc872rvQNKLVG7B7}"

if [ -z "$FILE_PATH" ] || [ ! -f "$FILE_PATH" ]; then
  echo "Error: File not found: $FILE_PATH"
  echo "Usage: $0 <file_path> [description]"
  exit 1
fi

echo "🌐 Getting Gofile upload server..."
SERVER_RESPONSE=$(curl -s "https://api.gofile.io/getServer")
SERVER=$(echo "$SERVER_RESPONSE" | grep -o '"server":"[^"]*"' | cut -d'"' -f4)

if [ -z "$SERVER" ] || [ "$SERVER" = "null" ]; then
  echo "Error: Failed to get upload server"
  echo "Response: $SERVER_RESPONSE"
  exit 1
fi

echo "✓ Server: $SERVER"
FILENAME=$(basename "$FILE_PATH")
echo "📤 Uploading: $FILENAME ($(du -h "$FILE_PATH" | cut -f1))..."

# Upload with token for account association
UPLOAD_RESPONSE=$(curl -s -X POST \
  -F "file=@$FILE_PATH" \
  -F "token=$TOKEN" \
  "https://${SERVER}.gofile.io/uploadFile")

# Check status
STATUS=$(echo "$UPLOAD_RESPONSE" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)

if [ "$STATUS" != "ok" ]; then
  echo "Error: Upload failed"
  echo "Response: $UPLOAD_RESPONSE"
  exit 1
fi

# Extract info
DOWNLOAD_PAGE=$(echo "$UPLOAD_RESPONSE" | grep -o '"downloadPage":"[^"]*"' | cut -d'"' -f4)
FILE_ID=$(echo "$UPLOAD_RESPONSE" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)
FILE_NAME=$(echo "$UPLOAD_RESPONSE" | grep -o '"name":"[^"]*"' | head -1 | cut -d'"' -f4)
FILE_SIZE=$(echo "$UPLOAD_RESPONSE" | grep -o '"size":[0-9]*' | head -1 | cut -d':' -f2)

echo ""
echo "✅ Upload successful!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📁 File: $FILE_NAME"
echo "🔗 Download: $DOWNLOAD_PAGE"
echo "🆔 File ID: $FILE_ID"
echo "📊 Size: $(numfmt --to=iec $FILE_SIZE 2>/dev/null || echo "${FILE_SIZE} bytes")"
[ -n "$DESCRIPTION" ] && echo "📝 Description: $DESCRIPTION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
