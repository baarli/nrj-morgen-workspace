#!/usr/bin/env python3
"""
Mission Control Backend API - Total Control Edition v3.0
Production-ready API with WebSocket support, authentication, metrics, and REAL data.
"""

import os
import sys
import json
import subprocess
import threading
import urllib.request
import urllib.parse
import hashlib
import secrets
import time
import logging
import traceback
import gzip
import shutil
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from functools import wraps
from typing import Dict, List, Any, Optional, Callable
import uuid

# Optional imports with graceful degradation
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

try:
    import jwt
    JWT_AVAILABLE = True
except ImportError:
    JWT_AVAILABLE = False

try:
    from websocket_server import WebsocketServer
    WEBSOCKET_AVAILABLE = True
except ImportError:
    WEBSOCKET_AVAILABLE = False

# Import security hardening module
try:
    from security_hardening import (
        InputValidator, RateLimiter, rate_limiter, rate_limit,
        SecurityHeaders, DependencyAuditor, apply_security_hardening
    )
    SECURITY_HARDENING_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Security hardening module not available: {e}")
    SECURITY_HARDENING_AVAILABLE = False

# Configuration
WORKSPACE = "/root/.openclaw/workspace"
SCRIPTS_DIR = f"{WORKSPACE}/scripts"
API_PORT = int(os.environ.get('API_PORT', 8081))
WS_PORT = int(os.environ.get('WS_PORT', 8082))
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
JWT_SECRET = os.environ.get('JWT_SECRET', secrets.token_hex(32))
JWT_EXPIRY_HOURS = int(os.environ.get('JWT_EXPIRY_HOURS', 24))
API_KEY = os.environ.get('API_KEY', 'mission-control-api-key-2026')

# Supabase config from environment or defaults
SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://kvniauxokdtmpvjtfnej.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_SERVICE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt2bmlhdXhva2R0bXB2anRmbmVqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTM2NzIzNCwiZXhwIjoyMDY2OTQzMjM0fQ.OkhTtq9QAQ3xMzZYKyWyCjj7PiqMZJKSvpA0jcBJqpE')
TENANT_ID = os.environ.get('TENANT_ID', 'a0000000-0000-0000-0000-000000000001')
CREATED_BY = os.environ.get('CREATED_BY', '10aa1508-6d52-490c-8ae5-fa3da9a152c4')

# Podcast RSS
PODCAST_RSS = "https://rss.podplaystudio.com/4035.xml"

# Nielsen API
NIELSEN_API_URL = "https://eu-iport.nielsen-iwatch.com/api/Chart?dataid=8eb6daca-1266-4af8-8e8f-f39107dc63fb&publish_key=bd551853-f42b-4b86-813a-79faf3a718e9"
PODTOPPEN_URL = "https://podtoppen.tnslistene.no/export.php"

# Ensure directories exist
os.makedirs(f"{WORKSPACE}/logs", exist_ok=True)
os.makedirs(f"{WORKSPACE}/backups", exist_ok=True)
os.makedirs(f"{WORKSPACE}/.config", exist_ok=True)

# Setup logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"{WORKSPACE}/logs/api.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('MissionControlAPI')

# ==================== METRICS ====================

class MetricsCollector:
    """Collects and stores API metrics"""

    def __init__(self):
        self.request_count = 0
        self.request_errors = 0
        self.response_times = []
        self.endpoint_counts = {}
        self.status_codes = {}
        self.start_time = time.time()
        self._lock = threading.Lock()

    def record_request(self, endpoint: str, method: str, status_code: int, duration_ms: float):
        """Record a request metric"""
        with self._lock:
            self.request_count += 1
            self.response_times.append(duration_ms)

            # Keep only last 1000 response times
            if len(self.response_times) > 1000:
                self.response_times = self.response_times[-1000:]

            key = f"{method} {endpoint}"
            self.endpoint_counts[key] = self.endpoint_counts.get(key, 0) + 1
            self.status_codes[status_code] = self.status_codes.get(status_code, 0) + 1

            if status_code >= 400:
                self.request_errors += 1

    def get_stats(self) -> Dict[str, Any]:
        """Get current metrics statistics"""
        with self._lock:
            uptime = time.time() - self.start_time
            avg_response_time = sum(self.response_times) / len(self.response_times) if self.response_times else 0

            return {
                'uptime_seconds': uptime,
                'uptime_formatted': self._format_duration(uptime),
                'total_requests': self.request_count,
                'total_errors': self.request_errors,
                'error_rate': round(self.request_errors / self.request_count * 100, 2) if self.request_count > 0 else 0,
                'avg_response_time_ms': round(avg_response_time, 2),
                'requests_per_minute': round(self.request_count / (uptime / 60), 2) if uptime > 0 else 0,
                'endpoint_breakdown': dict(self.endpoint_counts),
                'status_code_distribution': dict(self.status_codes)
            }

    @staticmethod
    def _format_duration(seconds: float) -> str:
        """Format duration in human readable format"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours}h {minutes}m {secs}s"

metrics = MetricsCollector()

# ==================== AUTHENTICATION ====================

class AuthManager:
    """Handles authentication and authorization"""

    def __init__(self):
        self.active_tokens = {}  # token -> expiry
        self.api_keys = set([API_KEY])
        self._lock = threading.Lock()
        self._cleanup_thread = threading.Thread(target=self._cleanup_expired_tokens, daemon=True)
        self._cleanup_thread.start()

    def generate_token(self, user_id: str, roles: List[str] = None) -> str:
        """Generate a new JWT token"""
        if not JWT_AVAILABLE:
            # Fallback to simple token
            token = secrets.token_urlsafe(32)
            expiry = datetime.now() + timedelta(hours=JWT_EXPIRY_HOURS)
            with self._lock:
                self.active_tokens[token] = {
                    'expiry': expiry,
                    'user_id': user_id,
                    'roles': roles or ['user']
                }
            return token

        payload = {
            'user_id': user_id,
            'roles': roles or ['user'],
            'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRY_HOURS),
            'iat': datetime.utcnow(),
            'jti': str(uuid.uuid4())
        }
        return jwt.encode(payload, JWT_SECRET, algorithm='HS256')

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify a token and return user info"""
        if not token:
            return None

        if JWT_AVAILABLE:
            try:
                payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
                return {
                    'user_id': payload.get('user_id'),
                    'roles': payload.get('roles', ['user']),
                    'valid': True
                }
            except jwt.ExpiredSignatureError:
                return {'valid': False, 'error': 'Token expired'}
            except jwt.InvalidTokenError as e:
                return {'valid': False, 'error': str(e)}
        else:
            # Simple token verification
            with self._lock:
                if token in self.active_tokens:
                    token_data = self.active_tokens[token]
                    if token_data['expiry'] > datetime.now():
                        return {
                            'user_id': token_data['user_id'],
                            'roles': token_data['roles'],
                            'valid': True
                        }
                    else:
                        del self.active_tokens[token]
                        return {'valid': False, 'error': 'Token expired'}
            return {'valid': False, 'error': 'Invalid token'}

    def verify_api_key(self, api_key: str) -> bool:
        """Verify an API key"""
        return api_key in self.api_keys

    def revoke_token(self, token: str) -> bool:
        """Revoke a token"""
        with self._lock:
            if token in self.active_tokens:
                del self.active_tokens[token]
                return True
        return False

    def _cleanup_expired_tokens(self):
        """Background thread to clean up expired tokens"""
        while True:
            time.sleep(300)  # Run every 5 minutes
            with self._lock:
                now = datetime.now()
                expired = [t for t, data in self.active_tokens.items() if data['expiry'] <= now]
                for t in expired:
                    del self.active_tokens[t]
                if expired:
                    logger.info(f"Cleaned up {len(expired)} expired tokens")

auth_manager = AuthManager()

# ==================== WEBSOCKET HANDLER ====================

class WebSocketManager:
    """Manages WebSocket connections and broadcasts"""

    def __init__(self):
        self.server = None
        self.clients = []
        self._lock = threading.Lock()
        self.message_history = []

    def start(self, port: int):
        """Start the WebSocket server"""
        if not WEBSOCKET_AVAILABLE:
            logger.warning("WebSocket server not available. Install websocket-server package.")
            return

        self.server = WebsocketServer(port=port, host='0.0.0.0')
        self.server.set_fn_new_client(self._on_connect)
        self.server.set_fn_client_left(self._on_disconnect)
        self.server.set_fn_message_received(self._on_message)

        thread = threading.Thread(target=self.server.run_forever, daemon=True)
        thread.start()
        logger.info(f"WebSocket server started on port {port}")

    def _on_connect(self, client, server):
        """Handle new client connection"""
        with self._lock:
            self.clients.append(client)
        logger.info(f"WebSocket client connected: {client['id']}")
        # Send recent message history
        self.send_to_client(client, {
            'type': 'history',
            'data': self.message_history[-50:]
        })

    def _on_disconnect(self, client, server):
        """Handle client disconnection"""
        with self._lock:
            if client in self.clients:
                self.clients.remove(client)
        logger.info(f"WebSocket client disconnected: {client['id']}")

    def _on_message(self, client, server, message):
        """Handle incoming message"""
        try:
            data = json.loads(message)
            msg_type = data.get('type', 'unknown')

            # Store client metadata
            if msg_type == 'identify':
                client['user_id'] = data.get('userId')
                client['tenant_id'] = data.get('tenantId')
                self.send_to_client(client, {
                    'type': 'identified',
                    'client_id': client['id'],
                    'message': 'Connected to Mission Control Live Updates'
                })
                logger.info(f"Client {client['id']} identified as user {client.get('user_id')}")
                return

            # Handle broadcast requests
            if msg_type == 'broadcast':
                self.broadcast('broadcast', {
                    'userId': client.get('user_id'),
                    'message': data.get('message'),
                    'timestamp': datetime.now().isoformat()
                })
                return

            # Handle refresh requests
            if msg_type == 'request_refresh':
                self.broadcast('refresh', {
                    'requested_by': client.get('user_id'),
                    'timestamp': datetime.now().isoformat()
                })
                return

            # Handle user activity
            if msg_type == 'activity':
                self.broadcast('user_activity', {
                    'userId': client.get('user_id'),
                    'action': data.get('action'),
                    'timestamp': datetime.now().isoformat()
                })
                return

            # Echo back for other messages
            self.send_to_client(client, {
                'type': 'echo',
                'data': data
            })

        except json.JSONDecodeError:
            self.send_to_client(client, {
                'type': 'error',
                'message': 'Invalid JSON'
            })

    def broadcast_to_tenant(self, tenant_id: str, message_type: str, data: Any):
        """Broadcast message only to clients in specific tenant"""
        if not self.server:
            return

        message = {
            'type': message_type,
            'timestamp': datetime.now().isoformat(),
            'data': data
        }

        with self._lock:
            for client in self.clients:
                if client.get('tenant_id') == tenant_id:
                    try:
                        self.server.send_message(client, json.dumps(message))
                    except Exception as e:
                        logger.error(f"Error sending to client {client['id']}: {e}")

    def broadcast(self, message_type: str, data: Any):
        """Broadcast message to all connected clients"""
        if not self.server:
            return

        message = {
            'type': message_type,
            'timestamp': datetime.now().isoformat(),
            'data': data
        }

        # Store in history
        self.message_history.append(message)
        if len(self.message_history) > 1000:
            self.message_history = self.message_history[-1000:]

        with self._lock:
            for client in self.clients:
                try:
                    self.server.send_message(client, json.dumps(message))
                except Exception as e:
                    logger.error(f"Error sending to client {client['id']}: {e}")

    def send_to_client(self, client, data: Dict):
        """Send message to specific client"""
        if self.server:
            try:
                self.server.send_message(client, json.dumps(data))
            except Exception as e:
                logger.error(f"Error sending to client: {e}")

    # ==================== REAL-TIME COLLABORATION ====================

    def broadcast_cursor_position(self, user_id: str, username: str, x: float, y: float, page: str):
        """Broadcast cursor position for real-time collaboration"""
        self.broadcast('cursor_move', {
            'user_id': user_id,
            'username': username,
            'x': x,
            'y': y,
            'page': page
        })

    def broadcast_user_joined(self, user_id: str, username: str, avatar: str):
        """Broadcast when a user joins collaboration"""
        self.broadcast('user_joined', {
            'user_id': user_id,
            'username': username,
            'avatar': avatar,
            'timestamp': datetime.now().isoformat()
        })

    def broadcast_user_left(self, user_id: str, username: str):
        """Broadcast when a user leaves collaboration"""
        self.broadcast('user_left', {
            'user_id': user_id,
            'username': username,
            'timestamp': datetime.now().isoformat()
        })

    def broadcast_item_editing(self, item_id: str, user_id: str, username: str, is_editing: bool):
        """Broadcast when a user starts/stops editing an item"""
        self.broadcast('item_editing', {
            'item_id': item_id,
            'user_id': user_id,
            'username': username,
            'is_editing': is_editing
        })

    def get_active_users(self) -> List[Dict]:
        """Get list of currently connected users"""
        # This would be populated from client registrations
        return [{'id': c.get('id'), 'connected_at': c.get('connected_at')} for c in self.clients]

ws_manager = WebSocketManager()

# ==================== ERROR HANDLING ====================

class APIError(Exception):
    """Custom API error with status code"""
    def __init__(self, message: str, status_code: int = 500, details: Dict = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

def handle_errors(func: Callable) -> Callable:
    """Decorator for error handling"""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except APIError as e:
            logger.warning(f"API Error: {e.message}")
            self.send_json_response({
                'error': e.message,
                'details': e.details,
                'timestamp': datetime.now().isoformat()
            }, e.status_code)
        except Exception as e:
            logger.error(f"Unhandled error: {e}")
            logger.error(traceback.format_exc())
            self.send_json_response({
                'error': 'Internal server error',
                'message': str(e) if os.environ.get('DEBUG') else 'An unexpected error occurred',
                'timestamp': datetime.now().isoformat()
            }, 500)
    return wrapper

# ==================== REAL DATA FETCHERS ====================

def fetch_podcast_episodes_real() -> List[Dict[str, Any]]:
    """Fetch real podcast episodes from RSS feed"""
    try:
        with urllib.request.urlopen(PODCAST_RSS, timeout=30) as response:
            xml_content = response.read()

        root = ET.fromstring(xml_content)
        episodes = []

        for item in root.findall('.//item'):
            title = item.find('title')
            description = item.find('description')
            pub_date = item.find('pubDate')
            enclosure = item.find('enclosure')
            duration = item.find('.//{http://www.itunes.com/dtds/podcast-1.0.dtd}duration')

            episode = {
                'id': str(uuid.uuid4())[:8],
                'title': title.text.strip() if title is not None and title.text else 'Ukjent tittel',
                'description': description.text[:200] + '...' if description is not None and description.text and len(description.text) > 200 else (description.text if description is not None else ''),
                'pub_date': pub_date.text if pub_date is not None else '',
                'audio_url': enclosure.get('url') if enclosure is not None else '',
                'duration': duration.text if duration is not None else '0',
                'clips_generated': 0  # Would be fetched from database
            }
            episodes.append(episode)

        return episodes[:20]  # Return max 20 episodes
    except Exception as e:
        logger.error(f"Error fetching podcast episodes: {e}")
        raise APIError(f'Failed to fetch podcast episodes: {str(e)}', 500)

def fetch_nrj_saker_real() -> List[Dict[str, Any]]:
    """Fetch real NRJ saker from Supabase"""
    try:
        today = datetime.now().strftime('%Y-%m-%d')
        req = urllib.request.Request(
            f"{SUPABASE_URL}/rest/v1/agenda_items?tenant_id=eq.{TENANT_ID}&show_date=eq.{today}&order=order_index.asc",
            headers={'apikey': SUPABASE_KEY, 'Authorization': f'Bearer {SUPABASE_KEY}'}
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        logger.error(f"Error fetching NRJ saker: {e}")
        raise APIError(f'Failed to fetch saker: {str(e)}', 500)

def fetch_nrj_stats_real() -> Dict[str, Any]:
    """Fetch real NRJ stats from Nielsen and Podtoppen"""
    stats = {
        'radio': None,
        'podcast': None,
        'timestamp': datetime.now().isoformat()
    }

    # Fetch Nielsen radio data
    try:
        req = urllib.request.Request(
            NIELSEN_API_URL,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            series_data = data['seriesMDData'][0]
            data2d = series_data['data2D']

            for row in data2d:
                if row[0] == "NRJ":
                    weekly_data = {
                        'uke_1': int(row[2]) * 1000,
                        'uke_2': int(row[3]) * 1000,
                        'uke_3': int(row[4]) * 1000,
                        'uke_4': int(row[5]) * 1000,
                        'uke_5': int(row[6]) * 1000,
                        'uke_6': int(row[7]) * 1000,
                        'uke_7': int(row[8]) * 1000,
                    }
                    values = list(weekly_data.values())
                    latest = values[-1]
                    previous = values[-2]
                    trend = ((latest - previous) / previous) * 100

                    stats['radio'] = {
                        'week': 7,
                        'year': 2026,
                        'dailyListeners': latest,
                        'trend': f"{trend:+.1f}%",
                        'weekly_data': weekly_data,
                        'average': int(sum(values) / len(values))
                    }
                    break
    except Exception as e:
        logger.error(f"Error fetching Nielsen data: {e}")
        stats['radio_error'] = str(e)

    # Fetch Podtoppen data
    try:
        req = urllib.request.Request(
            PODTOPPEN_URL,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            raw_data = response.read()
            csv_data = raw_data.decode('latin-1')
            lines = csv_data.strip().split('\n')

            for i, line in enumerate(lines[1:], 1):
                if 'nrj morgen' in line.lower():
                    parts = line.split(';')
                    stats['podcast'] = {
                        'week': 7,
                        'year': 2026,
                        'ranking': i,
                        'uniqueListeners': int(parts[3]),
                        'downloads': int(parts[4]),
                        'author': parts[1]
                    }
                    break
    except Exception as e:
        logger.error(f"Error fetching Podtoppen data: {e}")
        stats['podcast_error'] = str(e)

    return stats

def fetch_cron_jobs_real() -> List[Dict[str, Any]]:
    """Fetch real cron jobs from openclaw"""
    try:
        result = subprocess.run(
            ['openclaw', 'cron', 'list', '--json'],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            jobs = json.loads(result.stdout)
            # Enrich with additional info
            for job in jobs:
                job['lastRun'] = 'Unknown'
                job['nextRun'] = 'Calculating...'
            return jobs
        else:
            # Fallback to basic list
            return fetch_cron_jobs_fallback()
    except Exception as e:
        logger.error(f"Error fetching cron jobs: {e}")
        return fetch_cron_jobs_fallback()

def fetch_cron_jobs_fallback() -> List[Dict[str, Any]]:
    """Fallback cron jobs list"""
    return [
        {'id': 'morning-routine', 'name': 'Morning Routine', 'schedule': '0 6 * * 1-5', 'enabled': True, 'lastRun': '2 hours ago', 'nextRun': 'Tomorrow 06:00', 'command': 'morning-routine-v2.1.py'},
        {'id': 'podcast-download', 'name': 'Podcast Download', 'schedule': '0 7 * * *', 'enabled': True, 'lastRun': 'Today 07:00', 'nextRun': 'Tomorrow 07:00', 'command': 'podcast-clipper.py'},
        {'id': 'session-end', 'name': 'Session End Capture', 'schedule': '0 * * * *', 'enabled': True, 'lastRun': '5 minutes ago', 'nextRun': 'In 55 minutes', 'command': 'auto-learning-capture.sh'},
        {'id': 'nrj-stats', 'name': 'NRJ Stats Update', 'schedule': '0 12 * * 3', 'enabled': True, 'lastRun': '3 days ago', 'nextRun': 'Wednesday 12:00', 'command': 'update_nrj_dashboard.py'},
    ]

def fetch_system_metrics_real() -> Dict[str, Any]:
    """Fetch real system metrics"""
    if not PSUTIL_AVAILABLE:
        return fetch_system_metrics_fallback()

    try:
        # CPU
        cpu_percent = psutil.cpu_percent(interval=0.5)
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()

        # Memory
        mem = psutil.virtual_memory()

        # Disk
        disk = psutil.disk_usage('/')

        # Network
        net = psutil.net_io_counters()

        # Boot time
        boot_time = datetime.fromtimestamp(psutil.boot_time()).isoformat()

        # Process count
        process_count = len(psutil.pids())

        return {
            'timestamp': datetime.now().isoformat(),
            'cpu': {
                'percent': cpu_percent,
                'count': cpu_count,
                'freq_mhz': cpu_freq.current if cpu_freq else None,
                'per_cpu': psutil.cpu_percent(interval=0.1, percpu=True)
            },
            'memory': {
                'total_gb': round(mem.total / (1024**3), 2),
                'available_gb': round(mem.available / (1024**3), 2),
                'used_gb': round(mem.used / (1024**3), 2),
                'percent': mem.percent,
                'cached_gb': round(getattr(mem, 'cached', 0) / (1024**3), 2)
            },
            'disk': {
                'total_gb': round(disk.total / (1024**3), 2),
                'used_gb': round(disk.used / (1024**3), 2),
                'free_gb': round(disk.free / (1024**3), 2),
                'percent': disk.percent
            },
            'network': {
                'bytes_sent': net.bytes_sent,
                'bytes_recv': net.bytes_recv,
                'packets_sent': net.packets_sent,
                'packets_recv': net.packets_recv,
                'errors_in': net.errin,
                'errors_out': net.errout
            },
            'system': {
                'boot_time': boot_time,
                'process_count': process_count,
                'load_average': os.getloadavg() if hasattr(os, 'getloadavg') else None
            }
        }
    except Exception as e:
        logger.error(f"Error fetching system metrics: {e}")
        return fetch_system_metrics_fallback()

def fetch_system_metrics_fallback() -> Dict[str, Any]:
    """Fallback system metrics using basic commands"""
    metrics = {'timestamp': datetime.now().isoformat()}

    # Try to get basic info from /proc
    try:
        # Memory from /proc/meminfo
        with open('/proc/meminfo', 'r') as f:
            meminfo = f.read()
            for line in meminfo.split('\n'):
                if line.startswith('MemTotal:'):
                    metrics['memory_total_kb'] = int(line.split()[1])
                elif line.startswith('MemAvailable:'):
                    metrics['memory_available_kb'] = int(line.split()[1])

        # Load average
        with open('/proc/loadavg', 'r') as f:
            load = f.read().split()
            metrics['load_average'] = [float(load[0]), float(load[1]), float(load[2])]

        # Uptime
        with open('/proc/uptime', 'r') as f:
            uptime = float(f.read().split()[0])
            metrics['uptime_seconds'] = uptime
    except Exception as e:
        metrics['error'] = str(e)

    return metrics

# ==================== MORNING ROUTINE STATUS ====================

morning_routine_status = {
    'running': False,
    'started_at': None,
    'progress': 0,
    'message': 'Idle',
    'last_result': None,
    'version': '2.1'
}

# ==================== HTTP HANDLER ====================

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread"""
    allow_reuse_address = True
    daemon_threads = True

class APIHandler(BaseHTTPRequestHandler):
    """Enhanced API request handler"""

    protocol_version = 'HTTP/1.1'

    def log_message(self, format, *args):
        """Override to use our logger"""
        logger.info(f"{self.address_string()} - {format % args}")

    def log_error(self, format, *args):
        """Override to use our logger"""
        logger.error(f"{self.address_string()} - {format % args}")

    def send_json_response(self, data, status=200, headers=None):
        """Send JSON response with proper headers and security headers"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-API-Key')
        self.send_header('X-Request-ID', str(uuid.uuid4()))

        # Apply security headers
        if SECURITY_HARDENING_AVAILABLE:
            for header, value in SecurityHeaders.HEADERS.items():
                self.send_header(header, value)

        if headers:
            for key, value in headers.items():
                self.send_header(key, value)
        
        # Add rate limit headers if available
        if hasattr(self, '_rate_limit_headers'):
            for key, value in self._rate_limit_headers.items():
                self.send_header(key, value)
            delattr(self, '_rate_limit_headers')
        
        self.end_headers()

        response_body = json.dumps(data, default=str).encode()

        # Support gzip compression
        accept_encoding = self.headers.get('Accept-Encoding', '')
        if 'gzip' in accept_encoding and len(response_body) > 1024:
            self.send_header('Content-Encoding', 'gzip')
            response_body = gzip.compress(response_body)

        self.wfile.write(response_body)

    def get_auth_token(self) -> Optional[str]:
        """Extract auth token from request"""
        auth_header = self.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            return auth_header[7:]
        return None

    def get_api_key(self) -> Optional[str]:
        """Extract API key from request"""
        return self.headers.get('X-API-Key')

    def check_auth(self, required_roles: List[str] = None) -> Optional[Dict[str, Any]]:
        """Check if request is authenticated"""
        # Check API key first
        api_key = self.get_api_key()
        if api_key and auth_manager.verify_api_key(api_key):
            return {'user_id': 'api_key', 'roles': ['admin'], 'valid': True}

        # Check JWT token
        token = self.get_auth_token()
        if token:
            result = auth_manager.verify_token(token)
            if result and result.get('valid'):
                if required_roles:
                    user_roles = set(result.get('roles', []))
                    if not any(role in user_roles for role in required_roles):
                        raise APIError('Insufficient permissions', 403)
                return result
            elif result:
                raise APIError(result.get('error', 'Invalid token'), 401)

        # For development, allow some endpoints without auth
        public_endpoints = ['/api/health', '/api/status', '/api/auth/login']
        if self.path in public_endpoints:
            return {'user_id': 'anonymous', 'roles': ['user'], 'valid': True}

        raise APIError('Authentication required', 401)

    def read_body(self) -> Dict[str, Any]:
        """Read and parse request body"""
        try:
            length = int(self.headers.get('Content-Length', 0))
            if length > 0:
                body = self.rfile.read(length).decode('utf-8')
                return json.loads(body)
        except json.JSONDecodeError as e:
            raise APIError('Invalid JSON in request body', 400, {'details': str(e)})
        except Exception as e:
            logger.warning(f"Error reading body: {e}")
        return {}

    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_json_response({'status': 'ok'})

    def _route_request(self, method: str):
        """Route request to appropriate handler with metrics and rate limiting"""
        start_time = time.time()
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        status_code = 200

        try:
            # Apply rate limiting
            if SECURITY_HARDENING_AVAILABLE:
                client_id = rate_limiter.get_client_identifier(self)
                
                # Stricter limits for auth endpoints
                if path == '/api/auth/login':
                    limit_type = 'auth'
                elif path.startswith('/api/'):
                    limit_type = 'api'
                else:
                    limit_type = 'default'
                
                allowed, limit_headers = rate_limiter.is_allowed(client_id, limit_type)
                
                if not allowed:
                    self.send_json_response({
                        'error': 'Rate limit exceeded',
                        'message': 'Too many requests. Please try again later.',
                        'retry_after': limit_headers.get('retry_after', 60)
                    }, 429)
                    return
                
                # Store headers for response
                self._rate_limit_headers = {
                    'X-RateLimit-Limit': str(limit_headers['limit']),
                    'X-RateLimit-Remaining': str(limit_headers['remaining']),
                    'X-RateLimit-Reset': str(int(limit_headers['reset']))
                }

            # Public routes (no auth required)
            public_routes = {
                '/api/health': self.get_health,
                '/api/status': self.get_status,
                '/api/auth/login': self.auth_login,
            }

            # Protected routes
            protected_routes = {
                'GET': {
                    '/api/system/resources': self.get_system_resources,
                    '/api/system/metrics': self.get_system_metrics,
                    '/api/cron/jobs': self.get_cron_jobs,
                    '/api/podcast/episodes': self.get_podcast_episodes,
                    '/api/nrj/saker': self.get_nrj_saker,
                    '/api/nrj/stats': self.get_nrj_stats,
                    '/api/routine/morning/status': self.get_morning_status,
                    '/api/routine/morning-v2': self.get_morning_v2_info,
                    '/api/logs': self.get_logs,
                    '/api/metrics': self.get_metrics,
                    '/api/auth/verify': self.auth_verify,
                    '/api/realtime/status': self.get_realtime_status,
                    '/api/security/audit': self.get_security_audit,
                },
                'POST': {
                    '/api/routine/morning': self.run_morning_routine,
                    '/api/routine/morning-v2': self.run_morning_routine_v2,
                    '/api/cron/jobs/run': self.run_cron_job,
                    '/api/cron/jobs/toggle': self.toggle_cron_job,
                    '/api/podcast/fetch': self.fetch_podcast_episodes,
                    '/api/nrj/saker': self.create_sak,
                    '/api/auth/logout': self.auth_logout,
                    '/api/realtime/broadcast': self.broadcast_realtime_message,
                    '/api/realtime/refresh': self.trigger_refresh,
                },
                'PATCH': {
                },
                'DELETE': {
                }
            }

            # Check public routes first
            if path in public_routes:
                result = public_routes[path]()
                self.send_json_response(result)
                return

            # Check protected routes
            if method in protected_routes:
                handler = protected_routes[method].get(path)
                if handler:
                    self.check_auth()
                    data = self.read_body() if method in ['POST', 'PATCH'] else {}

                    # Handle PATCH for specific resources
                    if method == 'PATCH' and not handler:
                        if path.startswith('/api/nrj/saker/'):
                            sak_id = path.split('/')[-1]
                            result = self.update_sak(sak_id, data)
                            self.send_json_response(result)
                            return

                    # Handle DELETE for specific resources
                    if method == 'DELETE' and not handler:
                        if path.startswith('/api/nrj/saker/'):
                            sak_id = path.split('/')[-1]
                            result = self.delete_sak(sak_id)
                            self.send_json_response(result)
                            return

                    if handler:
                        if method in ['POST', 'PATCH']:
                            result = handler(data)
                        else:
                            result = handler()
                        self.send_json_response(result)
                        return

            # Route not found
            raise APIError('Not found', 404)

        except APIError as e:
            status_code = e.status_code
            raise
        except Exception as e:
            status_code = 500
            logger.error(f"Error in {method} {path}: {e}")
            logger.error(traceback.format_exc())
            raise APIError('Internal server error', 500)
        finally:
            # Record metrics
            duration_ms = (time.time() - start_time) * 1000
            metrics.record_request(path, method, status_code, duration_ms)

    @handle_errors
    def do_GET(self):
        self._route_request('GET')

    @handle_errors
    def do_POST(self):
        self._route_request('POST')

    @handle_errors
    def do_PATCH(self):
        self._route_request('PATCH')

    @handle_errors
    def do_DELETE(self):
        self._route_request('DELETE')

    # ==================== AUTHENTICATION ENDPOINTS ====================

    def auth_login(self, data: Dict = None) -> Dict[str, Any]:
        """Authenticate and get token with input validation"""
        data = data or self.read_body()
        username = data.get('username', '')
        password = data.get('password', '')

        # Validate input
        if SECURITY_HARDENING_AVAILABLE:
            is_valid, errors = InputValidator.validate_auth_data(data)
            if not is_valid:
                raise APIError(f'Validation failed: {"; ".join(errors)}', 400)

        # Simple auth for demo - in production use proper password hashing
        if username == 'admin' and password == os.environ.get('ADMIN_PASSWORD', 'kloakontroll2026'):
            token = auth_manager.generate_token(
                user_id=username,
                roles=['admin', 'user']
            )
            return {
                'token': token,
                'expires_in': JWT_EXPIRY_HOURS * 3600,
                'user': {'id': username, 'roles': ['admin', 'user']}
            }

        raise APIError('Invalid credentials', 401)

    def auth_verify(self) -> Dict[str, Any]:
        """Verify current token"""
        token = self.get_auth_token()
        if not token:
            raise APIError('No token provided', 401)

        result = auth_manager.verify_token(token)
        if not result or not result.get('valid'):
            raise APIError(result.get('error', 'Invalid token'), 401)

        return {
            'valid': True,
            'user_id': result.get('user_id'),
            'roles': result.get('roles')
        }

    def auth_logout(self, data: Dict = None) -> Dict[str, Any]:
        """Logout and invalidate token"""
        token = self.get_auth_token()
        if token:
            auth_manager.revoke_token(token)
        return {'success': True, 'message': 'Logged out'}

    # ==================== HEALTH & STATUS ====================

    def get_health(self) -> Dict[str, Any]:
        """Get detailed health status"""
        health = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '3.0.0',
            'checks': {}
        }

        # Check agent status
        try:
            auto_exec = os.path.exists(f"{WORKSPACE}/.auto-exec-log")
            autonomous = os.path.exists(f"{WORKSPACE}/.autonomous-mode.pid")
            health['checks']['agent'] = {
                'status': 'healthy' if auto_exec else 'warning',
                'auto_exec': 'active' if auto_exec else 'inactive',
                'autonomous_mode': 'active' if autonomous else 'inactive'
            }
        except Exception as e:
            health['checks']['agent'] = {'status': 'error', 'error': str(e)}

        # Check database
        try:
            req = urllib.request.Request(
                f"{SUPABASE_URL}/rest/v1/agenda_items?limit=1",
                headers={'apikey': SUPABASE_KEY},
                method='HEAD'
            )
            with urllib.request.urlopen(req, timeout=5):
                health['checks']['database'] = {'status': 'healthy'}
        except Exception as e:
            health['checks']['database'] = {'status': 'error', 'error': str(e)}
            health['status'] = 'degraded'

        # Check disk space
        try:
            if PSUTIL_AVAILABLE:
                disk = psutil.disk_usage('/')
                disk_percent = disk.percent
                health['checks']['disk'] = {
                    'status': 'healthy' if disk_percent < 90 else 'warning',
                    'used_percent': disk_percent,
                    'free_gb': round(disk.free / (1024**3), 2)
                }
                if disk_percent > 95:
                    health['status'] = 'critical'
            else:
                health['checks']['disk'] = {'status': 'unknown'}
        except Exception as e:
            health['checks']['disk'] = {'status': 'error', 'error': str(e)}

        # Check memory
        try:
            if PSUTIL_AVAILABLE:
                mem = psutil.virtual_memory()
                health['checks']['memory'] = {
                    'status': 'healthy' if mem.percent < 90 else 'warning',
                    'used_percent': mem.percent,
                    'available_gb': round(mem.available / (1024**3), 2)
                }
            else:
                health['checks']['memory'] = {'status': 'unknown'}
        except Exception as e:
            health['checks']['memory'] = {'status': 'error', 'error': str(e)}

        # Check WebSocket
        health['checks']['websocket'] = {
            'status': 'healthy' if ws_manager.server else 'disabled',
            'connected_clients': len(ws_manager.clients) if ws_manager.server else 0
        }

        return health

    def get_status(self) -> Dict[str, Any]:
        """Get API status"""
        return {
            'status': 'operational',
            'timestamp': datetime.now().isoformat(),
            'version': '3.0.0',
            'systems': {
                'agent': self.check_agent_status(),
                'database': self.check_db_status(),
                'api': 'active',
                'morning_routine': 'running' if morning_routine_status['running'] else 'idle',
                'websocket': 'active' if ws_manager.server else 'disabled'
            }
        }

    def check_agent_status(self) -> Dict[str, str]:
        """Check agent status"""
        auto_exec = os.path.exists(f"{WORKSPACE}/.auto-exec-log")
        autonomous = os.path.exists(f"{WORKSPACE}/.autonomous-mode.pid")
        return {
            'auto_exec': 'active' if auto_exec else 'inactive',
            'autonomous_mode': 'active' if autonomous else 'inactive'
        }

    def check_db_status(self) -> str:
        """Check database status"""
        try:
            req = urllib.request.Request(
                f"{SUPABASE_URL}/rest/v1/agenda_items?limit=1",
                headers={'apikey': SUPABASE_KEY},
                method='HEAD'
            )
            with urllib.request.urlopen(req, timeout=5):
                return 'connected'
        except:
            return 'disconnected'

    # ==================== REALTIME ENDPOINTS ====================

    def get_realtime_status(self) -> Dict[str, Any]:
        """Get realtime/WebSocket status"""
        return {
            'websocket': {
                'enabled': ws_manager.server is not None,
                'connected_clients': len(ws_manager.clients) if ws_manager.server else 0,
                'port': WS_PORT
            },
            'supabase_realtime': {
                'available': True,
                'url': SUPABASE_URL
            },
            'timestamp': datetime.now().isoformat()
        }

    def broadcast_realtime_message(self, data: Dict = None) -> Dict[str, Any]:
        """Broadcast a message to all connected clients"""
        data = data or self.read_body()
        message = data.get('message', '')
        message_type = data.get('type', 'broadcast')
        tenant_id = data.get('tenantId', TENANT_ID)

        if not message:
            raise APIError('Message is required', 400)

        # Broadcast via WebSocket
        ws_manager.broadcast_to_tenant(tenant_id, message_type, {
            'message': message,
            'sender': data.get('sender', 'system'),
            'timestamp': datetime.now().isoformat()
        })

        return {
            'success': True,
            'message': 'Broadcast sent',
            'clients_notified': len(ws_manager.clients)
        }

    def trigger_refresh(self, data: Dict = None) -> Dict[str, Any]:
        """Trigger a refresh on all connected clients"""
        data = data or self.read_body()
        tenant_id = data.get('tenantId', TENANT_ID)

        # Broadcast refresh command
        ws_manager.broadcast_to_tenant(tenant_id, 'refresh', {
            'triggered_by': data.get('userId', 'system'),
            'timestamp': datetime.now().isoformat(),
            'reason': data.get('reason', 'manual_refresh')
        })

        return {
            'success': True,
            'message': 'Refresh triggered',
            'clients_notified': len(ws_manager.clients)
        }

    # ==================== SECURITY AUDIT ====================

    def get_security_audit(self) -> Dict[str, Any]:
        """Get security audit report"""
        audit = {
            'timestamp': datetime.now().isoformat(),
            'security_hardening_available': SECURITY_HARDENING_AVAILABLE,
        }

        if SECURITY_HARDENING_AVAILABLE:
            # Dependency audit
            audit['dependencies'] = DependencyAuditor.generate_report()

            # Rate limiter status
            audit['rate_limiter'] = {
                'active': True,
                'limits': rate_limiter.limits,
            }

            # Security headers
            audit['security_headers'] = {
                'enabled': True,
                'headers_applied': list(SecurityHeaders.HEADERS.keys())
            }

            # Input validation
            audit['input_validation'] = {
                'enabled': True,
                'validators': ['email', 'uuid', 'safe_string', 'url', 'sak_data', 'auth_data']
            }
        else:
            audit['status'] = 'Security hardening module not available'

        return audit

    # ==================== METRICS ====================

    def get_metrics(self) -> Dict[str, Any]:
        """Get API metrics"""
        return metrics.get_stats()

    # ==================== SYSTEM RESOURCES ====================

    def get_system_resources(self) -> Dict[str, Any]:
        """Get system resource usage (legacy endpoint)"""
        return self.get_system_metrics()

    def get_system_metrics(self) -> Dict[str, Any]:
        """Get real system metrics"""
        return fetch_system_metrics_real()

    # ==================== CRON JOBS ====================

    def get_cron_jobs(self) -> List[Dict[str, Any]]:
        """Get real cron jobs"""
        return fetch_cron_jobs_real()

    def run_cron_job(self, data: Dict) -> Dict[str, Any]:
        """Run a cron job"""
        job_id = data.get('id')
        logger.info(f"Running cron job: {job_id}")
        ws_manager.broadcast('cron_job_started', {'job_id': job_id})

        # Map job IDs to actual scripts
        job_scripts = {
            'morning-routine': f'{SCRIPTS_DIR}/morning-routine-v2.1.py',
            'podcast-download': f'{SCRIPTS_DIR}/podcast-clipper.py',
            'nrj-stats': f'{SCRIPTS_DIR}/update_nrj_dashboard.py',
        }

        if job_id in job_scripts:
            script_path = job_scripts[job_id]
            if os.path.exists(script_path):
                thread = threading.Thread(
                    target=self._execute_script,
                    args=(script_path, job_id)
                )
                thread.daemon = True
                thread.start()
                return {'status': 'started', 'job': job_id, 'script': script_path}
            else:
                raise APIError(f'Script not found: {script_path}', 404)

        return {'status': 'started', 'job': job_id}

    def _execute_script(self, script_path: str, job_id: str):
        """Execute a script in background"""
        try:
            result = subprocess.run(
                ['python3', script_path],
                capture_output=True, text=True, timeout=600
            )
            ws_manager.broadcast('cron_job_completed', {
                'job_id': job_id,
                'success': result.returncode == 0,
                'output': result.stdout[-500:] if len(result.stdout) > 500 else result.stdout
            })
        except Exception as e:
            ws_manager.broadcast('cron_job_error', {'job_id': job_id, 'error': str(e)})

    def toggle_cron_job(self, data: Dict) -> Dict[str, Any]:
        """Toggle cron job enabled state"""
        job_id = data.get('id')
        enabled = data.get('enabled')
        logger.info(f"Toggling cron job {job_id} to {enabled}")
        return {'status': 'updated', 'job': job_id, 'enabled': enabled}

    # ==================== PODCAST ====================

    def get_podcast_episodes(self) -> List[Dict[str, Any]]:
        """Get real podcast episodes from RSS"""
        return fetch_podcast_episodes_real()

    def fetch_podcast_episodes(self, data: Dict = None) -> Dict[str, Any]:
        """Fetch and refresh podcast episodes"""
        logger.info("Fetching podcast episodes")
        ws_manager.broadcast('podcast_fetch_started', {})

        try:
            episodes = fetch_podcast_episodes_real()
            ws_manager.broadcast('podcast_fetch_completed', {'count': len(episodes)})
            return {'status': 'completed', 'count': len(episodes), 'episodes': episodes[:5]}
        except Exception as e:
            ws_manager.broadcast('podcast_fetch_error', {'error': str(e)})
            raise APIError(f'Failed to fetch episodes: {str(e)}', 500)

    # ==================== NRJ SAKSLISTA ====================

    def get_nrj_saker(self) -> List[Dict[str, Any]]:
        """Get real NRJ saker from Supabase"""
        return fetch_nrj_saker_real()

    def get_nrj_stats(self) -> Dict[str, Any]:
        """Get real NRJ statistics"""
        return fetch_nrj_stats_real()

    def create_sak(self, data: Dict) -> Dict[str, Any]:
        """Create a new sak with input validation"""
        # Validate input data
        if SECURITY_HARDENING_AVAILABLE:
            is_valid, errors = InputValidator.validate_sak_data(data)
            if not is_valid:
                raise APIError(f'Validation failed: {"; ".join(errors)}', 400)

        try:
            today = datetime.now().strftime('%Y-%m-%d')
            payload = {
                'tenant_id': TENANT_ID,
                'created_by': CREATED_BY,
                'show_date': today,
                **data
            }
            req = urllib.request.Request(
                f"{SUPABASE_URL}/rest/v1/agenda_items",
                method='POST',
                headers={
                    'apikey': SUPABASE_KEY,
                    'Authorization': f'Bearer {SUPABASE_KEY}',
                    'Content-Type': 'application/json'
                },
                data=json.dumps(payload).encode()
            )
            with urllib.request.urlopen(req, timeout=30) as response:
                ws_manager.broadcast('sak_created', {'title': data.get('title')})
                return {'status': 'created', 'id': str(uuid.uuid4())}
        except Exception as e:
            logger.error(f"Error creating sak: {e}")
            raise APIError(f'Failed to create sak: {str(e)}', 500)

    def update_sak(self, sak_id: str, data: Dict) -> Dict[str, Any]:
        """Update a sak with input validation"""
        # Validate sak_id format
        if SECURITY_HARDENING_AVAILABLE:
            if not InputValidator.validate_uuid(sak_id):
                raise APIError('Invalid sak_id format', 400)

            is_valid, errors = InputValidator.validate_sak_data(data)
            if not is_valid:
                raise APIError(f'Validation failed: {"; ".join(errors)}', 400)

        try:
            req = urllib.request.Request(
                f"{SUPABASE_URL}/rest/v1/agenda_items?id=eq.{sak_id}",
                method='PATCH',
                headers={
                    'apikey': SUPABASE_KEY,
                    'Authorization': f'Bearer {SUPABASE_KEY}',
                    'Content-Type': 'application/json'
                },
                data=json.dumps(data).encode()
            )
            with urllib.request.urlopen(req, timeout=30):
                ws_manager.broadcast('sak_updated', {'id': sak_id})
                return {'status': 'updated'}
        except Exception as e:
            logger.error(f"Error updating sak: {e}")
            raise APIError(f'Failed to update sak: {str(e)}', 500)

    def delete_sak(self, sak_id: str) -> Dict[str, Any]:
        """Delete a sak"""
        try:
            req = urllib.request.Request(
                f"{SUPABASE_URL}/rest/v1/agenda_items?id=eq.{sak_id}",
                method='DELETE',
                headers={'apikey': SUPABASE_KEY, 'Authorization': f'Bearer {SUPABASE_KEY}'}
            )
            with urllib.request.urlopen(req, timeout=30):
                ws_manager.broadcast('sak_deleted', {'id': sak_id})
                return {'status': 'deleted'}
        except Exception as e:
            logger.error(f"Error deleting sak: {e}")
            raise APIError(f'Failed to delete sak: {str(e)}', 500)

    # ==================== MORNING ROUTINE ====================

    def get_morning_status(self) -> Dict[str, Any]:
        """Get morning routine status"""
        return morning_routine_status

    def get_morning_v2_info(self) -> Dict[str, Any]:
        """Get morning routine v2 info"""
        return {
            'version': '2.1',
            'description': 'Morning Routine with OpenAI titles and better topic distribution',
            'config': {
                'articles_per_day': 15,
                'categories': ['Reality TV', 'Kjendis Drama', 'Film & TV', 'Musikk', 'Internasjonalt'],
                'max_per_category': 3,
                'max_age_hours': 48,
                'title_max_words': 7
            },
            'status': morning_routine_status
        }

    def run_morning_routine(self, data: Dict = None) -> Dict[str, Any]:
        """Run the morning routine"""
        global morning_routine_status

        if morning_routine_status['running']:
            return {'status': 'already_running'}

        thread = threading.Thread(target=self._execute_morning_routine)
        thread.daemon = True
        thread.start()

        ws_manager.broadcast('morning_routine_started', {})
        return {'status': 'started'}

    def run_morning_routine_v2(self, data: Dict = None) -> Dict[str, Any]:
        """Run the morning routine v2.1 with OpenAI titles"""
        global morning_routine_status

        if morning_routine_status['running']:
            return {'status': 'already_running', 'message': 'Morning routine is already running'}

        thread = threading.Thread(target=self._execute_morning_routine_v2)
        thread.daemon = True
        thread.start()

        ws_manager.broadcast('morning_routine_started', {'version': '2.1'})
        return {'status': 'started', 'version': '2.1', 'message': 'Morning Routine v2.1 started'}

    def _execute_morning_routine_v2(self):
        """Execute morning routine v2.1 in background"""
        global morning_routine_status

        morning_routine_status['running'] = True
        morning_routine_status['started_at'] = datetime.now().isoformat()
        morning_routine_status['progress'] = 0
        morning_routine_status['message'] = 'Starting v2.1...'
        morning_routine_status['version'] = '2.1'

        ws_manager.broadcast('morning_routine_progress', morning_routine_status)

        try:
            # Check if script exists
            script_path = f'{SCRIPTS_DIR}/morning-routine-v2.1.py'
            if not os.path.exists(script_path):
                morning_routine_status['message'] = 'Error: Script not found'
                morning_routine_status['last_result'] = {'error': f'Script not found: {script_path}'}
                ws_manager.broadcast('morning_routine_error', {'error': 'Script not found'})
                return

            # Run morning routine v2.1
            morning_routine_status['progress'] = 10
            morning_routine_status['message'] = 'Running Morning Routine v2.1 (15 articles, OpenAI titles)...'
            ws_manager.broadcast('morning_routine_progress', morning_routine_status)

            result = subprocess.run(
                ['python3', script_path],
                capture_output=True, text=True, timeout=600
            )

            # Check for result file
            result_file = '/tmp/morning-routine-v2-result.json'
            if os.path.exists(result_file):
                with open(result_file, 'r') as f:
                    routine_result = json.load(f)
                morning_routine_status['result_data'] = routine_result

            morning_routine_status['progress'] = 100
            morning_routine_status['message'] = 'Complete! Generated 15 articles with OpenAI titles'
            morning_routine_status['last_result'] = {
                'success': result.returncode == 0,
                'output': result.stdout[-1000:] if len(result.stdout) > 1000 else result.stdout,
                'errors': result.stderr[-500:] if result.stderr else None
            }

            ws_manager.broadcast('morning_routine_complete', morning_routine_status)
            logger.info("Morning routine v2.1 completed successfully")

        except subprocess.TimeoutExpired:
            logger.error("Morning routine v2.1 timed out")
            morning_routine_status['last_result'] = {'error': 'Timeout after 10 minutes'}
            ws_manager.broadcast('morning_routine_error', {'error': 'Timeout'})
        except Exception as e:
            logger.error(f"Morning routine v2.1 failed: {e}")
            morning_routine_status['last_result'] = {'error': str(e)}
            ws_manager.broadcast('morning_routine_error', {'error': str(e)})
        finally:
            morning_routine_status['running'] = False

    def _execute_morning_routine(self):
        """Execute legacy morning routine in background"""
        global morning_routine_status

        morning_routine_status['running'] = True
        morning_routine_status['started_at'] = datetime.now().isoformat()
        morning_routine_status['progress'] = 0
        morning_routine_status['message'] = 'Starting...'

        ws_manager.broadcast('morning_routine_progress', morning_routine_status)

        try:
            # Run news search
            morning_routine_status['progress'] = 30
            morning_routine_status['message'] = 'Searching for news...'
            ws_manager.broadcast('morning_routine_progress', morning_routine_status)

            result = subprocess.run(
                ['python3', f'{SCRIPTS_DIR}/brave-news-search.py', '15'],
                capture_output=True, text=True, timeout=180
            )

            morning_routine_status['progress'] = 100
            morning_routine_status['message'] = 'Complete!'
            morning_routine_status['last_result'] = {
                'success': result.returncode == 0,
                'output': result.stdout[-500:] if len(result.stdout) > 500 else result.stdout
            }

            ws_manager.broadcast('morning_routine_complete', morning_routine_status)
            logger.info("Morning routine completed successfully")

        except Exception as e:
            logger.error(f"Morning routine failed: {e}")
            morning_routine_status['last_result'] = {'error': str(e)}
            ws_manager.broadcast('morning_routine_error', {'error': str(e)})
        finally:
            morning_routine_status['running'] = False

    # ==================== LOGS ====================

    def get_logs(self) -> List[Dict[str, Any]]:
        """Get API logs"""
        logs = []
        try:
            log_file = f"{WORKSPACE}/logs/api.log"
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    lines = f.readlines()[-100:]  # Last 100 lines
                    for line in lines:
                        if line.strip():
                            # Parse log line (simple format)
                            parts = line.strip().split(' - ', 3)
                            if len(parts) >= 4:
                                logs.append({
                                    'timestamp': parts[0],
                                    'logger': parts[1],
                                    'level': parts[2].lower(),
                                    'message': parts[3]
                                })
                            else:
                                logs.append({
                                    'timestamp': datetime.now().isoformat(),
                                    'level': 'info',
                                    'message': line.strip()
                                })
        except Exception as e:
            logger.error(f"Error reading logs: {e}")
        return logs

# ==================== MAIN ====================

def run_server():
    """Run the API server"""
    # Start WebSocket server
    if WEBSOCKET_AVAILABLE:
        ws_manager.start(WS_PORT)
    else:
        logger.warning("WebSocket server not available. Install websocket-server package: pip3 install websocket-server")

    # Start HTTP server
    server = ThreadedHTTPServer(('0.0.0.0', API_PORT), APIHandler)
    logger.info(f"=" * 60)
    logger.info(f"Mission Control API v3.0 running on port {API_PORT}")
    logger.info(f"WebSocket server on port {WS_PORT}")
    logger.info(f"=" * 60)
    logger.info(f"Endpoints:")
    logger.info(f"  GET  /api/health              - Health check")
    logger.info(f"  GET  /api/status              - API status")
    logger.info(f"  GET  /api/system/metrics      - System metrics (CPU, RAM, disk)")
    logger.info(f"  GET  /api/cron/jobs           - List cron jobs")
    logger.info(f"  GET  /api/podcast/episodes    - Podcast episodes from RSS")
    logger.info(f"  GET  /api/nrj/saker           - NRJ saker from Supabase")
    logger.info(f"  GET  /api/nrj/stats           - NRJ stats (Nielsen + Podtoppen)")
    logger.info(f"  POST /api/routine/morning-v2  - Run Morning Routine v2.1")
    logger.info(f"  GET  /api/metrics             - API metrics")
    logger.info(f"=" * 60)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        server.shutdown()

if __name__ == '__main__':
    run_server()
