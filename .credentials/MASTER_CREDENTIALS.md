# NRJ MORGEN - MASTER CREDENTIALS
# SAMLET OVERSIKT OVER ALLE TOKENS OG API KEYS
# 
# ⚠️  VIKTIG: Denne filen inneholder sensitive data!
# 🔒  IKKE DEL MED NOEN!
# 📝  Oppdatert: 2026-02-21 00:44

================================================================================
SUPABASE (DATABASE & BACKEND)
================================================================================

Project URL:     https://kvniauxokdtmpvjtfnej.supabase.co
Project ID:      kvniauxokdtmpvjtfnej

Service Key:     eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt2bmlhdXhva2R0bXB2anRmbmVqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTM2NzIzNCwiZXhwIjoyMDY2OTQzMjM0fQ.OkhTtq9QAQ3xMzZYKyWyCjj7PiqMZJKSvpA0jcBJqpE
Anon Key:        eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt2bmlhdXhva2R0bXB2anRmbmVqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEzNjcyMzQsImV4cCI6MjA2Njk0MzIzNH0._24RuF95RnxxHj3sjGswdd36VVYlX_jKxut8dvELfSA
Access Token:    sbp_1b7a1be050e14cc714f2a11e9de22d741133c9b4
                 (Gyldig: 90 dager, til ca. 2026-05-22)

Bruk:
- Service Key: Server-side operasjoner (R/W alle data)
- Anon Key: Client-side operasjoner (R/W med RLS)
- Access Token: Deploy Edge Functions

================================================================================
SØK & AI (NYHETSINNHENTING)
================================================================================

Brave Search API:      BSAt0WSIpXP0Hp6sPvNwaaGuLoyewev
                        (Primær kilde for norske nyheter)

NewsAPI:               154c4f3283734a9dba8820939dfacdef
                        (Fallback for internasjonale nyheter)

OpenAI API:            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
                        (AI tittel-generering, GPT-4o-mini)

================================================================================
AUTENTISERING & GIT
================================================================================

NRJ Refresh Token:     5djoyezt2flm
                        (For NRJ Morgen autentisering)

GitHub PAT:            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
GitHub User:           baarli
                        (Full tilgang til repos)

================================================================================
E-POST & KOMMUNIKASJON
================================================================================

Gmail:                 baarliclaw@gmail.com
App Password:          urarfguqcvpxofft
                        (For sending av showprepp)

================================================================================
SYSTEM & TENANT
================================================================================

Tenant ID:             a0000000-0000-0000-0000-000000000001
                        (NRJ Morgen organisasjon)

================================================================================
HENVISNINGER
================================================================================

Primær credentials fil:  /root/.openclaw/workspace/.credentials/nrj-morgen.env
Søk/API credentials:     /root/.openclaw/workspace/.credentials/live-search.env
GitHub config:           /root/.config/gh/hosts.yml
Denne filen:             /root/.openclaw/workspace/.credentials/MASTER_CREDENTIALS.md

================================================================================
BRUK I SCRIPTS
================================================================================

# I bash scripts:
source /root/.openclaw/workspace/.credentials/nrj-morgen.env
export SUPABASE_URL SUPABASE_SERVICE_KEY BRAVE_API_KEY NRJ_REFRESH_TOKEN TENANT_ID

# I Python:
import os
from dotenv import load_dotenv
load_dotenv('/root/.openclaw/workspace/.credentials/nrj-morgen.env')

================================================================================
SIKKERHET
================================================================================

- Roter tokens hver 90. dag
- Bruk aldri Service Key i client-side kode
- Oppbevar backup på trygg lokasjon
- Ikke commit credentials til git (bruk .gitignore)

================================================================================
