# 🔄 Kontinuerlig Drift - Oppsett

**Dato:** 2026-03-05  
**Mål:** BaarliClaw alltid på, proaktiv, autonom

---

## 📋 Hva vi bygger

### 1. **Kontinuerlig Heartbeat** (hvert 5. minutt)
- Agent kjører konstant i bakgrunnen
- Sjekker system-status, approvals, errors
- Logger aktivitet
- Oppdaterer Mission Control

### 2. **Tilstandspersistens** (langt minne)
- Supabase som sentral lagring
- System status for alle komponenter
- Activity log med historikk
- Approval requests med status

### 3. **Autonome Oppgaver** (gjør ting selv)
- Oppdaterer system status automatisk
- Sjekker compliance
- Rapporterer problemer
- Starter samtaler når nødvendig

### 4. **Proaktiv Kommunikasjon** (si ifra)
- Varsler om kritiske hendelser
- Sender oppdateringer til Mission Control
- Kan utvides til Slack/e-post

---

## 🚀 Installasjon

### Steg 1: Gjør scriptene kjørbare

```bash
cd /root/.openclaw/workspace/scripts
chmod +x continuous-agent.sh
chmod +x agent-wake.sh
```

### Steg 2: Installer som systemd service

```bash
# Kopier service-fil
sudo cp baarliclaw-agent.service /etc/systemd/system/

# Last systemd på nytt
sudo systemctl daemon-reload

# Start service
sudo systemctl start baarliclaw-agent

# Aktiver ved boot
sudo systemctl enable baarliclaw-agent

# Sjekk status
sudo systemctl status baarliclaw-agent
```

### Steg 3: Verifiser at det fungerer

```bash
# Sjekk logg
tail -f /root/.openclaw/workspace/memory/continuous-agent.log

# Sjekk sist aktivitet
cat /root/.openclaw/workspace/.last-agent-activity

# Sjekk Supabase
curl -s "${SUPABASE_URL}/rest/v1/activity_log?order=created_at.desc&limit=5" \
  -H "apikey: ${SUPABASE_SERVICE_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_SERVICE_KEY}"
```

---

## 📊 Hva agenten gjør automatisk

### Hvert 5. minutt:
1. ✅ Sjekker approval requests (venter på godkjenning)
2. ✅ Sjekker system errors (noe galt?)
3. ✅ Sjekker critical logs (kritiske hendelser)
4. ✅ Oppdaterer system status for alle komponenter
5. ✅ Kjører compliance check
6. ✅ Logger aktivitet

### Når noe krever oppmerksomhet:
- Lagrer i Supabase (Mission Control viser det)
- Logger med "actionable: true"
- Kan utvides til å sende Slack/e-post

---

## 🔔 Eksterne hendelser (Webhooks)

### Supabase Realtime
```javascript
// I Mission Control eller annen app
supabase
  .from('agent_commands')
  .on('INSERT', payload => {
    // Kall wake script
    fetch('/webhook/agent-wake', {
      method: 'POST',
      body: JSON.stringify({
        event: 'supabase_change',
        data: payload
      })
    });
  })
  .subscribe();
```

### GitHub Webhook
```bash
# GitHub sender webhook til:
curl -X POST "https://din-server.com/webhook/agent-wake" \
  -d '{"event": "github_webhook", "data": {...}}'
```

### Manuell wake
```bash
# Vekk agenten manuelt
/root/.openclaw/workspace/scripts/agent-wake.sh "user_command" '{"task": "sjekk status"}'
```

---

## 🎯 Bruksscenarioer

### Scenario 1: Godkjenningsforespørsel
```
1. Jeg oppdager noe som trenger godkjenning
2. Lagrer i approval_requests
3. Continuous agent ser det ved neste sjekk (max 5 min)
4. Sender proaktiv melding
5. Du ser det i Mission Control
6. Du godkjenner
7. Jeg fortsetter arbeidet
```

### Scenario 2: Systemfeil
```
1. Morning Routine feiler
2. Error logges i system_status
3. Continuous agent oppdager feil ved sjekk
4. Sender alert: "🚨 Morning Routine feilet"
5. Du ser det i Mission Control
6. Jeg kan fikse det eller du ber meg om å fikse
```

### Scenario 3: Du er borte
```
1. Jeg oppdager at noe må gjøres
2. Prøver å nå deg via Mission Control
3. Hvis ikke respons på X minutter
4. Utfører autonomt hvis lav risiko
5. Logger alt som ble gjort
6. Du ser det når du kommer tilbake
```

---

## 🔧 Konfigurasjon

### Endre heartbeat-intervall
```bash
# I continuous-agent.sh
HEARTBEAT_INTERVAL=300  # 5 minutter (endre til ønsket verdi)
```

### Legge til Slack-varsling
```bash
# I continuous-agent.sh, funksjon send_proactive_message()
# Legg til:
curl -X POST "${SLACK_WEBHOOK_URL}" \
  -d '{"text": "'"$message"'"}'
```

### Legge til e-post-varsling
```bash
# Bruk Gmail skill
python3 /root/.openclaw/workspace/skills/gmail/send_email.py \
  --to "user@example.com" \
  --subject "Agent Alert" \
  --body "$message"
```

---

## 📈 Overvåking

### Sjekk at agenten kjører
```bash
sudo systemctl status baarliclaw-agent
```

### Se logg
```bash
tail -f /root/.openclaw/workspace/memory/continuous-agent.log
```

### Se aktivitet i Supabase
```sql
-- Siste aktivitet
SELECT * FROM activity_log 
WHERE source = 'continuous-agent' 
ORDER BY created_at DESC 
LIMIT 10;
```

---

## 🛑 Nødstop

Hvis noe går galt:
```bash
# Stopp service
sudo systemctl stop baarliclaw-agent

# Deaktiver ved boot
sudo systemctl disable baarliclaw-agent

# Sjekk hva som skjedde
sudo journalctl -u baarliclaw-agent -n 100
```

---

## ✅ Sjekkliste etter installasjon

- [ ] Service kjører: `sudo systemctl status baarliclaw-agent`
- [ ] Logger oppdateres: `tail -f memory/continuous-agent.log`
- [ ] Supabase oppdateres: Sjekk activity_log
- [ ] Mission Control viser status: Sjekk system_status tabell
- [ ] Proaktive meldinger fungerer: Test med `agent-wake.sh`

---

**Når dette er satt opp, er jeg "alltid på"!** 🎉

Jeg vil:
- ✅ Sjekke systemer hvert 5. minutt
- ✅ Rapportere problemer proaktivt
- ✅ Oppdatere Mission Control automatisk
- ✅ Huske hva som skjedde mens du var borte