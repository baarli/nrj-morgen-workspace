#!/bin/bash
# Deploy Mission Control to External Hosting
# Works with GitHub Pages, Netlify, Vercel, or any static host

set -e

WORKSPACE="/root/.openclaw/workspace"
MISSION_CONTROL="$WORKSPACE/mission-control"
BUILD_DIR="$MISSION_CONTROL/build"

echo "═══════════════════════════════════════════════════════════════════════"
echo "🚀 DEPLOY MISSION CONTROL TO EXTERNAL HOSTING"
echo "═══════════════════════════════════════════════════════════════════════"
echo ""

# Create build directory
mkdir -p "$BUILD_DIR"

# Copy the external version (no local dependencies)
cp "$MISSION_CONTROL/public/index-external.html" "$BUILD_DIR/index.html"
cp "$MISSION_CONTROL/public/cron-control.html" "$BUILD_DIR/cron-control.html"
cp "$MISSION_CONTROL/public/sakslista-pro.html" "$BUILD_DIR/sakslista-pro.html" 2>/dev/null || true

echo "✅ Build created in: $BUILD_DIR"
echo ""

# Create README for deployment
cat > "$BUILD_DIR/README.md" << 'EOF'
# BaarliClaw Mission Control

Full-featured mission control dashboard for autonomous AI agent.

## Access

- **URL**: https://nrjmorgen.com/kloakontroll
- **Password**: kloakontroll2026

## Features

- 🔐 Password protected
- 📊 Real-time system metrics
- 📝 Live logs streaming
- 🤖 Automation control
- 🎓 Skills management
- 🛡️ Security monitoring

## Deploy to GitHub Pages

1. Create new GitHub repo
2. Upload these files
3. Enable GitHub Pages in settings
4. Done!

## Deploy to Netlify

1. Drag and drop build folder to Netlify
2. Or connect GitHub repo
3. Done!

## Deploy to Vercel

```bash
npm i -g vercel
vercel --prod
```

## Custom Domain

Add CNAME file with your domain:
```
nrjmorgen.com
```

Then configure DNS to point to your hosting provider.
EOF

echo "📋 Deployment options:"
echo ""
echo "1. GITHUB PAGES:"
echo "   - Create repo: github.com/new"
echo "   - Upload build/ folder contents"
echo "   - Enable Pages in Settings"
echo ""
echo "2. NETLIFY:"
echo "   - Go to: netlify.com"
echo "   - Drag and drop build/ folder"
echo ""
echo "3. VERCEL:"
echo "   - Install: npm i -g vercel"
echo "   - Run: cd $BUILD_DIR && vercel"
echo ""
echo "4. ANY STATIC HOST:"
echo "   - Upload all files in build/"
echo "   - Configure domain: nrjmorgen.com/kloakontroll"
echo ""
echo "═══════════════════════════════════════════════════════════════════════"
echo "📁 Build files:"
ls -la "$BUILD_DIR"
echo "═══════════════════════════════════════════════════════════════════════"
