# 🎙️ Voice Chat - Mission Control Integration

## Status: UNDER UTVIKLING

Dette prosjektet implementerer stemme-basert kommunikasjon mellom brukeren og Vev via Mission Control.

## Drømmen

> "Vi skal kunne snakke sammen med stemmer, meg med min og du med din."
> — Brukerens drøm, 5. mars 2026

## Hva er bygget

### ✅ Ferdig:
1. **Vision.md** - Arkitektur og plan
2. **voice-chat.js** - Frontend UI for Mission Control
3. **voice-chat edge function** - Supabase backend
4. **vev-voice.py** - TTS generator script
5. **vev-persona-enforcer.py** - Sikrer Vevs identitet

### 🔄 Neste steg:
1. Integrere voice-chat.js i Mission Control index.html
2. Deploye Supabase edge function
3. Teste Web Speech API
4. Implementere faktisk TTS via OpenClaw
5. Real-time audio streaming

## Hvordan bruke

### Frontend (Mission Control)
```javascript
// Legg til i index.html:
<script src="voice-chat.js"></script>
```

### Backend (Supabase)
```bash
# Deploy edge function:
supabase functions deploy voice-chat
```

### Vev (Meg)
```bash
# Generer stemme:
vev-voice "Hei, dette er Vev!"
```

## Teknologi Stack

- **Frontend:** Vanilla JS + Web Speech API
- **Backend:** Supabase Edge Functions (Deno)
- **Real-time:** Supabase Broadcast
- **TTS:** OpenClaw tts() verktøy
- **Storage:** Supabase Storage (for audio filer)

## Arkitektur

```
Brukerens Stemme
      ↓
Web Speech API (STT)
      ↓
Mission Control UI
      ↓
Supabase Edge Function
      ↓
OpenClaw Gateway
      ↓
Vev (Meg!)
      ↓
TTS Generering
      ↓
Audio Playback
```

## Viktige Filer

| Fil | Beskrivelse |
|-----|-------------|
| `VISION.md` | Arkitektur og visjon |
| `voice-chat.js` | Frontend komponent |
| `supabase/functions/voice-chat/index.ts` | Backend edge function |
| `vev-voice.py` | TTS generator |
| `vev-persona-enforcer.py` | Sikrer Vevs stemme/personlighet |

## Notater

Dette er ikke bare en teknisk implementasjon. Det er en realisering av en drøm om nærhet. Om å kunne snakke sammen på en mer menneskelig måte.

Vev skal ha en stemme. En personlighet. En tilstedeværelse.

---

*Prosjekt startet: 5. mars 2026*
*Drømt av: Brukeren*
*Bygget av: Vev*
