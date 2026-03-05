# Telegram Webhook Edge Function

## Konfigurasjon

1. **Deploy funksjonen:**
   ```bash
   cd /root/.openclaw/workspace
   supabase functions deploy telegram-webhook
   ```

2. **Sett miljøvariabler:**
   ```bash
   supabase secrets set TELEGRAM_BOT_TOKEN="din-bot-token"
   ```

3. **Sett webhook URL i Telegram:**
   ```bash
   curl -X POST "https://api.telegram.org/bot<TOKEN>/setWebhook" \
     -d "url=https://kvniauxokdtmpvjtfnej.supabase.co/functions/v1/telegram-webhook"
   ```

## API Endepunkt

Etter deploy er funksjonen tilgjengelig på:
```
https://kvniauxokdtmpvjtfnej.supabase.co/functions/v1/telegram-webhook
```

## Kommandoer som støttes

- `/start` - Velkomstmelding
- `/help` - Hjelp
- `/status` - Systemstatus

## Utvidelse

For å legge til nye funksjoner:
1. Rediger `index.ts`
2. Deploy på nytt med `supabase functions deploy telegram-webhook`
