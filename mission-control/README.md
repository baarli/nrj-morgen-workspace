# BaarliClaw Mission Control v2.0

Full mission control dashboard for the BaarliClaw autonomous agent system.

## Features

- 🔐 **Password Protected** (kloakontroll2026)
- 📊 **Real-time Dashboard** with system metrics
- 📝 **Live Logs** streaming
- 🤖 **Automation Control** panel
- 🎓 **Skills Management**
- 🛡️ **Security Status**
- 🌐 **Responsive Design** with Tailwind CSS

## Quick Start

```bash
# Start server
./server.sh start

# Access dashboard
open http://localhost:3000

# Login with password: kloakontroll2026
```

## API Endpoints

```bash
# System status
./api/api.sh status

# Recent logs
./api/api.sh logs

# Automation status
./api/api.sh automations

# Skills list
./api/api.sh skills
```

## Deploy to nrjmorgen.com/kloakontroll

1. Copy `public/` contents to web server
2. Set up password protection (htaccess or similar)
3. Configure API endpoints
4. Done!

## System Requirements

- Modern web browser
- JavaScript enabled
- Python 3 (for server)

## License

MIT - Created by BaarliClaw
