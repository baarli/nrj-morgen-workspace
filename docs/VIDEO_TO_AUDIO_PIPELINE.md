# Video-til-Lyd Pipeline for NRJ Morgen

## Mål
Automatisk hente ut lyd fra videoer i nyhetssaker, klippe ut aktuelle sitater, og laste opp til content-hub.

## Hva som skal til

### 1. Verktøy for nedlasting og prosessering

**Påkrevde verktøy:**
```bash
# yt-dlp - For å laste ned videoer fra nettsider
pip install yt-dlp

# ffmpeg - For å konvertere video til lyd og klippe
apt-get install ffmpeg  # Ubuntu/Debian
brew install ffmpeg     # macOS

# whisper - OpenAI's tale-til-tekst (valgfritt, for transkripsjon)
pip install openai-whisper
```

### 2. Pipeline-steg

```
Nyhetssak med video
       ↓
1. Identifiser video-URL
       ↓
2. Last ned video (yt-dlp)
       ↓
3. Ekstraher lyd (ffmpeg)
       ↓
4. Transkriber (whisper/AI)
       ↓
5. Identifiser beste sitater (AI)
       ↓
6. Klipp ut sitater (ffmpeg)
       ↓
7. Last opp til content-hub
       ↓
8. Link til sak i Supabase
```

### 3. Implementasjon

**Nytt script:** `video-to-audio-pipeline.py`

Funksjoner:
- Sjekker om sak har video (scraper nettside)
- Laster ned video
- Ekstraherer lyd til MP3
- Bruker AI til å finne beste sitater
- Kliper ut 10-30 sekunders klipp
- Laster opp til content-hub via API

**Integrasjon med morgenrutine:**
- Etter at 10 saker er funnet
- For hver sak: sjekk om video finnes
- Hvis ja: kjør pipeline
- Maks 3-5 videoer per morgen (tidsbegrensning)

### 4. API-endepunkter for content-hub

```python
# Last opp fil til content-hub
POST /api/content-hub/upload
Content-Type: multipart/form-data

Body:
- file: <audio-file.mp3>
- title: "Sitat: [Person] - [Tema]"
- description: "Fra: [Kilde] | Sak: [Tittel]"
- tags: ["nyheter", "sitat", "2025-02-21"]
- related_agenda_item_id: "<sak-id>"
```

### 5. Kostnader

| Komponent | Kostnad |
|-----------|---------|
| OpenAI Whisper API | ~$0.006/minutt |
| Storage (Supabase) | ~$0.025/GB |
| Compute | Eksisterende server |
| **Total per video** | ~$0.05-0.10 |

### 6. Tidsbruk

| Steg | Tid |
|------|-----|
| Nedlasting | 10-30 sek |
| Ekstrahering | 5-10 sek |
| Transkripsjon | 1-2 min |
| Sitat-utvelgelse | 30 sek |
| Klipping | 5-10 sek |
| Opplasting | 10-20 sek |
| **Total per video** | ~2-3 minutter |

### 7. Begrensninger

- **Copyright:** Må sjekke om vi har rettigheter til å bruke klipp
- **Kvalitet:** Avhengig av video-kvalitet
- **Tid:** Maks 3-5 videoer per morgen pga. tidsbruk
- **Lagring:** Supabase har 1GB gratis, deretter $0.025/GB

## Implementasjonsforslag

### Fase 1: MVP (1-2 dager)
- Script som laster ned 1 video, ekstraherer lyd, laster opp
- Manuel utvelgelse av videoer

### Fase 2: Automatisering (3-5 dager)
- Integrasjon med morgenrutine
- AI-basert sitat-utvelgelse
- Automatisk opplasting

### Fase 3: Forbedringer (1 uke)
- Batch-prosessering
- Kvalitets-sjekk
- Feilhåndtering

## Vil du at jeg skal:
1. **Lage MVP-scriptet** (laste ned 1 video → lyd → content-hub)?
2. **Integrere med morgenrutinen** (automatisk hver morgen)?
3. **Vent til senere** (fokus på andre ting først)?
