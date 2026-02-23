# PODKAST KLIPP-STRATEGI FOR SOSIALE MEDIER
## NRJ Morgen Podkast & Baarli og Benjamin går i terapi

---

## STATUS: ✅ IMPLEMENTERT

**Siste oppdatering:** 2026-02-21
**System:** Automatisk daglig klippe-generering
**Podcast:** Baarli og Benjamin går i terapi (157 episoder)

---

## SYSTEM-ARKITEKTUR

### Komponenter
```
RSS Feed → podcast-clipper.py → FFmpeg → Klipp → (Video) → SoMe
```

**Filer:**
- `/root/.openclaw/workspace/scripts/podcast-clipper.py` - Hovedverktøy
- `/root/.openclaw/workspace/scripts/daily-podcast-clips.sh` - Daglig rutine
- `/tmp/podcast-clips/YYYYMMDD/` - Midlertidig lagring

### RSS Feed
- **URL:** https://rss.podplaystudio.com/4035.xml
- **Siste episode:** "Handleapp, hyperfokus og husfred på prøve" (16. feb 2026)
- **Antall episoder:** 157
- **Audio-host:** bauernordic-pods.sharp-stream.com

---

## AUTOMATISERT ARBEIDSFLYT

### Daglig kjøring (07:00)
```bash
# Cron-job: PODKAST – Daglig klipp-posting
cd /root/.openclaw/workspace/scripts
bash daily-podcast-clips.sh
```

### Steg-for-steg
1. **Hent RSS-feed** - Parse siste episoder
2. **Sjekk for duplikat** - Unngå å prosessere samme episode 2x
3. **Last ned MP3** - ~28MB per episode
4. **Analyser audio** - Finn beste øyeblikk (mock → pydub i fremtiden)
5. **Lag 3 klipp** - 30 sekunder hver med ffmpeg
6. **Konverter til video** (TODO) - Krever video-maler
7. **Post til SoMe** (TODO) - Krever API-tilgang

---

## KLIPP-TYPER

### Klipp 1: Laughter (Morsomt øyeblikk)
- **Tidspunkt:** ~2:00 inn i episoden
- **Lengde:** 30 sekunder
- **Formål:** Fange oppmerksomhet, humor
- **Platform:** TikTok/Reels (morgenpost)

### Klipp 2: Conversation (Relatable)
- **Tidspunkt:** ~7:30 inn i episoden
- **Lengde:** 30 sekunder
- **Formål:** Noe folk kjenner seg igjen i
- **Platform:** Instagram Stories (ettermiddag)

### Klipp 3: Reaction (Bak kulissene)
- **Tidspunkt:** ~14:50 inn i episoden
- **Lengde:** 30 sekunder
- **Formål:** Autentiske øyeblikk
- **Platform:** TikTok/Reels (kveld)

---

## POSTING-SKJEMA

### Daglig (7 dager i uken)
| Tid | Platform | Innhold | Klipp # |
|-----|----------|---------|---------|
| 07:00 | Reel/TikTok | Morsomt øyeblikk | #1 |
| 15:00 | Story | Relatable quote | #2 |
| 19:00 | Reel/TikTok | Bak kulissene | #3 |

### Ukentlig
- **Mandag:** Ukens høydepunkter
- **Onsdag:** Midt-uke teaser
- **Fredag:** Helgehumor
- **Søndag:** Best of uken

---

## TEKNISK SPEC

### Output-format
- **Audio:** MP3, 128kbps, stereo
- **Video:** 1080x1920 (9:16), 30fps (TODO)
- **Lengde:** 15-60 sekunder
- **Tekst:** Store, lesbare undertekster (TODO)

### Mappestruktur
```
/tmp/podcast-clips/
└── 20260221/
    ├── Handleapp_hyperfokus_og_husfre.mp3 (28MB)
    ├── clip_0_laughter.mp3 (471KB, 30s)
    ├── clip_1_conversation.mp3 (470KB, 30s)
    ├── clip_2_reaction.mp3 (470KB, 30s)
    ├── moments.json
    ├── latest_episode.txt
    └── daily-clips.log
```

---

## BRUK AV VERKTØYET

### Kommandolinje
```bash
# Hent siste episoder
python3 podcast-clipper.py fetch-latest

# List episoder
python3 podcast-clipper.py list --limit 5

# Last ned episode
python3 podcast-clipper.py download --episode-index 0 --output-dir ./clips

# Lag klipp
python3 podcast-clipper.py create-clip \
  --file episode.mp3 \
  --start 120 \
  --end 150 \
  --output clip.mp3
```

### Bash-script
```bash
# Manuell kjøring
cd /root/.openclaw/workspace/scripts
bash daily-podcast-clips.sh

# Se resultater
ls -la /tmp/podcast-clips/$(date +%Y%m%d)/
```

---

## MÅLING AV SUKSESS

### KPI-er (når SoMe-API er på plass)
- **Views** per klipp
- **Engagement rate** (likes, comments, shares)
- **Follower growth**
- **Link clicks** til podkast
- **New listeners** (sporbar via unike koder)

### Tekniske metrics
- Antall klipp generert per dag
- Suksessrate for nedlasting
- Tid brukt per episode

---

## HUSKELISTE

### Før hver post (når manuell):
- [ ] Klipp er under 60 sekunder
- [ ] Tekst er stor og lesbar
- [ ] Har trending lyd/effekt
- [ ] Inkluderer call-to-action ("Hør hele episoden!")
- [ ] Bruker relevante hashtags
- [ ] Har link i bio/beskrivelse

---

## NESTE STEG

### Prioritet 1: Video-generering
- [ ] Lag video-maler (1080x1920)
- [ ] Legg til tekst-overlay med ffmpeg
- [ ] Bakgrunnsgrafikk/bilder
- [ ] Test på TikTok/Instagram

### Prioritet 2: SoMe API-integrasjon
- [ ] Instagram Basic Display API
- [ ] TikTok for Business API
- [ ] Automatisk posting
- [ ] Scheduling

### Prioritet 3: Forbedret analyse
- [ ] Installer pydub for audio-analyse
- [ ] Finn faktiske "beste øyeblikk" basert på:
  - Lydnivå (latter = høyt)
  - Pause-mønstre
  - Talehastighet
- [ ] Whisper-transkribering for tekst

### Prioritet 4: Utvidelse
- [ ] Legg til NRJ Morgen Podkast
- [ ] Flere klipp per episode (5-10)
- [ ] A/B-testing av klipp-typer
- [ ] Automatisk hashtag-generering

---

## RESSURSER

**Skills:**
- `/root/.openclaw/skills/podcast-clipper/SKILL.md`
- `/root/.openclaw/skills/social-scheduler/SKILL.md`

**Scripts:**
- `/root/.openclaw/workspace/scripts/podcast-clipper.py`
- `/root/.openclaw/workspace/scripts/daily-podcast-clips.sh`

**Cron:**
- Jobb: `PODKAST – Daglig klipp-posting (Baarli og Benjamin)`
- Tid: 07:00 daglig
- Neste kjøring: Se `openclaw cron list`

---

*Opprettet: 2026-02-21*
*Sist oppdatert: 2026-02-21 (fungerende implementasjon)*
*Formål: Øke ekte lyttere til NRJ Morgen Podkast og Baarli og Benjamin går i terapi*
