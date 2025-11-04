#!/usr/bin/env python3
import time, json
from prometheus_client import start_http_server, Gauge

train_loss = Gauge('phase_f_train_loss', 'Training loss')
eval_loss  = Gauge('phase_f_eval_loss',  'Evaluation loss')
precision  = Gauge('phase_f_precision',  'Precision score')
recall     = Gauge('phase_f_recall',     'Recall score')
f1_score   = Gauge('phase_f_f1',         'F1 score')
neff_value = Gauge('phase_f_neff_value', 'Effective n_eff')
rho_value  = Gauge('phase_f_rho_value',  'Average correlation')
events_tot = Gauge('phase_f_events_total', 'Total Phase F events')
budget_use = Gauge('budget_usage_today', 'Current daily spend USD')
budget_warn= Gauge('budget_threshold_warn', 'Warn threshold USD')
budget_stop= Gauge('budget_threshold_stop', 'Stop threshold USD')

def read_json(path):
    try:
        with open(path,'r',encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

def update_from_files():
    metrics = read_json('/srv/manhaj2030/reports/phase_f_metrics.json')
    budget  = read_json('/srv/manhaj2030/pmc/memory/budget_guard.json')
    if metrics:
        train_loss.set(metrics.get('train_loss', 0))
        eval_loss.set(metrics.get('eval_loss', 0))
        precision.set(metrics.get('precision', 0))
        recall.set(metrics.get('recall', 0))
        f1_score.set(metrics.get('f1', 0))
        neff_value.set(metrics.get('n_eff', 0))
        rho_value.set(metrics.get('rho', 0))
        events_tot.set(metrics.get('events', 0))
    if budget:
        budget_use.set(budget.get('usage_today', 0))
        budget_warn.set(budget.get('warn_threshold', 900))
        budget_stop.set(budget.get('stop_threshold', 1000))

if __name__ == "__main__":
    start_http_server(9200)
    print("✅ Phase F Metrics Exporter running on port 9200")
    while True:
        update_from_files()
        time.sleep(30)
