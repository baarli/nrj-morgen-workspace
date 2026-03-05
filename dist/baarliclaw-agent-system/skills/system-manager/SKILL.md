---
name: system-manager
description: Manage and monitor all automated systems. Use when user asks about system status, cron jobs, automation health, or wants to add new automated tasks. Provides overview of all running automations and their status.
---

# System Manager

## Overview
This skill manages all automated systems and provides status overview.

## Commands

### Check System Status
```bash
cd /root/.openclaw/workspace/scripts
bash agent-dashboard.sh
```

### List All Cron Jobs
```bash
openclaw cron list
```

### Run ML Analysis
```bash
cd /root/.openclaw/workspace/scripts
bash ml-learning-analyzer.sh
```

### View Recent Logs
```bash
tail -50 /root/.openclaw/workspace/.auto-exec-log
tail -50 /root/.openclaw/workspace/.session-end-log
```

## Automated Systems

### 1. Pre-Flight System
- **Script:** auto-exec-enforcer.sh
- **Trigger:** Manual (must run at start)
- **Purpose:** Ensures full context before work

### 2. Learning Capture
- **Script:** session-end-handler.sh
- **Trigger:** Cron (hourly) + Manual
- **Purpose:** Documents all learnings

### 3. NRJ Dashboard Updates
- **Script:** update_nrj_dashboard.py
- **Trigger:** Cron (Wednesdays 14:00)
- **Purpose:** Auto-updates radio/podcast stats

### 4. Sakslista Morning Routine
- **Script:** integrated-morning-routine.sh
- **Trigger:** Cron (Mon-Fri 06:00)
- **Purpose:** Fetches daily news

### 5. Podkast Clip Download
- **Script:** daily-podcast-clips.sh
- **Trigger:** Cron (Daily 07:00)
- **Purpose:** Downloads and clips podcast episodes

## Health Checks

### Verify All Systems
```bash
echo "Checking all automated systems..."

# Check scripts
for script in auto-exec-enforcer.sh memory-validator.sh session-end-handler.sh; do
    if [ -f "/root/.openclaw/workspace/scripts/$script" ]; then
        echo "✅ $script: OK"
    else
        echo "❌ $script: MISSING"
    fi
done

# Check cron jobs
openclaw cron list

# Check skills
ls /root/.openclaw/workspace/skills/*.skill 2>/dev/null | wc -l | xargs echo "Skills available:"
```

## Adding New Automation

1. Create script in `/root/.openclaw/workspace/scripts/`
2. Test script manually
3. Add cron job via `openclaw cron add`
4. Document in MEMORY.md
5. Update this skill

## Troubleshooting

### If auto-exec-enforcer fails:
```bash
# Run manually
bash /root/.openclaw/workspace/scripts/mandatory-preflight.sh
bash /root/.openclaw/workspace/scripts/memory-validator.sh
```

### If cron jobs not running:
```bash
# Check cron status
openclaw cron status

# List all jobs
openclaw cron list
```

### If skills not loading:
```bash
# Verify skill files
ls -la /root/.openclaw/workspace/skills/
ls -la /usr/lib/node_modules/openclaw/skills/custom/
```
