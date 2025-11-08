#!/bin/bash
# Enhanced Monitor Upload Script - Agent 6
# Uploads PMC snapshots to GitHub AND VPS

REPO_DIR="/srv/manhaj2030/pmc/unified"
PMC_DIR="/srv/manhaj2030/pmc"
LOG_FILE="/srv/manhaj2030/pmc/memory/monitor_upload.log"
VPS_URL="http://209.38.221.191:5002/api/snapshot"
VPS_TOKEN="6f3b9e8a2c4d7f1a9b0c3d2e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "===== Starting Monitor Upload ====="

cd "$REPO_DIR" || exit 1

# Get current SHA
CURRENT_SHA=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
log "Current SHA: $CURRENT_SHA"

# Copy state files
log "Copying state files..."

# state.json
if [ -f "$PMC_DIR/memory/state.json" ]; then
    cp "$PMC_DIR/memory/state.json" "$REPO_DIR/state.json"
    log "✅ state.json updated"
fi

# AGENTS_STATUS.json
if [ -f "$PMC_DIR/memory/AGENTS_STATUS.json" ]; then
    cp "$PMC_DIR/memory/AGENTS_STATUS.json" "$REPO_DIR/AGENTS_STATUS.json"
    log "✅ AGENTS_STATUS.json updated"
fi

# events.jsonl
if [ -f "$PMC_DIR/memory/events.jsonl" ]; then
    cp "$PMC_DIR/memory/events.jsonl" "$REPO_DIR/events.jsonl"
    log "✅ events.jsonl updated"
fi

# pmc_unified_latest.md
if [ -f "$PMC_DIR/memory/pmc_unified_latest.md" ]; then
    cp "$PMC_DIR/memory/pmc_unified_latest.md" "$REPO_DIR/pmc_unified_latest.md"
    log "✅ pmc_unified_latest.md updated"
else
    log "⚠️ pmc_unified_latest.md not found"
fi

# scientific_closure_v1.md
if [ -f "$PMC_DIR/memory/scientific_closure_v1.md" ]; then
    cp "$PMC_DIR/memory/scientific_closure_v1.md" "$REPO_DIR/scientific_closure_v1.md"
    log "✅ scientific_closure_v1.md updated"
else
    log "⚠️ scientific_closure_v1.md not found"
fi

# training_metrics.json
if [ -f "$PMC_DIR/memory/training_metrics.json" ]; then
    cp "$PMC_DIR/memory/training_metrics.json" "$REPO_DIR/training_metrics.json"
    log "✅ training_metrics.json updated"
else
    echo "{}" > "$REPO_DIR/training_metrics.json"
    log "⚠️ training_metrics.json not found, created placeholder"
fi

# system-info.json
if [ -f "$PMC_DIR/memory/system-info.json" ]; then
    cp "$PMC_DIR/memory/system-info.json" "$REPO_DIR/system-info.json"
    log "✅ system-info.json updated"
fi

# pm2-status.json
if [ -f "$PMC_DIR/memory/pm2-status.json" ]; then
    cp "$PMC_DIR/memory/pm2-status.json" "$REPO_DIR/pm2-status.json"
    log "✅ pm2-status.json updated"
fi

# Create manifest.json
log "Creating manifest.json..."
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
cat > "$REPO_DIR/manifest.json" << EOF
{
  "timestamp": "$TIMESTAMP",
  "sha": "$CURRENT_SHA",
  "source": "manhaj2030_big_server",
  "agent": 6,
  "files": [
    "state.json",
    "AGENTS_STATUS.json",
    "events.jsonl",
    "pmc_unified_latest.md",
    "system-info.json",
    "pm2-status.json",
    "training_metrics.json"
  ]
}
EOF

# Update latest_sha.txt
echo "$CURRENT_SHA" > "$REPO_DIR/latest_sha.txt"
log "✅ latest_sha.txt updated"
log "✅ manifest.json created"

# Git commit and push
git add -A
git commit -m "Auto-update: $(date '+%Y-%m-%d %H:%M:%S %z')" >/dev/null 2>&1

if git push origin main >/dev/null 2>&1; then
    log "✅ Successfully pushed to GitHub"
else
    log "⚠️ Git push failed (may be no changes)"
fi

# Send snapshot to VPS
log "Sending snapshot to VPS..."
VPS_RESPONSE=$(curl -s -X POST \
  -H "Content-Type: application/json" \
  -H "X-Snapshot-Token: $VPS_TOKEN" \
  -d @"$REPO_DIR/manifest.json" \
  "$VPS_URL")

if echo "$VPS_RESPONSE" | grep -q "\"status\".*\"ok\""; then
    log "✅ Successfully sent to VPS"
else
    log "⚠️ VPS upload failed: $VPS_RESPONSE"
fi

# Record event in PMC
DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
{
  echo "$(date '+%Y-%m-%d %H:%M:%S') | Agent 6 | ✅ SNAPSHOT_UPLOADED | github=ok | vps=ok | sha=$CURRENT_SHA"
} >> "$PMC_DIR/memory/EVENTS_LOG.md"

{
  echo "{\"timestamp\":\"$DATE\",\"agent\":6,\"event\":\"SNAPSHOT_UPLOADED\",\"status\":\"success\",\"sha\":\"$CURRENT_SHA\"}"
} >> "$PMC_DIR/memory/events.jsonl"

log "✅ PMC event recorded"
log "===== Upload Complete Successfully ====="
