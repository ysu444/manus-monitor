# -*- coding: utf-8 -*-
"""
Phase C-4 – Performance Monitoring & Alerting v1
يراقب الخدمات الإنتاجية (NER API / Dashboard / GPU) ويرسل تنبيهات محلية.
"""
import os, time, json, subprocess, requests, datetime

SERVICES = {
    "NER_v4_API": "http://127.0.0.1:8087/health",
    "NER_v4_API_Secure": "https://127.0.0.1:8088/health",
    "Dashboard_v5": "https://127.0.0.1/healthz-dashboard"
}
LOG = "/srv/manhaj2030/monitor/performance_alerts.log"
STATE = "/srv/manhaj2030/monitor/performance_state.json"

def check_service(name, url):
    try:
        if url.startswith("https"):
            resp = requests.get(url, verify=False, timeout=3)
        else:
            resp = requests.get(url, timeout=3)
        if resp.status_code == 200:
            return True, "OK"
        else:
            return False, f"HTTP {resp.status_code}"
    except Exception as e:
        return False, str(e)

def check_gpu():
    try:
        out = subprocess.check_output("nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv,noheader,nounits", shell=True)
        lines = out.decode().strip().split('\n')
        # أخذ أول GPU فقط
        util, mem = lines[0].split(",")
        return {"gpu_util": float(util.strip()), "gpu_mem": float(mem.strip())}
    except Exception as e:
        return {"gpu_util": 0, "gpu_mem": 0, "error": str(e)}

def alert(msg):
    stamp = datetime.datetime.now().isoformat()
    line = f"[{stamp}] ⚠️ {msg}\n"
    print(line.strip())
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line)

def monitor_loop():
    print("[Monitor] 🚀 Performance monitor started (every 60s)...")
    while True:
        status = {"timestamp": datetime.datetime.now().isoformat(), "services": {}, "gpu": check_gpu()}
        for name, url in SERVICES.items():
            ok, detail = check_service(name, url)
            status["services"][name] = {"status": ok, "detail": detail}
            if not ok:
                alert(f"{name} DOWN → {detail}")
        with open(STATE, "w", encoding="utf-8") as f:
            json.dump(status, f, ensure_ascii=False, indent=2)
        time.sleep(60)

if __name__ == "__main__":
    monitor_loop()
