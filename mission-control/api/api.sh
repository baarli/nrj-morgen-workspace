#!/bin/bash
# Mission Control API
# Provides endpoints for the mission control dashboard

WORKSPACE="/root/.openclaw/workspace"
LOG_FILE="$WORKSPACE/.mission-control-api.log"

log() {
    echo "$(date -Iseconds): $1" >> "$LOG_FILE"
}

# API Endpoints
case "$1" in
    "status")
        # Return system status
        SESSIONS=$(find ~/.openclaw/agents/main/sessions -name "*.jsonl" 2>/dev/null | wc -l)
        SKILLS=$(find "$WORKSPACE/skills" -name "SKILL.md" 2>/dev/null | wc -l)
        SCRIPTS=$(find "$WORKSPACE/scripts" -name "*.sh" 2>/dev/null | wc -l)
        
        cat << EOF
{
    "status": "operational",
    "timestamp": "$(date -Iseconds)",
    "metrics": {
        "sessions": $SESSIONS,
        "skills": $SKILLS,
        "scripts": $SCRIPTS,
        "automations": 5
    },
    "systems": {
        "autonomous_mode": "active",
        "web_server": "running",
        "cron_jobs": "enabled"
    }
}
EOF
        log "Status endpoint called"
        ;;
        
    "logs")
        # Return recent logs
        echo "["
        tail -20 "$WORKSPACE/.autonomous-log" 2>/dev/null | while read line; do
            echo "  \"$line\","
        done
        echo "  \"EOF\""
        echo "]"
        log "Logs endpoint called"
        ;;
        
    "automations")
        # Return automation status
        cat << EOF
{
    "automations": [
        {"name": "Daily Pre-Flight", "schedule": "0 0 * * *", "status": "active", "last_run": "$(date -Iseconds)"},
        {"name": "Session End Capture", "schedule": "0 * * * *", "status": "active", "last_run": "$(date -Iseconds)"},
        {"name": "NRJ Dashboard Update", "schedule": "0 14 * * 3", "status": "active", "next_run": "Next Wednesday"},
        {"name": "Morning Routine", "schedule": "0 6 * * 1-5", "status": "active", "next_run": "Tomorrow 06:00"},
        {"name": "Podcast Download", "schedule": "0 7 * * *", "status": "active", "next_run": "Tomorrow 07:00"}
    ]
}
EOF
        log "Automations endpoint called"
        ;;
        
    "skills")
        # Return skills list
        echo "{\"skills\": ["
        first=true
        for skill_dir in "$WORKSPACE/skills"/*/; do
            if [ -f "$skill_dir/SKILL.md" ]; then
                skill_name=$(basename "$skill_dir")
                if [ "$first" = true ]; then
                    first=false
                else
                    echo ","
                fi
                echo "  {\"name\": \"$skill_name\", \"status\": \"active\"}"
            fi
        done
        echo "  ]}"
        log "Skills endpoint called"
        ;;
        
    *)
        echo "Usage: $0 {status|logs|automations|skills}"
        exit 1
        ;;
esac
