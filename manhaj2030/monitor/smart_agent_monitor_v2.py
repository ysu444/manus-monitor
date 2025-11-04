#!/usr/bin/env python3
import os, time, json, psutil, subprocess, datetime

LOG = "/srv/manhaj2030/reports/smart_agent_monitor_v2.log"
PMC = "/srv/manhaj2030/pmc/memory/EVENTS_LOG.md"
AGENTS = {10:"training",11:"integrity",12:"runtime",9:"error_map",8:"documentation",7:"api_health"}

def log_event(msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"{ts} | 🧠 SMART_MONITOR | {msg}\n"
    open(LOG,"a").write(entry)
    open(PMC,"a").write(entry)

def gpu_usage():
    try:
        out = subprocess.check_output("nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv,noheader,nounits",shell=True).decode().strip().split("\n")
        usage = [list(map(int,l.split(", "))) for l in out]
        avg = sum(u[0] for u in usage)/len(usage)
        mem = sum(u[1] for u in usage)
        return avg, mem
    except Exception: return 0,0

def check_agents():
    status = {}
    for a,name in AGENTS.items():
        try:
            p = subprocess.check_output(f"ps aux | grep -v grep | grep agent_{a}",shell=True).decode()
            status[a] = "🟢 active" if p else "⚫ idle"
        except: status[a] = "⚫ idle"
    return status

def main():
    log_event("Smart Agent Monitor v2 started ✅")
    while True:
        avg_gpu, mem_gpu = gpu_usage()
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/srv").percent
        agents = check_agents()
        snapshot = {
            "time": datetime.datetime.now().isoformat(),
            "cpu": cpu, "mem": mem, "disk": disk,
            "gpu_util": avg_gpu, "gpu_mem": mem_gpu,
            "agents": agents
        }
        open("/srv/manhaj2030/reports/smart_agent_monitor_snapshot.json","w").write(json.dumps(snapshot,indent=2))
        if cpu>90 or mem>90 or disk>90 or avg_gpu>95:
            log_event(f"⚠️ Resource alert — CPU:{cpu}% MEM:{mem}% DISK:{disk}% GPU:{avg_gpu}%")
        time.sleep(300)  # every 5 minutes

if __name__ == "__main__":
    main()
