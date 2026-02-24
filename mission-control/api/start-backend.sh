#!/bin/bash
# Mission Control Backend Startup Script
# Kjøres ved boot for å starte API server

WORKSPACE="/root/.openclaw/workspace"
API_SCRIPT="$WORKSPACE/mission-control/api/backend-simple.py"
PID_FILE="$WORKSPACE/mission-control/.api.pid"
LOG_FILE="/tmp/mission-control-api.log"

# Sjekk om allerede kjører
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "Backend already running (PID: $PID)"
        exit 0
    fi
fi

# Start backend
echo "Starting Mission Control Backend..."
nohup python3 "$API_SCRIPT" > "$LOG_FILE" 2>&1 &
echo $! > "$PID_FILE"

sleep 2

# Verifiser at den startet
if ps -p $(cat "$PID_FILE") > /dev/null 2>&1; then
    echo "✅ Backend started successfully!"
    echo "   PID: $(cat $PID_FILE)"
    echo "   API: http://localhost:8081"
    echo "   Logs: $LOG_FILE"
else
    echo "❌ Failed to start backend"
    cat "$LOG_FILE"
    exit 1
fi
