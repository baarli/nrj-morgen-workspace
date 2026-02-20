# Supabase Access Token Backup

## Token Details

**Token:** `sbp_1b7a1be050e14cc714f2a11e9de22d741133c9b4`

**Type:** Personal Access Token

**Project:** kvniauxokdtmpvjtfnej (NRJ Morgen)

**Generert:** 2026-02-21 00:42

**Gyldig til:** 90 dager (ca. 2026-05-22)

**Bruk:** Deploy Supabase Edge Functions

## Hvordan bruke

```bash
# Sett token
export SUPABASE_ACCESS_TOKEN=sbp_1b7a1be050e14cc714f2a11e9de22d741133c9b4

# Deploy funksjon
npx supabase functions deploy process-video --project-ref kvniauxokdtmpvjtfnej
```

## Hvor er den lagret?

1. **Primær:** `/root/.openclaw/workspace/.credentials/nrj-morgen.env`
2. **Backup:** Denne filen
3. **Dokumentasjon:** `TOOLS.md`

## Fornyelse

Når token utløper:
1. Gå til https://app.supabase.com/account/tokens
2. Slett gammel token
3. Generer ny
4. Oppdater alle filer

---
**VIKTIG:** Ikke del denne token med noen!
