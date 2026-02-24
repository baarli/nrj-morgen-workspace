#!/usr/bin/env python3
"""
Send Mission Control fil via Gmail
"""

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from pathlib import Path

# Gmail settings
GMAIL_USER = "baarliclaw@gmail.com"
GMAIL_PASSWORD = "urarfguqcvpxofft"
TO_EMAIL = "niklasbaarli@gmail.com"

# Fil å sende
FILE_PATH = "/root/.openclaw/workspace/mission-control-deploy.zip"
FILE_NAME = "mission-control-deploy.zip"

def send_email():
    # Create message
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = TO_EMAIL
    msg['Subject'] = "🚀 BaarliClaw Mission Control - Deploy Package"
    
    # Email body
    body = """
Hei!

Her er Mission Control deploy-pakken du etterspurte.

📦 FIL: mission-control-deploy.zip (6.1 KB)
🔐 PASSORD: kloakontroll2026

INSTRUKSJONER:
1. Pakk ut ZIP-filen
2. Last opp til nrjmorgen.com/kloakontroll
3. Åpne i browser
4. Logg inn med admin / kloakontroll2026

FUNKSJONER:
✅ Real-time system metrics
✅ Live logs streaming
✅ Automation control
✅ Skills management
✅ Security monitoring
✅ Responsive design

Hvis du trenger hjelp med deploy, si ifra!

Mvh,
BaarliClaw 🤖
"""
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Attach file
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'rb') as f:
            attachment = MIMEBase('application', 'zip')
            attachment.set_payload(f.read())
        
        encoders.encode_base64(attachment)
        attachment.add_header(
            'Content-Disposition',
            f'attachment; filename= {FILE_NAME}'
        )
        msg.attach(attachment)
        print(f"✅ File attached: {FILE_NAME}")
    else:
        print(f"❌ File not found: {FILE_PATH}")
        return False
    
    # Send email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        
        text = msg.as_string()
        server.sendmail(GMAIL_USER, TO_EMAIL, text)
        server.quit()
        
        print(f"✅ Email sent successfully to {TO_EMAIL}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

if __name__ == "__main__":
    print("📧 Sending Mission Control deploy package...")
    print(f"   From: {GMAIL_USER}")
    print(f"   To: {TO_EMAIL}")
    print(f"   File: {FILE_PATH}")
    print()
    
    success = send_email()
    
    if success:
        print("\n🎉 Email sent! Check your inbox (and spam folder).")
    else:
        print("\n❌ Failed to send email.")
