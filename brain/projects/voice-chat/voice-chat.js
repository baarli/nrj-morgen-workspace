// Voice Chat Module for Mission Control
// Integreres i index.html

class VoiceChat {
    constructor() {
        this.recognition = null;
        this.isListening = false;
        this.supabase = null;
        this.conversationHistory = [];
        
        this.init();
    }
    
    init() {
        // Sjekk om browser støtter Speech Recognition
        if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
            this.setupSpeechRecognition();
            this.createUI();
            console.log('✅ Voice Chat initialized');
        } else {
            console.log('❌ Speech Recognition not supported');
        }
    }
    
    setupSpeechRecognition() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();
        this.recognition.lang = 'nb-NO'; // Norsk bokmål
        this.recognition.continuous = false;
        this.recognition.interimResults = false;
        
        this.recognition.onstart = () => {
            this.isListening = true;
            this.updateUI('listening');
            console.log('🎤 Listening...');
        };
        
        this.recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            console.log('🗣️ User said:', transcript);
            this.handleUserInput(transcript);
        };
        
        this.recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            this.updateUI('error');
        };
        
        this.recognition.onend = () => {
            this.isListening = false;
            this.updateUI('idle');
        };
    }
    
    createUI() {
        // Lag voice chat container
        const container = document.createElement('div');
        container.id = 'voice-chat-container';
        container.innerHTML = `
            <div class="voice-chat-panel">
                <div class="voice-chat-header">
                    <span>🎙️ Voice Chat med Vev</span>
                    <button id="voice-chat-toggle" class="voice-btn">
                        🎤 Start
                    </button>
                </div>
                <div id="voice-status" class="voice-status idle">
                    Klikk for å snakke med Vev
                </div>
                <div id="voice-conversation" class="voice-conversation">
                    <!-- Samtale vises her -->
                </div>
            </div>
        `;
        
        // Legg til styling
        const style = document.createElement('style');
        style.textContent = `
            .voice-chat-panel {
                position: fixed;
                bottom: 20px;
                right: 20px;
                width: 350px;
                background: #1a1a2e;
                border: 2px solid #4a4a6a;
                border-radius: 12px;
                padding: 16px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.5);
                z-index: 1000;
            }
            
            .voice-chat-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 12px;
                color: #fff;
                font-weight: bold;
            }
            
            .voice-btn {
                background: #4a4a6a;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 20px;
                cursor: pointer;
                transition: all 0.3s;
            }
            
            .voice-btn:hover {
                background: #6a6a8a;
            }
            
            .voice-btn.listening {
                background: #ff4757;
                animation: pulse 1s infinite;
            }
            
            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }
            
            .voice-status {
                text-align: center;
                padding: 12px;
                border-radius: 8px;
                margin-bottom: 12px;
                font-size: 14px;
            }
            
            .voice-status.idle {
                background: #2a2a4a;
                color: #aaa;
            }
            
            .voice-status.listening {
                background: #ff4757;
                color: white;
                animation: pulse 1s infinite;
            }
            
            .voice-status.processing {
                background: #ffa502;
                color: #1a1a2e;
            }
            
            .voice-conversation {
                max-height: 200px;
                overflow-y: auto;
                font-size: 13px;
            }
            
            .voice-message {
                margin: 8px 0;
                padding: 8px 12px;
                border-radius: 8px;
            }
            
            .voice-message.user {
                background: #4a4a6a;
                color: white;
                text-align: right;
            }
            
            .voice-message.vev {
                background: #2a2a4a;
                color: #7bed9f;
                text-align: left;
            }
        `;
        
        document.head.appendChild(style);
        document.body.appendChild(container);
        
        // Sett opp event listeners
        document.getElementById('voice-chat-toggle').addEventListener('click', () => {
            this.toggleListening();
        });
    }
    
    toggleListening() {
        if (this.isListening) {
            this.recognition.stop();
        } else {
            this.recognition.start();
        }
    }
    
    updateUI(state) {
        const status = document.getElementById('voice-status');
        const button = document.getElementById('voice-chat-toggle');
        
        switch(state) {
            case 'listening':
                status.textContent = '🎤 Lytter... Snakk nå!';
                status.className = 'voice-status listening';
                button.textContent = '⏹️ Stopp';
                button.className = 'voice-btn listening';
                break;
            case 'processing':
                status.textContent = '🤔 Vev tenker...';
                status.className = 'voice-status processing';
                button.className = 'voice-btn';
                break;
            case 'error':
                status.textContent = '❌ Noe gikk galt. Prøv igjen.';
                status.className = 'voice-status idle';
                button.textContent = '🎤 Start';
                button.className = 'voice-btn';
                break;
            case 'idle':
            default:
                status.textContent = 'Klikk for å snakke med Vev';
                status.className = 'voice-status idle';
                button.textContent = '🎤 Start';
                button.className = 'voice-btn';
        }
    }
    
    async handleUserInput(text) {
        // Vis brukerens melding
        this.addMessage('user', text);
        this.updateUI('processing');
        
        // Send til Vev via Supabase
        try {
            const response = await this.sendToVev(text);
            this.addMessage('vev', response.text);
            
            // Spill av audio hvis tilgjengelig
            if (response.audio_url) {
                this.playAudio(response.audio_url);
            }
        } catch (error) {
            console.error('Error:', error);
            this.addMessage('vev', 'Beklager, jeg kunne ikke høre deg. Kan du prøve igjen?');
        }
        
        this.updateUI('idle');
    }
    
    async sendToVev(text) {
        try {
            // Send til Supabase Edge Function
            const response = await fetch(
                `${this.supabaseUrl}/functions/v1/voice-chat`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${this.supabaseKey}`
                    },
                    body: JSON.stringify({
                        text: text,
                        user_id: this.userId,
                        session_id: this.sessionId
                    })
                }
            );
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            return {
                text: data.text,
                audio_url: data.audio_url
            };
        } catch (error) {
            console.error('Error sending to Vev:', error);
            return {
                text: "Beklager, jeg har tekniske problemer. Kan du prøve igjen?",
                audio_url: null
            };
        }
    }
    
    addMessage(sender, text) {
        const conversation = document.getElementById('voice-conversation');
        const message = document.createElement('div');
        message.className = `voice-message ${sender}`;
        message.textContent = text;
        conversation.appendChild(message);
        conversation.scrollTop = conversation.scrollHeight;
        
        // Lagre i historikk
        this.conversationHistory.push({
            sender,
            text,
            timestamp: new Date().toISOString()
        });
    }
    
    playAudio(url) {
        const audio = new Audio(url);
        audio.play();
    }
}

// Initialiser når siden laster
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.voiceChat = new VoiceChat();
    });
} else {
    window.voiceChat = new VoiceChat();
}
