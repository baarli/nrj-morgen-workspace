# AI Tittel-Generering for NRJ Morgen

For å få optimale titler som "Ida Elise Broch søker ny jobb", anbefales følgende tilnærming:

## Alternativ 1: Manuell redigering i nrjmorgen.com (Anbefalt)
- La systemet hente nyheter med Brave API
- Vis originaltittel + beskrivelse i dashboard
- La bruker (Niklas/Baarli) redigere tittelen med ett klikk
- Lagre den formaterte tittelen tilbake til Supabase

## Alternativ 2: AI-integrasjon (krever API-nøkkel)
Krever en av følgende:
- OpenAI API-nøkkel (GPT-4)
- Anthropic API-nøkkel (Claude)
- Google AI API-nøkkel (Gemini)

Med API-nøkkel kan vi:
1. Sende original tittel + beskrivelse til AI
2. Be om konsis 5-7 ords tittel
3. Lagre resultatet i Supabase

## Alternativ 3: Forbedret regel-basert (nåværende)
Bruke avanserte regex-mønstre og erstatninger for å:
- Gjenkjenne navn-mønstre
- Trekke ut handling fra beskrivelse
- Bygge konsise titler

## Anbefaling:
**Start med Alternativ 1** (manuell redigering) for best kontroll,
derettervurdere AI-integrasjon hvis volumet blir for høyt.

Vil du:
1. Legge til manuell tittel-redigering i nrjmorgen.com?
2. Skaffe OpenAI/Claude API-nøkkel for automatisk generering?
3. Forbedre den regel-baserte løsningen?
