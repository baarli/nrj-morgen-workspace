#!/bin/bash
set -e  # Exit on error
# /root/.openclaw/workspace/scripts/send-daily-email.sh
# Sender daglig rapport via Gmail

# Last credentials
source /root/.openclaw/workspace/.credentials/nrj-morgen.env

# Konfigurasjon
DATE=$(date +%Y-%m-%d)
REPORT_FILE="/root/.openclaw/workspace/brain/reports/daily-report-$DATE.md"
TO_EMAIL="petter@nrj.no"  # Endre til din e-post
FROM_EMAIL="$GMAIL_USER"

# Sjekk om rapport finnes
if [ ! -f "$REPORT_FILE" ]; then
  echo "Rapport ikke funnet: $REPORT_FILE"
  exit 1
fi

# Les rapporten
REPORT_CONTENT=$(cat "$REPORT_FILE")

# Konverter Markdown til ren tekst for e-post
REPORT_TEXT=$(echo "$REPORT_CONTENT" | sed 's/^# //g; s/^## //g; s/^### //g; s/^- //g; s/\*\*//g; s/`//g')

# Lag e-post (MIME format)
SUBJECT="=?UTF-8?B?$(echo -n "📊 NRJ Morgen - Daglig Rapport $DATE" | base64 -w 0)?="
BOUNDARY="$(date +%s%N)"

# Lag temp-fil for e-post
EMAIL_TEMP=$(mktemp)

{
echo "From: $FROM_EMAIL"
echo "To: $TO_EMAIL"
echo "Subject: $SUBJECT"
echo "MIME-Version: 1.0"
echo "Content-Type: multipart/alternative; boundary=\"$BOUNDARY\""
echo ""
echo "--$BOUNDARY"
echo "Content-Type: text/plain; charset=UTF-8"
echo "Content-Transfer-Encoding: 8bit"
echo ""
echo "$REPORT_TEXT"
echo ""
echo "--$BOUNDARY"
echo "Content-Type: text/html; charset=UTF-8"
echo "Content-Transfer-Encoding: 8bit"
echo ""
echo "<html><body style='font-family: Arial, sans-serif; line-height: 1.6; color: #333;'>"
echo "<h1 style='color: #1a73e8;'>📊 NRJ Morgen - Daglig Rapport</h1>"
echo "<p><strong>Dato:</strong> $DATE</p>"
echo "<hr style='border: none; border-top: 2px solid #1a73e8; margin: 20px 0;'>"

# Konverter markdown til HTML
HTML_CONTENT=$(echo "$REPORT_CONTENT" | \
  sed 's/^# \(.*\)/<h1 style="color: #1a73e8; border-bottom: 2px solid #1a73e8; padding-bottom: 10px;">\1<\/h1>/g' | \
  sed 's/^## \(.*\)/<h2 style="color: #333; margin-top: 30px;">\1<\/h2>/g' | \
  sed 's/^### \(.*\)/<h3 style="color: #666;">\1<\/h3>/g' | \
  sed 's/^- \(.*\)/<li>\1<\/li>/g' | \
  sed 's/^| \(.*\) |/<tr><td>\1<\/td><\/tr>/g' | \
  sed 's/\*\*\(.*\)\*\*/<strong>\1<\/strong>/g' | \
  sed 's/`\(.*\)`/<code style="background: #f4f4f4; padding: 2px 5px; border-radius: 3px;">\1<\/code>/g' | \
  sed 's/✅/<span style="color: green;">✅<\/span>/g' | \
  sed 's/⚠️/<span style="color: orange;">⚠️<\/span>/g' | \
  sed 's/❌/<span style="color: red;">❌<\/span>/g' | \
  sed 's/⏳/<span style="color: blue;">⏳<\/span>/g')

echo "$HTML_CONTENT"

echo "<hr style='border: none; border-top: 1px solid #ddd; margin: 30px 0;'>"
echo "<p style='color: #666; font-size: 12px;'>Denne rapporten ble generert automatisk av Kimi Claw - Din AI-assistent for NRJ Morgen</p>"
echo "</body></html>"
echo ""
echo "--${BOUNDARY}--"
} > "$EMAIL_TEMP"

# Send e-post via Gmail SMTP
# Bruker curl med SMTP

# Alternativ 1: Bruk sendmail hvis tilgjengelig
if which sendmail > /dev/null 2>&1; then
  sendmail -t < "$EMAIL_TEMP"
  echo "✅ E-post sendt via sendmail til $TO_EMAIL"
  
# Alternativ 2: Bruk msmtp hvis tilgjengelig
elif which msmtp > /dev/null 2>&1; then
  msmtp -t < "$EMAIL_TEMP"
  echo "✅ E-post sendt via msmtp til $TO_EMAIL"
  
# Alternativ 3: Bruk Python med smtplib
elif which python3 > /dev/null 2>&1; then
  python3 << PYTHON_SCRIPT
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

# Les e-post fra fil
with open('$EMAIL_TEMP', 'r') as f:
    email_content = f.read()

# Parse e-post
lines = email_content.split('\n')
msg = MIMEMultipart('alternative')
msg['From'] = '$FROM_EMAIL'
msg['To'] = '$TO_EMAIL'
msg['Subject'] = Header('📊 NRJ Morgen - Daglig Rapport $DATE', 'UTF-8')

# Finn HTML-del
html_start = email_content.find('<html>')
html_end = email_content.find('</html>') + 7
text_start = email_content.find('Content-Type: text/plain')
text_end = email_content.find('Content-Type: text/html')

if html_start > 0 and text_start > 0:
    text_content = email_content[text_start:text_end].split('\n\n', 1)[1] if '\n\n' in email_content[text_start:text_end] else ''
    html_content = email_content[html_start:html_end]
    
    part1 = MIMEText(text_content, 'plain', 'UTF-8')
    part2 = MIMEText(html_content, 'html', 'UTF-8')
    
    msg.attach(part1)
    msg.attach(part2)

try:
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login('$GMAIL_USER', '$GMAIL_PASS')
        server.sendmail('$FROM_EMAIL', '$TO_EMAIL', msg.as_string())
    print('✅ E-post sendt via Gmail SMTP til $TO_EMAIL')
except Exception as e:
    print(f'❌ Feil ved sending: {e}')
PYTHON_SCRIPT

else
  echo "❌ Ingen e-postklient funnet (sendmail, msmtp, eller python3)"
  echo "Rapporten er lagret her: $REPORT_FILE"
  exit 1
fi

# Rydd opp
rm -f "$EMAIL_TEMP"

echo ""
echo "📧 Rapport sendt!"
echo "   Til: $TO_EMAIL"
echo "   Fra: $FROM_EMAIL"
echo "   Dato: $DATE"
