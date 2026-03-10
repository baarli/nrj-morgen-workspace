# SYSTEMFORBEDRINGSPLAN 2026
**Versjon:** 1.0  
**Dato:** 11. mars 2026  
**Status:** Under arbeid

---

## 📋 OVERSIKT

Denne planen er resultatet av en systematisk gjennomgang av hele BaarliClaw-systemet. Analysen identifiserer forbedringsområder på tvers av dokumentasjon, kodekvalitet, automatisering, frontend, integrasjon og sikkerhet.

---

## 🔴 KRITISKE FORBEDRINGER (Umiddelbart)

### 1. Error Handling System
**Status:** ✅ Påbegynt - `error_handler.py` opprettet

**Problem:**
- Ingen felles error handling på tvers av scripts
- Unødig duplisering av try-except blokker
- Ingen retry-logikk for API-kall
- Ingen sentralisert logging

**Løsning:**
```python
# scripts/error_handler.py - Opprettet ✅
- safe_execute decorator
- retry_on_error decorator  
- rate_limited decorator
- ErrorContext manager
- APIError exception
- Structured logging
```

**Gjenstående:**
- [ ] Oppdater alle eksisterende scripts til å bruke error_handler.py
- [ ] Legg til error boundaries i Mission Control
- [ ] Implementer global error handler i frontend

---

### 2. Sentralisert Konfigurasjon
**Status:** ✅ Påbegynt - `config_manager.py` opprettet

**Problem:**
- SUPABASE_URL/KEY duplisert i flere filer
- Hardkodede API-nøkler i kode
- Ingen validering av credentials ved startup

**Løsning:**
```python
# scripts/config_manager.py - Opprettet ✅
- Centraliserte konstanter
- Lazy credential loading
- API konfigurasjoner
- Validation funksjoner
```

**Gjenstående:**
- [ ] Refaktorer alle scripts til å bruke config_manager.py
- [ ] Fjern dupliserte konstanter
- [ ] Legg til .env file loading

---

### 3. Frontend Error Boundaries
**Status:** 🔄 Planlagt

**Problem:**
- En JavaScript-feil kan krasje hele Mission Control
- Ingen global error handler
- Brukere får ingen feedback ved feil

**Løsning:**
```javascript
// error-boundary.js - Planlagt
window.onerror = function(msg, url, line) {
    showNotification('En feil oppstod. Siden vil lastes på nytt.', 'error');
    console.error(`Error: ${msg} at ${url}:${line}`);
    return true;
};

window.addEventListener('unhandledrejection', function(event) {
    showNotification('En uventet feil oppstod', 'error');
    console.error('Unhandled promise rejection:', event.reason);
});
```

---

## 🟡 HØY PRIORITET (Innen 1 uke)

### 4. Lazy Loading av Seksjoner
**Status:** 📋 Ikke påbegynt

**Problem:**
- `index.html` = 181 KB (2,454 linjer) - lastes alt på én gang
- Alle seksjoner (dashboard, sakslista, podkast, etc.) i DOM samtidig
- Chart.js lastes selv om bruker aldri ser dashboard

**Løsning:**
```javascript
// Dynamisk import av seksjoner
const sections = {
    dashboard: () => import('./sections/dashboard.js'),
    sakslista: () => import('./sections/sakslista.js'),
    podkast: () => import('./sections/podkast.js'),
    // ...
};

async function showSection(name) {
    if (!loadedSections.has(name)) {
        await sections[name]();
        loadedSections.add(name);
    }
    // Vis seksjon
}
```

---

### 5. Duplisert Konfigurasjon
**Status:** 📋 Ikke påbegynt

**Problem:**
- `SUPABASE_URL` definert i både `sakslista-pro.js` og `supabase-integration.js`
- `escapeHtml()` duplisert
- `showNotification()` duplisert

**Filer å rydde:**
- [ ] `sakslista-pro.js` linje 3-7
- [ ] `supabase-integration.js` linje 4-8
- [ ] Eventuelle andre duplikater

**Løsning:**
- Eksporter fra `config_manager.py` (Python) eller lag `config.js` (JavaScript)
- Felles `utils.js` for delte funksjoner

---

### 6. Debounced Filtering
**Status:** 📋 Ikke påbegynt

**Problem:**
- `filterSaker()` kalles ved hver keystroke
- Full re-render av sakslista hver gang
- Performance problem ved mange saker

**Løsning:**
```javascript
// utilities.js
function debounce(fn, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => fn.apply(this, args), delay);
    };
}

// Bruk:
document.getElementById('search-input').addEventListener('input', 
    debounce(() => filterSaker(), 300)
);
```

---

### 7. Virtuell Scrolling for Sakslista
**Status:** 📋 Ikke påbegynt

**Problem:**
- Alle saker rendres i DOM samtidig
- Performance forringes ved 50+ saker
- Layout/paint tar lang tid

**Løsning:**
- Implementer virtual scrolling
- Render kun synlige items (~10-15 om gangen)
- Reuse DOM elements ved scrolling

---

## 🟢 MEDIUM PRIORITET (Innen 1 måned)

### 8. CSS Separering
**Status:** 📋 Ikke påbegynt

**Problem:**
- ~380 linjer inline CSS i `index.html`
- Kan ikke caches separat
- Vanskelig å vedlikeholde

**Løsning:**
```
mission-control/public/
├── css/
│   ├── base.css        # Reset, variables, base styles
│   ├── components.css  # Cards, modals, buttons
│   ├── layout.css      # Grid, sections, responsive
│   └── utilities.css   # Helper classes
```

---

### 9. Optimistiske Oppdateringer
**Status:** 📋 Ikke påbegynt

**Problem:**
- UI venter på API-svar før oppdatering
- Treg opplevelse ved sletting/endring

**Løsning:**
```javascript
// Optimistisk oppdatering
async function deleteSak(id) {
    const previous = saker;
    saker = saker.filter(s => s.id !== id); // Oppdater UI først
    renderSaker();
    
    try {
        await api.deleteSak(id); // Send API-kall
    } catch (error) {
        saker = previous; // Rollback ved feil
        renderSaker();
        showNotification('Sletting feilet', 'error');
    }
}
```

---

### 10. Memory Cache for Saker
**Status:** 📋 Ikke påbegynt

**Problem:**
- Hver page load henter fra Supabase på nytt
- Ingen caching i minnet
- Unødvendige API-kall

**Løsning:**
```javascript
class MemoryCache {
    constructor(maxSize = 100) {
        this.cache = new Map();
        this.maxSize = maxSize;
    }
    
    get(key) {
        const item = this.cache.get(key);
        if (item && Date.now() - item.timestamp < 5 * 60 * 1000) {
            return item.value;
        }
        this.cache.delete(key);
        return null;
    }
    
    set(key, value) {
        if (this.cache.size >= this.maxSize) {
            const firstKey = this.cache.keys().next().value;
            this.cache.delete(firstKey);
        }
        this.cache.set(key, { value, timestamp: Date.now() });
    }
}
```

---

## 🔵 LAV PRIORITET (Fremtidig)

### 11. Web Workers
- Flytt tung prosessering (duplikat-sjekk) til web worker
- Ikke-blokkerende UI

### 12. Analytics & Monitoring
- Core Web Vitals tracking
- Bruker-interaksjon logging
- Performance metrics

### 13. PWA Forbedringer
- Push notifications for nye saker
- Background sync for kommentarer
- App-like experience

---

## 📊 MÅLEPUNKTER

| Metrikk | Nåværende | Mål | Hvordan måle |
|---------|-----------|-----|--------------|
| HTML Bundle Size | 181 KB | <100 KB | DevTools Network |
| FCP (First Contentful Paint) | ~2.5s | <1.5s | Lighthouse |
| TTI (Time to Interactive) | ~4s | <2.5s | Lighthouse |
| Error Rate | Ukjent | <1% | Error Boundary logs |
| API Cache Hit | ~30% | >70% | Service Worker logs |
| Script Duplication | 3+ steder | 0 | Code review |

---

## 🗓️ TIDSPLAN

### Uke 1 (11-17 mars 2026)
- [x] Opprette error_handler.py
- [x] Opprette config_manager.py
- [ ] Implementer error boundaries i Mission Control
- [ ] Refaktorer scripts til å bruke nye moduler

### Uke 2 (18-24 mars 2026)
- [ ] Lazy loading av seksjoner
- [ ] Debounced filtering
- [ ] CSS separering

### Uke 3 (25-31 mars 2026)
- [ ] Virtuell scrolling
- [ ] Optimistiske oppdateringer
- [ ] Memory cache

### Uke 4 (1-7 april 2026)
- [ ] Testing og validering
- [ ] Performance måling
- [ ] Dokumentasjon

---

## ✅ FULLFØRTE FORBEDRINGER

| Dato | Forbedring | Status |
|------|------------|--------|
| 2026-03-11 | error_handler.py opprettet | ✅ Ferdig |
| 2026-03-11 | config_manager.py opprettet | ✅ Ferdig |
| 2026-03-11 | Frontend analyse rapport | ✅ Ferdig |

---

**Sist oppdatert:** 11. mars 2026  
**Ansvarlig:** Vev 🤖
