#!/bin/bash
# Simple API for external access to agent status
# Returns JSON with system status

WORKSPACE="/root/.openclaw/workspace"

echo "Content-Type: application/json"
echo ""

# Gather data
SESSIONS=$(find ~/.openclaw/agents/main/sessions -name "*.jsonl" 2>/dev/null | wc -l)
LOGS=$(find "$WORKSPACE/memory" -name "*.md" 2>/dev/null | wc -l)
SKILLS=$(find "$WORKSPACE/skills" -name "SKILL.md" 2>/dev/null | wc -l)
SCRIPTS=$(find "$WORKSPACE/scripts" -name "*.sh" 2>/dev/null | wc -l)

cat << EOF
{
  "status": "operational",
  "timestamp": "$(date -Iseconds)",
  "agent": "BaarliClaw",
  "version": "2.0",
  "metrics": {
    "sessions": $SESSIONS,
    "learning_logs": $LOGS,
    "skills": $SKILLS,
    "scripts": $SCRIPTS
  },
  "systems": {
    "pre_flight": "enabled",
    "learning_capture": "enabled",
    "auto_updates": "enabled",
    "self_improvement": "active"
  },
  "automations": [
    {"name": "Daily Pre-Flight", "schedule": "0 0 * * *", "status": "active"},
    {"name": "Session End Capture", "schedule": "0 * * * *", "status": "active"},
    {"name": "NRJ Dashboard Update", "schedule": "0 14 * * 3", "status": "active"},
    {"name": "Morning Routine", "schedule": "0 6 * * 1-5", "status": "active"},
    {"name": "Podcast Download", "schedule": "0 7 * * *", "status": "active"}
  ]
}
EOF
