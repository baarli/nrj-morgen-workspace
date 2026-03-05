#!/bin/bash
#
# telegram-reply.sh
# Svar på en melding fra Telegram
#
# Bruk: telegram-reply.sh "Ditt svar her"
#

source /root/.openclaw/workspace/.credentials/telegram-bot.env

if [ -z "$1" ]; then
    echo "Bruk: telegram-reply.sh 'Ditt svar her'"
    echo ""
    echo "Chat ID: $TELEGRAM_CHAT_ID"
    exit 1
fi

MESSAGE="$1"

echo "=== Sender svar til Telegram ==="
echo "Til: Chat ID $TELEGRAM_CHAT_ID"
echo "Melding: $MESSAGE"
echo ""

curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -d "chat_id=${TELEGRAM_CHAT_ID}" \
  -d "text=${MESSAGE}" \
  -d "parse_mode=HTML" | \
  python3 -m json.tool

echo ""
echo "=== Svar sendt ==="
