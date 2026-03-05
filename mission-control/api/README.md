# Mission Control API v2.0

Production-ready backend API for Mission Control with WebSocket support, authentication, metrics, and comprehensive error handling.

## Features

### 1. WebSocket Support (Real-time Updates)
- WebSocket server running on port 8082
- Real-time broadcasts for:
  - Morning routine progress
  - Backup/restore operations
  - Sak creation/updates/deletion
  - System events
- Message history for new connections

### 2. Authentication & Authorization
- JWT token-based authentication
- API key authentication for service-to-service
- Role-based access control
- Token expiration and cleanup
- Login/logout endpoints

### 3. Detailed Logging
- Structured logging to file and stdout
- Log rotation support
- Request logging with timestamps
- Error stack traces
- Separate log levels (DEBUG, INFO, WARNING, ERROR)

### 4. Error Handling & Recovery
- Custom APIError exceptions
- Standardized error responses
- Automatic retry for transient failures
- Graceful degradation
- Detailed error messages (in debug mode)

### 5. Health Check Endpoint
- Comprehensive health status
- Individual component checks:
  - Agent status
  - Database connectivity
  - Disk space
  - Memory usage
  - WebSocket status
- Status levels: healthy, warning, degraded, critical

### 6. Metrics Collection
- Request count tracking
- Response time histograms
- Error rate calculation
- Endpoint usage breakdown
- Status code distribution
- Uptime tracking

### 7. Backup/Restore Functionality
- Create manual backups
- Automatic backup scheduling
- List all backups with metadata
- Restore from any backup
- Pre-restore safety backup
- Backup size tracking

### 8. Configuration Management API
- Runtime configuration updates
- Environment-based configuration
- Feature flags
- Backup settings
- Notification settings

## Installation

### 1. Install Dependencies

```bash
cd /root/.openclaw/workspace/mission-control/api
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Start the API

Using the service script:
```bash
./api-service.sh start
```

Or manually:
```bash
python3 total-control-api.py
```

With systemd:
```bash
sudo cp mission-control-api.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable mission-control-api
sudo systemctl start mission-control-api
```

## API Endpoints

### Public Endpoints (No Auth Required)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Detailed health status |
| `/api/status` | GET | Basic API status |
| `/api/auth/login` | POST | Authenticate and get token |

### Protected Endpoints (Auth Required)

#### Authentication
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/verify` | GET | Verify current token |
| `/api/auth/logout` | POST | Logout and invalidate token |

#### System
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/system/resources` | GET | CPU, memory, disk usage |
| `/api/metrics` | GET | API metrics and statistics |
| `/api/logs` | GET | Recent API logs |

#### Configuration
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/config` | GET | Get configuration |
| `/api/config` | POST | Update configuration |
| `/api/settings` | GET | Get NRJ settings |
| `/api/settings` | POST | Save NRJ settings |

#### Backup/Restore
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/backups` | GET | List all backups |
| `/api/backups` | POST | Create new backup |
| `/api/backups/:name` | DELETE | Delete backup |
| `/api/backups/restore` | POST | Restore from backup |

#### Morning Routine
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/routine/morning/status` | GET | Get routine status |
| `/api/routine/morning` | POST | Start morning routine |

#### NRJ Saklista
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/nrj/saker` | GET | Get today's saker |
| `/api/nrj/saker` | POST | Create new sak |
| `/api/nrj/saker/:id` | PATCH | Update sak |
| `/api/nrj/saker/:id` | DELETE | Delete sak |
| `/api/nrj/stats` | GET | Get NRJ statistics |

#### Cron Jobs
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/cron/jobs` | GET | List cron jobs |
| `/api/cron/jobs/run` | POST | Run a cron job |
| `/api/cron/jobs/toggle` | POST | Enable/disable job |

#### Git & Deploy
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/git/repos` | GET | List git repositories |
| `/api/git/deploy` | POST | Deploy repository |

#### Podcast
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/podcast/episodes` | GET | List episodes |
| `/api/podcast/fetch` | POST | Fetch new episodes |

#### Control
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/control` | POST | System control actions |

## Authentication

### Login

```bash
curl -X POST http://localhost:8081/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your-password"}'
```

Response:
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "expires_in": 86400,
  "user": {
    "id": "admin",
    "roles": ["admin", "user"]
  }
}
```

### Using the Token

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8081/api/system/resources
```

### API Key Authentication

```bash
curl -H "X-API-Key: your-api-key" \
  http://localhost:8081/api/system/resources
```

## WebSocket Usage

Connect to `ws://localhost:8082`

### Message Format

```json
{
  "type": "event_type",
  "timestamp": "2024-01-01T12:00:00",
  "data": {}
}
```

### Event Types

- `morning_routine_started` - Morning routine started
- `morning_routine_progress` - Progress update
- `morning_routine_complete` - Routine completed
- `morning_routine_error` - Routine failed
- `sak_created` - New sak created
- `sak_updated` - Sak updated
- `sak_deleted` - Sak deleted
- `backup_created` - Backup created
- `backup_restored` - Backup restored
- `config_updated` - Configuration updated
- `settings_updated` - Settings updated
- `history` - Initial history on connect

## Health Check

```bash
curl http://localhost:8081/api/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00",
  "version": "2.0.0",
  "checks": {
    "agent": {"status": "healthy", ...},
    "database": {"status": "healthy"},
    "disk": {"status": "healthy", "used_percent": 45},
    "memory": {"status": "healthy", "used_percent": 60},
    "websocket": {"status": "healthy", "connected_clients": 5}
  }
}
```

## Metrics

```bash
curl http://localhost:8081/api/metrics
```

Response:
```json
{
  "uptime_seconds": 3600,
  "uptime_formatted": "1h 0m 0s",
  "total_requests": 150,
  "total_errors": 2,
  "error_rate": 1.33,
  "avg_response_time_ms": 45.5,
  "requests_per_minute": 2.5,
  "endpoint_breakdown": {
    "GET /api/health": 50,
    "GET /api/status": 30
  },
  "status_code_distribution": {
    "200": 145,
    "404": 3,
    "500": 2
  }
}
```

## Backup/Restore

### Create Backup

```bash
curl -X POST http://localhost:8081/api/backups \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "manual_backup_2024"}'
```

### List Backups

```bash
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:8081/api/backups
```

### Restore Backup

```bash
curl -X POST http://localhost:8081/api/backups/restore \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "manual_backup_2024"}'
```

## Configuration

### Get Configuration

```bash
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:8081/api/config
```

### Update Configuration

```bash
curl -X POST http://localhost:8081/api/config \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "backup": {
      "auto_backup": true,
      "backup_interval_hours": 12
    }
  }'
```

## Error Responses

All errors follow this format:

```json
{
  "error": "Error message",
  "details": {},
  "timestamp": "2024-01-01T12:00:00"
}
```

### Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

## Service Management

```bash
# Check status
./api-service.sh status

# View logs
./api-service.sh logs

# Restart
./api-service.sh restart

# Stop
./api-service.sh stop
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `API_PORT` | 8081 | HTTP API port |
| `WS_PORT` | 8082 | WebSocket port |
| `LOG_LEVEL` | INFO | Logging level |
| `JWT_SECRET` | auto-generated | JWT signing secret |
| `JWT_EXPIRY_HOURS` | 24 | Token expiry time |
| `API_KEY` | auto-generated | API key for service auth |
| `ADMIN_PASSWORD` | admin | Admin password |
| `SUPABASE_URL` | - | Supabase URL |
| `SUPABASE_SERVICE_KEY` | - | Supabase service key |

## Security Considerations

1. **Change default passwords** - Update `ADMIN_PASSWORD` and `JWT_SECRET`
2. **Use HTTPS** - In production, use a reverse proxy (nginx) with SSL
3. **Firewall** - Restrict access to ports 8081 and 8082
4. **API Keys** - Rotate API keys regularly
5. **Token Expiry** - Set appropriate JWT expiry times

## Troubleshooting

### API won't start
- Check if ports 8081/8082 are in use: `netstat -tlnp | grep 808`
- Check logs: `tail -f /root/.openclaw/workspace/logs/api.log`
- Verify Python dependencies: `pip install -r requirements.txt`

### Authentication fails
- Verify JWT_SECRET is set correctly
- Check token expiry
- Ensure Authorization header format: `Bearer TOKEN`

### WebSocket not working
- Check if websocket-server is installed: `pip show websocket-server`
- Verify firewall allows port 8082
- Check WebSocket status in health endpoint

### Database connection errors
- Verify SUPABASE_URL and SUPABASE_SERVICE_KEY
- Check network connectivity to Supabase
- Review Supabase dashboard for service status

## Changelog

### v2.0.0
- Added WebSocket support for real-time updates
- Added JWT-based authentication
- Added comprehensive error handling
- Added health check endpoint with detailed status
- Added metrics collection
- Added backup/restore functionality
- Added configuration management API
- Added detailed logging
- Added gzip compression for responses
- Added CORS support
- Improved thread safety
- Production-ready service scripts