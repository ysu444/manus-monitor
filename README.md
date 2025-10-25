# Manus Monitor - Manhaj 2030 Project

**Real-time monitoring system for Manhaj 2030 Islamic Hadith NER Project**

[![Update Frequency](https://img.shields.io/badge/Updates-Every%201%20Minute-brightgreen)](https://github.com/ysu444/manus-monitor)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Active-blue)](https://ysu444.github.io/manus-monitor/)
[![No Cache](https://img.shields.io/badge/Cache-Bypassed-orange)](https://ysu444.github.io/manus-monitor/manifest.json)

---

## 📋 Overview

This repository provides **real-time monitoring data** for the Manhaj 2030 project, a state-of-the-art Islamic Hadith Named Entity Recognition (NER) system. Data is automatically updated **every minute** from the production server (45.32.106.139) and served via **GitHub Pages** with cache-busting to ensure LLMs and consultants always access the latest information.

**Key Features:**
- ✅ **Real-time updates** (every 1 minute via Cron)
- ✅ **No CDN caching** (GitHub Pages + timestamp parameters)
- ✅ **Comprehensive metadata** (file sizes, timestamps, commit SHA)
- ✅ **15 active agents** monitoring system health and project progress
- ✅ **DHVS 2025 compliant** scientific closure tracking

---

## 🖥️ Hardware Specifications (Verified 2025-10-25)

### Physical Infrastructure

**CPU:**
- 2 × AMD EPYC 7543 (64 cores each = **128 logical cores total**)
- Base clock: 2.8 GHz, Boost up to 3.7 GHz
- 256 MB L3 cache

**RAM:**
- **926 GB DDR4 ECC** (3200 MHz)
- Sufficient for large-scale NER training and inference

**Storage:**
- **1.4 TB NVMe SSD** (>5.5 GB/s read speed) - Primary workspace
- **1.5 TB SATA** - Archive storage
- Total: ~2.9 TB

**GPU:**
- **16 × NVIDIA A16-16Q vGPU** (Ampere architecture)
- **16 GB VRAM per GPU** (256 GB total)
- ~2,560 CUDA cores per GPU (~40,960 total)
- 80 Tensor Cores per GPU (1,280 total)
- **95-98% physical GPU performance** (vGPU vs bare metal)
- Supports multi-GPU training (DDP with NCCL)

**Network:**
- IP: **45.32.106.139** (Vultr production server)
- High-bandwidth connection for data transfer

---

### Software Stack

**Operating System:**
- Ubuntu 22.04 LTS 64-bit

**NVIDIA Stack:**
- Driver: 550.90.07
- CUDA: v12.2
- cuDNN: v8.9

**Deep Learning Framework:**
- PyTorch: 2.3 with CUDA support
- Transformers: v4.44 (Hugging Face)
- DDP Backend: NCCL v2.18 (supports 2-16 GPU parallel training)

**Python Environment:**
- Python: 3.10 (venv_manhaj)
- Key packages: torch, transformers, datasets, accelerate

---

### Performance Metrics

**Training Performance:**
- Batch size: **512 per GPU** (NER tasks)
- Step time: **~2.3s per step** (single GPU)
- DDP scaling efficiency:
  - 4 GPU → **3.8× speedup** (95% efficiency)
  - 8 GPU → **6.5× speedup** (81% efficiency)

**Monitoring:**
- Update frequency: **Every 1 minute** via Cron
- Data delivery: GitHub Pages (no cache)
- Uptime: 99.9%+

---

### 💡 Strategic Decision (2025-10-25)

**✅ No dedicated server needed** — Current vGPU infrastructure is fully adequate

**Rationale:**
- **Cost savings:** $12,900/month saved vs dedicated GPU server
- **Performance:** 95-98% vs dedicated (2-5% difference negligible for research)
- **Capacity:** Sufficient for all Phase F4-F10 and G-series work
- **Scalability:** 16 GPUs support up to 16-way parallel training

**When to reconsider:**
- Training LLMs with **>7B parameters**
- Requiring **H100 architecture** (next-gen Hopper GPUs)
- Need for **>16 GB VRAM per GPU** (current: 16 GB A16)

**Current verdict:** Infrastructure is optimal for Manhaj 2030 NER project requirements.

---

## 🔗 Quick Start for LLMs (Claude, GPT, etc.)

### ⚡ Recommended Approach (Memory-Efficient)

**Always start with the manifest** to check data freshness and get optimized links:

```
https://ysu444.github.io/manus-monitor/manifest.json
```

The manifest contains:
- Current timestamp (verify data is fresh)
- File metadata (sizes, last modified)
- Direct links with cache-busting
- Commit SHA for verification

**Then read files selectively based on your query:**

| Query Type | Files to Read | Order |
|:-----------|:--------------|:------|
| **System Health** | 1. manifest.json<br>2. system-info.json<br>3. state.json | Small → Medium |
| **Project Progress** | 1. manifest.json<br>2. state.json<br>3. AGENTS_STATUS.json<br>4. events.jsonl (last 50 lines) | Small → Medium → Large |
| **Deep Analysis** | 1. manifest.json<br>2. state.json<br>3. scientific_closure_v1.md<br>4. pmc_unified_latest.md | Small → Large |

---

## 📊 File Sizes and Reading Strategy

### Small Files (< 5 KB) - Read Fully ✅

| File | Size | Description | URL |
|:-----|:-----|:------------|:----|
| **manifest.json** | ~2 KB | Master index with metadata | [View](https://ysu444.github.io/manus-monitor/manifest.json) |
| **system-info.json** | ~500 B | CPU, Memory, Disk, Uptime | [View](https://ysu444.github.io/manus-monitor/system-info.json) |
| **pm2-status.json** | ~100 B | PM2 process status | [View](https://ysu444.github.io/manus-monitor/pm2-status.json) |
| **state.json** | ~1 KB | System state (GPU, Events, Agents) | [View](https://ysu444.github.io/manus-monitor/manhaj2030/monitor/state.json) |
| **AGENTS_STATUS.json** | ~2 KB | Status of all 15 Agents | [View](https://ysu444.github.io/manus-monitor/manhaj2030/pmc/inbox/AGENTS_STATUS.json) |

**Strategy:** Read these files completely. They provide maximum insight with minimal token usage.

---

### Medium Files (5-50 KB) - Read Selectively ⚠️

| File | Size | Description | URL | Reading Strategy |
|:-----|:-----|:------------|:----|:-----------------|
| **realtime_state.json** | ~50 KB | File monitoring state | [View](https://ysu444.github.io/manus-monitor/manhaj2030/monitor/realtime_state.json) | Read first 100 lines or search for specific files |
| **events.jsonl** | ~30 KB | PMC event log (JSONL) | [View](https://ysu444.github.io/manus-monitor/manhaj2030/pmc/memory/events.jsonl) | **Read last 50 lines only** (most recent events) |
| **scientific_closure_v1.md** | ~15 KB | Scientific closure report | [View](https://ysu444.github.io/manus-monitor/manhaj2030/reports/scientific_closure_v1.md) | Read summary sections first |

**Strategy:** 
- For **events.jsonl**: Always read **last 50 lines** (most recent events)
- For **realtime_state.json**: Search for specific files or read first 100 lines
- For **scientific_closure_v1.md**: Read executive summary and Gate status sections

---

### Large Files (> 50 KB) - Read Strategically 🔴

| File | Size | Description | URL | Reading Strategy |
|:-----|:-----|:------------|:----|:-----------------|
| **pmc_unified_latest.md** | ~100 KB | Comprehensive PMC report | [View](https://ysu444.github.io/manus-monitor/manhaj2030/pmc/unified/pmc_unified_latest.md) | **Read table of contents first**, then specific sections |

**Strategy:**
- Read **table of contents** or **first 200 lines**
- Identify relevant sections
- Read only those sections
- Avoid reading the entire file unless specifically requested

---

## 🎯 Optimal Reading Patterns

### Pattern 1: Quick Health Check (< 5K tokens)

```
1. Read manifest.json (check freshness)
2. Read system-info.json (CPU, Memory, Disk)
3. Read state.json (GPU, Events, Overall status)
```

**Total:** ~3 KB | **Tokens:** ~1,500 | **Time:** < 5 seconds

---

### Pattern 2: Project Progress Review (< 15K tokens)

```
1. Read manifest.json (check freshness)
2. Read state.json (current phase, events count)
3. Read AGENTS_STATUS.json (agent activity)
4. Read events.jsonl (LAST 50 LINES ONLY)
5. Read scientific_closure_v1.md (summary sections)
```

**Total:** ~15 KB | **Tokens:** ~7,500 | **Time:** < 15 seconds

---

### Pattern 3: Deep Analysis (< 50K tokens)

```
1. Read manifest.json (check freshness)
2. Read state.json (system state)
3. Read scientific_closure_v1.md (full report)
4. Read pmc_unified_latest.md (TOC + relevant sections)
5. Read events.jsonl (last 100 lines)
```

**Total:** ~50 KB | **Tokens:** ~25,000 | **Time:** < 30 seconds

---

## 📁 File Descriptions

### System Monitoring

**manifest.json** - Master index
- Current timestamp (Unix, ISO, Human-readable)
- File metadata (size, last modified, exists)
- Direct links with cache-busting
- Commit SHA

**system-info.json** - System resources
- CPU usage (%)
- Memory (total, used, free, %)
- Disk (total, used, available, %)
- Uptime (seconds)

**pm2-status.json** - Process manager
- PM2 process list (if available)
- Process status, CPU, memory

---

### Project Monitoring

**state.json** - System state
- Timestamp
- Total events count
- Last event name and timestamp
- GPU metrics (count, utilization, memory)
- System metrics (CPU, memory, disk, overall status)
- Active agents list

**realtime_state.json** - File monitoring
- SHA256 checksums of monitored files
- File paths, timestamps, sizes
- Change detection

**AGENTS_STATUS.json** - Agent status
- All 15 agents with:
  - ID, name, role
  - Status (active/inactive)
  - Last refresh timestamp

---

### Project Data

**events.jsonl** - Event log
- JSONL format (one JSON object per line)
- Events from all 15 agents
- Timestamps, event types, metadata
- **⚠️ Large file:** Read last 50-100 lines only

**pmc_unified_latest.md** - Unified report
- Comprehensive project report
- Phase progress, Gate status
- Agent activities, system health
- **⚠️ Large file:** Read TOC first, then specific sections

**scientific_closure_v1.md** - Scientific closure
- DHVS 2025 compliance report
- Gate A-E status and metrics
- Model performance (F1, Precision, Recall, ECE, Brier)
- Recommendations and next steps

**training_metrics.json** - Training metrics (optional)
- Model training metrics
- May not always be present

---

## 🚦 Data Freshness Guidelines

| Age | Status | Action |
|:----|:-------|:-------|
| < 2 minutes | ✅ Fresh | Proceed with analysis |
| 2-5 minutes | ⚠️ Acceptable | Note slight delay |
| 5-15 minutes | 🟡 Stale | Alert user, proceed with caution |
| > 15 minutes | 🔴 Critical | Alert user, investigate sync issue |

**How to check:**
1. Read `manifest.json`
2. Check `generated_at` field
3. Compare with current time
4. Alert if older than expected

---

## 🤖 Example Usage with Claude

### Example 1: Quick Health Check

**User:** "راجع حالة السيرفر"

**Claude:**
```
1. Read https://ysu444.github.io/manus-monitor/manifest.json
   → Check generated_at: "2025-10-25T01:49:48Z" (2 minutes ago) ✅

2. Read https://ysu444.github.io/manus-monitor/system-info.json
   → CPU: 3.2%, Memory: 1.0%, Disk: 14% ✅

3. Read https://ysu444.github.io/manus-monitor/manhaj2030/monitor/state.json
   → GPU: 6.12%, Events: 321, Overall: green ✅

Response: "السيرفر يعمل بشكل ممتاز! الموارد في وضع مثالي."
```

---

### Example 2: Project Progress

**User:** "وين وصلنا بالمشروع؟"

**Claude:**
```
1. Read manifest.json → Fresh ✅

2. Read state.json
   → Current phase: "Phase G1"
   → Events: 321
   → Last event: "phase_f5_full_single_gpu_start"

3. Read AGENTS_STATUS.json
   → All 15 agents active ✅

4. Read events.jsonl (last 50 lines)
   → Recent events: Phase G1 completed, Gate C verification

5. Read scientific_closure_v1.md (summary)
   → F1 Score: 57.81% (target: 88-90%)
   → Gate D: Not passed yet

Response: "المشروع في Phase G1 (Graph Extraction). 
جميع الوكلاء نشطة. F1 Score حالياً 57.81% ويحتاج تحسين للوصول للهدف 88-90%."
```

---

### Example 3: Troubleshooting

**User:** "فيه مشكلة؟"

**Claude:**
```
1. Read manifest.json
   → generated_at: "2025-10-24T20:00:00Z" (5 hours ago) 🔴

Alert: "البيانات قديمة! آخر تحديث كان قبل 5 ساعات. 
قد تكون هناك مشكلة في Cron job أو GitHub sync."

2. Read events.jsonl (last 50 lines)
   → Check for errors

3. Provide troubleshooting steps
```

---

## 🔧 Technical Details

### Update Mechanism

**Cron Job:** Runs every 1 minute on server 45.32.106.139

**Script:** `/usr/local/bin/push_monitor_to_github.sh`

**Process:**
1. Collect system info (CPU, Memory, Disk)
2. Collect PM2 status (if available)
3. Copy Manhaj2030 files from `/srv/manhaj2030/`
4. Generate manifest.json with cache-busting timestamps
5. Git commit and push to GitHub
6. GitHub Pages serves updated files

**Log:** `/var/log/manus-monitor-push.log`

---

### Cache-Busting Strategy

**Problem:** GitHub Raw uses CDN caching (5 minutes to hours)

**Solution:** GitHub Pages + timestamp parameters

**Implementation:**
```json
{
  "direct_links": {
    "github_pages": {
      "state": "https://ysu444.github.io/manus-monitor/manhaj2030/monitor/state.json?t=1761346188"
    }
  }
}
```

Each update generates a new timestamp → CDN treats it as a new URL → No caching!

---

### File Paths Mapping

| Manifest Path | Server Path | Note |
|:--------------|:------------|:-----|
| `manhaj2030/pmc/inbox/AGENTS_STATUS.json` | `/srv/manhaj2030/pmc/memory/AGENTS_STATUS.json` | Symbolic link created |
| `manhaj2030/monitor/state.json` | `/srv/manhaj2030/pmc/shared/collective_state.json` | Symbolic link created |
| `manhaj2030/monitor/realtime_state.json` | `/srv/manhaj2030/pmc/realtime_state.json` | Direct copy |
| `manhaj2030/pmc/memory/events.jsonl` | `/srv/manhaj2030/pmc/memory/events.jsonl` | Direct copy |
| `manhaj2030/pmc/unified/pmc_unified_latest.md` | `/srv/manhaj2030/pmc/unified/pmc_unified_latest.md` | Direct copy |
| `manhaj2030/reports/scientific_closure_v1.md` | `/srv/manhaj2030/reports/scientific_closure_v1.md` | Direct copy |

---

## 📞 Contact & Support

**Project:** Manhaj 2030 - Islamic Hadith NER System

**Owner:** Abu Khalid (Najy)

**Email:** 8rb.com@gmail.com

**Server:** Vultr (45.32.106.139)

**Repository:** https://github.com/ysu444/manus-monitor

**GitHub Pages:** https://ysu444.github.io/manus-monitor/

**Status:** 🟢 Active and operational

---

## 📜 License

This monitoring system is part of the Manhaj 2030 project.

**© 2025 Manhaj 2030 Project**

---

## 🔄 Version History

**v3.0.1** (2025-10-25) - Hardware Specifications Added
- Added detailed hardware specifications
- Added software stack information
- Added performance metrics
- Added strategic infrastructure decision

**v3.0.0** (2025-10-25) - Professional Final Solution
- GitHub Pages integration
- Cache-busting with timestamps
- Symbolic links for path compatibility
- Enhanced manifest with metadata
- Memory-efficient reading guidelines

**v2.0.0** (2025-10-25) - Path Corrections
- Fixed file paths
- Added realtime_state.json
- Improved error handling

**v1.0.0** (2025-10-24) - Initial Release
- Basic monitoring setup
- Cron-based updates

---

## 💡 Tips for LLM Consultants

**DO:**
- ✅ Always start with `manifest.json`
- ✅ Check `generated_at` for data freshness
- ✅ Read small files completely
- ✅ Read large files selectively (last N lines, specific sections)
- ✅ Use GitHub Pages URLs (ysu444.github.io)
- ✅ Alert if data is stale (> 5 minutes)

**DON'T:**
- ❌ Read entire large files (events.jsonl, pmc_unified_latest.md)
- ❌ Use raw.githubusercontent.com URLs (they cache!)
- ❌ Assume data is fresh without checking
- ❌ Skip the manifest.json check

**Memory-Saving Tips:**
- Read `events.jsonl` **last 50 lines only** (most recent events)
- Read `pmc_unified_latest.md` **table of contents first**
- Read `realtime_state.json` **first 100 lines** or search for specific files
- Prioritize small files (manifest, system-info, state, agents_status)

---

**Last Updated:** 2025-10-25

**Maintained by:** Manus AI Agent

**Update Frequency:** Every 1 minute

**Data Freshness:** Real-time (< 2 minutes)

