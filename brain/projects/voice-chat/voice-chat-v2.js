// Voice Chat Module v2.0 for Mission Control
// Med real-time streaming og emosjonell stemme

class VoiceChatV2 {
    constructor() {
        this.recognition = null;
        this.isListening = false;
        this.audioContext = null;
        this.mediaRecorder = null;
        this.stream = null;
        this.conversationHistory = [];
        
        this.init();
    }
    
    init() {
        if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
            this.setupSpeechRecognition();
            this.createUI();
            console.log('✅ Voice Chat v2.0 initialized');
        } else {
            console.log('❌ Speech Recognition not supported');
        }
    }
    
    setupSpeechRecognition() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();
        this.recognition.lang = 'nb-NO';
        this.recognition.continuous = false;
        this.recognition.interimResults = true;
        
        this.recognition.onstart = () => {
            this.isListening = true;
            this.updateUI('listening');
            console.log('🎤 Listening...');
        };
        
        this.recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            const isFinal = event.results[0].isFinal;
            
            if (isFinal) {
                console.log('🗣️ User said:', transcript);
                this.handleUserInput(transcript);
            } else {
                this.updateInterim(transcript);
            }
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
        const container = document.createElement('div');
        container.id = 'voice-chat-v2-container';
        container.innerHTML = `
            <div id="voice-v2-panel" style="
                position: fixed;
                bottom: 20px;
                right: 20px;
                width: 350px;
                background: linear-gradient(135deg, #1e293b, #0f172a);
                border: 2px solid #6366f1;
                border-radius: 16px;
                padding: 16px;
                box-shadow: 0 8px 32px rgba(99, 102, 241, 0.3);
                z-index: 10000;
                font-family: Inter, sans-serif;
            ">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <span style="color: #fff; font-weight: 600;">🎙️ Snakk med Vev v2.0</span>
                    <button id="voice-v2-btn" style="
                        background: #6366f1;
                        color: white;
                        border: none;
                        padding: 8px 16px;
                        border-radius: 20px;
                        cursor: pointer;
                        font-size: 14px;
                    ">🎤 Start</button>
                </div>
                <div id="voice-v2-status" style="
                    text-align: center;
                    padding: 12px;
                    border-radius: 8px;
                    background: #334155;
                    color: #94a3b8;
                    font-size: 13px;
                ">Klikk for å snakke med Vev</div>
            </div>
        `;
        
        document.body.appendChild(container);
        
        document.getElementById('voice-v2-btn').addEventListener('click', () => {
            this.toggleListening();
        });
    }
    
    updateUI(state) {
        const status = document.getElementById('voice-v2-status');
        const btn = document.getElementById('voice-v2-btn');
        
        switch(state) {
            case 'listening':
                status.textContent = '🎤 Lytter... Snakk nå!';
                status.style.background = '#ef4444';
                btn.textContent = '⏹️ Stopp';
                break;
            case 'processing':
                status.textContent = '🤔 Vev tenker...';
                status.style.background = '#f59e0b';
                btn.textContent = '⏳ Venter';
                break;
            case 'error':
                status.textContent = '❌ Feil. Prøv igjen.';
                status.style.background = '#334155';
                btn.textContent = '🎤 Start';
                break;
            default:
                status.textContent = 'Klikk for å snakke med Vev';
                status.style.background = '#334155';
                btn.textContent = '🎤 Start';
        }
    }
    
    updateInterim(text) {
        // Show what we're hearing in real-time
        console.log('Hører:', text);
    }
    
    toggleListening() {
        if (this.isListening) {
            this.recognition.stop();
        } else {
            this.recognition.start();
        }
    }
    
    async handleUserInput(text) {
        this.updateUI('processing');
        
        try {
            // TODO: Implement streaming response
            console.log('Sending to Vev:', text);
            
            // Simulate response for now
            setTimeout(() => {
                this.updateUI('idle');
            }, 2000);
            
        } catch (error) {
            console.error('Error:', error);
            this.updateUI('error');
        }
    }
}

// Initialize
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.voiceChatV2 = new VoiceChatV2();
    });
} else {
    window.voiceChatV2 = new VoiceChatV2();
}
