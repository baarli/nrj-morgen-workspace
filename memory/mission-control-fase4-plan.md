# 🚀 Mission Control Fase 4 - Avansert

**Startet:** 2026-03-04  
**Mål:** 9.5/10 brukeropplevelse  
**Fokus:** Grafer, eksport, autosave, offline

---

## 📋 Oppgaver

### 1. Trend-grafer 📊 ⭐ HØYEST PRIORITET
**Beskrivelse:** Visuell fremstilling av radio/podcast statistikk over tid

**Implementasjon:**
- [ ] SVG-basert linjegraf for radio lyttere
- [ ] SVG-basert linjegraf for podcast ranking
- [ ] Tidsperiode-valg (siste 4 uker, 3 måneder, 1 år)
- [ ] Hover for å se eksakte verdier
- [ ] Automatisk skalering av Y-akse
- [ ] Animert tegning av grafen

**Tidsestimat:** 2-3 timer

### 2. Eksport til PDF/Excel 📄
**Beskrivelse:** Eksporter saksliste og statistikk

**Implementasjon:**
- [ ] Eksport saksliste til CSV
- [ ] Eksport saksliste til PDF (print-friendly CSS)
- [ ] Eksport statistikk til CSV
- [ ] Download-knapper i UI
- [ ] Filnavn med dato

**Tidsestimat:** 1-2 timer

### 3. Autosave 💾
**Beskrivelse:** Automatisk lagring av endringer

**Implementasjon:**
- [ ] Autosave ved redigering (debounced)
- [ ] Indikator for "Lagret"/"Lagrer..."/"Endringer"
- [ ] Gjenopprett utkast ved crash
- [ ] Versjonshistorikk (siste 5 versjoner)

**Tidsestimat:** 1-2 timer

### 4. Offline-støtte 📱
**Beskrivelse:** Funksjonalitet uten nett

**Implementasjon:**
- [ ] Service Worker for caching
- [ ] Offline indikator
- [ ] Kø-endringer for synk når online
- [ ] Cache saksliste lokalt

**Tidsestimat:** 2-3 timer

### 5. Fuzzy Search 🔎
**Beskrivelse:** Bedre søk i saksliste

**Implementasjon:**
- [ ] Søk i tittel, beskrivelse, notater
- [ ] Fuzzy matching (f.eks. "frm" matcher "farmen")
- [ ] Highlight av søkeord
- [ ] Filtrer etter dato + kategori

**Tidsestimat:** 1-2 timer

---

## 🎯 Rekkefølge

1. **Trend-grafer** - Størst wow-faktor
2. **Eksport** - Etterspurt funksjon
3. **Autosave** - Sikkerhet
4. **Fuzzy search** - Bedre UX
5. **Offline** - Kompleks, lav prioritet

---

## 📝 Fremdriftslogg

| Oppgave | Status | Start | Ferdig | Notater |
|---------|--------|-------|--------|---------|
| Trend-grafer | ⏳ Klar | - | - | - |
| Eksport | ⏳ Klar | - | - | - |
| Autosave | ⏳ Klar | - | - | - |
| Fuzzy search | ⏳ Klar | - | - | - |
| Offline | ⏳ Klar | - | - | - |

---

## 💡 Design-notater

### Graf SVG-struktur
```svg
<svg viewBox="0 0 800 200">
  <!-- Grid lines -->
  <line x1="0" y1="50" x2="800" y2="50" stroke="#334155" />
  
  <!-- Data line -->
  <path d="M0,150 L200,120 L400,80 L600,100 L800,60" 
        fill="none" 
        stroke="#6366f1" 
        stroke-width="2"/>
  
  <!-- Data points -->
  <circle cx="0" cy="150" r="4" fill="#6366f1"/>
</svg>
```

### CSV Export format
```csv
Nummer,Tittel,Kategori,Dato,Lenke
1,Farmen-premiere,REALITY_TV,2026-03-05,https://...
2,Kjendis-brudd,KJENDIS_DRAMA,2026-03-05,https://...
```

### Autosave indikator
```
🟢 Lagret      → Alt OK
🟡 Lagrer...   → Venter på API
🔴 Endringer   → Ikke lagret ennå
```

---

## 🔧 Tekniske Detaljer

### SVG Graf generering
```javascript
function renderChart(data, container) {
  const width = 800, height = 200;
  const max = Math.max(...data.map(d => d.value));
  
  const points = data.map((d, i) => {
    const x = (i / (data.length - 1)) * width;
    const y = height - (d.value / max) * height;
    return `${x},${y}`;
  }).join(' ');
  
  return `<svg viewBox="0 0 ${width} ${height}">
    <polyline points="${points}" fill="none" stroke="#6366f1" stroke-width="2"/>
  </svg>`;
}
```

### CSV Download
```javascript
function downloadCSV(data, filename) {
  const csv = convertToCSV(data);
  const blob = new Blob([csv], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
}
```

### Autosave med debounce
```javascript
let autosaveTimer;
function scheduleAutosave() {
  clearTimeout(autosaveTimer);
  showSaveStatus('saving');
  autosaveTimer = setTimeout(() => {
    saveChanges();
    showSaveStatus('saved');
  }, 2000);
}
```
