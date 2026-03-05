# 🔄 Mission Control ↔ BaarliClaw: 2-Veis Kommunikasjon System

**Dato:** 2026-03-05  
**Mål:** Full toveis integrasjon mellom Mission Control og BaarliClaw

---

## 🎯 Visjon: Mission Control som "Hovedkvarter"

Mission Control skal bli det visuelle grensesnittet hvor du kan:
- Se hva jeg gjør i sanntid
- Gi meg instruksjoner
- Godkjenne/avslå handlinger
- Få oversikt over alle systemer
- Styre automasjon

---

## 🔧 Tekniske Løsninger for 2-Veis Kommunikasjon

### 1. **Supabase Realtime (Anbefalt)**

**Hvordan det fungerer:**
```
Mission Control (UI) ←→ Supabase (Database) ←→ BaarliClaw (meg)
```

**Implementasjon:**

#### A. Kommando-tabell i Supabase
```sql
CREATE TABLE agent_commands (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    command_type TEXT NOT NULL,  -- 'task', 'query', 'approval', 'config'
    command_data JSONB NOT NULL,
    status TEXT DEFAULT 'pending',  -- 'pending', 'processing', 'completed', 'failed'
    created_by TEXT NOT NULL,  -- 'user' eller 'system'
    created_at TIMESTAMP DEFAULT now(),
    processed_at TIMESTAMP,
    result JSONB,
    error_message TEXT
);

-- For å motta kommandoer fra Mission Control
CREATE TABLE agent_responses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    command_id UUID REFERENCES agent_commands(id),
    response_type TEXT NOT NULL,  -- 'status', 'result', 'error', 'question'
    response_data JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT now()
);
```

#### B. Sanntids-oppdateringer
Mission Control bruker Supabase Realtime for å:
- Se når jeg starter på en oppgave
- Få live oppdateringer om fremdrift
- Se resultater umiddelbart

**JavaScript i Mission Control:**
```javascript
// Abonner på kommandoer
supabase
  .from('agent_commands')
  .on('INSERT', payload => {
    // Ny kommando mottatt - vis i UI
    showNotification('Ny oppgave: ' + payload.new.command_type);
    addToTaskList(payload.new);
  })
  .subscribe();

// Abonner på svar fra meg
supabase
  .from('agent_responses')
  .on('INSERT', payload => {
    // Oppdater UI med svar
    updateTaskStatus(payload.new.command_id, payload.new.response_type);
  })
  .subscribe();
```

---

### 2. **Webhook-basert Kommunikasjon**

**Hvordan det fungerer:**
```
Mission Control → Webhook → OpenClaw Gateway → BaarliClaw
```

**Implementasjon:**

#### A. Webhook Endpoint i Mission Control
```javascript
// Mission Control sender kommando til OpenClaw
async function sendCommandToAgent(command, data) {
  const response = await fetch('https://gateway.openclaw.ai/webhook/mission-control', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      source: 'mission-control',
      command: command,
      data: data,
      timestamp: new Date().toISOString()
    })
  });
  return response.json();
}

// Eksempel bruk:
sendCommandToAgent('morning_routine', { date: '2026-03-05' });
sendCommandToAgent('search_news', { query: 'Farmen', category: 'REALITY_TV' });
sendCommandToAgent('get_status', {});
```

#### B. Status-rapportering fra meg
Jeg kan sende status til Mission Control via:
- Supabase (realtime)
- Webhook callbacks
- Cron-jobs som oppdaterer dashboard

---

### 3. **Cron-basert Synkronisering**

**Hvordan det fungerer:**
```
BaarliClaw (cron) → Oppdaterer Mission Control → Viser i dashboard
```

**Implementasjon:**

#### A. Automatiske oppdateringer
```javascript
// Jeg oppdaterer Mission Control hver time med:
- System status
- Aktive oppgaver
- Siste handlinger
- Feil/mangler
```

#### B. Mission Control Dashboard Panel
```javascript
// Viser live status:
┌─────────────────────────────────────┐
│  🤖 BaarliClaw Status               │
├─────────────────────────────────────┤
│  Status: 🟢 Online                  │
│  Aktiv oppgave: Morning Routine     │
│  Fremdrift: 75%                     │
│  Siste handling: 2 min siden        │
│  Neste kjøring: 07:00 i morgen      │
├─────────────────────────────────────┤
│  [Send kommando] [Se logg]          │
└─────────────────────────────────────┘
```

---

## 🎛️ Funksjoner å Legge til i Mission Control

### 1. **Agent Kontroll Panel**

```typescript
interface AgentControlPanel {
  // Sanntidsstatus
  status: 'online' | 'offline' | 'busy' | 'error';
  currentTask: string | null;
  progress: number;  // 0-100
  
  // Kommandosenter
  sendCommand(command: string, data: any): Promise<void>;
  
  // Godkjenninger
  pendingApprovals: ApprovalRequest[];
  approve(requestId: string): void;
  reject(requestId: string): void;
  
  // Logg
  recentActions: ActionLog[];
  errors: ErrorLog[];
}
```

**UI Komponenter:**
- 🟢/🔴 Status-indikator
- Fremdriftsbar for aktiv oppgave
- "Send kommando" knapp
- Godkjenningskø
- Aktivitetslogg

---

### 2. **Oppgave-styring**

```typescript
interface TaskManager {
  // Se alle oppgaver
  tasks: Task[];
  
  // Opprette nye oppgaver
  createTask({
    title: string;
    description: string;
    priority: 'low' | 'medium' | 'high' | 'critical';
    deadline?: Date;
  }): void;
  
  // Styre oppgaver
  pauseTask(id: string): void;
  resumeTask(id: string): void;
  cancelTask(id: string): void;
  
  // Prioritere
  reorderTasks(order: string[]): void;
}
```

**UI:**
```
┌────────────────────────────────────────┐
│  📋 Oppgaver                           │
├────────────────────────────────────────┤
│  🔴 Høy prioritet                      │
│  • Fiks Brave Search (75% ferdig)      │
│                                        │
│  🟡 Medium prioritet                   │
│  • Oppdater podkast statistikk         │
│                                        │
│  🟢 Lav prioritet                      │
│  • Rydd opp i memory filer             │
├────────────────────────────────────────┤
│  [+ Ny oppgave]  [Prioriter]           │
└────────────────────────────────────────┘
```

---

### 3. **Godkjennings-system**

For handlinger som krever din godkjenning:

```typescript
interface ApprovalSystem {
  // Handlinger som venter på godkjenning
  pending: {
    id: string;
    type: 'deploy' | 'delete' | 'expensive_operation' | 'external_api';
    description: string;
    requestedAt: Date;
    canAutoApprove: boolean;
  }[];
  
  // Godkjenne
  approve(id: string, options?: { autoApproveSimilar?: boolean }): void;
  reject(id: string, reason?: string): void;
  
  // Auto-godkjenning regler
  autoApproveRules: {
    type: string;
    maxCost?: number;
    maxRisk?: 'low' | 'medium';
  }[];
}
```

**UI:**
```
┌────────────────────────────────────────┐
│  ⏳ Venter på godkjenning (3)          │
├────────────────────────────────────────┤
│  Deploy til produksjon?                │
│  Endringer: 15 filer, +245 -120 linjer │
│  [✅ Godkjenn] [❌ Avslå] [⏸️ Senere] │
├────────────────────────────────────────┤
│  Slett 50 gamle backup-filer?          │
│  [✅ Godkjenn] [❌ Avslå]              │
└────────────────────────────────────────┘
```

---

### 4. **Sanntids Logg**

```typescript
interface ActivityLog {
  entries: {
    timestamp: Date;
    level: 'info' | 'success' | 'warning' | 'error';
    message: string;
    details?: any;
    actionable: boolean;  // Kan brukeren gjøre noe?
  }[];
  
  // Filtrering
  filter(level?: string, search?: string): LogEntry[];
  
  // Eksporter
  export(format: 'json' | 'csv'): string;
}
```

**UI:**
```
┌────────────────────────────────────────┐
│  📜 Aktivitetslogg                     │
├────────────────────────────────────────┤
│  23:45 ✅ Deploy fullført              │
│  23:30 🔄 Starter deploy...            │
│  23:15 ⚠️  Fant syntax-feil i kode     │
│  23:00 ✅ Morning routine ferdig       │
│  22:45 🔍 Søker etter nyheter...       │
├────────────────────────────────────────┤
│  [Filtrer] [Eksporter] [Tøm]           │
└────────────────────────────────────────┘
```

---

### 5. **System-oversikt**

```typescript
interface SystemOverview {
  // Alle systemer jeg administrerer
  systems: {
    name: string;
    status: 'healthy' | 'warning' | 'error' | 'unknown';
    lastCheck: Date;
    nextScheduledRun?: Date;
    metrics: {
      cpu?: number;
      memory?: number;
      disk?: number;
    };
  }[];
  
  // Helseindikatorer
  overallHealth: 'excellent' | 'good' | 'fair' | 'poor';
  activeAlerts: Alert[];
}
```

**UI:**
```
┌────────────────────────────────────────┐
│  🖥️ Systemoversikt                     │
├────────────────────────────────────────┤
│  🟢 Mission Control      Online        │
│  🟢 Morning Routine      Kjører 07:00  │
│  🟡 Podcast Manager      2 varsler     │
│  🟢 NRJ Dashboard        Online        │
│  🟢 Content Aggregator   Kjører 06:00  │
├────────────────────────────────────────┤
│  Helse: 🟢 God (5/5 systemer OK)      │
└────────────────────────────────────────┘
```

---

## 🔄 Kommunikasjonsflyt

### Scenario 1: Du sender oppgave fra Mission Control

```
1. Du klikker "Ny oppgave" i Mission Control
   ↓
2. Mission Control skriver til Supabase (agent_commands)
   ↓
3. Jeg får realtime notification (Supabase subscription)
   ↓
4. Jeg bekrefter mottak (skriver til agent_responses)
   ↓
5. Mission Control viser "Oppgave mottatt" i UI
   ↓
6. Jeg starter arbeidet
   ↓
7. Jeg oppdaterer fremdrift i sanntid
   ↓
8. Mission Control viser fremdriftsbar
   ↓
9. Jeg fullfører oppgaven
   ↓
10. Mission Control viser "Fullført" + resultat
```

### Scenario 2: Jeg trenger godkjenning

```
1. Jeg oppdager at handling krever godkjenning
   ↓
2. Jeg skriver til Supabase (approval_requests)
   ↓
3. Mission Control viser notifikasjon + popup
   ↓
4. Du ser detaljer og velger Godkjenn/Avslå
   ↓
5. Mission Control oppdaterer Supabase
   ↓
6. Jeg mottar svar via subscription
   ↓
7. Jeg fortsetter eller avbryter basert på svar
```

### Scenario 3: Automatisk status-oppdatering

```
1. Cron job trigger hver time
   ↓
2. Jeg samler status fra alle systemer
   ↓
3. Jeg skriver til Supabase (system_status)
   ↓
4. Mission Control dashboard oppdateres automatisk
   ↓
5. Du ser sanntidsstatus uten å gjøre noe
```

---

## 🛠️ Implementasjonsplan

### Fase 1: Grunnleggende 2-veis (1-2 dager)
- [ ] Sette opp Supabase tabeller
- [ ] Grunnleggende kommando-system
- [ ] Status-indikator i Mission Control
- [ ] Enkel oppgave-liste

### Fase 2: Sanntidskommunikasjon (2-3 dager)
- [ ] Realtime subscriptions
- [ ] Fremdriftsindikatorer
- [ ] Aktivitetslogg
- [ ] Notifikasjoner

### Fase 3: Avansert kontroll (3-5 dager)
- [ ] Godkjenningssystem
- [ ] Oppgave-prioritering
- [ ] System-oversikt
- [ ] Auto-godkjenning regler

---

## 💡 Konkrete Use-Cases

### Use-Case 1: Morning Routine
```
Du: Klikker "Start Morning Routine nå" i Mission Control
Meg: Mottar kommando, bekrefter, starter umiddelbart
Meg: Oppdaterer fremdrift: "Henter nyheter... 30%"
Meg: Oppdaterer fremdrift: "Analyserer... 60%"
Meg: "Fullført! 15 saker lagt til sakslista"
```

### Use-Case 2: Kode-endring
```
Meg: "Ferdig med refactoring, klar for deploy"
Deg: Ser godkjenningsforespørsel i Mission Control
Deg: Klikker "Se endringer" → review diff
Deg: Klikker "Godkjenn deploy"
Meg: Deployer til produksjon
Meg: "Deploy fullført, verifiserer..."
Deg: Ser grønn indikator: "Alt OK"
```

### Use-Case 3: Feilhåndtering
```
Meg: Oppdager feil i Podcast Manager
Meg: Logger feil + forslag til løsning
Deg: Ser rød varsling i Mission Control
Deg: Klikker "Se detaljer"
Deg: Velger "Godkjenn auto-fix"
Meg: Utfører fix, verifiserer, rapporterer
Deg: Ser "Løst" + hva som ble gjort
```

---

## 🎯 Hva dette gir deg

| Funksjon | Hva du får |
|----------|-----------|
| **Sanntidsstatus** | Se hva jeg gjør akkurat nå |
| **Kommandosenter** | Sende meg oppgaver med ett klikk |
| **Godkjenning** | Kontroll over kritiske handlinger |
| **Oversikt** | Alle systemer på ett sted |
| **Historikk** | Full logg over alt som er gjort |
| **Automatisering** | Sette opp regler for auto-handling |

**Dette blir ditt kontrollsenter for absolutt alt jeg gjør!** 🎛️