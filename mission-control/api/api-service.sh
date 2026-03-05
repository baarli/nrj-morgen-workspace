#!/bin/bash
# Mission Control API Service Manager
# Usage: ./api-service.sh {start|stop|restart|status|logs}

WORKSPACE="/root/.openclaw/workspace"
API_DIR="$WORKSPACE/mission-control/api"
PIDFILE="/tmp/mission-control-api.pid"
LOGFILE="$WORKSPACE/logs/api-service.log"

cd "$API_DIR" || exit 1

start() {
    if [ -f "$PIDFILE" ] && kill -0 $(cat "$PIDFILE") 2>/dev/null; then
        echo "API is already running (PID: $(cat $PIDFILE))"
        return 1
    fi
    
    echo "Starting Mission Control API..."
    nohup python3 total-control-api.py >> "$LOGFILE" 2>&1 &
    echo $! > "$PIDFILE"
    echo "API started with PID: $(cat $PIDFILE)"
    echo "HTTP: http://localhost:8081"
    echo "WebSocket: ws://localhost:8082"
}

stop() {
    if [ ! -f "$PIDFILE" ]; then
        echo "API is not running"
        return 1
    fi
    
    echo "Stopping Mission Control API..."
    kill $(cat "$PIDFILE") 2>/dev/null
    rm -f "$PIDFILE"
    echo "API stopped"
}

restart() {
    stop
    sleep 2
    start
}

status() {
    if [ -f "$PIDFILE" ] && kill -0 $(cat "$PIDFILE") 2>/dev/null; then
        echo "API is running (PID: $(cat $PIDFILE))"
        echo "HTTP: http://localhost:8081"
        echo "WebSocket: ws://localhost:8082"
        
        # Check health
        curl -s http://localhost:8081/api/health | python3 -m json.tool 2>/dev/null || echo "Health check failed"
    else
        echo "API is not running"
        rm -f "$PIDFILE"
        return 1
    fi
}

logs() {
    tail -f "$WORKSPACE/logs/api.log"
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    status)
        status
        ;;
    logs)
        logs
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs}"
        exit 1
        ;;
esac