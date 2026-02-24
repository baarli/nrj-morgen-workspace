# 🚀 Mission Control - BaarliClaw

**Total Control Dashboard for NRJ Morgen Operations**

[![Status](https://img.shields.io/badge/status-operational-success)](https://creative-muffin-dcf3a0.netlify.app)
[![Version](https://img.shields.io/badge/version-3.0-blue)](https://github.com/baarliclaw/mission-control)
[![License](https://img.shields.io/badge/license-MIT-green)]()

---

## 🎯 Overview

Mission Control is a comprehensive dashboard system for managing all aspects of NRJ Morgen radio show operations. Built with autonomous AI development, it provides 100% GUI-based control over:

- 📋 **Content Management** (Sakslista Pro)
- 🎧 **Podcast Operations**
- 🤖 **Agent Control**
- ⏰ **Cron Automation**
- 📊 **System Monitoring**
- 🗄️ **Database Admin**
- 📈 **Analytics**
- 🔔 **Notifications**

---

## ✨ Features

### Real-time Dashboard
- WebSocket-powered live updates
- System metrics (CPU, RAM, Disk)
- Activity log stream
- Toast notifications
- Offline mode support

### Content Management
- Drag & drop interface
- AI-powered suggestions
- Bulk actions
- Advanced search & filter
- Export/Import functionality

### Automation
- 18 scheduled cron jobs
- Morning Routine (04:50 CET weekdays)
- Podcast clip generation (07:00 daily)
- Trending Pulse (12:00 weekdays)
- Weekly reports (Sundays)

### System Control
- Agent management
- Cron job control
- Git integration
- Database administration
- System monitoring

---

## 🚀 Quick Start

### Local Development
```bash
# Clone repository
git clone https://github.com/baarliclaw/mission-control.git
cd mission-control

# Start local server
cd public
python3 -m http.server 8888

# Start backend API
cd ../api
python3 total-control-api.py
```

### Access Dashboard
- **Local:** http://localhost:8888
- **Production:** https://creative-muffin-dcf3a0.netlify.app
- **API:** http://localhost:8081

---

## 📁 Project Structure

```
mission-control/
├── public/                 # Frontend files
│   ├── total-control.html      # Main dashboard
│   ├── sakslista-pro.html      # Content management
│   ├── podkast-control.html    # Podcast operations
│   ├── agent-control.html      # Agent management
│   ├── cron-control.html       # Cron jobs
│   ├── system-monitor.html     # System monitoring
│   ├── notifications.html      # Notification center
│   ├── database-admin.html     # Database admin
│   ├── api-docs.html           # API documentation
│   ├── mobile-dashboard.html   # Mobile version
│   └── ...
├── api/                    # Backend files
│   ├── total-control-api.py    # Main API
│   ├── test-api.py             # Test suite
│   ├── README.md               # API docs
│   └── ...
├── docs/                   # Documentation
│   ├── AI_ASSISTANT.md         # AI roadmap
│   ├── AI_ROADMAP.md           # AI assistant plan
│   ├── TEST_PLAN.md            # Testing strategy
│   └── ...
└── scripts/                # Utility scripts
    ├── brave-news-search.py    # News search
    ├── integrated-morning-routine.sh
    └── ...
```

---

## 🔧 Configuration

### Environment Variables
```bash
SUPABASE_URL=https://kvniauxokdtmpvjtfnej.supabase.co
SUPABASE_KEY=your_key_here
BRAVE_API_KEY=your_key_here
```

### Cron Jobs
18 automated jobs including:
- Morning Routine (04:50 CET)
- Podcast clips (07:00)
- Trending Pulse (12:00)
- Weekly reports (Sundays)

---

## 🛠️ Technology Stack

### Frontend
- HTML5, CSS3, JavaScript
- Font Awesome icons
- Chart.js for visualizations
- Socket.IO for real-time updates

### Backend
- Python 3.9+
- Flask/FastAPI
- WebSocket support
- REST API

### Database
- Supabase (PostgreSQL)
- Real-time subscriptions

### Infrastructure
- Netlify (hosting)
- Linux server (backend)
- Cron (scheduling)

---

## 📊 System Requirements

### Minimum
- 2 CPU cores
- 4GB RAM
- 10GB disk space

### Recommended
- 4 CPU cores
- 8GB RAM
- 50GB SSD

---

## 🔒 Security

- API key authentication
- Rate limiting
- Input validation
- XSS protection
- CORS configuration

---

## 🧪 Testing

```bash
# Run test suite
cd api
python3 test-api.py

# Test endpoints
curl http://localhost:8081/api/status
curl http://localhost:8081/api/system/resources
```

---

## 📈 Performance

- API response time: < 100ms
- Page load time: < 2s
- WebSocket latency: < 50ms
- Database queries: < 50ms

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📝 License

MIT License - see LICENSE file for details

---

## 🙏 Credits

Built with autonomous AI development by BaarliClaw

---

**Mission Control is LIVE and OPERATIONAL! 🚀**
