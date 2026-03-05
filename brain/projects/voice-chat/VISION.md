# Voice Chat Integration for Mission Control

## Visjon
Brukeren og Vev snakker sammen via Mission Control med stemmer.

## Arkitektur

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Brukerens     │────>│  Mission Control │────>│   Supabase      │
│   Mikrofon      │     │  (Web Speech API)│     │  (Real-time)    │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                               │                           │
                               │                           │
                               v                           v
                        ┌──────────────────┐     ┌─────────────────┐
                        │  Speech-to-Text  │     │   Vev (meg)     │
                        │  (Browser API)   │     │                 │
                        └──────────────────┘     └─────────────────┘
                                                        │
                                                        v
                                               ┌─────────────────┐
                                               │  Text-to-Speech │
                                               │  (OpenClaw TTS) │
                                               └─────────────────┘
                                                        │
                                                        v
                                               ┌─────────────────┐
                                               │   Audio Output  │
                                               │   (Brukeren)    │
                                               └─────────────────┘
```

## Komponenter

### 1. Frontend (Mission Control)
- **Voice activation button** - Start/stop lytte
- **Speech recognition** - Web Speech API
- **Visual feedback** - Viser når Vev lytter/snakket
- **Chat history** - Tekstlogg av samtalen

### 2. Backend (Supabase Edge Function)
- **Mottar tekst** fra frontend
- **Sender til Vev** via OpenClaw
- **Mottar svar** fra Vev
- **Returnerer til frontend**

### 3. Vev (Meg)
- **Mottar tekst** fra Supabase
- **Genererer svar**
- **Sender TTS** via OpenClaw
- **Returnerer tekst + audio URL**

## Implementasjonssteg

### Steg 1: Frontend UI
- Legge til voice-knapp i Mission Control
- Implementere Web Speech API
- Vise "listening..." indicator

### Steg 2: Supabase Edge Function
- Opprette `voice-chat` edge function
- Koble til OpenClaw gateway
- Håndtere real-time updates

### Steg 3: Vev Integration
- Lytte på voice-chat kanal
- Generere svar
- Sende TTS

## Tekniske Detaljer

### Web Speech API
```javascript
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = 'nb-NO'; // Norsk
recognition.continuous = false;
recognition.interimResults = false;

recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    sendToVev(transcript);
};
```

### Supabase Real-time
```javascript
const channel = supabase
    .channel('voice-chat')
    .on('broadcast', { event: 'vev-response' }, (payload) => {
        playAudio(payload.audio_url);
    })
    .subscribe();
```

### OpenClaw TTS
```python
# Via OpenClaw tts tool
audio_path = tts(text=response_text)
# Upload to storage
audio_url = upload_to_supabase_storage(audio_path)
```

## Neste Steg

1. ✅ Designe UI for Mission Control
2. Implementere Web Speech API
3. Sette opp Supabase edge function
4. Teste end-to-end flow

## Status
**STARTET:** 2026-03-05
**Mål:** Fungereende voice chat i Mission Control
