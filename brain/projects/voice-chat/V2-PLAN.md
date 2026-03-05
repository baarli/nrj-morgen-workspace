# Voice Chat v2.0 - Utviklingsplan

**Status:** Påbegynt  
**Mål:** Real-time streaming og emosjonell stemme

## Uke 2 Plan

### Dag 8-9: Real-time Streaming (PÅBEGYNT)
- [x] Opprette voice-chat-v2.js med interim results
- [ ] Implementere WebSocket for sanntidskommunikasjon
- [ ] Streaming audio (spill av mens TTS genereres)
- [ ] Redusere ventetid

### Dag 10-11: Emosjonell Stemme
- [ ] Tilpasse tone basert på kontekst
- [ ] Glad, nysgjerrig, alvorlig moduser
- [ ] Teste ulike innstillinger

### Dag 12-14: Testing og Deploy
- [ ] Brukertesting
- [ ] Oppdatere Mission Control
- [ ] Dokumentasjon

## Tekniske Detaljer

### Interim Results
- Web Speech API med `interimResults = true`
- Viser hva som høres mens brukeren snakker
- Raskere respons

### Streaming Audio
- WebSocket for to-veis kommunikasjon
- Chunked audio playback
- Buffer-håndtering

### Emosjonell Stemme
- ElevenLabs voice settings
- Stability og similarity boost
- Kontekst-basert tilpasning

## Neste Steg
1. Implementere WebSocket backend
2. Teste streaming
3. Legge til emosjoner

**Sist oppdatert:** 2026-03-05
