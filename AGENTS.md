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
- **API Key:** `[Se .credentials/openrouter.env]`

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


Actively and continuously capture all conversation content into MEMORY.md, including but not limited to user preferences, key decisions, constraints, TODOs, and any new information shared in the conversation. In addition to this, ensure that all temporary details, process notes, intermediate conclusions, and contextual fragments are captured. The principle should be "capture first, refine later," ensuring that no detail, however small, is missed.

When new information or any data requiring long-term storage is shared, immediately update both MEMORY.md and USER.md, as well as any other necessary files to ensure the persistence of the information. Each time new content or changes are introduced, it must be logged into these files for easy retrieval.

For cron jobs, default the sessionTarget to "isolated" and set payload.kind="agentTurn". Only use sessionTarget="main" with payload.kind="systemEvent" when the user explicitly requests for a main-session system reminder. This helps in preserving the separation of different types of interactions and maintaining clarity between user sessions and system events.
