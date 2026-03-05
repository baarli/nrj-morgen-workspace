# VEV MISSION CONTROL INTEGRATION PLAN
## Connecting All Vev Systems to Mission Control

**Date:** 2026-03-05  
**Mission Control:** https://baarli.github.io/mission-control-live/  
**Goal:** Full integration of all Vev systems

---

## 🔗 SYSTEMS TO INTEGRATE

### 1. Telegram Bot (@Vev_kompis_bot)
**Current Status:** ✅ Running (systemd service)
**Integration Points:**
- Show Telegram status in Mission Control dashboard
- Display recent messages/conversations
- Show user profile info
- Control bot (start/stop/restart) from dashboard
- View auto-responder logs

**API Endpoint Needed:**
```javascript
// GET /api/telegram/status
{
  "bot_username": "@Vev_kompis_bot",
  "status": "online",
  "total_messages": 152,
  "last_message": "2026-03-05 20:30",
  "auto_responder": "running",
  "voice_messages_sent": 45
}
```

---

### 2. Learning Loop System
**Current Status:** ✅ Running (file watcher + auto-sync)
**Integration Points:**
- Show learning database stats
- Display recent learnings
- Show pattern analysis results
- View auto-sync activity
- Display documentation update status

**API Endpoint Needed:**
```javascript
// GET /api/learning/status
{
  "total_learnings": 47,
  "total_sessions": 23,
  "last_sync": "2026-03-05 20:45",
  "file_watcher": "running",
  "patterns_detected": 5
}
```

---

### 3. Health Monitor
**Current Status:** ✅ Running (cron every 5 min)
**Integration Points:**
- Real-time system health dashboard
- Show all service statuses
- Display disk/memory usage
- Show GitHub connectivity
- Alert history

**API Endpoint Needed:**
```javascript
// GET /api/health/status
{
  "overall_status": "healthy",
  "services": {
    "telegram_responder": "running",
    "file_watcher": "running",
    "health_monitor": "running"
  },
  "disk_usage": "73%",
  "memory_usage": "45%",
  "github_connected": true,
  "last_check": "2026-03-05 21:15"
}
```

---

### 4. Sub-Agent System
**Current Status:** ✅ Implemented (Python multiprocessing)
**Integration Points:**
- Show active background tasks
- Display task progress in real-time
- Allow spawning new tasks from dashboard
- View task history/results
- Interrupt tasks

**API Endpoint Needed:**
```javascript
// GET /api/subagents/status
{
  "active_tasks": [
    {
      "task_id": "abc123",
      "type": "research",
      "status": "running",
      "progress": 45,
      "started": "2026-03-05 21:00"
    }
  ],
  "completed_tasks": 12
}
```

---

### 5. Nightly Backup System
**Current Status:** ✅ Running (cron at 03:00)
**Integration Points:**
- Show backup status
- Display backup history
- Show GitHub sync status
- Allow manual backup trigger
- View backup logs

**API Endpoint Needed:**
```javascript
// GET /api/backup/status
{
  "last_backup": "2026-03-05 03:00",
  "status": "success",
  "commits_pushed": 3,
  "next_backup": "2026-03-06 03:00",
  "github_repo": "baarli/nrj-morgen-workspace"
}
```

---

### 6. Morning Routine System
**Current Status:** ✅ Implemented
**Integration Points:**
- Show next scheduled run
- Display saksliste status
- View morning routine logs
- Manual trigger button
- Show news sources configured

**API Endpoint Needed:**
```javascript
// GET /api/morning-routine/status
{
  "next_run": "2026-03-06 06:00",
  "last_run": "2026-03-05 06:00",
  "stories_found": 15,
  "stories_added": 10,
  "sources": ["VG", "Dagbladet", "NRK"]
}
```

---

### 7. Voice Chat System
**Current Status:** ✅ Running (Mission Control + Telegram)
**Integration Points:**
- Already integrated! Just needs status display
- Show voice chat usage stats
- Display TTS configuration
- View voice message history

---

## 🛠️ IMPLEMENTATION APPROACH

### Option 1: Python API Server (Recommended)
Create `vev-mission-control-api.py`:
- Flask/FastAPI server
- Exposes all system statuses
- Runs as systemd service
- Mission Control fetches data via HTTP

### Option 2: Supabase Edge Functions
Create edge functions in Supabase:
- Each function queries a system
- Mission Control calls Supabase directly
- No separate server needed

### Option 3: File-Based (Simplest)
Status files written to disk:
- Each system writes JSON status
- Mission Control reads files
- No server needed

---

## 📋 RECOMMENDED: Hybrid Approach

### Real-time Data (via API Server):
- Telegram status
- Sub-agent tasks
- Health monitor
- System controls

### Periodic Data (via Supabase):
- Learning stats
- Backup history
- Morning routine logs
- Historical data

### Static Data (via files):
- Configuration
- Documentation links
- Version info

---

## 🚀 IMPLEMENTATION STEPS

### Phase 1: API Server (1-2 hours)
- [ ] Create vev-mission-control-api.py
- [ ] Implement /status endpoint for all systems
- [ ] Run as systemd service
- [ ] Test from Mission Control

### Phase 2: Dashboard Widgets (2-3 hours)
- [ ] System Status Widget
- [ ] Telegram Activity Widget
- [ ] Learning Progress Widget
- [ ] Sub-Agent Tasks Widget
- [ ] Health Monitor Widget

### Phase 3: Controls (1-2 hours)
- [ ] Start/Stop services
- [ ] Trigger manual backup
- [ ] Spawn sub-agent tasks
- [ ] Run morning routine

### Phase 4: Notifications (1 hour)
- [ ] Alert on system failures
- [ ] Notify on task completion
- [ ] Show backup success/failure

---

## 🎨 DASHBOARD LAYOUT

```
┌─────────────────────────────────────────────────────────────┐
│  MISSION CONTROL | VEV SYSTEM DASHBOARD                     │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ 🟢 HEALTH   │  │ 📱 TELEGRAM │  │ 🧠 LEARNING │         │
│  │ All Good    │  │ 152 msgs    │  │ 47 items    │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
├─────────────────────────────────────────────────────────────┤
│  ACTIVE TASKS                    BACKGROUND WORKERS         │
│  ┌─────────────────────────┐    ┌─────────────────────────┐ │
│  │ Research: 45%           │    │ File Watcher: Running   │ │
│  │ Analysis: 100% ✅       │    │ Auto-Sync: Active       │ │
│  │ Coding: Waiting...      │    │ Health Monitor: OK      │ │
│  └─────────────────────────┘    └─────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  QUICK ACTIONS                                              │
│  [Run Morning Routine] [Trigger Backup] [Spawn Task]        │
└─────────────────────────────────────────────────────────────┘
```

---

## ⏱️ TIME ESTIMATE

| Phase | Time | Priority |
|-------|------|----------|
| API Server | 2h | P1 |
| Dashboard Widgets | 3h | P1 |
| Controls | 2h | P2 |
| Notifications | 1h | P2 |
| **Total** | **8h** | |

---

**This will create a unified command center for all Vev systems!**
