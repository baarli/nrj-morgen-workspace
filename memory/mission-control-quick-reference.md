# Mission Control - Hurtigreferanse

## 🔧 Vanlige Problemer og Løsninger

### Problem: Kan ikke logge inn
**Løsning:**
1. Passord er: `kloakontroll2026`
2. Prøv hard refresh: Ctrl+Shift+R (Windows) eller Cmd+Shift+R (Mac)
3. Sjekk browser console (F12) for røde feilmeldinger
4. Prøk test-siden: https://baarli.github.io/mission-control-live/test.html

---

### Problem: Ingen data vises
**Løsning:**
1. Klikk "🔌 Test tilkobling" knapp på Dashboard
2. Hvis feil: Sjekk at Supabase er oppe
3. Hvis suksess men ingen data: Sjekk at saker finnes i databasen
4. Husk: Morgenrutinen bruker **neste dags dato**

---

### Problem: Sakene vises ikke
**Løsning:**
1. Gå til Saksliste-seksjonen
2. Klikk "🔄 Oppdater"
3. Sjekk console for feilmeldinger
4. Verifiser at `show_date` i databasen er riktig

---

### Problem: Kan ikke legge til sak
**Løsning:**
1. Sjekk at alle felter er fylt ut
2. Sjekk console for CORS-feil
3. Verifiser at TENANT_ID er korrekt i koden

---

### Problem: Kan ikke slette sak
**Løsning:**
1. Bekreft at du klikket "OK" i confirm-dialog
2. Sjekk at sak_id er gyldig
3. Sjekk Supabase RLS-policy for DELETE

---

## 🚀 Deploy Sjekkliste

### Før deploy
- [ ] Test alle funksjoner lokalt
- [ ] Verifiser at Supabase-kall fungerer
- [ ] Sjekk at passord er riktig
- [ ] Test på mobil og desktop

### Etter deploy
- [ ] Vent 30 sekunder på GitHub Pages
- [ ] Test login
- [ ] Test dashboard lasting
- [ ] Test saksliste
- [ ] Test legge til/slette sak
- [ ] Test podcast-seksjon
- [ ] Test statistikk

---

## 📝 Kode Endringer

### Legge til ny seksjon
1. Legg til knapp i `.nav`:
```html
<button onclick="showSection('nyseksjon')" data-section="nyseksjon">Ny Seksjon</button>
```

2. Legg til HTML:
```html
<section class="section" id="nyseksjon">
  <div class="card">
    <h2>Ny Seksjon</h2>
    <div id="nyseksjon-content"></div>
  </div>
</section>
```

3. Legg til JavaScript:
```javascript
async function loadNySeksjon() {
  // Din kode her
}
```

4. Oppdater `showSection()`:
```javascript
if (section === 'nyseksjon') loadNySeksjon();
```

---

### Endre passord
```javascript
// Finn denne linjen:
const PASSWORD = 'kloakontroll2026';

// Endre til:
const PASSWORD = 'nyttpassord';
```

---

### Endre farger
```css
/* I <style> seksjonen */
:root {
  --color-primary: #nyfarge;  /* Endre denne */
}
```

---

## 🔌 Supabase Spørringer

### Hent alle saker
```sql
SELECT * FROM agenda_items 
WHERE tenant_id = 'a0000000-0000-0000-0000-000000000001'
ORDER BY show_date DESC, order_index ASC;
```

### Hent saker for dato
```sql
SELECT * FROM agenda_items 
WHERE tenant_id = 'a0000000-0000-0000-0000-000000000001'
AND show_date = '2026-03-05'
ORDER BY order_index ASC;
```

### Slett gamle saker
```sql
DELETE FROM agenda_items 
WHERE tenant_id = 'a0000000-0000-0000-0000-000000000001'
AND show_date < CURRENT_DATE - INTERVAL '7 days';
```

### Tell saker per kategori
```sql
SELECT category, COUNT(*) 
FROM agenda_items 
WHERE tenant_id = 'a0000000-0000-0000-0000-000000000001'
GROUP BY category;
```

---

## 🎯 Viktige URL-er

| Tjeneste | URL |
|----------|-----|
| Mission Control | https://baarli.github.io/mission-control-live/ |
| GitHub Repo | https://github.com/baarli/mission-control-live |
| Supabase Dashboard | https://app.supabase.com/project/kvniauxokdtmpvjtfnej |
| Test Side | https://baarli.github.io/mission-control-live/test.html |

---

## 📊 Miljøvariabler

```javascript
// Disse må være korrekte:
const SUPABASE_URL = 'https://kvniauxokdtmpvjtfnej.supabase.co';
const TENANT_ID = 'a0000000-0000-0000-0000-000000000001';
const CREATED_BY = '10aa1508-6d52-490c-8ae5-fa3da9a152c4';
```

---

## 🐛 Debug Tips

### Åpne console
- Windows/Linux: `F12` eller `Ctrl+Shift+J`
- Mac: `Cmd+Option+J`

### Se etter meldinger
- `[INFO]` - Normal drift
- `[SUCCESS]` - Operasjon fullført
- `[ERROR]` - Noe gikk galt

### Test API-kall
```javascript
// I console:
await supabaseRequest('/agenda_items?limit=1')
```

### Sjekk localStorage
```javascript
// I console:
localStorage.getItem('mc_auth')
localStorage.setItem('mc_auth', 'true')  // Force login
```

---

## 📞 Support

Hvis ingenting fungerer:
1. Sjekk denne dokumentasjonen
2. Se i `/root/.openclaw/workspace/memory/mission-control-*.md`
3. Sjekk GitHub repo for issues
4. Verifiser Supabase status
