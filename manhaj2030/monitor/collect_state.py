#!/usr/bin/env python3
# يُشغّل فقط على: السيرفر الكبير (45.32.106.139)
# /srv/manhaj2030/monitor/collect_state.py

import os, json, time, hashlib, subprocess, argparse
from datetime import datetime

# ====== CONFIG ======
PMC_FILES = [
    "/srv/manhaj2030/pmc/memory/EVENTS_LOG.md",
    "/srv/manhaj2030/data/shared/pmc_dossier_latest.md"
]
SNAPSHOT_PATH = "/srv/manhaj2030/dashboard/ai_dashboard_snapshot.json"
AGENT_STATUS_FILES = {
    "Agent 10": "/srv/manhaj2030/training/agent10_status.json",
    "Agent 11": "/srv/manhaj2030/training/agent11_status.json"
}
OUTPUT_DIR = "/srv/manhaj2030/monitor/output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "live_state.json")
PUSH_MODE = "http"   # "http" or "rsync" or "local"
VPS_RECEIVER = "https://jojosa.com/snapshot"  # على الVPS
VPS_TOKEN = "6f3b9e8a2c4d7f1a9b0c3d2e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3"
INTERVAL = 120
# ====================

os.makedirs(OUTPUT_DIR, exist_ok=True)

def sha256_of_file(path):
    try:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None

def read_small_file(path, max_bytes=200000):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read(max_bytes)
    except Exception:
        return None

def run_cmd(cmd):
    try:
        out = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL, timeout=10)
        return out.decode("utf-8", errors="ignore").strip()
    except Exception:
        return None

def gather_system():
    sysinfo = {}
    sysinfo['time'] = datetime.utcnow().isoformat() + "Z"
    sysinfo['hostname'] = run_cmd("hostname")
    # Disk
    sysinfo['disk'] = run_cmd("df -h --output=source,size,used,avail,pcent,target -x tmpfs -x devtmpfs | tail -n +2")
    # Memory
    sysinfo['mem'] = run_cmd("free -h")
    # CPU load
    sysinfo['load'] = run_cmd("cat /proc/loadavg")
    # GPU
    sysinfo['nvidia_smi'] = run_cmd("nvidia-smi --query-gpu=index,name,memory.total,memory.used,utilization.gpu --format=csv,noheader,nounits")
    # processes for known training patterns (example)
    sysinfo['training_procs'] = run_cmd("ps aux | grep -E 'python.*train|run_training|torch' | grep -v grep | head -n 50")
    return sysinfo

def gather_pmc():
    data = {}
    for p in PMC_FILES:
        data[p] = {
            "sha256": sha256_of_file(p),
            "snippet": read_small_file(p, max_bytes=10000)
        }
    return data

def gather_snapshot():
    if os.path.exists(SNAPSHOT_PATH):
        return {
            "path": SNAPSHOT_PATH,
            "sha256": sha256_of_file(SNAPSHOT_PATH),
            "content_sample": read_small_file(SNAPSHOT_PATH, max_bytes=20000)
        }
    return None

def gather_agents():
    agents = {}
    for name, path in AGENT_STATUS_FILES.items():
        if os.path.exists(path):
            try:
                agents[name] = json.load(open(path))
                agents[name]['sha256'] = sha256_of_file(path)
            except Exception:
                agents[name] = {
                    "raw": read_small_file(path, max_bytes=20000),
                    "sha256": sha256_of_file(path)
                }
        else:
            agents[name] = {"status": "missing", "path": path}
    return agents

def write_output(payload):
    tmp = OUTPUT_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    os.replace(tmp, OUTPUT_FILE)
    return OUTPUT_FILE

def push_http(output_path):
    try:
        import requests
        with open(output_path, "r", encoding="utf-8") as f:
            payload = json.load(f)
        r = requests.post(VPS_RECEIVER,
                          headers={"X-Snapshot-Token": VPS_TOKEN,
                                   "Content-Type": "application/json"},
                          json=payload,
                          verify=False)  # Skip SSL verification for self-signed cert
        return r.status_code, r.text
    except Exception as e:
        return None, str(e)

def main_loop():
    while True:
        payload = {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "server": "السيرفر الكبير (45.32.106.139)",
            "system": gather_system(),
            "pmc": gather_pmc(),
            "snapshot": gather_snapshot(),
            "agents": gather_agents(),
            "notes": {
                "interval_seconds": INTERVAL
            }
        }
        out = write_output(payload)
        if PUSH_MODE == "http":
            code, text = push_http(out)
            # احتفظ بسجل محلي قصير
            with open(os.path.join(OUTPUT_DIR, "last_push.log"), "a", encoding="utf-8") as lg:
                lg.write(f"{datetime.utcnow().isoformat()} pushed -> {code}\n")
        elif PUSH_MODE == "rsync":
            # مثال rsync إلى الVPS: requires ssh key setup
            run_cmd(f"rsync -avz {out} youruser@jojosa.com:/var/www/snapshots_state/manus_state.json")
        # انتظر
        time.sleep(INTERVAL)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--interval", type=int, default=INTERVAL)
    parser.add_argument("--push-mode", choices=["http","rsync","local"], default=PUSH_MODE)
    args = parser.parse_args()
    INTERVAL = args.interval
    PUSH_MODE = args.push_mode
    main_loop()

