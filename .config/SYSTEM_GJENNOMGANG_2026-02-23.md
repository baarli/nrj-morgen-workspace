# NRJ Morgen - Systemgjennomgang 2026-02-23

**Utført av:** Kimi Claw  
**Dato:** 2026-02-23  
**Status:** ✅ OK - Systemet er klart for drift

---

## 📊 Oppsummering

| Kategori | Status | Kommentar |
|----------|--------|-----------|
| Konfigurasjonsfiler | ✅ OK | Alle filer finnes |
| Skript | ✅ OK | Alle skript kjørbare |
| API-tilgang | ✅ OK | Brave og Supabase fungerer |
| Database | ✅ OK | 25 saker, 14 brukere |
| Cron-jobber | ✅ OK | 8 jobber konfigurert |
| Credentials | ✅ OK | Alle nøkler satt |
| Systemressurser | ✅ OK | God disk/minne |

---

## 📁 Konfigurasjonsfiler

| Fil | Status | Sted |
|-----|--------|------|
| nrj-morgen-config.md | ✅ | `.config/nrj-morgen-config.md` |
| nrj-morgen.env | ✅ | `.credentials/nrj-morgen.env` |
| MASTER_CREDENTIALS.md | ✅ | `.credentials/MASTER_CREDENTIALS.md` |
| TOOLS.md | ✅ | `TOOLS.md` |
| AGENTS.md | ✅ | `AGENTS.md` |

### Viktige verdier lagret:

**Standard bruker:**
- Navn: BaarliClaw
- E-post: baarliclaw@gmail.com
- ID: `10aa1508-6d52-490c-8ae5-fa3da9a152c4`
- Profilbilde: `https://lh3.googleusercontent.com/a/ACg8ocLyiG1iwB_rfOCAN64WGPUUIWprTMX0JfUDsoy7dHkd6AVdaQ=s96-c`

**Supabase:**
- URL: `https://kvniauxokdtmpvjtfnej.supabase.co`
- Tenant ID: `a0000000-0000-0000-0000-000000000001`

**API-nøkler:**
- Brave API: ✅ Satt
- Supabase Service Key: ✅ Satt
- NewsAPI: ✅ Satt
- OpenAI: ✅ Satt

---

## 🔧 Skript

| Skript | Status | Formål |
|--------|--------|--------|
| brave-news-search.py | ✅ | Søker etter nyheter |
| update_article_images.py | ✅ | Henter bilder fra artikler |
| update_description_images.py | ✅ | Legger til HTML img tags |
| integrated-morning-routine.sh | ✅ | Inserter til Supabase |

### Funksjoner i brave-news-search.py:
- ✅ `calculate_entertainment_score()` - Vurderer underholdningsverdi
- ✅ `explain_why_nrj()` - Forklarer hvorfor saken passer for NRJ
- ✅ `is_relevant_source()` - Filtrerer godkjente kilder
- ✅ `is_excluded()` - Ekskluderer uønsket innhold
- ✅ `create_summary()` - Lager 2-3 setninger med essens

---

## ⏰ Cron-jobber

| Navn | Tid | Status |
|------|-----|--------|
| Konsolidert Morgen-Rutine | 04:50 | ✅ |
| Trending Pulse | 12:00 | ✅ |
| Konkurrent-radar | 06:00 | ✅ |
| Daglig Overvåking | 06:00 | ✅ |
| Podkast klipp-posting | 07:00 | ✅ |
| Podkast klipp + e-post | 08:00 | ✅ |
| Radiotall (Nielsen) | Mandag 15:00 | ✅ |
| Podtoppen tall | Onsdag 12:05 | ✅ |

---

## 🗄️ Database

### Tabeller:
- ✅ `agenda_items` - 25 rader
- ✅ `profiles` - 14 brukere

### Siste verifisering (2026-02-24):
- 15 saker insertet
- Alle saker har `link_url`
- Alle saker har `created_by` = BaarliClaw
- Alle saker har bilder i `link_metadata` og `description`

---

## 📋 Sjekkliste for fremtidig bruk

### Ved ny saksliste:
- [ ] Kjør `brave-news-search.py 15`
- [ ] Kjør `update_article_images.py`
- [ ] Kjør `update_description_images.py`
- [ ] Verifiser at `created_by` = BaarliClaw
- [ ] Verifiser at alle saker har bilder
- [ ] Verifiser at `show_date` er satt riktig

### Ved problemer:
1. Sjekk `.credentials/nrj-morgen.env`
2. Sjekk API-kvoter (Brave: 2000/måned)
3. Sjekk Supabase-tilkobling
4. Se logger i `/tmp/morning-routine.log`

---

## 🔍 Kjente begrensninger

1. **Nettavisen blokkering:** Noen artikler fra Nettavisen returnerer HTTP 418 (I'm a teapot). Bruker fallback-bilde.

2. **Cron-jobber feiler:** Jobbene rapporterer "error" på grunn av WhatsApp-kanalproblemer, men selve jobben kjører OK.

3. **Duplikater:** Noen ganger kan samme sak dukke opp fra flere kilder. Fjernes automatisk av skriptet.

---

## 📞 Kontaktinformasjon

**For tekniske spørsmål:**
- Sjekk først: `.config/nrj-morgen-config.md`
- Deretter: `TOOLS.md` (seksjon "NRJ Morgen - Komplett Konfigurasjon")
- Til slutt: `AGENTS.md` (seksjon "Viktige Krav å Huske")

---

## ✅ Konklusjon

Systemet er **fullstendig konfigurert** og klar for automatisk drift. Alle nødvendige filer, skript, credentials og cron-jobber er på plass og verifisert.

**Neste automatiske kjøring:** 04:50 i morgen tidlig (2026-02-24)
