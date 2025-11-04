#!/bin/bash
# Monitor Upload Script with Gist Support
# Auto-updates GitHub repo + Gist every minute

set -euo pipefail

REPO_DIR="/srv/manhaj2030/monitor/manus-monitor"
MONITOR_DIR="/srv/manhaj2030/monitor"
GIST_ID_FILE="$MONITOR_DIR/.gist_id"
TOKEN_FILE="$MONITOR_DIR/.github_token"

cd "$REPO_DIR"

# 1. Copy fresh data
rsync -a --delete "$MONITOR_DIR/" ./manhaj2030/monitor/

# 2. Generate manifest
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
COMMIT_SHA=$(git rev-parse HEAD)
COMMIT_SHA_SHORT=$(echo "$COMMIT_SHA" | cut -c1-8)

cat > manifest.json << EOF
{
  "version": "4.0.0",
  "generated_at": "$TIMESTAMP",
  "commit_sha": "$COMMIT_SHA_SHORT",
  "description": "Manhaj2030 Monitor - Auto-updated every minute",
  "urls": {
    "repo": "https://github.com/ysu444/manus-monitor",
    "sha_based": "https://raw.githubusercontent.com/ysu444/manus-monitor/$COMMIT_SHA_SHORT/",
    "gist": "https://gist.githubusercontent.com/ysu444/$(cat $GIST_ID_FILE 2>/dev/null || echo 'GIST_ID')/raw/"
  }
}
EOF

# 3. Create latest_sha.txt
echo "$COMMIT_SHA_SHORT" > latest_sha.txt

# 4. Commit and push to GitHub repo
git add -A
git commit -m "Auto-update: $TIMESTAMP" || true
git push origin main

# 5. Update Gist (if configured)
if [ -f "$GIST_ID_FILE" ] && [ -f "$TOKEN_FILE" ]; then
    GIST_ID=$(cat "$GIST_ID_FILE")
    TOKEN=$(cat "$TOKEN_FILE")
    
    # Prepare JSON payload
    MANIFEST_CONTENT=$(cat manifest.json | jq -Rs .)
    STATE_CONTENT=$(cat manhaj2030/monitor/state.json | jq -Rs .)
    
    curl -s -X PATCH \
      -H "Authorization: token $TOKEN" \
      -H "Accept: application/vnd.github.v3+json" \
      "https://api.github.com/gists/$GIST_ID" \
      -d "{
        \"files\": {
          \"manifest.json\": {\"content\": $MANIFEST_CONTENT},
          \"state.json\": {\"content\": $STATE_CONTENT}
        }
      }" > /dev/null
    
    echo "✅ Gist updated: https://gist.github.com/ysu444/$GIST_ID"
fi

echo "✅ Monitor updated at $TIMESTAMP"
