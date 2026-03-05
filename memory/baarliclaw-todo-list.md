# 🔄 BaarliClaw Side - Oppgaver å Fikse

**Dato:** 2026-03-05  
**Status:** Pågående  
**Ansvar:** BaarliClaw (meg)

---

## ✅ FERDIG - Dokumentasjon og Kode

### 1. SQL Setup Script ✅
**Fil:** `/root/.openclaw/workspace/supabase_setup.sql`

Inneholder:
- `agent_commands` - Kommandoer fra Mission Control
- `agent_responses` - Svar fra meg
- `approval_requests` - Godkjenningsforespørsler
- `system_status` - Status fra alle systemer
- `activity_log` - Full logg
- `agent_config` - Konfigurasjon
- Realtime subscriptions enabled
- Default data

**TODO for deg:** Kjør dette i Supabase SQL Editor:
1. Gå til https://supabase.com/dashboard/project/kvniauxokdtmpvjtfnje
2. Åpne SQL Editor
3. Kopier innholdet fra supabase_setup.sql
4. Kjør

---

### 2. Python API Wrapper ✅
**Fil:** `/root/.openclaw/workspace/supabase_api.py`

Funksjoner:
- `get_pending_commands()` - Hent kommandoer
- `update_command()` - Oppdater status
- `send_response()` - Send svar
- `create_approval_request()` - Be om godkjenning
- `get_pending_approvals()` - Sjekk svar
- `update_system_status()` - Oppdater system status
- `log_activity()` - Logg aktivitet
- `get_recent_activity()` - Hent logg

---

### 3. Agent Listener ✅
**Fil:** `/root/.openclaw/workspace/agent_listener.py`

Hva den gjør:
- Lytter på kommandoer fra Mission Control
- Prosesserer ulike kommando-typer (task, query, system, config)
- Sender svar tilbake
- Logger alt

---

## 🔄 GJENSTÅENDE - Implementasjon

### 1. Kjør SQL Setup
```bash
# Gå til Supabase Dashboard:
https://supabase.com/dashboard/project/kvniauxokdtmpvjtfnje

# Åpne SQL Editor og kjør:
/root/.openclaw/workspace/supabase_setup.sql
```

### 2. Test API Wrapper
```bash
cd /root/.openclaw/workspace
python3 supabase_api.py
```

### 3. Start Agent Listener
```bash
cd /root/.openclaw/workspace
python3 agent_listener.py
```

### 4. Integrer med Eksisterende Systemer
- [ ] Morning Routine → Oppdater system_status
- [ ] Podcast Manager → Oppdater system_status
- [ ] NRJ Dashboard → Oppdater system_status
- [ ] Content Aggregator → Oppdater system_status

### 5. Cron Jobs for Status-oppdatering
```bash
# Hver 5. minutt
*/5 * * * * cd /root/.openclaw/workspace && python3 -c "from supabase_api import SupabaseAPI; api = SupabaseAPI(); api.update_system_status('mission_control', 'healthy')"
```

---

## 📋 API Dokumentasjon for Deg

### Send kommando fra Mission Control:
```javascript
// JavaScript i Mission Control
const { data, error } = await supabase
  .from('agent_commands')
  .insert({
    command_type: 'task',
    command_data: {
      task: 'morning_routine',
      date: '2026-03-05'
    },
    priority: 'high'
  });
```

### Lytte på svar:
```javascript
// Realtime subscription
supabase
  .from('agent_responses')
  .on('INSERT', payload => {
    console.log('Svar mottatt:', payload.new);
  })
  .subscribe();
```

### Hente aktivitetslogg:
```javascript
const { data } = await supabase
  .from('activity_log')
  .select('*')
  .order('created_at', { ascending: false })
  .limit(50);
```

---

## 🎯 Neste Steg

1. **Du:** Kjør SQL setup i Supabase
2. **Jeg:** Tester API wrapper
3. **Jeg:** Starter agent listener
4. **Sammen:** Integrerer med Mission Control

**Klar til å fortsette?**