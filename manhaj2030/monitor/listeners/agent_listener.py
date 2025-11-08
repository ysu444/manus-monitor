#!/usr/bin/env python3
import os, time, json, sys

INBOX_BASE = "/srv/manhaj2030/monitor/inbox"
LOG_FILE   = "/srv/manhaj2030/monitor/logs/agent_listeners.log"

def log(msg):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{ts}] {msg}\n")

def run_listener(agent_id:int):
    inbox = os.path.join(INBOX_BASE, f"agent_{agent_id}.jsonl")
    open(inbox, "a").close()  # تأكد أن الملف موجود
    log(f"🔊 Listener for Agent {agent_id} started, monitoring {inbox}")

    last_size = 0
    while True:
        try:
            size = os.path.getsize(inbox)
            if size != last_size:
                with open(inbox, "r") as f:
                    lines = f.readlines()
                    if lines:
                        event = json.loads(lines[-1])
                        log(f"📨 Agent {agent_id} received event: {event.get('event')}")
                last_size = size
            time.sleep(1)
        except Exception as e:
            log(f"⚠️ Listener error for Agent {agent_id}: {e}")
            time.sleep(5)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: agent_listener.py <agent_id>")
        sys.exit(1)
    run_listener(int(sys.argv[1]))
