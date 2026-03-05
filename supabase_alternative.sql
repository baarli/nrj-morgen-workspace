-- ============================================
-- ALTERNATIV LØSNING: Bruk eksisterende tabeller
-- ============================================

-- Siden vi ikke har direkte SQL-tilgang, kan vi bruke agenda_items 
-- med en spesiell category for å simulere kommandoer

-- 1. Legg til nye kategorier for agent-kommunikasjon
-- Dette kan gjøres via REST API

-- 2. Bruk følgende struktur i agenda_items:
-- category = 'AGENT_COMMAND' for kommandoer
-- category = 'AGENT_RESPONSE' for svar
-- category = 'APPROVAL_REQUEST' for godkjenning
-- category = 'SYSTEM_STATUS' for status
-- category = 'ACTIVITY_LOG' for logg

-- Eksempel på kommando (JSON i description-feltet):
{
  "type": "command",
  "command_type": "task",
  "data": {
    "task": "morning_routine",
    "date": "2026-03-05"
  },
  "priority": "high",
  "status": "pending"
}

-- Eksempel på respons:
{
  "type": "response",
  "command_id": "...",
  "response_type": "result",
  "data": {
    "success": true,
    "message": "Ferdig"
  }
}

-- Denne løsningen er midlertidig men funksjonell!
