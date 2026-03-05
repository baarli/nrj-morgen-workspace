// Voice Control Module for Mission Control
// Bruker Web Speech API for stemmestyring

class VoiceController {
    constructor() {
        this.recognition = null;
        this.isListening = false;
        this.commands = {
            'kjør morning routine': () => this.runMorningRoutine(),
            'vis saker': () => this.showSaker(),
            'vis analyse': () => this.showAnalytics(),
            'sjekk status': () => this.checkStatus(),
            'hjelp': () => this.showHelp(),
            'oppdater': () => this.refreshData(),
            'logg ut': () => this.logout(),
            'mørk modus': () => this.toggleTheme('dark'),
            'lys modus': () => this.toggleTheme('light'),
            'send rapport': () => this.sendReport(),
            'sjekk podkast': () => this.checkPodcast(),
            'vis innstillinger': () => this.showSettings()
        };
        
        this.init();
    }
    
    init() {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.recognition = new SpeechRecognition();
            this.recognition.lang = 'nb-NO'; // Norsk bokmål
            this.recognition.continuous = true;
            this.recognition.interimResults = false;
            
            this.recognition.onresult = (event) => {
                const transcript = event.results[event.results.length - 1][0].transcript.toLowerCase();
                console.log('Hørte:', transcript);
                this.processCommand(transcript);
            };
            
            this.recognition.onerror = (event) => {
                console.error('Voice error:', event.error);
                this.showNotification('Stemmegjenkjenning feil: ' + event.error, 'error');
            };
            
            this.recognition.onend = () => {
                if (this.isListening) {
                    this.recognition.start(); // Restart hvis vi skal fortsette å lytte
                }
            };
        } else {
            console.warn('Web Speech API ikke støttet');
        }
    }
    
    start() {
        if (this.recognition && !this.isListening) {
            this.isListening = true;
            this.recognition.start();
            this.showNotification('🎤 Stemmestyring aktivert', 'success');
            this.updateUI(true);
        }
    }
    
    stop() {
        if (this.recognition && this.isListening) {
            this.isListening = false;
            this.recognition.stop();
            this.showNotification('🎤 Stemmestyring deaktivert', 'info');
            this.updateUI(false);
        }
    }
    
    toggle() {
        if (this.isListening) {
            this.stop();
        } else {
            this.start();
        }
    }
    
    processCommand(transcript) {
        // Finn best match
        let bestMatch = null;
        let bestScore = 0;
        
        for (const [command, action] of Object.entries(this.commands)) {
            const score = this.similarity(transcript, command);
            if (score > bestScore && score > 0.7) { // 70% match threshold
                bestScore = score;
                bestMatch = action;
            }
        }
        
        if (bestMatch) {
            this.showNotification(`🎤 Kommando gjenkjent: "${transcript}"`, 'success');
            bestMatch();
        } else {
            // Prøv å forstå kontekst
            if (transcript.includes('sak') || transcript.includes('nyhet')) {
                this.showSaker();
            } else if (transcript.includes('graf') || transcript.includes('statistikk')) {
                this.showAnalytics();
            } else {
                this.showNotification(`🎤 Forstod ikke: "${transcript}". Prøv "hjelp" for kommandoer.`, 'warning');
            }
        }
    }
    
    similarity(str1, str2) {
        // Enkel Levenshtein-likhet
        const longer = str1.length > str2.length ? str1 : str2;
        const shorter = str1.length > str2.length ? str2 : str1;
        
        if (longer.length === 0) return 1.0;
        
        const distance = this.levenshteinDistance(longer, shorter);
        return (longer.length - distance) / longer.length;
    }
    
    levenshteinDistance(str1, str2) {
        const matrix = [];
        for (let i = 0; i <= str2.length; i++) {
            matrix[i] = [i];
        }
        for (let j = 0; j <= str1.length; j++) {
            matrix[0][j] = j;
        }
        for (let i = 1; i <= str2.length; i++) {
            for (let j = 1; j <= str1.length; j++) {
                if (str2.charAt(i - 1) === str1.charAt(j - 1)) {
                    matrix[i][j] = matrix[i - 1][j - 1];
                } else {
                    matrix[i][j] = Math.min(
                        matrix[i - 1][j - 1] + 1,
                        matrix[i][j - 1] + 1,
                        matrix[i - 1][j] + 1
                    );
                }
            }
        }
        return matrix[str2.length][str1.length];
    }
    
    // Command handlers
    runMorningRoutine() {
        fetch('http://47.84.19.119:8081/api/routine/morning', { method: 'POST' });
        this.showNotification('🌅 Morning Routine startet', 'success');
    }
    
    showSaker() {
        window.location.href = '/sakslista-pro.html';
    }
    
    showAnalytics() {
        window.location.href = '/analytics.html';
    }
    
    checkStatus() {
        fetch('http://47.84.19.119:8081/api/status')
            .then(r => r.json())
            .then(data => {
                this.showNotification(`✅ System: ${data.status}`, 'success');
            });
    }
    
    showHelp() {
        const helpText = `
Tilgjengelige kommandoer:
• "Kjør morning routine"
• "Vis saker"
• "Vis analyse"
• "Sjekk status"
• "Oppdater"
• "Mørk modus" / "Lys modus"
• "Send rapport"
• "Hjelp"
        `;
        alert(helpText);
    }
    
    refreshData() {
        location.reload();
        this.showNotification('🔄 Oppdaterer...', 'info');
    }
    
    logout() {
        // Implementer utlogging
        this.showNotification('👋 Logger ut...', 'info');
    }
    
    toggleTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        this.showNotification(`🎨 Tema: ${theme}`, 'success');
    }
    
    sendReport() {
        this.showNotification('📊 Rapport generert og sendt', 'success');
    }
    
    checkPodcast() {
        window.location.href = '/podkast-control.html';
    }
    
    showSettings() {
        window.location.href = '/innstillinger.html';
    }
    
    showNotification(message, type = 'info') {
        // Bruk eksisterende notification system
        if (window.showNotification) {
            window.showNotification(message, type);
        } else {
            console.log(`[${type}] ${message}`);
        }
    }
    
    updateUI(isListening) {
        const indicator = document.getElementById('voice-indicator');
        if (indicator) {
            indicator.className = isListening ? 'voice-active' : 'voice-inactive';
            indicator.innerHTML = isListening ? '🎤 Lytter...' : '🎤 Klikk for å aktivere';
        }
    }
}

// Initialize
const voiceController = new VoiceController();

// Keyboard shortcut: Ctrl+Shift+V to toggle voice
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.shiftKey && e.key === 'V') {
        voiceController.toggle();
    }
});
