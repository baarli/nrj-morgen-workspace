# NRJ Morgen - Konfigurasjon

**Sist oppdatert:** 2026-02-23
**Formål:** Sentral konfigurasjonsfil for alle NRJ Morgen-relaterte verdier

---

## 🎯 Søksprompt

Utfør et sanntids nyhetssøk optimalisert for NRJ Morgen.

### Mål
Finn de 15 beste og mest underholdende sakene fra siste 24–48 timer som egner seg for kommersiell morgenradio med høyt tempo og bred appell (18–35).

### Innholdskategorier (prioritert)
- Norske og internasjonale kjendisnyheter
- TV-nyheter (underholdning, nye programmer, deltakere, konflikter)
- Reality (drama, brudd, konflikter, avsløringer, exit)
- Influencere og profiler med høy SoMe-rekkevidde
- Skandaler, kontroverser, krangler, rettssaker
- Rød løper, prisutdelinger, film, musikk
- Virale øyeblikk med norsk relevans

### Krav
- Kun saker publisert siste 48 timer (prioriter <24t)
- Kilder: VG, Dagbladet, Nettavisen, TV2, NRK, Se & Hør, Aftenposten + relevante internasjonale tabloider ved stor norsk interesse
- Unngå politiske tungvektsaker uten kjendiskobling
- Prioriter konflikt, overraskelse, brudd, comeback, drama, pinlige øyeblikk, sterke sitater

### Leveranse for hver sak
For hver sak lever:
1. Kort, punchy tittel
2. 2–3 setninger med essens
3. Hvorfor den fungerer på NRJ Morgen (drama, humor, gjenkjennelse, diskusjonspotensial)
4. Publiseringstidspunkt og kilde
5. Direkte lenke

### Sortering
Sorter etter:
1) Aktualitet
2) Underholdningsverdi
3) Snakkis-potensial

### Restriksjoner
Returner kun topp 15. Ingen duplikater. Ingen saker eldre enn 48 timer.

---

## 👤 Standard Bruker

| Egenskap | Verdi |
|----------|-------|
| **Navn** | BaarliClaw |
| **E-post** | `baarliclaw@gmail.com` |
| **ID** | `10aa1508-6d52-490c-8ae5-fa3da9a152c4` |
| **Profilbilde** | `https://lh3.googleusercontent.com/a/ACg8ocLyiG1iwB_rfOCAN64WGPUUIWprTMX0JfUDsoy7dHkd6AVdaQ=s96-c` |

---

## 🖼️ Bilde-krav

### Hver sak MÅ ha:
- `link_metadata`: JSON med `{"image_url": "..."}`
- `description`: HTML img tag: `<img src="..." alt="..." style="max-width:100%;height:auto;border-radius:8px;" />`

### Hvordan hente bilder
Fra artikkelens meta tags:
- `<meta property="og:image" content="...">`
- `<meta name="twitter:image" content="...">`

### Fallback-bilder
| Kilde | URL |
|-------|-----|
| Nettavisen | `https://www.nettavisen.no/logo.png` |
| Dagbladet | `https://www.dagbladet.no/logo.png` |
| Se og Hør | `https://www.seher.no/logo.png` |
| NRK | `https://www.nrk.no/logo.png` |

---

## 📝 Saksliste-data

### Obligatoriske felter
| Felt | Type | Beskrivelse |
|------|------|-------------|
| `title` | string | Kort, punchy tittel |
| `description` | string | HTML img tag med bilde |
| `notes` | string | Oppsummering + kilde |
| `link_url` | string | Direkte lenke til artikkel |
| `link_metadata` | json | `{"image_url": "..."}` |
| `created_by` | uuid | BaarliClaw bruker-ID |
| `category` | string | "TALK" |
| `show_date` | date | Dagens dato |
| `tenant_id` | uuid | `a0000000-0000-0000-0000-000000000001` |

### Notes-format
```
[Første setning fra beskrivelse]

Kilde: [Kildenavn]
```

---

## 🔧 Skript

### Hovedskript
| Skript | Beskrivelse |
|--------|-------------|
| `brave-news-search.py` | Søker etter nyheter |
| `update_article_images.py` | Henter bilder fra artikler |
| `update_description_images.py` | Legger til HTML img tags |
| `integrated-morning-routine.sh` | Inserter til Supabase |

### Kjøringsrekkefølge
1. `brave-news-search.py` → Søk etter nyheter
2. `update_article_images.py` → Hent bilder
3. `update_description_images.py` → Legg til HTML
4. `integrated-morning-routine.sh` → Insert til Supabase

---

## 🗄️ Supabase

### URL
`https://kvniauxokdtmpvjtfnej.supabase.co`

### Tabeller
- `agenda_items` - Sakslista
- `profiles` - Brukerprofiler

### Storage Buckets
- `profile-pictures` - Profilbilder
- `voice-messages` - Lydklipp
- `thumbnails` - Thumbnails
- `media-library` - Mediefiler

---

## ⏰ Cron-jobber

| Navn | Tid | Beskrivelse |
|------|-----|-------------|
| Konsolidert Morgen-Rutine | 04:50 | Henter 15 saker |
| Trending Pulse | 12:00 | Henter 10 saker |
| Daglig Overvåking | 06:00 | Sjekker konkurrenter |
| Konkurrent-radar | 06:00 | Analyserer konkurrenter |

---

## 📁 Filer

### Konfigurasjon
- `.config/nrj-morgen-config.md` - Denne filen
- `.credentials/nrj-morgen.env` - API-nøkler
- `.credentials/MASTER_CREDENTIALS.md` - Master credentials

### Dokumentasjon
- `AGENTS.md` - Viktige krav
- `TOOLS.md` - Komplett konfigurasjon
- `.config/REQUIREMENT_LINK_AND_SUMMARY.md` - Link- og sammendragskrav

---

## ✅ Sjekkliste ved ny saksliste

- [ ] 15 saker hentet
- [ ] Alle saker har `link_url`
- [ ] Alle saker har `notes` med riktig format
- [ ] Alle saker har bilde i `link_metadata`
- [ ] Alle saker har bilde i `description`
- [ ] Alle saker har `created_by` satt til BaarliClaw
- [ ] Alle saker har `category` = "TALK"
- [ ] Alle saker har `show_date` = dagens dato
- [ ] Profilbilde er oppdatert
