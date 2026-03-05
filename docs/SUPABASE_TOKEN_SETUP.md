# Supabase Access Token - Hvordan generere

## Hvorfor trengs det?
For å deploye Edge Functions fra CLI trengs et Supabase Personal Access Token.

## Hvordan generere:

1. **Gå til Supabase Dashboard:**
   https://app.supabase.com/account/tokens

2. **Klikk "New Token"**

3. **Fyll inn:**
   - Token name: `NRJ-Morgen-Deploy`
   - Expiration: Velg passende (f.eks. 90 dager)

4. **Kopier token** (vises kun én gang!)

5. **Lagre token:**
   ```bash
   # Legg til i credentials
   echo 'SUPABASE_ACCESS_TOKEN=din_token_her' >> /root/.openclaw/workspace/.credentials/nrj-morgen.env
   ```

6. **Deploy funksjon:**
   ```bash
   cd /root/.openclaw/workspace/nrjmorgen-ui
   export SUPABASE_ACCESS_TOKEN=din_token_her
   npx supabase functions deploy process-video
   ```

## Alternativ: Deploy via Dashboard

Hvis du ikke vil bruke CLI:

1. Gå til: https://app.supabase.com/project/kvniauxokdtmpvjtfnej/functions
2. Klikk "New Function"
3. Velg "Create from scratch"
4. Navn: `process-video`
5. Kopier innholdet fra `supabase/functions/process-video/index.ts`
6. Klikk "Deploy"

## Verifiser deploy

```bash
# Test funksjonen
curl -X POST https://kvniauxokdtmpvjtfnej.supabase.co/functions/v1/process-video \
  -H "Authorization: Bearer din_anon_key" \
  -H "Content-Type: application/json" \
  -d '{"videoUrl": "https://example.com/video"}'
```
