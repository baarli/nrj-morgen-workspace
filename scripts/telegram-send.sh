#!/bin/bash
#
# telegram-send.sh
# Sender melding til bruker via Telegram
#

source /root/.openclaw/workspace/.credentials/telegram-bot.env

if [ -z "$1" ]; then
    echo "Bruk: telegram-send.sh 'Din melding her'"
    exit 1
fi

MESSAGE="$1"

echo "=== Sender melding til Telegram ==="
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -d "chat_id=${TELEGRAM_CHAT_ID}" \
  -d "text=${MESSAGE}" \
  -d "parse_mode=HTML" | \
  python3 -m json.tool

echo ""
echo "=== Melding sendt ==="
