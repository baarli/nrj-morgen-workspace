#!/bin/bash
# Mission Control Server
# Hosts the mission control dashboard with API

WORKSPACE="/root/.openclaw/workspace"
MISSION_CONTROL="$WORKSPACE/mission-control"
PID_FILE="$WORKSPACE/.mission-control-server.pid"
PORT=3000

start() {
    echo "Starting Mission Control Server on port $PORT..."
    
    # Check if already running
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            echo "Server already running (PID: $PID)"
            return 0
        fi
    fi
    
    # Start Python HTTP server in background
    cd "$MISSION_CONTROL/public"
    nohup python3 -m http.server $PORT > /dev/null 2>&1 &
echo $! > "$PID_FILE"
    
    echo "✅ Mission Control Server started!"
    echo "📍 URL: http://localhost:$PORT"
    echo "🔒 Password: kloakontroll2026"
    echo ""
    echo "To stop: $0 stop"
}

stop() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            kill "$PID"
            rm "$PID_FILE"
            echo "✅ Mission Control Server stopped"
        else
            echo "Server not running"
            rm "$PID_FILE"
        fi
    else
        echo "Server not running"
    fi
}

status() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            echo "✅ Mission Control Server is running (PID: $PID)"
            echo "📍 URL: http://localhost:$PORT"
        else
            echo "❌ Server not running (stale PID file)"
            rm "$PID_FILE"
        fi
    else
        echo "❌ Server not running"
    fi
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    status)
        status
        ;;
    restart)
        stop
        sleep 1
        start
        ;;
    *)
        echo "Usage: $0 {start|stop|status|restart}"
        exit 1
        ;;
esac
