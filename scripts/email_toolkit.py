#!/usr/bin/env python3
"""
📧 BAARLICLAW EMAIL TOOLKIT
E-post automatisering
"""

import os
import sys
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Optional, Dict
from dataclasses import dataclass

sys.path.insert(0, '/root/.openclaw/workspace/scripts')
from baarliclaw_toolkit import setup_logging

logger = setup_logging("EmailToolkit")

@dataclass
class EmailMessage:
    """Email message structure"""
    subject: str
    body: str
    to: List[str]
    from_addr: str = ""
    html_body: Optional[str] = None
    attachments: List[str] = None
    
    def __post_init__(self):
        if self.attachments is None:
            self.attachments = []

class EmailSender:
    """Send emails via SMTP"""
    
    def __init__(self, smtp_server: str = "", smtp_port: int = 587,
                 username: str = "", password: str = ""):
        self.smtp_server = smtp_server or os.environ.get('SMTP_SERVER', '')
        self.smtp_port = smtp_port
        self.username = username or os.environ.get('SMTP_USERNAME', '')
        self.password = password or os.environ.get('SMTP_PASSWORD', '')
    
    def send(self, message: EmailMessage) -> bool:
        """Send an email"""
        if not all([self.smtp_server, self.username, self.password]):
            logger.error("SMTP credentials not configured")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = message.subject
            msg['From'] = message.from_addr or self.username
            msg['To'] = ', '.join(message.to)
            
            # Add text body
            msg.attach(MIMEText(message.body, 'plain'))
            
            # Add HTML body if provided
            if message.html_body:
                msg.attach(MIMEText(message.html_body, 'html'))
            
            # Add attachments
            for filepath in message.attachments:
                if os.path.exists(filepath):
                    with open(filepath, 'rb') as f:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {os.path.basename(filepath)}'
                    )
                    msg.attach(part)
            
            # Send
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.username, self.password)
                server.send_message(msg)
            
            logger.info(f"Email sent to {', '.join(message.to)}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
    
    def send_simple(self, to: str, subject: str, body: str) -> bool:
        """Send simple text email"""
        message = EmailMessage(
            subject=subject,
            body=body,
            to=[to]
        )
        return self.send(message)

class EmailTemplate:
    """Email templates"""
    
    TEMPLATES = {
        "daily_report": {
            "subject": "Daily Report - {date}",
            "body": """Hello,

Here is your daily report for {date}:

{content}

Best regards,
BaarliClaw
"""
        },
        "alert": {
            "subject": "🚨 Alert: {title}",
            "body": """Alert triggered:

Title: {title}
Severity: {severity}
Message: {message}

Time: {timestamp}
"""
        },
        "summary": {
            "subject": "Weekly Summary - {week}",
            "body": """Weekly Summary ({week}):

{summary}

Have a great week!
"""
        }
    }
    
    @classmethod
    def render(cls, template_name: str, **kwargs) -> Dict[str, str]:
        """Render a template"""
        template = cls.TEMPLATES.get(template_name)
        if not template:
            return {"subject": "", "body": ""}
        
        return {
            "subject": template["subject"].format(**kwargs),
            "body": template["body"].format(**kwargs)
        }

# === TESTING ===
if __name__ == "__main__":
    print("📧 BaarliClaw Email Toolkit - Testing")
    print("=" * 50)
    
    # Test template rendering
    print("\n🧪 Testing templates")
    report = EmailTemplate.render(
        "daily_report",
        date="2026-02-27",
        content="- Task 1 completed\n- Task 2 pending"
    )
    print(f"✅ Subject: {report['subject']}")
    
    alert = EmailTemplate.render(
        "alert",
        title="Disk Space Low",
        severity="HIGH",
        message="Disk usage above 90%",
        timestamp="2026-02-27 10:00"
    )
    print(f"✅ Alert subject: {alert['subject']}")
    
    print("\n✅ Email Toolkit ready!")
    print("\nTo send emails, configure SMTP:")
    print("  export SMTP_SERVER=smtp.gmail.com")
    print("  export SMTP_USERNAME=your@email.com")
    print("  export SMTP_PASSWORD=yourpassword")
