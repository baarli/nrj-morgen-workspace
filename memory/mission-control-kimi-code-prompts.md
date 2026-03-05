# 🎯 Mission Control - Komplett Forbedringsplan for Kimi Code

**Dato:** 2026-03-05  
**Nåværende Status:** Funksjonell, men trenger refactoring  
**Mål:** 100% perfekt, robust, vedlikeholdbar

---

## 📊 Nåværende Tilstand

### Filstruktur
- **index.html**: 1507 linjer (HTML + CSS + JavaScript i én fil)
- **Hosting**: GitHub Pages
- **Database**: Supabase
- **API-er**: Brave News API, Nielsen, Podtoppen

### Kjente Problemer
1. ❌ **Monolitisk arkitektur** - Alt i én fil
2. ❌ **Ingen modulær struktur** - Vanskelig å vedlikeholde
3. ❌ **Gjentatte syntax-feil** - Ubalanserte krøllparenteser
4. ❌ **Ingen testing** - Ingen måte å verifisere funksjonalitet
5. ❌ **Ingen type-sikkerhet** - JavaScript uten typesjekking
6. ❌ **Ingen byggeprosess** - Direkte deploy av kildekode
7. ❌ **Manglende error handling** - Mange ubehandlede promises
8. ❌ **Ingen linting** - Konsistensproblemer

---

## 🎯 Mål for 100% Perfekt System

### 1. Arkitektur (Kritisk)
- ✅ Modularisert kodebase
- ✅ Separasjon av concerns (HTML/CSS/JS)
- ✅ Komponent-basert struktur
- ✅ TypeScript for type-sikkerhet

### 2. Kvalitet (Kritisk)
- ✅ ESLint + Prettier konfigurert
- ✅ Automatisk syntax-validering
- ✅ Unit tester
- ✅ E2E tester

### 3. Funksjonalitet (Høy)
- ✅ Alle nåværende features beholdes
- ✅ Brave Search med custom prompts
- ✅ Inline editing av saker
- ✅ Charts for statistikk
- ✅ Dark/Light mode
- ✅ Keyboard shortcuts

### 4. DevEx (Medium)
- ✅ Hot reload under utvikling
- ✅ Automatisk deploy ved push
- ✅ GitHub Actions for CI/CD
- ✅ Code splitting for ytelse

---

## 📝 Prompts til Kimi Code

### PROMPT 1: Arkitektur-Refactoring

```
Jeg trenger at du refactore Mission Control fra en monolitisk HTML-fil til en moderne, modulær kodebase.

**Nåværende fil:**
- /root/.openclaw/workspace/mission-control-gh-pages/index.html (1507 linjer)
- Inneholder HTML, CSS, og JavaScript i én fil

**Ønsket struktur:**
mission-control-gh-pages/
├── index.html              # Minimal HTML, kun struktur
├── src/
│   ├── main.ts            # Entry point
│   ├── styles/
│   │   ├── variables.css   # CSS custom properties
│   │   ├── base.css        # Reset og base styles
│   │   ├── components.css  # Komponent-spesifikke styles
│   │   └── utilities.css   # Utility classes
│   ├── components/
│   │   ├── Login.ts
│   │   ├── Dashboard.ts
│   │   ├── Saksliste.ts
│   │   ├── Search.ts
│   │   ├── Stats.ts
│   │   └── ThemeToggle.ts
│   ├── services/
│   │   ├── supabase.ts     # Database API
│   │   ├── brave.ts        # Brave News API
│   │   └── nielsen.ts      # Nielsen/Podtoppen API
│   ├── utils/
│   │   ├── dom.ts          # DOM helpers
│   │   ├── validation.ts   # Input validation
│   │   └── formatting.ts   # Date/number formatting
│   └── types/
│       └── index.ts        # TypeScript interfaces
├── dist/                   # Bygget output
├── package.json
├── tsconfig.json
├── vite.config.ts         # Build tool
└── .github/
    └── workflows/
        └── deploy.yml     # Automatisk deploy

**Krav:**
1. Behold ALL nåværende funksjonalitet
2. Bruk TypeScript for alt
3. Ingen runtime errors
4. Strict mode påslått
5. ES modules

**API-nøkler (hardkodet i nåværende fil):**
- Supabase URL: https://kvniauxokdtmpvjtfnje.supabase.co
- Supabase Key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt2bmlhdXhva2R0bXB2anRmbmVqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTM2NzIzNCwiZXhwIjoyMDY2OTQzMjM0fQ.OkhTtq9QAQ3xMzZYKyWyCjj7PiqMZJKSvpA0jcBJqpE
- Brave Key: BSAt0WSIpXP0Hp6sPvNwaaGuLoyewev

Start med å sette opp prosjektstrukturen og konfigurasjon, deretter migrer koden komponent for komponent.
```

---

### PROMPT 2: TypeScript + Testing Setup

```
Sett opp TypeScript og testing for Mission Control.

**Krav:**
1. TypeScript strict mode
2. Vitest for unit testing
3. Playwright for E2E testing
4. ESLint + Prettier konfigurert
5. Husky for pre-commit hooks

**Tester som MÅ passere:**
- Login fungerer med riktig passord
- Login feiler med feil passord
- Dashboard laster data
- Saksliste viser saker
- Søk returnerer resultater
- Inline editing fungerer
- Tema-bytte fungerer

**Konfigurasjonsfiler som trengs:**
- tsconfig.json
- vite.config.ts
- vitest.config.ts
- playwright.config.ts
- .eslintrc.json
- .prettierrc
- package.json med scripts

Sørg for at all konfigurasjon er korrekt og at testene kan kjøres med `npm test`.
```

---

### PROMPT 3: Komponent-Implementering

```
Implementer følgende komponenter for Mission Control:

**1. Login Komponent (src/components/Login.ts)**
```typescript
interface LoginProps {
  onSuccess: () => void;
}

class Login {
  constructor(props: LoginProps);
  render(): HTMLElement;
  validatePassword(password: string): boolean;
}
```

**2. Dashboard Komponent (src/components/Dashboard.ts)**
```typescript
interface DashboardStats {
  saker: number;
  radioListeners: string;
  podcastRank: string;
}

class Dashboard {
  constructor(container: HTMLElement);
  async loadStats(): Promise<DashboardStats>;
  render(stats: DashboardStats): void;
  startAutoRefresh(intervalMs: number): void;
}
```

**3. Saksliste Komponent (src/components/Saksliste.ts)**
```typescript
interface Sak {
  id: string;
  title: string;
  description?: string;
  category: string;
  show_date: string;
  link_url?: string;
  order_index: number;
}

class Saksliste {
  constructor(container: HTMLElement);
  async loadSaker(date: string): Promise<Sak[]>;
  renderSaker(saker: Sak[]): void;
  startEdit(sak: Sak): void;
  async saveEdit(sak: Sak): Promise<void>;
  async deleteSak(id: string): Promise<void>;
}
```

**4. Search Komponent (src/components/Search.ts)**
```typescript
interface SearchResult {
  id: number;
  title: string;
  description: string;
  url: string;
  source: string;
  published: string;
  score: number;
  category: string;
}

class Search {
  constructor(container: HTMLElement);
  async search(query: string, category?: string, freshness?: string): Promise<SearchResult[]>;
  renderResults(results: SearchResult[]): void;
  toggleSelection(id: number): void;
  async addToSaksliste(results: SearchResult[]): Promise<void>;
}
```

**5. Stats Komponent (src/components/Stats.ts)**
```typescript
class Stats {
  constructor(container: HTMLElement);
  async loadRadioStats(): Promise<RadioData[]>;
  async loadPodcastStats(): Promise<PodcastData[]>;
  renderCharts(): void;
  exportToCSV(): void;
}
```

**Krav til alle komponenter:**
- TypeScript interfaces for all data
- Error handling på alle async operasjoner
- Loading states
- Toast notifications ved suksess/feil
- Keyboard accessibility
```

---

### PROMPT 4: Service Layer

```
Implementer service layer for Mission Control.

**1. Supabase Service (src/services/supabase.ts)**
```typescript
import { createClient } from '@supabase/supabase-js';

const SUPABASE_URL = 'https://kvniauxokdtmpvjtfnje.supabase.co';
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...';

export const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

export interface AgendaItem {
  id: string;
  tenant_id: string;
  title: string;
  description?: string;
  category?: string;
  show_date: string;
  link_url?: string;
  notes?: string;
  order_index: number;
  created_by?: string;
}

export async function getAgendaItems(date: string): Promise<AgendaItem[]>;
export async function updateAgendaItem(id: string, data: Partial<AgendaItem>): Promise<void>;
export async function deleteAgendaItem(id: string): Promise<void>;
export async function createAgendaItem(item: Omit<AgendaItem, 'id'>): Promise<AgendaItem>;
```

**2. Brave News Service (src/services/brave.ts)**
```typescript
const BRAVE_API_KEY = 'BSAt0WSIpXP0Hp6sPvNwaaGuLoyewev';

export interface BraveNewsResult {
  title: string;
  description: string;
  url: string;
  source: string;
  published: string;
}

export async function searchNews(
  query: string, 
  options?: {
    category?: string;
    freshness?: 'pd' | 'pw' | 'pm';
    customPrompt?: string;
  }
): Promise<BraveNewsResult[]>;

export function calculateEntertainmentScore(
  title: string, 
  description?: string
): number;
```

**3. Nielsen/Podtoppen Service (src/services/metrics.ts)**
```typescript
export interface RadioMetrics {
  week_number: number;
  year: number;
  value: number;
}

export interface PodcastMetrics {
  week_number: number;
  year: number;
  rank: number;
  unique_units?: number;
}

export async function getLatestRadioMetrics(): Promise<RadioMetrics>;
export async function getRadioHistory(limit?: number): Promise<RadioMetrics[]>;
export async function getLatestPodcastMetrics(): Promise<PodcastMetrics>;
export async function getPodcastHistory(limit?: number): Promise<PodcastMetrics[]>;
```

**Krav:**
- All error handling må være robust
- Retry-logikk for nettverksfeil
- Caching der det er hensiktsmessig
- Logging for debugging
```

---

### PROMPT 5: CI/CD + Deploy

```
Sett opp CI/CD pipeline for Mission Control.

**GitHub Actions Workflow (.github/workflows/deploy.yml):**
```yaml
name: Build and Deploy

on:
  push:
    branches: [master]
  pull_request:
    branches: [master]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm run lint
      - run: npm run test:unit
      - run: npm run test:e2e

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-pages-artifact@v2
        with:
          path: ./dist

  deploy:
    needs: build
    runs-on: ubuntu-latest
    permissions:
      pages: write
      id-token: write
    steps:
      - uses: actions/deploy-pages@v2
```

**package.json scripts:**
```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "lint:fix": "eslint . --ext ts,tsx --fix",
    "format": "prettier --write \"src/**/*.{ts,tsx,css}\"",
    "test:unit": "vitest",
    "test:e2e": "playwright test",
    "test": "npm run test:unit && npm run test:e2e"
  }
}
```

**Krav:**
- Automatisk testing på PR
- Automatisk deploy til GitHub Pages ved push til master
- Bygget må feile ved TypeScript errors
- Bygget må feile ved lint errors
- Bygget må feile ved test failures
```

---

### PROMPT 6: Testing Komplett

```
Skriv komplette tester for Mission Control.

**Unit Tester (src/**/*.test.ts):**

1. **Login.test.ts**
```typescript
import { describe, it, expect, vi } from 'vitest';
import { Login } from '../components/Login';

describe('Login', () => {
  it('should validate correct password', () => {
    const login = new Login({ onSuccess: vi.fn() });
    expect(login.validatePassword('kloakontroll2026')).toBe(true);
  });

  it('should reject incorrect password', () => {
    const login = new Login({ onSuccess: vi.fn() });
    expect(login.validatePassword('wrong')).toBe(false);
  });

  it('should call onSuccess when login succeeds', () => {
    const onSuccess = vi.fn();
    const login = new Login({ onSuccess });
    login.login('kloakontroll2026');
    expect(onSuccess).toHaveBeenCalled();
  });
});
```

2. **brave.test.ts**
```typescript
import { describe, it, expect } from 'vitest';
import { calculateEntertainmentScore } from '../services/brave';

describe('calculateEntertainmentScore', () => {
  it('should give high score for drama keywords', () => {
    const score = calculateEntertainmentScore('Brudd i Paradise Hotel', '');
    expect(score).toBeGreaterThan(70);
  });

  it('should give low score for sport keywords', () => {
    const score = calculateEntertainmentScore('Fotballkamp resultat', '');
    expect(score).toBeLessThan(50);
  });

  it('should return score between 0 and 100', () => {
    const score = calculateEntertainmentScore('Test', '');
    expect(score).toBeGreaterThanOrEqual(0);
    expect(score).toBeLessThanOrEqual(100);
  });
});
```

**E2E Tester (e2e/*.spec.ts):**

1. **login.spec.ts**
```typescript
import { test, expect } from '@playwright/test';

test('user can login with correct password', async ({ page }) => {
  await page.goto('/');
  await page.fill('#password-input', 'kloakontroll2026');
  await page.click('#login-btn');
  await expect(page.locator('#app')).toBeVisible();
});

test('user cannot login with wrong password', async ({ page }) => {
  await page.goto('/');
  await page.fill('#password-input', 'wrong');
  await page.click('#login-btn');
  await expect(page.locator('#login-error')).toBeVisible();
});
```

2. **dashboard.spec.ts**
```typescript
import { test, expect } from '@playwright/test';

test.beforeEach(async ({ page }) => {
  await page.goto('/');
  await page.fill('#password-input', 'kloakontroll2026');
  await page.click('#login-btn');
});

test('dashboard shows stats', async ({ page }) => {
  await expect(page.locator('#dash-saker')).not.toHaveText('-');
  await expect(page.locator('#dash-radio')).not.toHaveText('-');
  await expect(page.locator('#dash-podcast')).not.toHaveText('-');
});

test('can navigate to saksliste', async ({ page }) => {
  await page.click('[data-section="saksliste"]');
  await expect(page.locator('#saksliste')).toHaveClass(/active/);
});
```

**Krav:**
- 100% coverage av kritiske funksjoner
- Alle tester må passere
- Ingen flaky tester
```

---

## 🎁 Bonus: Integrasjon med Eksisterende Skills

### Skills som bør integreres i Mission Control:

1. **content-aggregator** - Morning Routine integrasjon
2. **podcast-manager** - Podkast statistikk
3. **nrj-dashboard-system** - Automatisk dataoppdatering
4. **calendar** - Visning av kommende sendinger
5. **gmail** - Varsler om viktige e-poster

### PROMPT 7: Skill Integrasjon

```
Integrer følgende eksisterende skills i Mission Control:

**Filer å integrere:**
- /root/.openclaw/workspace/skills/content-aggregator/
- /root/.openclaw/workspace/skills/podcast-manager/
- /root/.openclaw/workspace/skills/nrj-dashboard-system/

**Integrasjonspunkter:**
1. **Morning Routine Panel** - Vis status for dagens morning routine
2. **Podkast Panel** - Vis siste episoder og statistikk
3. **Auto-refresh** - Hent data automatisk fra alle kilder
4. **Notifikasjoner** - Varsle om nye episoder, endringer, etc.

**Krav:**
- Gjenbruk eksisterende kode fra skills
- Ikke dupliser logikk
- Hold skills uavhengige men integrerte
```

---

## 📋 Oppsummering for Kimi Code

**Rekkefølge:**
1. PROMPT 1: Arkitektur-Refactoring
2. PROMPT 2: TypeScript + Testing Setup
3. PROMPT 3: Komponent-Implementering
4. PROMPT 4: Service Layer
5. PROMPT 5: CI/CD + Deploy
6. PROMPT 6: Testing Komplett
7. PROMPT 7: Skill Integrasjon (bonus)

**Suksesskriterier:**
- ✅ Ingen TypeScript errors
- ✅ 100% av tester passerer
- ✅ All funksjonalitet bevart
- ✅ Ingen console errors
- ✅ Lighthouse score > 90
- ✅ Deploy fungerer automatisk

**Tidsanslag:** 2-3 dager med fokusert arbeid