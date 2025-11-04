#!/usr/bin/env python3
# Smart Agent Monitor v3 — Coordinator Mode (Fixed)
import os, json, time

EVENTS = "/srv/manhaj2030/pmc/events.jsonl"
INBOX = "/srv/manhaj2030/pmc/inbox"
STATE = "/srv/manhaj2030/pmc/.coord_pos"

def read_pos():
    try:
        return int(open(STATE).read().strip())
    except:
        return 0

def write_pos(p):
    tmp = STATE + ".tmp"
    with open(tmp, "w") as f:
        f.write(str(p))
    os.replace(tmp, STATE)

def send_to(agent_id, payload):
    dest = os.path.join(INBOX, f"agent_{agent_id}")
    os.makedirs(dest, exist_ok=True)
    fn = os.path.join(dest, f"coord_evt_{int(time.time())}.json")
    tmp = fn + ".tmp"
    with open(tmp, "w") as f:
        json.dump(payload, f)
    os.replace(tmp, fn)

def broadcast(payload):
    for a in range(1,16):  # Agents 1 → 15
        send_to(a, payload)

def main():
    # --- Dynamic Decision Loader (added 2025-10-24) ---
    DECISION_PATH = "/srv/manhaj2030/pmc/memory/system_decisions.json"
    decision_mode = "default"
    if os.path.exists(DECISION_PATH):
        try:
            decision = json.load(open(DECISION_PATH))
            if not decision.get("use_ping_ack", True):
                decision_mode = "IntegrationValidationOnly"
                print("[Coordinator] Mode: IntegrationValidationOnly ✅")
        except Exception as e:
            print("[Coordinator] Decision file read error:", e)
    # --------------------------------------------------
    
    pos = read_pos()
    while True:
        if not os.path.exists(EVENTS):
            time.sleep(2); continue
        with open(EVENTS, "r") as f:
            lines = f.readlines()
        if pos < len(lines):
            for i in range(pos, len(lines)):
                line = lines[i].strip()
                if not line: continue
                try:
                    evt = json.loads(line)
                except:
                    continue
                tgt = evt.get("to", "all")
                if tgt == "all" or not isinstance(tgt, (int, str)):
                    broadcast(evt)
                else:
                    # Try to convert to int, if fails, broadcast
                    try:
                        agent_id = int(tgt)
                        if 1 <= agent_id <= 15:
                            send_to(agent_id, evt)
                        else:
                            broadcast(evt)
                    except (ValueError, TypeError):
                        broadcast(evt)
            pos = len(lines)
            write_pos(pos)
        time.sleep(1)

if __name__ == "__main__":
    main()
