#!/usr/bin/env python3
# /root/.openclaw/workspace/scripts/send-daily-email.py
# Sender daglig SHOWPREPP via Gmail SMTP

import smtplib
import ssl
import sys
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from datetime import datetime
import re

def load_credentials():
    """Last credentials fra .env fil"""
    creds = {}
    env_file = '/root/.openclaw/workspace/.credentials/nrj-morgen.env'
    
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    creds[key] = value
    return creds

def markdown_to_showprepp_html(markdown_text):
    """Konverter markdown til mobilvennlig SHOWPREPP HTML"""
    html = markdown_text
    
    # Headers - tydelige og store
    html = re.sub(r'^# (.*?)$', r'<h1 style="color: #ff6b00; font-size: 24px; margin: 0 0 15px 0; padding: 10px; background: #fff3e6; border-left: 5px solid #ff6b00;">\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h2 style="color: #333; font-size: 18px; margin: 25px 0 10px 0; border-bottom: 2px solid #ff6b00; padding-bottom: 5px;">\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.*?)$', r'<h3 style="color: #666; font-size: 16px; margin: 20px 0 8px 0;">\1</h3>', html, flags=re.MULTILINE)
    
    # Bold - tydelig
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong style="color: #000;">\1</strong>', html)
    
    # Emojis - behold dem
    # Ingen endring nødvendig
    
    # Avsnitt - god lesbarhet
    html = re.sub(r'\n\n', '</div><div style="margin: 15px 0;">', html)
    
    # Wrap i container
    html = '<div style="margin: 10px 0;">' + html + '</div>'
    
    return html

def send_showprepp_email(report_file, to_email):
    """Send SHOWPREPP e-post via Gmail"""
    creds = load_credentials()
    
    gmail_user = creds.get('GMAIL_USER', 'baarliclaw@gmail.com')
    gmail_pass = creds.get('GMAIL_APP_PASSWORD', creds.get('GMAIL_PASS', ''))
    
    if not gmail_pass:
        print("❌ Gmail app-passord ikke funnet i credentials")
        return False
    
    # Les rapport
    if not os.path.exists(report_file):
        print(f"❌ Rapport ikke funnet: {report_file}")
        return False
    
    with open(report_file, 'r', encoding='utf-8') as f:
        report_content = f.read()
    
    # Lag e-post
    msg = MIMEMultipart('alternative')
    msg['From'] = gmail_user
    msg['To'] = to_email
    
    # Subject med dato
    today = datetime.now().strftime('%A %d. %B')
    msg['Subject'] = Header(f'📻 NRJ MORGEN SHOWPREPP - {today}', 'UTF-8')
    
    # Tekst-versjon (for eldre klienter)
    text_part = MIMEText(report_content, 'plain', 'UTF-8')
    
    # HTML-versjon - optimalisert for mobil/lesing i taxi
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif; 
                line-height: 1.6; 
                color: #333; 
                max-width: 100%; 
                margin: 0; 
                padding: 15px;
                font-size: 16px;
                background: #fff;
            }}
            h1 {{ 
                color: #ff6b00; 
                font-size: 22px; 
                margin: 0 0 15px 0; 
                padding: 12px; 
                background: #fff3e6; 
                border-left: 5px solid #ff6b00;
                border-radius: 0 8px 8px 0;
            }}
            h2 {{ 
                color: #333; 
                font-size: 18px; 
                margin: 25px 0 10px 0; 
                border-bottom: 2px solid #ff6b00; 
                padding-bottom: 5px;
            }}
            h3 {{ 
                color: #555; 
                font-size: 16px; 
                margin: 20px 0 8px 0;
                font-weight: 600;
            }}
            strong {{ color: #000; font-weight: 600; }}
            p {{ margin: 10px 0; }}
            hr {{ 
                border: none; 
                border-top: 1px solid #ddd; 
                margin: 20px 0; 
            }}
            .emoji {{ font-size: 1.2em; }}
            .footer {{ 
                color: #666; 
                font-size: 12px; 
                margin-top: 30px; 
                padding-top: 15px; 
                border-top: 2px solid #ff6b00;
                text-align: center;
            }}
            .quick-info {{
                background: #f8f9fa;
                padding: 15px;
                border-radius: 8px;
                margin: 15px 0;
            }}
            .quick-info table {{
                width: 100%;
                border-collapse: collapse;
            }}
            .quick-info td {{
                padding: 8px;
                border-bottom: 1px solid #ddd;
            }}
            .quick-info td:first-child {{
                font-weight: 600;
                color: #555;
                width: 40%;
            }}
            a {{ color: #ff6b00; text-decoration: none; }}
            a:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        {markdown_to_showprepp_html(report_content)}
        <div class="footer">
            <p>🎙️ <strong>Kimi Claw</strong> - Din AI-assistent for NRJ Morgen</p>
            <p>Generert: {datetime.now().strftime('%H:%M')} | Neste rapport: I morgen 05:50</p>
        </div>
    </body>
    </html>
    """
    html_part = MIMEText(html_content, 'html', 'UTF-8')
    
    msg.attach(text_part)
    msg.attach(html_part)
    
    # Send via Gmail SMTP
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(gmail_user, gmail_pass)
            server.sendmail(gmail_user, to_email, msg.as_string())
        
        print(f"✅ Showprepp sendt til {to_email}")
        return True
        
    except Exception as e:
        print(f"❌ Feil ved sending: {e}")
        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        # Standard: send dagens rapport
        date_str = datetime.now().strftime('%Y-%m-%d')
        report_file = f'/root/.openclaw/workspace/brain/reports/daily-report-{date_str}.md'
        to_email = 'niklasbaarli@gmail.com'  # Standard mottaker
    else:
        report_file = sys.argv[1]
        to_email = sys.argv[2] if len(sys.argv) > 2 else 'niklasbaarli@gmail.com'
    
    success = send_showprepp_email(report_file, to_email)
    sys.exit(0 if success else 1)
