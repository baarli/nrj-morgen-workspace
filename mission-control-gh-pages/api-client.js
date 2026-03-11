// Mission Control Frontend - API Client
// Kobler til backend API for ekte data

const API_BASE_URL = '/kloakontroll/api';

class MissionControlAPI {
    async fetch(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;
        try {
            const response = await fetch(url, options);
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }
    
    // Saker
    async getSaker(date = null) {
        const dateParam = date ? `?date=${date}` : '';
        return this.fetch(`/saker${dateParam}`);
    }
    
    async createSak(data) {
        return this.fetch('/saker', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
    }
    
    async updateSak(id, data) {
        return this.fetch(`/saker/${id}`, {
            method: 'PATCH',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
    }
    
    async deleteSak(id) {
        return this.fetch(`/saker/${id}`, {method: 'DELETE'});
    }
    
    // Stats
    async getNRJStats() {
        return this.fetch('/nrj/stats');
    }
    
    // Morning Routine
    async runMorningRoutine() {
        return this.fetch('/routine/morning', {method: 'POST'});
    }
    
    async getMorningRoutineStatus() {
        return this.fetch('/routine/morning/status');
    }
    
    // Health
    async healthCheck() {
        return this.fetch('/health');
    }
}

const api = new MissionControlAPI();

// Oppdaterte Manager-klasser som bruker API
class SakslisteManager {
    constructor() {
        this.items = [];
        this.currentDate = new Date();
        this.loading = false;
    }
    
    async init() {
        await this.loadData();
    }
    
    async loadData() {
        this.loading = true;
        this.renderLoading();
        
        try {
            const result = await api.getSaker();
            this.items = result.saker || [];
            this.render();
        } catch (error) {
            console.error('Error loading saker:', error);
            this.renderError();
        } finally {
            this.loading = false;
        }
    }
    
    renderLoading() {
        const container = document.getElementById('saksliste-items');
        if (container) {
            container.innerHTML = '<div style="text-align: center; padding: 2rem;"><div class="spinner"></div><p>Laster saker...</p></div>';
        }
    }
    
    renderError() {
        const container = document.getElementById('saksliste-items');
        if (container) {
            container.innerHTML = '<div style="text-align: center; padding: 2rem; color: var(--color-danger);">Kunne ikke laste saker. Sjekk at API er tilgjengelig.</div>';
        }
    }
    
    render() {
        const container = document.getElementById('saksliste-items');
        if (!container) return;
        
        if (this.items.length === 0) {
            container.innerHTML = '<div style="text-align: center; padding: 2rem; color: var(--text-muted);">Ingen saker for i dag. Kjør Morning Routine for å legge til saker.</div>';
            return;
        }
        
        container.innerHTML = this.items.map((item, index) => {
            const categoryClass = this.getCategoryClass(item.category);
            return `
                <div class="sak-item" data-id="${item.id}">
                    <div class="sak-number">${index + 1}</div>
                    <div class="sak-content">
                        <div class="sak-title">${item.title}</div>
                        <div class="sak-meta">
                            <span class="sak-category ${categoryClass}">${item.category || 'TALK'}</span>
                            ${item.link_url ? `<a href="${item.link_url}" target="_blank" class="sak-link"><i class="fas fa-external-link-alt"></i> Lenke</a>` : ''}
                        </div>
                        ${item.notes ? `<div class="sak-notes">${item.notes.substring(0, 150)}...</div>` : ''}
                    </div>
                    <div class="sak-actions">
                        <button onclick="sakslisteManager.deleteSak('${item.id}')" class="btn-icon" title="Slett"><i class="fas fa-trash"></i></button>
                    </div>
                </div>
            `;
        }).join('');
        
        this.updateStats();
    }
    
    getCategoryClass(category) {
        const map = {
            'TALK': 'category-talk',
            'REALITY_TV': 'category-reality',
            'KJENDIS_DRAMA': 'category-kjendis',
            'FILM_TV': 'category-film',
            'MUSIKK': 'category-musikk',
            'INTERNASJONALT': 'category-internasjonalt'
        };
        return map[category] || 'category-talk';
    }
    
    updateStats() {
        const statsEl = document.getElementById('saksliste-count');
        if (statsEl) {
            statsEl.textContent = `${this.items.length} saker`;
        }
    }
    
    async deleteSak(id) {
        if (!confirm('Er du sikker på at du vil slette denne saken?')) return;
        
        try {
            await api.deleteSak(id);
            this.items = this.items.filter(item => item.id !== id);
            this.render();
        } catch (error) {
            alert('Kunne ikke slette sak: ' + error.message);
        }
    }
    
    async refresh() {
        await this.loadData();
    }
}

class StatsManager {
    async init() {
        await this.loadData();
    }
    
    async loadData() {
        try {
            const stats = await api.getNRJStats();
            this.render(stats);
        } catch (error) {
            console.error('Error loading stats:', error);
        }
    }
    
    render(stats) {
        if (stats.radio && stats.radio.link_metadata) {
            const metadata = typeof stats.radio.link_metadata === 'string' 
                ? JSON.parse(stats.radio.link_metadata) 
                : stats.radio.link_metadata;
            this.updateElement('radio-week', metadata.week || '-');
            this.updateElement('radio-listeners', metadata.dailyListeners ? metadata.dailyListeners.toLocaleString() : '-');
            this.updateElement('radio-trend', metadata.trend || '-');
        }
        
        if (stats.podcast && stats.podcast.link_metadata) {
            const metadata = typeof stats.podcast.link_metadata === 'string'
                ? JSON.parse(stats.podcast.link_metadata)
                : stats.podcast.link_metadata;
            this.updateElement('podcast-week', metadata.week || '-');
            this.updateElement('podcast-ranking', metadata.ranking || '-');
            this.updateElement('podcast-listeners', metadata.uniqueListeners ? metadata.uniqueListeners.toLocaleString() : '-');
        }
    }
    
    updateElement(id, value) {
        const el = document.getElementById(id);
        if (el) el.textContent = value;
    }
}

class MorningRoutineManager {
    constructor() {
        this.statusInterval = null;
    }
    
    async start() {
        try {
            const result = await api.runMorningRoutine();
            alert(result.message);
            this.startStatusPolling();
        } catch (error) {
            alert('Kunne ikke starte Morning Routine: ' + error.message);
        }
    }
    
    startStatusPolling() {
        if (this.statusInterval) clearInterval(this.statusInterval);
        
        this.statusInterval = setInterval(async () => {
            try {
                const status = await api.getMorningRoutineStatus();
                this.updateStatusUI(status);
                
                if (!status.running && this.statusInterval) {
                    clearInterval(this.statusInterval);
                    this.statusInterval = null;
                    // Refresh saksliste når ferdig
                    if (window.sakslisteManager) {
                        window.sakslisteManager.refresh();
                    }
                }
            } catch (error) {
                console.error('Error polling status:', error);
            }
        }, 3000);
    }
    
    updateStatusUI(status) {
        const statusEl = document.getElementById('morning-routine-status');
        if (statusEl) {
            statusEl.innerHTML = `
                <div class="status-badge ${status.running ? 'running' : 'idle'}">
                    ${status.running ? '⏳ Kjører' : '✅ Klar'}
                </div>
                ${status.message ? `<div class="status-message">${status.message}</div>` : ''}
                ${status.running ? `<div class="progress-bar"><div class="progress" style="width: ${status.progress}%"></div></div>` : ''}
            `;
        }
    }
}

// Initialiser når DOM er klar
document.addEventListener('DOMContentLoaded', () => {
    window.sakslisteManager = new SakslisteManager();
    window.statsManager = new StatsManager();
    window.morningRoutineManager = new MorningRoutineManager();
    window.api = api;
    
    // Start initialisering
    window.sakslisteManager.init();
    window.statsManager.init();
    
    // Sjekk API health
    api.healthCheck().then(() => {
        console.log('✅ Mission Control API tilkoblet');
    }).catch(err => {
        console.warn('⚠️ API ikke tilgjengelig:', err);
    });
});
