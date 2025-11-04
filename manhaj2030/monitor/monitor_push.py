#!/usr/bin/env python3
import json, os, subprocess, datetime, requests
from pathlib import Path

# CONFIG - اضبط URL و TOKEN كما في الـ Receiver
RECEIVER_URL = "http://209.38.221.191:5002/snapshot"
TOKEN = "6f3b9e8a2c4d7f1a9b0c3d2e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3"

OUTPUT_LOG_DIR = Path("/srv/manhaj2030/pmc/system_logs")
OUTPUT_LOG_DIR.mkdir(parents=True, exist_ok=True)
SNAPSHOT_NAME = "MANUS_AUTO_SNAPSHOT"

def run(cmd):
    try:
        out = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL, timeout=12)
        return out.decode("utf-8", errors="ignore")
    except Exception as e:
        return f"ERROR: {str(e)}"

def collect():
    base = Path("/srv/manhaj2030")
    data = {}
    data["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data["disk_top"] = run("du -h --max-depth=1 /srv/manhaj2030/ | sort -hr | head -n 20")
    data["screen_ls"] = run("screen -ls || true")
    data["nvidia_smi"] = run("nvidia-smi --query-gpu=index,name,utilization.gpu,memory.used,memory.total --format=csv,noheader,nounits || nvidia-smi")
    data["recent_logs_tail"] = run("tail -n 200 /srv/manhaj2030/pmc/system_logs/*.log 2>/dev/null || true")
    key_files = [
      "data/validation/HADITHS_VALIDATED_NER_v3_FIXED_CLEAN.json",
      "data/graph/isnad_graph_v5.json",
      "data/validation/HADITHS_CREDIBILITY_INDEX_v5.json",
      "data/analytics/HADITHS_ANALYTICS_v5.json",
      "dashboard/ai_dashboard_snapshot_v5.json"
    ]
    files_info = {}
    for f in key_files:
        p = Path("/srv/manhaj2030") / f
        if p.exists():
            files_info[f] = {"exists": True, "size": p.stat().st_size, "mtime": p.stat().st_mtime}
        else:
            files_info[f] = {"exists": False}
    data["files"] = files_info
    data["top_ps"] = run("ps -eo pid,comm,%cpu,%mem --sort=-%cpu | head -n 20")
    return data

def post_snapshot(payload):
    headers = {"Content-Type":"application/json","X-Snapshot-Token":TOKEN}
    try:
        r = requests.post(RECEIVER_URL, json=payload, headers=headers, timeout=15)
        return {"status": r.status_code, "text": r.text}
    except Exception as e:
        return {"status": "error", "error": str(e)}

if __name__ == "__main__":
    snap = collect()
    res = post_snapshot(snap)
    ts = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
    with open(OUTPUT_LOG_DIR / f"{SNAPSHOT_NAME}_{ts}.json","w",encoding="utf-8") as f:
        json.dump({"snapshot": snap, "post_result": res}, f, ensure_ascii=False, indent=2)
    print("Posted:", res)
