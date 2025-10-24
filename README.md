# 📡 Manus Monitor — Server State & Manhaj 2030

مرآة عامة لحالة السيرفر **45.32.106.139** ومخرجات مشروع **منهج 2030**.  
يُحدّث تلقائياً كل 5 دقائق بواسطة Manus Agents.

---

## 🔗 الروابط المباشرة (للقراءة من Claude أو أي AI)

### 📋 نقطة البداية
**Manifest** (فهرس شامل لكل الملفات):
```
https://raw.githubusercontent.com/ysu444/manus-monitor/main/manifest.json
```

### 🖥️ معلومات السيرفر
```
https://raw.githubusercontent.com/ysu444/manus-monitor/main/system-info.json
https://raw.githubusercontent.com/ysu444/manus-monitor/main/pm2-status.json
```

### 📚 ملفات منهج 2030
```
https://raw.githubusercontent.com/ysu444/manus-monitor/main/manhaj2030/monitor/state.json
https://raw.githubusercontent.com/ysu444/manus-monitor/main/manhaj2030/pmc/inbox/AGENTS_STATUS.json
https://raw.githubusercontent.com/ysu444/manus-monitor/main/manhaj2030/pmc/memory/events.jsonl
https://raw.githubusercontent.com/ysu444/manus-monitor/main/manhaj2030/pmc/unified/pmc_unified_latest.md
https://raw.githubusercontent.com/ysu444/manus-monitor/main/manhaj2030/reports/scientific_closure_status.json
https://raw.githubusercontent.com/ysu444/manus-monitor/main/manhaj2030/reports/training_metrics.json
```

---

## 💬 كيف تستخدم مع Claude

### طريقة سريعة (Manifest + State):
```
مرحباً Claude، راجع حالة السيرفر:

https://raw.githubusercontent.com/ysu444/manus-monitor/main/manifest.json
https://raw.githubusercontent.com/ysu444/manus-monitor/main/manhaj2030/monitor/state.json

ما هي الملاحظات؟
```

### طريقة شاملة (كل الملفات):
```
مرحباً Claude، أريد تحليل شامل:

معلومات النظام:
https://raw.githubusercontent.com/ysu444/manus-monitor/main/system-info.json

حالة PM2:
https://raw.githubusercontent.com/ysu444/manus-monitor/main/pm2-status.json

حالة الوكلاء:
https://raw.githubusercontent.com/ysu444/manus-monitor/main/manhaj2030/pmc/inbox/AGENTS_STATUS.json

حالة المراقبة:
https://raw.githubusercontent.com/ysu444/manus-monitor/main/manhaj2030/monitor/state.json

أحداث PMC:
https://raw.githubusercontent.com/ysu444/manus-monitor/main/manhaj2030/pmc/memory/events.jsonl

ما هي التوصيات؟
```

### طريقة مخصصة (حسب الحاجة):
```
مرحباً Claude، أريد مراجعة الإغلاق العلمي:

https://raw.githubusercontent.com/ysu444/manus-monitor/main/manhaj2030/reports/scientific_closure_status.json

ومقاييس التدريب:
https://raw.githubusercontent.com/ysu444/manus-monitor/main/manhaj2030/reports/training_metrics.json

ما هي الملاحظات؟
```

---

## 📊 الملفات المتاحة

| الملف | الوصف | التحديث |
|:--|:--|:--:|
| `manifest.json` | فهرس شامل لكل الملفات | 5 دقائق |
| `system-info.json` | معلومات النظام (CPU, Memory, Disk) | 5 دقائق |
| `pm2-status.json` | حالة تطبيقات PM2 | 5 دقائق |
| `manhaj2030/monitor/state.json` | حالة المراقبة الرئيسية | 1 دقيقة |
| `manhaj2030/pmc/inbox/AGENTS_STATUS.json` | حالة الوكلاء 1-15 | 5 دقائق |
| `manhaj2030/pmc/memory/events.jsonl` | سجل الأحداث | 2 دقائق |
| `manhaj2030/pmc/unified/pmc_unified_latest.md` | التقرير الموحد | 5 دقائق |
| `manhaj2030/reports/scientific_closure_status.json` | حالة الإغلاق العلمي | 15 دقيقة |
| `manhaj2030/reports/training_metrics.json` | مقاييس التدريب | 10 دقائق |

---

## 🔄 التحديث التلقائي

يتم تحديث الملفات تلقائياً بواسطة:
```bash
/usr/local/bin/push_monitor_to_github.sh
```

يعمل كل 5 دقائق عبر Cron:
```cron
*/5 * * * * /usr/local/bin/push_monitor_to_github.sh >> /var/log/manus-monitor-push.log 2>&1
```

---

## 🧩 الأدوار

| الكيان | الدور |
|:--|:--|
| **Najy** | مدير التنفيذ على السيرفر |
| **Manus Agents (1-15)** | وكلاء تشغيليون متخصصون |
| **Claude** | مستشار تحليلي (قراءة فقط) |
| **Abu Khalid** | المشرف العام |

---

## 🔐 سياسة الاستخدام

- **قراءة فقط** (Read-Only)
- **لا تخزين** للمفاتيح أو التوكنات
- **البيانات قديمة** إن تجاوزت 15 دقيقة
- **للاستشارة والتحليل** فقط

---

## 📞 المعلومات

**السيرفر:** 45.32.106.139  
**المشروع:** منهج 2030  
**المستودع:** https://github.com/ysu444/manus-monitor  
**المشرف:** Abu Khalid

---

**© 2025 Manhaj 2030 Project**

