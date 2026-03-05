// Real-Time Collaboration Module for Mission Control
// Enables live cursor tracking and simultaneous editing

class RealTimeCollaboration {
    constructor() {
        this.socket = null;
        this.userId = this.generateUserId();
        this.username = this.getUsername();
        this.avatar = this.getAvatar();
        this.connected = false;
        this.otherCursors = new Map();
        this.activeEditors = new Map();
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
    }

    // Initialize collaboration
    init() {
        console.log('🤝 Initializing Real-Time Collaboration...');
        this.connect();
        this.setupCursorTracking();
        this.setupEditingTracking();
        this.createUserPresenceUI();
    }

    // Generate unique user ID
    generateUserId() {
        return 'user_' + Math.random().toString(36).substr(2, 9);
    }

    // Get username from localStorage or generate
    getUsername() {
        return localStorage.getItem('collab_username') || 
               'User ' + Math.floor(Math.random() * 1000);
    }

    // Get avatar URL
    getAvatar() {
        return localStorage.getItem('collab_avatar') || 
               `https://api.dicebear.com/7.x/avataaars/svg?seed=${this.userId}`;
    }

    // Connect to WebSocket
    connect() {
        const wsUrl = 'ws://47.84.19.119:8082';
        
        try {
            this.socket = new WebSocket(wsUrl);
            
            this.socket.onopen = () => {
                console.log('✅ Collaboration connected');
                this.connected = true;
                this.reconnectAttempts = 0;
                this.broadcastUserJoined();
                this.updateConnectionStatus('connected');
            };
            
            this.socket.onmessage = (event) => {
                this.handleMessage(JSON.parse(event.data));
            };
            
            this.socket.onclose = () => {
                console.log('❌ Collaboration disconnected');
                this.connected = false;
                this.updateConnectionStatus('disconnected');
                this.attemptReconnect();
            };
            
            this.socket.onerror = (error) => {
                console.error('Collaboration error:', error);
                this.updateConnectionStatus('error');
            };
            
        } catch (error) {
            console.error('Failed to connect:', error);
            this.updateConnectionStatus('error');
        }
    }

    // Attempt to reconnect
    attemptReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            console.log(`🔄 Reconnecting... Attempt ${this.reconnectAttempts}`);
            this.updateConnectionStatus('reconnecting');
            setTimeout(() => this.connect(), 3000 * this.reconnectAttempts);
        } else {
            console.log('❌ Max reconnection attempts reached');
            this.updateConnectionStatus('failed');
        }
    }

    // Handle incoming messages
    handleMessage(message) {
        switch (message.type) {
            case 'cursor_move':
                this.handleCursorMove(message.data);
                break;
            case 'user_joined':
                this.handleUserJoined(message.data);
                break;
            case 'user_left':
                this.handleUserLeft(message.data);
                break;
            case 'item_editing':
                this.handleItemEditing(message.data);
                break;
            case 'history':
                console.log('📜 Received message history');
                break;
        }
    }

    // Broadcast user joined
    broadcastUserJoined() {
        if (this.socket && this.connected) {
            this.socket.send(JSON.stringify({
                type: 'user_joined',
                data: {
                    user_id: this.userId,
                    username: this.username,
                    avatar: this.avatar
                }
            }));
        }
    }

    // Setup cursor tracking
    setupCursorTracking() {
        let lastX = 0;
        let lastY = 0;
        let throttleTimer = null;
        
        document.addEventListener('mousemove', (e) => {
            if (!this.connected) return;
            
            // Throttle to 20 updates per second
            if (throttleTimer) return;
            
            throttleTimer = setTimeout(() => {
                throttleTimer = null;
            }, 50);
            
            // Only send if position changed significantly
            if (Math.abs(e.clientX - lastX) > 5 || Math.abs(e.clientY - lastY) > 5) {
                lastX = e.clientX;
                lastY = e.clientY;
                
                this.socket.send(JSON.stringify({
                    type: 'cursor_move',
                    data: {
                        user_id: this.userId,
                        username: this.username,
                        x: e.clientX / window.innerWidth,
                        y: e.clientY / window.innerHeight,
                        page: window.location.pathname
                    }
                }));
            }
        });
    }

    // Handle cursor move from other users
    handleCursorMove(data) {
        if (data.user_id === this.userId) return;
        if (data.page !== window.location.pathname) return;
        
        let cursor = this.otherCursors.get(data.user_id);
        
        if (!cursor) {
            cursor = this.createCursorElement(data);
            this.otherCursors.set(data.user_id, cursor);
        }
        
        // Update position
        const x = data.x * window.innerWidth;
        const y = data.y * window.innerHeight;
        cursor.element.style.left = x + 'px';
        cursor.element.style.top = y + 'px';
        cursor.lastUpdate = Date.now();
    }

    // Create cursor element for other user
    createCursorElement(data) {
        const el = document.createElement('div');
        el.className = 'collab-cursor';
        el.innerHTML = `
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M5.65376 12.3673H5.46026L5.31717 12.4976L0.500002 16.8829L0.500002 1.19177L11.7841 12.3673H5.65376Z" fill="${this.getUserColor(data.user_id)}" stroke="white"/>
            </svg>
            <span class="collab-cursor-label">${data.username}</span>
        `;
        el.style.cssText = `
            position: fixed;
            pointer-events: none;
            z-index: 9999;
            transition: left 0.1s, top 0.1s;
        `;
        document.body.appendChild(el);
        
        return { element: el, lastUpdate: Date.now() };
    }

    // Get consistent color for user
    getUserColor(userId) {
        const colors = ['#667eea', '#f093fb', '#4facfe', '#43e97b', '#fa709a', '#feca57'];
        let hash = 0;
        for (let i = 0; i < userId.length; i++) {
            hash = userId.charCodeAt(i) + ((hash << 5) - hash);
        }
        return colors[Math.abs(hash) % colors.length];
    }

    // Setup editing tracking
    setupEditingTracking() {
        // Track when user starts editing
        document.addEventListener('focus', (e) => {
            if (e.target.matches('input, textarea, [contenteditable]')) {
                const itemId = this.findItemId(e.target);
                if (itemId && this.connected) {
                    this.socket.send(JSON.stringify({
                        type: 'item_editing',
                        data: {
                            item_id: itemId,
                            user_id: this.userId,
                            username: this.username,
                            is_editing: true
                        }
                    }));
                }
            }
        }, true);

        // Track when user stops editing
        document.addEventListener('blur', (e) => {
            if (e.target.matches('input, textarea, [contenteditable]')) {
                const itemId = this.findItemId(e.target);
                if (itemId && this.connected) {
                    this.socket.send(JSON.stringify({
                        type: 'item_editing',
                        data: {
                            item_id: itemId,
                            user_id: this.userId,
                            username: this.username,
                            is_editing: false
                        }
                    }));
                }
            }
        }, true);
    }

    // Find item ID from element
    findItemId(element) {
        const item = element.closest('[data-id]');
        return item ? item.dataset.id : null;
    }

    // Handle item editing from other users
    handleItemEditing(data) {
        if (data.user_id === this.userId) return;
        
        const item = document.querySelector(`[data-id="${data.item_id}"]`);
        if (!item) return;
        
        if (data.is_editing) {
            // Show editing indicator
            let indicator = item.querySelector('.collab-editing-indicator');
            if (!indicator) {
                indicator = document.createElement('div');
                indicator.className = 'collab-editing-indicator';
                item.appendChild(indicator);
            }
            indicator.innerHTML = `✏️ ${data.username} redigerer...`;
            indicator.style.cssText = `
                position: absolute;
                top: -20px;
                right: 0;
                background: ${this.getUserColor(data.user_id)};
                color: white;
                padding: 2px 8px;
                border-radius: 4px;
                font-size: 12px;
                z-index: 100;
            `;
            this.activeEditors.set(data.item_id, data.user_id);
        } else {
            // Remove editing indicator
            const indicator = item.querySelector('.collab-editing-indicator');
            if (indicator) indicator.remove();
            this.activeEditors.delete(data.item_id);
        }
    }

    // Handle user joined
    handleUserJoined(data) {
        if (data.user_id === this.userId) return;
        console.log(`👋 ${data.username} joined`);
        this.showNotification(`${data.username} joined`, 'info');
        this.updateUserPresenceList();
    }

    // Handle user left
    handleUserLeft(data) {
        console.log(`👋 ${data.username} left`);
        
        // Remove cursor
        const cursor = this.otherCursors.get(data.user_id);
        if (cursor) {
            cursor.element.remove();
            this.otherCursors.delete(data.user_id);
        }
        
        this.showNotification(`${data.username} left`, 'info');
        this.updateUserPresenceList();
    }

    // Create user presence UI
    createUserPresenceUI() {
        const container = document.createElement('div');
        container.id = 'collab-presence';
        container.innerHTML = `
            <div class="collab-presence-header">
                <span>🤝 Aktive brukere</span>
                <span id="collab-status" class="collab-status">●</span>
            </div>
            <div id="collab-users" class="collab-users"></div>
        `;
        container.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: rgba(30, 41, 59, 0.95);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px;
            padding: 12px;
            z-index: 1000;
            min-width: 180px;
            font-size: 14px;
        `;
        document.body.appendChild(container);
    }

    // Update user presence list
    updateUserPresenceList() {
        const container = document.getElementById('collab-users');
        if (!container) return;
        
        let html = `
            <div class="collab-user me">
                <img src="${this.avatar}" alt="" style="width: 24px; height: 24px; border-radius: 50%;">
                <span>${this.username} (deg)</span>
            </div>
        `;
        
        this.otherCursors.forEach((cursor, userId) => {
            // This would need to store username with cursor
            html += `
                <div class="collab-user">
                    <div style="width: 24px; height: 24px; border-radius: 50%; background: ${this.getUserColor(userId)};"></div>
                    <span>Bruker</span>
                </div>
            `;
        });
        
        container.innerHTML = html;
    }

    // Update connection status
    updateConnectionStatus(status) {
        const indicator = document.getElementById('collab-status');
        if (!indicator) return;
        
        const colors = {
            connected: '#10b981',
            disconnected: '#ef4444',
            reconnecting: '#f59e0b',
            error: '#ef4444',
            failed: '#64748b'
        };
        
        indicator.style.color = colors[status] || '#64748b';
    }

    // Show notification
    showNotification(message, type = 'info') {
        // Use existing notification system if available
        if (window.showNotification) {
            window.showNotification('🤝 Collaboration', message, type, 3000);
        } else {
            console.log(`[Collaboration] ${message}`);
        }
    }
}

// Initialize when DOM is ready
let collaboration;
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        collaboration = new RealTimeCollaboration();
        collaboration.init();
    });
} else {
    collaboration = new RealTimeCollaboration();
    collaboration.init();
}

// Export for use in other modules
window.RealTimeCollaboration = RealTimeCollaboration;
window.collaboration = collaboration;
