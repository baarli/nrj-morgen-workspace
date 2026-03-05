---
name: telegram
description: Send and receive messages via Telegram Bot API for 24/7 communication with user.
---

# Telegram Bot Skill - @Vev_kompis_bot

## Bot Info
**Bot:** @Vev_kompis_bot (navn: Vev)  
**Token:** `8585778087:AAGNtnHCH3ki0fwu-9Hhmm_h37gku49SZQU`  
**Chat ID:** 6426967326 (N B)  
**Credentials:** `/root/.openclaw/workspace/.credentials/telegram-bot.env`  
**Status:** ✅ FUNGERER - To-veis kommunikasjon aktiv

## Hvordan det fungerer
1. Bruker sender melding til @Vev_kompis_bot
2. Jeg sjekker etter meldinger med `telegram-poll.py`
3. Jeg ser meldingen og svarer personlig
4. Svar sendes via `telegram-reply.sh`

## Scripts

### Sjekk nye meldinger
```bash
cd /root/.openclaw/workspace && python3 scripts/telegram-poll.py
```

### Svar på melding
```bash
/root/.openclaw/workspace/scripts/telegram-reply.sh "Ditt svar her"
```

### Send melding
```bash
/root/.openclaw/workspace/scripts/telegram-send.sh "Melding"
```

## API Endpoints

### Send Message
```bash
curl -s -X POST "https://api.telegram.org/bot8585778087:AAGNtnHCH3ki0fwu-9Hhmm_h37gku49SZQU/sendMessage" \
  -d "chat_id=6426967326" \
  -d "text=Ditt svar"
```

### Get Updates
```bash
curl -s "https://api.telegram.org/bot8585778087:AAGNtnHCH3ki0fwu-9Hhmm_h37gku49SZQU/getUpdates"
```

## Viktig å huske
- Bruker: N B (Chat ID: 6426967326)
- Bot: @Vev_kompis_bot (navn: Vev)
- Token: 8585778087:AAGNtnHCH3ki0fwu-9Hhmm_h37gku49SZQU
- Kommunikasjon: To-veis, jeg svarer personlig
