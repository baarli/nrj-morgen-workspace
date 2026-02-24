#!/bin/bash
# User Notification System for Autonomous Tasks
# Sends notification when starting new tasks

LOG_FILE="/var/log/autonomous-mission-control.log"
USER_EMAIL="niklasbaarli@gmail.com"
WORKSPACE="/root/.openclaw/workspace"

# Function to send notification
notify_user() {
    local task_name="$1"
    local task_description="$2"
    local priority="$3"
    local estimated_time="$4"
    
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local oslo_time=$(TZ=Europe/Oslo date '+%H:%M')
    
    # Log the notification
    echo "[$timestamp] 🔔 NOTIFICATION: Starting new task - $task_name" | tee -a "$LOG_FILE"
    
    # Create notification message
    local message="🚀 Ny Oppgave Startet - BaarliClaw

Hei! Jeg har nettopp startet på en ny oppgave:

📋 OPPGAVE: $task_name
📝 BESKRIVELSE: $task_description
⚡ PRIORITET: $priority
⏱️ ESTIMERT TID: $estimated_time
🕐 STARTET: $oslo_time (Oslo-tid)

Du vil få en ny melding når oppgaven er fullført.

---
Dette er en automatisk melding fra Mission Control.
https://creative-muffin-dcf3a0.netlify.app"

    # Send notification via available channels
    # 1. Log to file
    echo "$message" >> "$WORKSPACE/.config/notifications.log"
    
    # 2. Create notification marker
    echo "$timestamp|$task_name|$priority|$estimated_time" >> "$WORKSPACE/.config/active-tasks.log"
    
    # 3. Print to console (for OpenClaw to relay)
    echo "NOTIFICATION_TO_USER:"
    echo "$message"
    echo "END_NOTIFICATION"
}

# Function to notify task completion
notify_completion() {
    local task_name="$1"
    local result="$2"
    local duration="$3"
    
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local oslo_time=$(TZ=Europe/Oslo date '+%H:%M')
    
    echo "[$timestamp] ✅ NOTIFICATION: Task completed - $task_name" | tee -a "$LOG_FILE"
    
    local message="✅ Oppgave Fullført - BaarliClaw

Hei! Jeg har nettopp fullført en oppgave:

📋 OPPGAVE: $task_name
✅ RESULTAT: $result
⏱️ VARIGHET: $duration
🕐 FULLFØRT: $oslo_time (Oslo-tid)

Sjekk Mission Control for detaljer:
https://creative-muffin-dcf3a0.netlify.app

---
Dette er en automatisk melding."

    echo "NOTIFICATION_TO_USER:"
    echo "$message"
    echo "END_NOTIFICATION"
}

# Function to notify about issues
notify_issue() {
    local issue_type="$1"
    local description="$2"
    local severity="$3"
    
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    echo "[$timestamp] ⚠️ NOTIFICATION: Issue detected - $issue_type" | tee -a "$LOG_FILE"
    
    local message="⚠️ Problem Oppdaget - BaarliClaw

Hei! Jeg har oppdaget et problem som trenger oppmerksomhet:

🔴 TYPE: $issue_type
📝 BESKRIVELSE: $description
⚡ ALVORLIGHET: $severity
🕐 TID: $(TZ=Europe/Oslo date '+%H:%M') (Oslo-tid)

Jeg jobber med å løse dette automatisk, men du kan følge med på:
https://creative-muffin-dcf3a0.netlify.app

---
Dette er en automatisk melding."

    echo "NOTIFICATION_TO_USER:"
    echo "$message"
    echo "END_NOTIFICATION"
}

# Main execution
if [ "$1" == "start" ]; then
    notify_user "$2" "$3" "$4" "$5"
elif [ "$1" == "complete" ]; then
    notify_completion "$2" "$3" "$4"
elif [ "$1" == "issue" ]; then
    notify_issue "$2" "$3" "$4"
fi
