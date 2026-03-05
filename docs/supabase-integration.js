// Mission Control - Supabase Integration Module
// Henter ekte data fra Supabase for NRJ Morgen

const SUPABASE_URL = 'https://kvniauxokdtmpvjtfnej.supabase.co';
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt2bmlhdXhva2R0bXB2anRmbmVqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEzNjcyMzQsImV4cCI6MjA2Njk0MzIzNH0._24RuF95RnxxHj3sjGswdd36VVYlX_jKxut8dvELfSA';
const TENANT_ID = 'a0000000-0000-0000-0000-000000000001';

class SupabaseClient {
    constructor() {
        this.baseUrl = SUPABASE_URL;
        this.apiKey = SUPABASE_KEY;
    }
    
    async fetch(endpoint, options = {}) {
        const url = `${this.baseUrl}/rest/v1${endpoint}`;
        const headers = {
            'apikey': this.apiKey,
            'Authorization': `Bearer ${this.apiKey}`,
            'Content-Type': 'application/json',
            ...options.headers
        };
        
        try {
            const response = await fetch(url, { ...options, headers });
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error('Supabase fetch error:', error);
            throw error;
        }
    }
    
    // Hent dagens saker
    async getTodaysSaker() {
        const today = new Date().toISOString().split('T')[0];
        return this.fetch(`/agenda_items?tenant_id=eq.${TENANT_ID}&show_date=eq.${today}&order=order_index.asc`);
    }
    
    // Hent saker for en spesifikk dato
    async getSakerForDate(date) {
        return this.fetch(`/agenda_items?tenant_id=eq.${TENANT_ID}&show_date=eq.${date}&order=order_index.asc`);
    }
    
    // Hent alle saker (siste 30 dager)
    async getAllSaker() {
        const thirtyDaysAgo = new Date();
        thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
        const dateStr = thirtyDaysAgo.toISOString().split('T')[0];
        return this.fetch(`/agenda_items?tenant_id=eq.${TENANT_ID}&show_date=gte.${dateStr}&order=show_date.desc`);
    }
    
    // Hent NRJ statistikk
    async getNRJStats() {
        // Hent siste radio-stats
        const radioStats = await this.fetch(`/agenda_items?tenant_id=eq.${TENANT_ID}&category=eq.STATS&order=created_at.desc&limit=1`);
        
        // Hent siste podcast-ranking
        const podcastStats = await this.fetch(`/agenda_items?tenant_id=eq.${TENANT_ID}&category=eq.PODCAST_RANKING&order=created_at.desc&limit=1`);
        
        return {
            radio: radioStats[0] || null,
            podcast: podcastStats[0] || null
        };
    }
    
    // Hent podkast-episoder
    async getPodcastEpisodes() {
        return this.fetch(`/podcast_episodes?order=published_at.desc&limit=20`);
    }
    
    // Slett en sak
    async deleteSak(id) {
        return this.fetch(`/agenda_items?id=eq.${id}`, {
            method: 'DELETE'
        });
    }
    
    // Oppdater en sak
    async updateSak(id, data) {
        return this.fetch(`/agenda_items?id=eq.${id}`, {
            method: 'PATCH',
            body: JSON.stringify(data)
        });
    }
}

// Initialiser Supabase-klient
const supabase = new SupabaseClient();

// Oppdatert Saksliste-klasse med ekte data
class RealSakslisteManager {
    constructor() {
        this.items = [];
        this.currentDate = new Date();
        this.loading = false;
        this.supabase = supabase;
    }
    
    async init() {
        await this.loadData();
        this.render();
    }
    
    async loadData() {
        this.loading = true;
        this.renderLoading();
        
        try {
            const today = new Date().toISOString().split('T')[0];
            this.items = await this.supabase.getSakerForDate(today);
            this.updateStats();
        } catch (error) {
            console.error('Error loading saker:', error);
            this.items = [];
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
    
    render() {
        const container = document.getElementById('saksliste-items');
        if (!container) return;
        
        if (this.items.length === 0) {
            container.innerHTML = '<div style="text-align: center; padding: 2rem; color: var(--text-muted);">Ingen saker for i dag. Kjør Morning Routine for å legge til saker.</div>';
            return;
        }
        
        container.innerHTML = this.items.map((item, index) => {
            const categoryClass = this.getCategoryClass(item.category);
            const imageUrl = item.link_metadata?.image_url || item.image_url || '';
            
            return `
                <div class="sak-item" data-id="${item.id}">
                    <div class="sak-number">${index + 1}</div>
                    <div class="sak-content">
                        <div class="sak-title">${item.title}</div>
                        <div class="sak-meta">
                            <span class="sak-category ${categoryClass}">${item.category || 'TALK'}</span>
                            ${item.link_url ? `<a href="${item.link_url}" target="_blank" class="sak-link"><i class="fas fa-external-link-alt"></i> Lenke</a>` : ''}
                        </div>
                        ${item.notes ? `<div class="sak-notes">${item.notes.substring(0, 100)}...</div>` : ''}
                    </div>
                    <div class="sak-actions">
                        <button onclick="sakslisteManager.deleteSak('${item.id}')" class="btn-icon" title="Slett"><i class="fas fa-trash"></i></button>
                    </div>
                </div>
            `;
        }).join('');
    }
    
    getCategoryClass(category) {
        const map = {
            'TALK': 'category-talk',
            'REALITY_TV': 'category-reality',
            'KJENDIS_DRAMA': 'category-kjendis',
            'FILM_TV': 'category-film',
            'MUSIKK': 'category-musikk',
            'INTERNASJONALT': 'category-internasjonalt',
            'STATS': 'category-stats'
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
            await this.supabase.deleteSak(id);
            this.items = this.items.filter(item => item.id !== id);
            this.render();
            this.updateStats();
        } catch (error) {
            alert('Kunne ikke slette sak: ' + error.message);
        }
    }
}

// Oppdatert Podkast-klasse med ekte data
class RealPodcastManager {
    constructor() {
        this.episodes = [];
        this.supabase = supabase;
    }
    
    async init() {
        await this.loadData();
        this.render();
    }
    
    async loadData() {
        try {
            // Hent fra Supabase hvis tabellen finnes, ellers bruk mock
            this.episodes = await this.supabase.getPodcastEpisodes();
        } catch (error) {
            console.log('Podcast episodes not available in Supabase, using fallback');
            this.episodes = this.getFallbackEpisodes();
        }
    }
    
    getFallbackEpisodes() {
        return [
            { title: 'Baarli og Benjamin går i terapi - Episode 1', date: '2026-03-01', duration: '45:30' },
            { title: 'NRJ Morgen Podkast - Uke 9', date: '2026-03-02', duration: '32:15' }
        ];
    }
    
    render() {
        const container = document.getElementById('podcast-episodes');
        if (!container) return;
        
        container.innerHTML = this.episodes.map(ep => `
            <div class="podcast-episode">
                <div class="episode-title">${ep.title}</div>
                <div class="episode-meta">${ep.date} • ${ep.duration || '45:00'}</div>
            </div>
        `).join('');
    }
}

// Oppdatert Statistikk-klasse med ekte data
class RealStatsManager {
    constructor() {
        this.supabase = supabase;
    }
    
    async init() {
        await this.loadData();
    }
    
    async loadData() {
        try {
            const stats = await this.supabase.getNRJStats();
            this.render(stats);
        } catch (error) {
            console.error('Error loading stats:', error);
        }
    }
    
    render(stats) {
        // Oppdater radio-stats
        if (stats.radio) {
            const metadata = stats.radio.link_metadata ? JSON.parse(stats.radio.link_metadata) : {};
            this.updateElement('radio-week', metadata.week || '-');
            this.updateElement('radio-listeners', metadata.dailyListeners ? metadata.dailyListeners.toLocaleString() : '-');
            this.updateElement('radio-trend', metadata.trend || '-');
        }
        
        // Oppdater podcast-stats
        if (stats.podcast) {
            const metadata = stats.podcast.link_metadata ? JSON.parse(stats.podcast.link_metadata) : {};
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

// Initialiser alle managere når siden lastes
document.addEventListener('DOMContentLoaded', () => {
    // Gjør tilgjengelig globalt
    window.sakslisteManager = new RealSakslisteManager();
    window.podcastManager = new RealPodcastManager();
    window.statsManager = new RealStatsManager();
    window.supabase = supabase;
    
    // Initialiser
    window.sakslisteManager.init();
    window.podcastManager.init();
    window.statsManager.init();
});
