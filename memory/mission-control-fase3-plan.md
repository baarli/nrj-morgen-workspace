# 🎨 Mission Control Fase 3 - UX Polish

**Startet:** 2026-03-04  
**Mål:** 9/10 brukeropplevelse  
**Fokus:** Animasjoner, ikoner, tema, onboarding

---

## 📋 Oppgaver

### 1. Animerte Overganger ⭐ HØYEST PRIORITET
**Beskrivelse:** Smooth CSS transitions for alle interaksjoner

**Implementasjon:**
- [ ] Page transitions (fade in/out)
- [ ] Card hover effects (lift + shadow)
- [ ] Button press animations
- [ ] Toast slide-in/out
- [ ] Loading skeleton shimmer
- [ ] Modal/dialog animations

**Tidsestimat:** 1-2 timer

### 2. Profesjonelle Ikoner
**Beskrivelse:** Bytt ut emojis med SVG-ikoner

**Implementasjon:**
- [ ] Dashboard ikon
- [ ] Saksliste ikon
- [ ] Søk ikon
- [ ] Statistikk ikon
- [ ] Rediger/Slett/Lagre ikoner
- [ ] Kategori-ikoner

**Tidsestimat:** 1-2 timer

### 3. Dark/Light Mode Toggle
**Beskrivelse:** La bruker velge mellom dark og light theme

**Implementasjon:**
- [ ] CSS variabler for begge temaer
- [ ] Toggle-knapp i header
- [ ] Lagre preferanse i localStorage
- [ ] Auto-detect system preference
- [ ] Smooth transition mellom temaer

**Tidsestimat:** 1-2 timer

### 4. Onboarding for Nye Brukere
**Beskrivelse:** Introduksjon for førstegangsbrukere

**Implementasjon:**
- [ ] Welcome modal
- [ ] Step-by-step guide
- [ ] Highlight viktige funksjoner
- [ ] Skip/Next knapper
- [ ] Vis kun første gang (localStorage)

**Tidsestimat:** 2-3 timer

### 5. Micro-interactions
**Beskrivelse:** Små detaljer som gjør appen delightful

**Implementasjon:**
- [ ] Success animation (checkmark)
- [ ] Shake animation på error
- [ ] Pulse animation på nye saker
- [ ] Number count-up animation
- [ ] Drag ghost styling

**Tidsestimat:** 1-2 timer

---

## 🎯 Rekkefølge

1. **Animasjoner** - Størst visuell impact
2. **Ikoner** - Profesjonelt utseende
3. **Tema-toggle** - Brukerpreferanse
4. **Onboarding** - Hjelper nye brukere
5. **Micro-interactions** - Polish

---

## 📝 Fremdriftslogg

| Oppgave | Status | Start | Ferdig | Notater |
|---------|--------|-------|--------|---------|
| Animasjoner | ⏳ Klar | - | - | - |
| Ikoner | ⏳ Klar | - | - | - |
| Tema-toggle | ⏳ Klar | - | - | - |
| Onboarding | ⏳ Klar | - | - | - |
| Micro-interactions | ⏳ Klar | - | - | - |

---

## 💡 Design-notater

### Animasjonstider
```css
--transition-fast: 150ms;
--transition-normal: 300ms;
--transition-slow: 500ms;
--easing-default: ease-in-out;
--easing-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
```

### Page Transition
```css
.section {
  opacity: 0;
  transform: translateY(10px);
  transition: opacity 300ms ease, transform 300ms ease;
}
.section.active {
  opacity: 1;
  transform: translateY(0);
}
```

### Card Hover
```css
.card {
  transition: transform 200ms ease, box-shadow 200ms ease;
}
.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}
```

### Dark/Light Mode
```css
:root {
  --bg: #0f172a; /* dark */
  --bg: #ffffff; /* light */
}
[data-theme="light"] {
  --bg: #ffffff;
  --bg2: #f8fafc;
  --tx: #0f172a;
}
```

---

## 🔧 Tekniske Detaljer

### localStorage for tema
```javascript
function toggleTheme() {
  const current = localStorage.getItem('theme') || 'dark';
  const next = current === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
}
```

### Onboarding sjekk
```javascript
if (!localStorage.getItem('mc_onboarding_seen')) {
  showOnboarding();
  localStorage.setItem('mc_onboarding_seen', 'true');
}
```

### SVG Icon system
```javascript
const icons = {
  dashboard: '<svg>...</svg>',
  edit: '<svg>...</svg>',
  delete: '<svg>...</svg>'
};
```
