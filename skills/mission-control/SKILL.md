# Mission Control Skill

## Description
Manage and deploy Mission Control dashboard for BaarliClaw Agent system.

## Triggers
- "deploy mission control"
- "update dashboard"
- "mission control status"
- "nettlify deploy"

## Actions

### Deploy Dashboard
```bash
export NETLIFY_AUTH_TOKEN="nfp_8B3dDBwZS9W1GSHTUy3am4fia6iZmF6b0092"
cd /root/.openclaw/workspace/mission-control/public
netlify deploy --prod
```

### Check Status
```bash
export NETLIFY_AUTH_TOKEN="nfp_8B3dDBwZS9W1GSHTUy3am4fia6iZmF6b0092"
netlify status
```

### Open Dashboard
- URL: https://creative-muffin-dcf3a0.netlify.app/
- Password: kloakontroll2026

## Files
- Source: `/root/.openclaw/workspace/mission-control/`
- Public: `/root/.openclaw/workspace/mission-control/public/`
- Docs: `/root/.openclaw/workspace/docs/MISSION_CONTROL_NETLIFY.md`

## Site Details
- **Site ID:** 834576a6-da2b-4412-9433-315f6437508a
- **Name:** creative-muffin-dcf3a0
- **Owner:** niklasbaarli@gmail.com
- **Plan:** nf_team_dev

## Features
- Password protected login
- System overview with statistics
- Live logs (simulated)
- Automation status
- Skills display
- Security monitoring
- Responsive design

## Planned Improvements
- Real-time data integration
- Live log streaming
- Charts and graphs
- Automation controls
- Push notifications
- User settings
