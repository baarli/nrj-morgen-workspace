// AI Content Suggestions Module for Mission Control
// Integrates with OpenAI to suggest improvements to sakslista items

class AIContentSuggester {
    constructor() {
        this.apiEndpoint = '/api/ai/suggest';
        this.isEnabled = true;
    }

    // Initialize the module
    init() {
        console.log('🤖 AI Content Suggestions initialized');
        this.addSuggestionButtons();
        this.observeNewItems();
    }

    // Add suggestion buttons to all sakslista items
    addSuggestionButtons() {
        const items = document.querySelectorAll('.saks-item');
        items.forEach(item => {
            if (!item.querySelector('.ai-suggest-btn')) {
                const btn = document.createElement('button');
                btn.className = 'ai-suggest-btn';
                btn.innerHTML = '💡 AI Forslag';
                btn.onclick = () => this.getSuggestions(item);
                item.appendChild(btn);
            }
        });
    }

    // Get AI suggestions for an item
    async getSuggestions(item) {
        const title = item.querySelector('.item-title')?.textContent || '';
        const description = item.querySelector('.item-desc')?.textContent || '';

        try {
            const response = await fetch(this.apiEndpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title, description })
            });

            const suggestions = await response.json();
            this.displaySuggestions(item, suggestions);
        } catch (error) {
            console.error('AI suggestion error:', error);
            this.showFallbackSuggestions(item);
        }
    }

    // Display suggestions in UI
    displaySuggestions(item, suggestions) {
        const container = document.createElement('div');
        container.className = 'ai-suggestions-panel';
        container.innerHTML = `
            <h4>🤖 AI Forslag</h4>
            <div class="suggestion-list">
                ${suggestions.map((s, i) => `
                    <div class="suggestion-item">
                        <span class="suggestion-type">${s.type}</span>
                        <p>${s.text}</p>
                        <button onclick="aiSuggester.applySuggestion(this, '${s.text.replace(/'/g, "\\'")}')">Bruk</button>
                    </div>
                `).join('')}
            </div>
        `;

        // Remove existing panel
        const existing = item.querySelector('.ai-suggestions-panel');
        if (existing) existing.remove();

        item.appendChild(container);
    }

    // Apply a suggestion
    applySuggestion(button, text) {
        const item = button.closest('.saks-item');
        const descField = item.querySelector('.item-desc');
        if (descField) {
            descField.textContent = text;
            descField.classList.add('ai-modified');
        }
        button.closest('.ai-suggestions-panel').remove();
    }

    // Fallback suggestions if API fails
    showFallbackSuggestions(item) {
        const suggestions = [
            { type: 'Tittel', text: 'Gjør tittelen mer spennende med action-verb' },
            { type: 'Beskrivelse', text: 'Legg til 1-2 setninger om hvorfor dette er relevant' },
            { type: 'Inngang', text: 'Start med et spørsmål for å engasjere lytteren' }
        ];
        this.displaySuggestions(item, suggestions);
    }

    // Observe for new items added to DOM
    observeNewItems() {
        const observer = new MutationObserver(() => {
            this.addSuggestionButtons();
        });
        observer.observe(document.body, { childList: true, subtree: true });
    }
}

// Initialize when DOM is ready
let aiSuggester;
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        aiSuggester = new AIContentSuggester();
        aiSuggester.init();
    });
} else {
    aiSuggester = new AIContentSuggester();
    aiSuggester.init();
}

// Export for use in other modules
window.AIContentSuggester = AIContentSuggester;
window.aiSuggester = aiSuggester;
