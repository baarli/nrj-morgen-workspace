#!/bin/bash
set -e  # Exit on error
# Deploy Total Control Dashboard to Netlify

cd /root/.openclaw/workspace/mission-control/public

# Deploy using netlify CLI with token
NETLIFY_AUTH_TOKEN="nfp_8B3dDBwZS9W1GSHTUy3am4fia6iZmF6b0092" \
netlify deploy --prod \
  --site=834576a6-da2b-4412-9433-315f6437508a \
  --dir=. \
  --message="Deploy Total Control Dashboard v3.0"

echo ""
echo "✅ Deploy complete!"
echo "🔗 URL: https://creative-muffin-dcf3a0.netlify.app/total-control.html"
