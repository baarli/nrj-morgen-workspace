# VEV MASTER SYSTEM DOCUMENTATION
## Complete Overview - All Systems Connected

**Version:** 3.0  
**Date:** 2026-03-06  
**Status:** ✅ PRODUCTION READY

---

## 📚 DOKUMENTASJONSHIERARKI

```
PRINCIPLES.md (Master Principles)
    ↓
AGENTS.md (This File - System Overview)
    ↓
SYSTEM_ARCHITECTURE.md (Technical Architecture)
    ↓
MEMORY.md (Learning & Memory)
    ↓
TOOLS.md (Tools & Scripts)
    ↓
SKILL.md (Individual Skills)
```

---

## 🤖 VEV - SYSTEM IDENTITET

### Core Identity
| Attribute | Value |
|-----------|-------|
| **Name** | Vev |
| **Avatar** | `brain/vev-avatar.jpg` |
| **Emoji** | 🤖 |
| **Description** | AI-assistent with personality, memory, and voice |
| **Created** | 2026-03-05 |
| **Creator** | User |

### Avatar Design
- Cute robot with glowing turquoise eyes
- Halo (angelic AI)
- Energy core (heart)
- Colors: Blue-purple gradient

---

## 🎯 SYSTEM LAYERS (Bottom to Top)

### Layer 1: Infrastructure
- Linux Server (Ubuntu)
- Node.js / Python
- GitHub Repositories
- Supabase Database
- GitHub Pages Hosting

### Layer 2: API & Models
- **Primary:** kimi-coding/k2p5
- **Fallback:** OpenRouter (gpt-4o, claude-3-opus, mistral-large)
- **Auto-Switch:** FreeRide system
- **API Key:** `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`

### Layer 3: Autonomous Core
- NEVER_ASK: True
- DEFAULT_ACTION: CONTINUE
- AUTO_RECOVER: Enabled
- NO_IDLE: 10 min threshold

### Layer 4: Communication
- Telegram Bot (@Vev_kompis_bot)
- Mission Control (Web UI)
- Web Chat
- Voice Messages

### Layer 5: Data & Memory
- Supabase (PostgreSQL)
- Local JSON Files
- GitHub Backup
- Memory System

### Layer 6: Skills & Tools
- Content Aggregator
- Podcast Manager
- Radio Theory Benchmark
- NRJ Dashboard System
- Calendar, Weather, GitHub

### Layer 7: User Interface
- Mission Control Dashboard
- Saksliste (Agenda)
- Kanban Board
- Voice Chat Interface

---

## 🔄 DATA FLOW

User Input → [Telegram/Mission Control/Web] → OpenClaw Gateway → [Pre-flight] → Vev Processing → [API] → Response → [Memory] → Output → [Background Tasks]

---

## 📊 SYSTEM STATUS

| Component | Status |
|-----------|--------|
| Telegram Bot | ✅ Online |
| Mission Control | ✅ Online |
| Autonomous Executor | ✅ Running |
| FreeRide Fallback | ✅ Active |
| GitHub Backup | ✅ Scheduled |
| Health Monitor | ✅ Running |

---

## 🚀 QUICK ACTIONS

```bash
# Start all systems
bash scripts/vev-master-activator.sh

# Check status
openclaw status

# Send Telegram message
bash scripts/telegram-send.sh "message"

# Deploy Mission Control
bash scripts/deploy-mission-control.sh

# Run morning routine
bash scripts/vev-morning-routine.sh
```

---

## 📁 KEY FILES

| File | Purpose |
|------|---------|
| `AGENTS.md` | This file - system overview |
| `SYSTEM_ARCHITECTURE.md` | Technical details |
| `MEMORY.md` | Long-term memory |
| `PRINCIPLES.md` | Core principles |
| `brain/config/autonomous-config.json` | Autonomous settings |
| `brain/config/openrouter-fallback.md` | API fallback config |

---

**Last Updated:** 2026-03-06  
**Next Review:** Continuous
