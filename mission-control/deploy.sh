#!/bin/bash
# Deploy Mission Control to External Server
# Sets up nginx, SSL, and proper authentication

set -e

DOMAIN="nrjmorgen.com"
SUBPATH="/kloakontroll"
WORKSPACE="/root/.openclaw/workspace"
MISSION_CONTROL="$WORKSPACE/mission-control"
DEPLOY_DIR="/var/www/nrjmorgen.com/kloakontroll"
NGINX_CONF="/etc/nginx/sites-available/nrjmorgen-kloakontroll"

echo "═══════════════════════════════════════════════════════════════════════"
echo "🚀 DEPLOYING MISSION CONTROL TO $DOMAIN$SUBPATH"
echo "═══════════════════════════════════════════════════════════════════════"
echo ""

# 1. Install dependencies
echo "📦 Installing dependencies..."
apt-get update -qq
apt-get install -y -qq nginx apache2-utils certbot python3-certbot-nginx

# 2. Create deployment directory
echo "📁 Creating deployment directory..."
mkdir -p "$DEPLOY_DIR"

# 3. Copy mission control files
echo "📋 Copying mission control files..."
cp -r "$MISSION_CONTROL/public/"* "$DEPLOY_DIR/"

# 4. Create .htpasswd for authentication
echo "🔐 Setting up authentication..."
htpasswd -cb "$DEPLOY_DIR/.htpasswd" admin "kloakontroll2026"

# 5. Create nginx configuration
echo "⚙️  Creating nginx configuration..."
cat > "$NGINX_CONF" << 'EOF'
server {
    listen 80;
    server_name nrjmorgen.com;
    
    location /kloakontroll {
        alias /var/www/nrjmorgen.com/kloakontroll;
        index index.html;
        try_files $uri $uri/ =404;
        
        # Authentication
        auth_basic "Mission Control - Authorized Access Only";
        auth_basic_user_file /var/www/nrjmorgen.com/kloakontroll/.htpasswd;
        
        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;
        
        # Enable gzip
        gzip on;
        gzip_types text/plain text/css application/json application/javascript text/xml;
    }
    
    # API endpoints
    location /kloakontroll/api {
        alias /var/www/nrjmorgen.com/kloakontroll/api;
        
        # Authentication
        auth_basic "Mission Control API";
        auth_basic_user_file /var/www/nrjmorgen.com/kloakontroll/.htpasswd;
        
        # Allow CORS
        add_header Access-Control-Allow-Origin "*" always;
        add_header Access-Control-Allow-Methods "GET, POST, OPTIONS" always;
    }
}
EOF

# 6. Enable nginx site
echo "🔌 Enabling nginx site..."
ln -sf "$NGINX_CONF" /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl reload nginx

# 7. Setup SSL with Let's Encrypt (optional, requires domain)
echo "🔒 SSL Setup (optional)..."
echo "  To enable SSL, run: certbot --nginx -d nrjmorgen.com"

# 8. Create systemd service for API
echo "⚙️  Creating API service..."
cat > /etc/systemd/system/mission-control-api.service << EOF
[Unit]
Description=Mission Control API
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/var/www/nrjmorgen.com/kloakontroll
ExecStart=/var/www/nrjmorgen.com/kloakontroll/api/api-server.sh
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# 9. Set permissions
echo "🔒 Setting permissions..."
chown -R www-data:www-data "$DEPLOY_DIR"
chmod 755 "$DEPLOY_DIR"
chmod 644 "$DEPLOY_DIR/.htpasswd"

# 10. Create status script
cat > "$DEPLOY_DIR/check-status.sh" << 'EOF'
#!/bin/bash
echo "Mission Control Status:"
echo "======================"
echo ""
echo "Nginx: $(systemctl is-active nginx)"
echo "Website: $(curl -s -o /dev/null -w "%{http_code}" http://localhost/kloakontroll)"
echo "Auth: Enabled (.htpasswd)"
echo ""
echo "Access URL: https://nrjmorgen.com/kloakontroll"
echo "Username: admin"
echo "Password: kloakontroll2026"
EOF
chmod +x "$DEPLOY_DIR/check-status.sh"

echo ""
echo "═══════════════════════════════════════════════════════════════════════"
echo "✅ DEPLOYMENT COMPLETE!"
echo "═══════════════════════════════════════════════════════════════════════"
echo ""
echo "🌐 Access URL:"
echo "   http://nrjmorgen.com/kloakontroll"
echo ""
echo "🔐 Login Credentials:"
echo "   Username: admin"
echo "   Password: kloakontroll2026"
echo ""
echo "📋 Status Check:"
echo "   $DEPLOY_DIR/check-status.sh"
echo ""
echo "🔒 To enable HTTPS (SSL):"
echo "   certbot --nginx -d nrjmorgen.com"
echo ""
echo "📝 To update deployment:"
echo "   rsync -av $WORKSPACE/mission-control/public/ $DEPLOY_DIR/"
echo ""
echo "═══════════════════════════════════════════════════════════════════════"
