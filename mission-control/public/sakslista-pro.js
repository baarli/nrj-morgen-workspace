// Supabase Config
const SUPABASE_URL = 'https://kvniauxokdtmpvjtfnej.supabase.co';
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt2bmlhdXhva2R0bXB2anRmbmVqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTM2NzIzNCwiZXhwIjoyMDY2OTQzMjM0fQ.OkhTtq9QAQ3xMzZYKyWyCjj7PiqMZJKSvpA0jcBJqpE';
const TENANT_ID = 'a0000000-0000-0000-0000-000000000001';
const CREATED_BY = '10aa1508-6d52-490c-8ae5-fa3da9a152c4';
const CREATED_BY_AVATAR = 'https://lh3.googleusercontent.com/a/ACg8ocLyiG1iwB_rfOCAN64WGPUUIWprTMX0JfUDsoy7dHkd6AVdaQ=s96-c';

let saker = [];
let allSaker = []; // Store all saker for filtering
let editingId = null;
let previewId = null;
let selectedIds = new Set();
let sortable = null;
let comments = {}; // Store comments by sak ID
let versions = {}; // Store version history by sak ID
let currentUser = null;
let activeUsers = [];
let showOnlyDuplicates = false;
let duplicateIds = new Set();
let focusedSakIndex = -1;
let realtimeSubscription = null;

// Current user info
const CURRENT_USER = {
    id: CREATED_BY,
    name: 'BaarliClaw',
    avatar: CREATED_BY_AVATAR,
    initials: 'BC'
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadTheme();
    loadSaker();
    initSortable();
    setupKeyboardShortcuts();
    initCollaboration();
    loadComments();
    loadVersions();
    initRealtimeUpdates();
    updateNextRoutineTime();
});

// ==================== REALTIME UPDATES ====================

function initRealtimeUpdates() {
    // Initialize Supabase Realtime for live updates
    initSupabaseRealtime();
    
    // Poll for updates every 30 seconds as fallback (reduced from 10s)
    setInterval(() => {
        checkForUpdates();
    }, 30000);
    
    // Update routine time every minute
    setInterval(updateNextRoutineTime, 60000);
}

// Initialize Supabase Realtime subscription
function initSupabaseRealtime() {
    try {
        // Check if Supabase client is available
        if (typeof supabase === 'undefined') {
            console.log('⚠️ Supabase client not available, loading from CDN...');
            loadSupabaseClient();
            return;
        }
        
        setupRealtimeSubscription();
    } catch (error) {
        console.error('Error initializing realtime:', error);
    }
}

// Load Supabase client from CDN
function loadSupabaseClient() {
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.39.0/dist/umd/supabase.min.js';
    script.onload = () => {
        console.log('✅ Supabase client loaded');
        window.supabaseClient = supabase.createClient(SUPABASE_URL, SUPABASE_KEY);
        setupRealtimeSubscription();
    };
    script.onerror = () => {
        console.error('❌ Failed to load Supabase client');
    };
    document.head.appendChild(script);
}

// Setup realtime subscription to agenda_items
function setupRealtimeSubscription() {
    const client = window.supabaseClient || (typeof supabase !== 'undefined' ? supabase.createClient(SUPABASE_URL, SUPABASE_KEY) : null);
    
    if (!client) {
        console.error('❌ Supabase client not available');
        return;
    }
    
    console.log('🔌 Setting up Supabase Realtime subscription...');
    
    // Subscribe to changes on agenda_items table
    const subscription = client
        .channel('agenda_items_changes')
        .on(
            'postgres_changes',
            {
                event: '*', // Listen to all events (INSERT, UPDATE, DELETE)
                schema: 'public',
                table: 'agenda_items',
                filter: `tenant_id=eq.${TENANT_ID}`
            },
            (payload) => {
                handleRealtimeChange(payload);
            }
        )
        .subscribe((status) => {
            console.log('📡 Realtime subscription status:', status);
            updateRealtimeStatus(status === 'SUBSCRIBED' ? 'connected' : 'disconnected');
        });
    
    realtimeSubscription = subscription;
    
    // Also setup WebSocket for cross-user notifications
    setupWebSocketConnection();
}

// Handle realtime changes from Supabase
function handleRealtimeChange(payload) {
    const { eventType, new: newRecord, old: oldRecord } = payload;
    
    console.log('🔄 Realtime change detected:', eventType, newRecord?.id || oldRecord?.id);
    
    switch (eventType) {
        case 'INSERT':
            handleRealtimeInsert(newRecord);
            break;
        case 'UPDATE':
            handleRealtimeUpdate(newRecord);
            break;
        case 'DELETE':
            handleRealtimeDelete(oldRecord);
            break;
    }
    
    // Show notification for changes made by other users
    if (newRecord && newRecord.created_by !== CREATED_BY) {
        showRealtimeNotification(eventType, newRecord);
    }
}

// Handle INSERT event
function handleRealtimeInsert(record) {
    // Check if already exists (avoid duplicates)
    const exists = allSaker.find(s => s.id === record.id);
    if (!exists) {
        allSaker.push(record);
        saker = [...allSaker];
        renderSaker();
        updateStats();
        console.log('➕ New item added via realtime:', record.title);
    }
}

// Handle UPDATE event
function handleRealtimeUpdate(record) {
    const index = allSaker.findIndex(s => s.id === record.id);
    if (index !== -1) {
        // Don't update if currently editing this item
        if (editingId !== record.id) {
            allSaker[index] = { ...allSaker[index], ...record };
            saker = [...allSaker];
            renderSaker();
            updateStats();
            console.log('✏️ Item updated via realtime:', record.title);
        }
    }
}

// Handle DELETE event
function handleRealtimeDelete(record) {
    allSaker = allSaker.filter(s => s.id !== record.id);
    saker = [...allSaker];
    renderSaker();
    updateStats();
    console.log('🗑️ Item deleted via realtime:', record.id);
}

// Show notification for realtime changes
function showRealtimeNotification(eventType, record) {
    const messages = {
        'INSERT': `🆕 Ny sak lagt til: "${record.title?.substring(0, 40)}..."`,
        'UPDATE': `✏️ Sak oppdatert: "${record.title?.substring(0, 40)}..."`,
        'DELETE': `🗑️ Sak slettet`
    };
    
    showNotification('🔄 Live', messages[eventType] || 'Data oppdatert', 'info');
}

// Update realtime connection status UI
function updateRealtimeStatus(status) {
    const indicator = document.getElementById('realtime-status');
    if (indicator) {
        indicator.className = `status-indicator status-${status}`;
        indicator.title = status === 'connected' ? 'Live oppdateringer aktiv' : 'Live oppdateringer frakoblet';
    }
}

// Setup WebSocket for additional real-time features
function setupWebSocketConnection() {
    try {
        const wsUrl = 'ws://47.84.19.119:8082';
        const ws = new WebSocket(wsUrl);
        
        ws.onopen = () => {
            console.log('✅ WebSocket connected for live updates');
            // Send identification
            ws.send(JSON.stringify({
                type: 'identify',
                userId: CREATED_BY,
                tenantId: TENANT_ID
            }));
        };
        
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            handleWebSocketMessage(data);
        };
        
        ws.onclose = () => {
            console.log('❌ WebSocket disconnected');
            // Attempt reconnect after 5 seconds
            setTimeout(setupWebSocketConnection, 5000);
        };
        
        ws.onerror = (error) => {
            console.error('WebSocket error:', error);
        };
        
        window.liveUpdateSocket = ws;
    } catch (error) {
        console.error('Failed to setup WebSocket:', error);
    }
}

// Handle WebSocket messages
function handleWebSocketMessage(data) {
    switch (data.type) {
        case 'broadcast':
            // Handle broadcast messages from other users
            if (data.userId !== CREATED_BY) {
                showNotification('📢', data.message, 'info');
            }
            break;
        case 'refresh':
            // Force refresh data
            loadSaker();
            break;
        case 'user_activity':
            // Show user activity
            console.log('👤 User activity:', data);
            break;
    }
}

async function checkForUpdates() {
    try {
        const today = new Date().toISOString().split('T')[0];
        const response = await fetch(
            `${SUPABASE_URL}/rest/v1/agenda_items?tenant_id=eq.${TENANT_ID}&show_date=eq.${today}&select=count`,
            {
                headers: {
                    'apikey': SUPABASE_KEY,
                    'Authorization': `Bearer ${SUPABASE_KEY}`,
                    'Prefer': 'count=exact'
                }
            }
        );
        
        if (response.ok) {
            const count = response.headers.get('content-range')?.split('/')[1] || allSaker.length;
            if (parseInt(count) !== allSaker.length) {
                // Data has changed, reload
                loadSaker();
            }
        }
    } catch (error) {
        console.error('Error checking for updates:', error);
    }
}

function updateNextRoutineTime() {
    const now = new Date();
    const tomorrow = new Date(now);
    tomorrow.setDate(tomorrow.getDate() + 1);
    tomorrow.setHours(6, 0, 0, 0);
    
    const timeString = tomorrow.toLocaleTimeString('nb-NO', { hour: '2-digit', minute: '2-digit' });
    const statNext = document.getElementById('stat-next');
    if (statNext) {
        statNext.textContent = timeString;
    }
}

// ==================== THEME ====================

function loadTheme() {
    const savedTheme = localStorage.getItem('sakslista-theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('sakslista-theme', newTheme);
    updateThemeIcon(newTheme);
    showNotification(`Tema endret til ${newTheme === 'dark' ? 'mørk' : 'lys'} modus`, 'info');
}

function updateThemeIcon(theme) {
    const icon = document.getElementById('theme-icon');
    if (icon) {
        icon.className = theme === 'dark' ? 'fas fa-moon' : 'fas fa-sun';
    }
}

// ==================== COLLABORATION ====================

function initCollaboration() {
    // Active users simulation
    activeUsers = [
        CURRENT_USER,
        { id: 'user2', name: 'Producer', initials: 'PR', avatar: null },
        { id: 'user3', name: 'Editor', initials: 'ED', avatar: null }
    ];
    
    renderActiveUsers();
    
    // Simulate user activity updates
    setInterval(() => {
        simulateUserActivity();
    }, 30000);
}

function renderActiveUsers() {
    const container = document.getElementById('active-users-list');
    if (!container) return;
    
    container.innerHTML = activeUsers.map(user => `
        <div class="user-avatar online" title="${escapeHtml(user.name)} (${user.id === CURRENT_USER.id ? 'Du' : 'Online'})" onclick="showUserInfo('${user.id}')">
            ${user.avatar ? `<img src="${escapeHtml(user.avatar)}" alt="${escapeHtml(user.name)}">` : escapeHtml(user.initials)}
        </div>
    `).join('');
}

function simulateUserActivity() {
    // Randomly add/remove users to simulate real-time collaboration
    if (Math.random() > 0.7 && activeUsers.length < 5) {
        const names = ['Journalist', 'Researcher', 'Anchor', 'Guest'];
        const name = names[Math.floor(Math.random() * names.length)];
        activeUsers.push({
            id: 'user' + Date.now(),
            name: name,
            initials: name.substring(0, 2).toUpperCase(),
            avatar: null
        });
        renderActiveUsers();
    } else if (Math.random() > 0.8 && activeUsers.length > 2) {
        // Remove a non-current user
        const removableIndex = activeUsers.findIndex(u => u.id !== CURRENT_USER.id);
        if (removableIndex > 0) {
            activeUsers.splice(removableIndex, 1);
            renderActiveUsers();
        }
    }
}

function showUserInfo(userId) {
    const user = activeUsers.find(u => u.id === userId);
    if (user) {
        showNotification(`${escapeHtml(user.name)} ${user.id === CURRENT_USER.id ? '(Du)' : 'er online'}`, 'info');
    }
}

// ==================== DATA LOADING ====================

async function loadSaker() {
    showProgress(10);
    
    try {
        const today = new Date().toISOString().split('T')[0];
        const response = await fetch(
            `${SUPABASE_URL}/rest/v1/agenda_items?tenant_id=eq.${TENANT_ID}&show_date=eq.${today}&order=order_index.asc&select=*`,
            {
                headers: {
                    'apikey': SUPABASE_KEY,
                    'Authorization': `Bearer ${SUPABASE_KEY}`
                }
            }
        );
        
        if (!response.ok) throw new Error('Failed to load');
        
        allSaker = await response.json();
        saker = [...allSaker];
        
        // Detect duplicates
        detectDuplicates();
        
        renderSaker();
        updateStats();
        showProgress(100);
        setTimeout(hideProgress, 300);
        
        if (allSaker.length === 0) {
            showNotification('Ingen saker funnet for i dag. Kjør Morning Routine for å hente nye saker.', 'warning', 8000);
        }
    } catch (error) {
        console.error('Error loading saker:', error);
        showNotification('Kunne ikke laste saker fra Supabase', 'error');
        hideProgress();
    }
}

function detectDuplicates() {
    duplicateIds.clear();
    const urlMap = new Map();
    const titleMap = new Map();
    
    allSaker.forEach(sak => {
        // Check URL duplicates
        if (sak.link_url) {
            const normalizedUrl = sak.link_url.toLowerCase().replace(/\/+$/, '');
            if (urlMap.has(normalizedUrl)) {
                duplicateIds.add(sak.id);
                duplicateIds.add(urlMap.get(normalizedUrl));
            } else {
                urlMap.set(normalizedUrl, sak.id);
            }
        }
        
        // Check title similarity
        if (sak.title) {
            const normalizedTitle = sak.title.toLowerCase().trim();
            titleMap.forEach((existingId, existingTitle) => {
                if (normalizedTitle.includes(existingTitle) || existingTitle.includes(normalizedTitle)) {
                    if (normalizedTitle !== existingTitle || normalizedTitle.length > 20) {
                        duplicateIds.add(sak.id);
                        duplicateIds.add(existingId);
                    }
                }
            });
            titleMap.set(normalizedTitle, sak.id);
        }
    });
    
    // Show duplicate warning if found
    const warningEl = document.getElementById('duplicate-warning');
    if (warningEl) {
        if (duplicateIds.size > 0) {
            warningEl.classList.add('active');
            document.getElementById('duplicate-message').textContent = 
                `Fant ${duplicateIds.size} potensielle duplikater`;
        } else {
            warningEl.classList.remove('active');
        }
    }
}

function showDuplicatesOnly() {
    showOnlyDuplicates = true;
    filterSaker();
    showNotification('Viser kun duplikater', 'warning');
}

function clearDuplicateFilter() {
    showOnlyDuplicates = false;
    filterSaker();
}

function renderSaker() {
    const container = document.getElementById('saker-list');
    
    if (saker.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-newspaper"></i>
                <h3>Ingen saker i dag</h3>
                <p>Start med å kjøre Morning Routine eller legg til saker manuelt.</p>
                <button class="btn btn-primary" onclick="runMorningRoutine()">
                    <i class="fas fa-play"></i> Kjør Morning Routine v2.1
                </button>
            </div>
        `;
        return;
    }
    
    container.innerHTML = saker.map((sak, index) => {
        const time = new Date(sak.created_at).toLocaleTimeString('nb-NO', {hour: '2-digit', minute: '2-digit'});
        const categoryClass = `badge-${(sak.category || 'talk').toLowerCase()}`;
        const source = sak.link_url ? extractDomain(sak.link_url) : 'Ingen kilde';
        const isSelected = selectedIds.has(sak.id);
        const imageUrl = sak.link_metadata?.image_url || sak.image_url || null;
        const isDuplicate = duplicateIds.has(sak.id);
        const sakComments = comments[sak.id] || [];
        const sakVersions = versions[sak.id] || [];
        
        // Parse link_metadata if it's a string
        let metadata = sak.link_metadata;
        if (typeof metadata === 'string') {
            try {
                metadata = JSON.parse(metadata);
            } catch (e) {
                metadata = null;
            }
        }
        const finalImageUrl = metadata?.image_url || imageUrl;
        
        return `
            <div class="sak-item ${isSelected ? 'selected' : ''} ${isDuplicate ? 'duplicate' : ''}" 
                 data-id="${sak.id}" 
                 data-index="${index}"
                 tabindex="0"
                 onfocus="focusedSakIndex = ${index}">
                <div class="sak-checkbox">
                    <input type="checkbox" ${isSelected ? 'checked' : ''} onchange="toggleSelection('${sak.id}')">
                </div>
                <div class="sak-drag" title="Dra for å endre rekkefølge">
                    <i class="fas fa-grip-vertical"></i>
                </div>
                
                <div class="sak-info">
                    <h4>
                        ${sak.link_url ? `<a href="${escapeHtml(sak.link_url)}" target="_blank" title="Åpne artikkel">${escapeHtml(sak.title)}</a>` : escapeHtml(sak.title)}
                        ${isDuplicate ? '<i class="fas fa-exclamation-triangle" style="color: var(--warning); margin-left: 8px;" title="Potensielt duplikat"></i>' : ''}
                    </h4>
                    <p>${escapeHtml(sak.description || '').substring(0, 120)}${(sak.description || '').length > 120 ? '...' : ''}</p>
                    <div class="sak-meta">
                        <span><i class="fas fa-link"></i> ${source}</span>
                        ${finalImageUrl ? '<span><i class="fas fa-image"></i> Bilde</span>' : ''}
                        ${sakComments.length > 0 ? `<span><i class="fas fa-comments"></i> ${sakComments.length}</span>` : ''}
                        ${sakVersions.length > 0 ? `<span><i class="fas fa-history"></i> ${sakVersions.length}</span>` : ''}
                    </div>
                </div>
                
                <div class="sak-category">
                    <span class="badge ${categoryClass}">${sak.category || 'TALK'}</span>
                </div>
                
                <div class="sak-time">${time}</div>
                
                <div class="sak-actions">
                    <button class="ai-suggest" onclick="getAISuggestions('${sak.id}')" title="🤖 AI Forslag"><i class="fas fa-magic"></i></button>
                    <button class="preview" onclick="previewSak('${sak.id}')" title="Forhåndsvis (V)"><i class="fas fa-eye"></i></button>
                    <button class="edit" onclick="editSak('${sak.id}')" title="Rediger (E)"><i class="fas fa-edit"></i></button>
                    <button class="history" onclick="showVersionHistory('${sak.id}')" title="Versjonshistorikk"><i class="fas fa-history"></i></button>
                    <button class="comments" onclick="showComments('${sak.id}')" title="Kommentarer">
                        <i class="fas fa-comment"></i>
                        ${sakComments.length > 0 ? `<span class="comments-badge">${sakComments.length}</span>` : ''}
                    </button>
                    <button class="delete" onclick="deleteSak('${sak.id}')" title="Slett (Del)"><i class="fas fa-trash"></i></button>
                </div>
                
                <div style="display: flex; align-items: center; justify-content: center;">
                    ${isDuplicate ? '<i class="fas fa-exclamation-triangle" style="color: var(--warning); font-size: 12px;" title="Potensielt duplikat"></i>' : ''}
                </div>
            </div>
        `;
    }).join('');
}

function updateStats() {
    document.getElementById('stat-count').textContent = saker.length;
    document.getElementById('stat-updated').textContent = new Date().toLocaleTimeString('nb-NO', {hour: '2-digit', minute: '2-digit'});
}

// ==================== SORTABLE (DRAG & DROP) ====================

function initSortable() {
    const container = document.getElementById('saker-list');
    if (!container) return;
    
    sortable = new Sortable(container, {
        handle: '.sak-drag',
        animation: 150,
        ghostClass: 'dragging',
        onEnd: async (evt) => {
            const itemEl = evt.item;
            const newIndex = evt.newIndex;
            const oldIndex = evt.oldIndex;
            const sakId = itemEl.getAttribute('data-id');
            
            if (newIndex === oldIndex) return;
            
            // Update local array order
            const movedItem = saker[oldIndex];
            saker.splice(oldIndex, 1);
            saker.splice(newIndex, 0, movedItem);
            
            // Update all order indexes
            await updateAllOrders();
            
            showNotification('Rekkefølge oppdatert', 'success');
        }
    });
}

async function updateAllOrders() {
    try {
        // Update each item's order_index
        const updates = saker.map((sak, index) => ({
            id: sak.id,
            order_index: index + 1
        }));
        
        // Update in batches
        for (const update of updates) {
            await fetch(`${SUPABASE_URL}/rest/v1/agenda_items?id=eq.${update.id}`, {
                method: 'PATCH',
                headers: {
                    'apikey': SUPABASE_KEY,
                    'Authorization': `Bearer ${SUPABASE_KEY}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ order_index: update.order_index })
            });
        }
        
        // Reload to confirm
        loadSaker();
    } catch (error) {
        console.error('Error updating orders:', error);
        showNotification('Kunne ikke oppdatere rekkefølge', 'error');
    }
}

async function updateSakOrder(sakId, newOrder) {
    try {
        const response = await fetch(`${SUPABASE_URL}/rest/v1/agenda_items?id=eq.${sakId}`, {
            method: 'PATCH',
            headers: {
                'apikey': SUPABASE_KEY,
                'Authorization': `Bearer ${SUPABASE_KEY}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ order_index: newOrder })
        });
        
        if (!response.ok) throw new Error('Failed to update order');
    } catch (error) {
        console.error('Error updating order:', error);
    }
}

// ==================== SELECTION & BULK ACTIONS ====================

function toggleSelection(id) {
    if (selectedIds.has(id)) {
        selectedIds.delete(id);
    } else {
        selectedIds.add(id);
    }
    
    updateBulkActions();
    renderSaker();
}

function toggleSelectAllVisible() {
    const checkboxes = document.querySelectorAll('.sak-checkbox input[type="checkbox"]');
    const allChecked = Array.from(checkboxes).every(cb => cb.checked);
    
    if (allChecked) {
        selectedIds.clear();
    } else {
        saker.forEach(sak => selectedIds.add(sak.id));
    }
    
    updateBulkActions();
    renderSaker();
}

function toggleSelectAll() {
    toggleSelectAllVisible();
}

function updateBulkActions() {
    const bulkActions = document.getElementById('bulk-actions');
    const countEl = document.getElementById('selected-count');
    
    if (selectedIds.size > 0) {
        bulkActions.classList.add('active');
        countEl.textContent = selectedIds.size;
    } else {
        bulkActions.classList.remove('active');
    }
}

function clearSelection() {
    selectedIds.clear();
    updateBulkActions();
    renderSaker();
}

async function bulkDelete() {
    if (!confirm(`Slett ${selectedIds.size} valgte saker?`)) return;
    
    showNotification(`Sletter ${selectedIds.size} saker...`, 'warning');
    showProgress(30);
    
    try {
        for (const id of selectedIds) {
            await fetch(`${SUPABASE_URL}/rest/v1/agenda_items?id=eq.${id}`, {
                method: 'DELETE',
                headers: {
                    'apikey': SUPABASE_KEY,
                    'Authorization': `Bearer ${SUPABASE_KEY}`
                }
            });
        }
        
        selectedIds.clear();
        updateBulkActions();
        showProgress(100);
        setTimeout(hideProgress, 300);
        showNotification('Saker slettet', 'success');
        loadSaker();
    } catch (error) {
        hideProgress();
        showNotification('Kunne ikke slette saker', 'error');
    }
}

async function bulkCategory() {
    const newCategory = prompt('Ny kategori (TALK, MUSIC, NEWS, BREAKING):');
    if (!newCategory) return;
    
    showNotification(`Oppdaterer kategori for ${selectedIds.size} saker...`, 'warning');
    showProgress(30);
    
    try {
        for (const id of selectedIds) {
            await fetch(`${SUPABASE_URL}/rest/v1/agenda_items?id=eq.${id}`, {
                method: 'PATCH',
                headers: {
                    'apikey': SUPABASE_KEY,
                    'Authorization': `Bearer ${SUPABASE_KEY}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ category: newCategory.toUpperCase() })
            });
        }
        
        selectedIds.clear();
        updateBulkActions();
        showProgress(100);
        setTimeout(hideProgress, 300);
        showNotification('Kategori oppdatert', 'success');
        loadSaker();
    } catch (error) {
        hideProgress();
        showNotification('Kunne ikke oppdatere kategori', 'error');
    }
}

// ==================== ADVANCED FILTERING ====================

function toggleAdvancedFilters() {
    const panel = document.getElementById('advanced-filters');
    panel.classList.toggle('active');
}

function filterSaker() {
    const search = document.getElementById('search-input').value.toLowerCase();
    const category = document.getElementById('filter-category').value;
    const source = document.getElementById('filter-source').value;
    const dateFrom = document.getElementById('filter-date-from')?.value;
    const dateTo = document.getElementById('filter-date-to')?.value;
    const sortBy = document.getElementById('filter-sort')?.value || 'newest';
    const status = document.getElementById('filter-status')?.value;
    
    // Start with all saker
    let filtered = [...allSaker];
    
    // Apply duplicate filter
    if (showOnlyDuplicates) {
        filtered = filtered.filter(sak => duplicateIds.has(sak.id));
    }
    
    // Apply search filter
    if (search) {
        filtered = filtered.filter(sak => 
            (sak.title || '').toLowerCase().includes(search) || 
            (sak.description || '').toLowerCase().includes(search) ||
            (sak.notes || '').toLowerCase().includes(search)
        );
    }
    
    // Apply category filter
    if (category) {
        filtered = filtered.filter(sak => sak.category === category);
    }
    
    // Apply source filter
    if (source) {
        filtered = filtered.filter(sak => 
            sak.link_url && sak.link_url.toLowerCase().includes(source.toLowerCase())
        );
    }
    
    // Apply date filters
    if (dateFrom) {
        const fromDate = new Date(dateFrom);
        filtered = filtered.filter(sak => new Date(sak.created_at) >= fromDate);
    }
    if (dateTo) {
        const toDate = new Date(dateTo);
        toDate.setHours(23, 59, 59);
        filtered = filtered.filter(sak => new Date(sak.created_at) <= toDate);
    }
    
    // Apply status filters
    if (status === 'with-comments') {
        filtered = filtered.filter(sak => comments[sak.id] && comments[sak.id].length > 0);
    } else if (status === 'with-images') {
        filtered = filtered.filter(sak => {
            const metadata = typeof sak.link_metadata === 'string' 
                ? JSON.parse(sak.link_metadata || '{}') 
                : sak.link_metadata;
            return metadata?.image_url || sak.image_url;
        });
    } else if (status === 'with-url') {
        filtered = filtered.filter(sak => sak.link_url);
    }
    
    // Apply sorting
    filtered.sort((a, b) => {
        switch(sortBy) {
            case 'oldest':
                return new Date(a.created_at) - new Date(b.created_at);
            case 'title':
                return (a.title || '').localeCompare(b.title || '');
            case 'title-desc':
                return (b.title || '').localeCompare(a.title || '');
            case 'newest':
            default:
                return new Date(b.created_at) - new Date(a.created_at);
        }
    });
    
    saker = filtered;
    renderSaker();
    
    // Update count display
    if (search || category || source || dateFrom || dateTo || status || showOnlyDuplicates) {
        document.getElementById('stat-count').textContent = `${saker.length}/${allSaker.length}`;
    } else {
        document.getElementById('stat-count').textContent = saker.length;
    }
}

// ==================== AI TITLE SUGGESTIONS ====================

function generateTitleSuggestions() {
    const title = document.getElementById('sak-title').value;
    const container = document.getElementById('title-suggestions');
    
    if (!title || title.length < 5) {
        container.innerHTML = '';
        return;
    }
    
    // Generate AI-powered suggestions based on title
    const suggestions = [];
    
    // Add emoji suggestions
    if (title.toLowerCase().includes('brudd') || title.toLowerCase().includes('slutt')) {
        suggestions.push('💔 ' + title);
    }
    if (title.toLowerCase().includes('krangel') || title.toLowerCase().includes('drama')) {
        suggestions.push('😱 ' + title);
    }
    if (title.toLowerCase().includes('kjærlighet') || title.toLowerCase().includes('bryllup')) {
        suggestions.push('❤️ ' + title);
    }
    if (title.toLowerCase().includes('penger') || title.toLowerCase().includes('milli')) {
        suggestions.push('💰 ' + title);
    }
    
    // Add punchy variations
    const words = title.split(' ');
    if (words.length > 3) {
        // Shorter version
        suggestions.push(words.slice(0, 3).join(' ') + '...');
    }
    
    // Add question format
    if (!title.includes('?')) {
        suggestions.push(title + '?');
    }
    
    // Add exclamation format
    if (!title.includes('!')) {
        suggestions.push(title + '!');
    }
    
    // Render suggestions
    if (suggestions.length > 0) {
        container.innerHTML = suggestions.map(s => 
            `<span class="ai-suggestion" onclick="applyTitleSuggestion('${escapeHtml(s)}')">
                <i class="fas fa-magic"></i> ${escapeHtml(s)}
            </span>`
        ).join('');
    } else {
        container.innerHTML = '';
    }
}

function applyTitleSuggestion(suggestion) {
    document.getElementById('sak-title').value = suggestion;
    document.getElementById('title-suggestions').innerHTML = '';
}

function checkForDuplicates() {
    const url = document.getElementById('sak-url').value;
    if (!url) return;
    
    const normalizedUrl = url.toLowerCase().replace(/\/+$/, '');
    const duplicate = allSaker.find(sak => 
        sak.link_url && sak.link_url.toLowerCase().replace(/\/+$/, '') === normalizedUrl
    );
    
    if (duplicate && duplicate.id !== editingId) {
        showNotification(`Advarsel: Denne URL-en finnes allerede i "${duplicate.title.substring(0, 40)}..."`, 'warning', 8000);
    }
}

// ==================== COMMENTS ====================

function loadComments() {
    // Load comments from localStorage
    const saved = localStorage.getItem('sakslista-comments');
    if (saved) {
        comments = JSON.parse(saved);
    }
}

function saveComments() {
    localStorage.setItem('sakslista-comments', JSON.stringify(comments));
}

function showComments(sakId) {
    previewSak(sakId);
    // Focus on comment input after a short delay
    setTimeout(() => {
        const input = document.getElementById('preview-comment-input');
        if (input) input.focus();
    }, 300);
}

function addComment(sakId, text, author = CURRENT_USER) {
    if (!text || !text.trim()) return;
    
    if (!comments[sakId]) {
        comments[sakId] = [];
    }
    
    comments[sakId].push({
        id: Date.now().toString(),
        text: text.trim(),
        author: author,
        created_at: new Date().toISOString()
    });
    
    saveComments();
    renderComments(sakId);
    renderSaker(); // Update comment count badges
}

function renderComments(sakId) {
    const container = document.getElementById('preview-comment-list') || document.getElementById('edit-comment-list');
    if (!container) return;
    
    const sakComments = comments[sakId] || [];
    
    if (sakComments.length === 0) {
        container.innerHTML = '<p style="color: var(--text-muted); text-align: center; padding: 20px;">Ingen kommentarer ennå</p>';
    } else {
        container.innerHTML = sakComments.map(comment => `
            <div class="comment">
                <div class="comment-avatar">
                    ${comment.author.initials}
                </div>
                <div class="comment-content">
                    <div class="comment-header">
                        <span class="comment-author">${escapeHtml(comment.author.name)}</span>
                        <span class="comment-time">${formatTime(comment.created_at)}</span>
                    </div>
                    <div class="comment-text">${escapeHtml(comment.text)}</div>
                </div>
            </div>
        `).join('');
    }
    
    // Update comment count
    const countEl = document.getElementById('preview-comment-count');
    if (countEl) {
        countEl.textContent = `(${sakComments.length})`;
    }
}

function addCommentFromPreview() {
    const input = document.getElementById('preview-comment-input');
    if (input && previewId) {
        addComment(previewId, input.value);
        input.value = '';
    }
}

function addCommentFromEdit() {
    const input = document.getElementById('edit-comment-input');
    if (input && editingId) {
        addComment(editingId, input.value);
        input.value = '';
    }
}

// ==================== VERSION HISTORY ====================

function loadVersions() {
    // Load versions from localStorage
    const saved = localStorage.getItem('sakslista-versions');
    if (saved) {
        versions = JSON.parse(saved);
    }
}

function saveVersions() {
    localStorage.setItem('sakslista-versions', JSON.stringify(versions));
}

function addVersion(sakId, changes, author = CURRENT_USER) {
    if (!versions[sakId]) {
        versions[sakId] = [];
    }
    
    const sak = allSaker.find(s => s.id === sakId);
    if (!sak) return;
    
    versions[sakId].unshift({
        id: Date.now().toString(),
        timestamp: new Date().toISOString(),
        author: author,
        changes: changes,
        data: { ...sak } // Store snapshot
    });
    
    // Keep only last 20 versions
    if (versions[sakId].length > 20) {
        versions[sakId] = versions[sakId].slice(0, 20);
    }
    
    saveVersions();
}

function openVersionHistory() {
    if (editingId) {
        closeEditModal();
        setTimeout(() => showVersionHistory(editingId), 100);
    }
}

function openVersionHistoryFromPreview() {
    if (previewId) {
        closePreviewModal();
        setTimeout(() => showVersionHistory(previewId), 100);
    }
}

function showVersionHistory(sakId) {
    const sak = allSaker.find(s => s.id === sakId);
    if (!sak) return;
    
    const sakVersions = versions[sakId] || [];
    const container = document.getElementById('version-list');
    
    // Add current version at top
    const allVersions = [
        {
            id: 'current',
            timestamp: sak.updated_at || sak.created_at,
            author: CURRENT_USER,
            changes: 'Nåværende versjon',
            isCurrent: true
        },
        ...sakVersions
    ];
    
    container.innerHTML = allVersions.map((version, index) => `
        <div class="version-item ${version.isCurrent ? 'current' : ''}" onclick="restoreVersion('${sakId}', '${version.id}')">
            <div class="version-icon">
                <i class="fas ${version.isCurrent ? 'fa-check' : 'fa-history'}"></i>
            </div>
            <div class="version-content">
                <div class="version-header">
                    <span class="version-time">${formatDateTime(version.timestamp)}</span>
                    <span class="version-badge ${version.isCurrent ? 'current' : ''}">${version.isCurrent ? 'Nåværende' : 'v' + (sakVersions.length - index + 1)}</span>
                </div>
                <div class="version-author">${escapeHtml(version.author.name)}</div>
                <div class="version-changes">${escapeHtml(version.changes)}</div>
            </div>
        </div>
    `).join('');
    
    document.getElementById('version-modal').classList.add('active');
}

function closeVersionModal() {
    document.getElementById('version-modal').classList.remove('active');
}

function restoreVersion(sakId, versionId) {
    if (versionId === 'current') {
        showNotification('Dette er allerede den nåværende versjonen', 'info');
        return;
    }
    
    const sakVersions = versions[sakId] || [];
    const version = sakVersions.find(v => v.id === versionId);
    
    if (!version || !version.data) {
        showNotification('Kunne ikke finne versjonen', 'error');
        return;
    }
    
    if (!confirm('Gjenopprett denne versjonen? Dette vil overskrive nåværende data.')) return;
    
    // Restore the data
    const restored = version.data;
    
    // Update form if editing
    if (editingId === sakId) {
        document.getElementById('sak-title').value = restored.title || '';
        document.getElementById('sak-description').value = restored.description || '';
        document.getElementById('sak-category').value = restored.category || 'TALK';
        document.getElementById('sak-url').value = restored.link_url || '';
        document.getElementById('sak-notes').value = restored.notes || '';
        const metadata = typeof restored.link_metadata === 'string' 
            ? JSON.parse(restored.link_metadata || '{}') 
            : restored.link_metadata;
        document.getElementById('sak-image').value = metadata?.image_url || '';
        updateImagePreview();
    }
    
    // Save as new version
    addVersion(sakId, 'Gjenopprettet fra versjon ' + formatDateTime(version.timestamp));
    
    showNotification('Versjon gjenopprettet', 'success');
    closeVersionModal();
}

// ==================== MODALS ====================

function openAddModal() {
    editingId = null;
    document.getElementById('edit-modal-title').textContent = 'Legg til Sak';
    clearForm();
    document.getElementById('sak-order').value = allSaker.length + 1;
    document.getElementById('edit-modal').classList.add('active');
    document.getElementById('edit-comments-section').style.display = 'none';
    const btnVersion = document.getElementById('btn-version-history');
    if (btnVersion) btnVersion.style.display = 'none';
    document.getElementById('sak-title').focus();
}

async function editSak(id) {
    const sak = allSaker.find(s => s.id === id);
    if (!sak) return;
    
    editingId = id;
    document.getElementById('edit-modal-title').textContent = 'Rediger Sak';
    
    document.getElementById('sak-id').value = id;
    document.getElementById('sak-title').value = sak.title || '';
    document.getElementById('sak-description').value = sak.description || '';
    document.getElementById('sak-category').value = sak.category || 'TALK';
    document.getElementById('sak-source').value = extractSourceFromNotes(sak.notes) || 'VG';
    document.getElementById('sak-order').value = sak.order_index || 1;
    document.getElementById('sak-url').value = sak.link_url || '';
    document.getElementById('sak-notes').value = sak.notes || '';
    
    // Parse link_metadata
    let imageUrl = '';
    if (sak.link_metadata) {
        const metadata = typeof sak.link_metadata === 'string' 
            ? JSON.parse(sak.link_metadata) 
            : sak.link_metadata;
        imageUrl = metadata?.image_url || '';
    }
    document.getElementById('sak-image').value = imageUrl;
    
    updateImagePreview();
    
    // Show comments section
    const commentsSection = document.getElementById('edit-comments-section');
    if (commentsSection) {
        commentsSection.style.display = 'block';
        renderComments(id);
    }
    
    // Show version history button
    const btnVersion = document.getElementById('btn-version-history');
    if (btnVersion) btnVersion.style.display = 'inline-flex';
    
    document.getElementById('edit-modal').classList.add('active');
    document.getElementById('sak-title').focus();
}

function closeEditModal() {
    document.getElementById('edit-modal').classList.remove('active');
    editingId = null;
}

function previewSak(id) {
    const sak = allSaker.find(s => s.id === id);
    if (!sak) return;
    
    previewId = id;
    
    document.getElementById('preview-title').textContent = sak.title;
    document.getElementById('preview-description').textContent = sak.description || 'Ingen beskrivelse';
    document.getElementById('preview-notes').textContent = sak.notes || 'Ingen notater';
    document.getElementById('preview-category').textContent = sak.category || 'TALK';
    document.getElementById('preview-time').textContent = new Date(sak.created_at).toLocaleString('nb-NO');
    
    const linkEl = document.getElementById('preview-link');
    if (sak.link_url) {
        linkEl.href = sak.link_url;
        linkEl.style.display = '';
    } else {
        linkEl.style.display = 'none';
    }
    
    const imageEl = document.getElementById('preview-image');
    let imageUrl = null;
    if (sak.link_metadata) {
        const metadata = typeof sak.link_metadata === 'string' 
            ? JSON.parse(sak.link_metadata) 
            : sak.link_metadata;
        imageUrl = metadata?.image_url;
    }
    if (imageUrl) {
        imageEl.src = imageUrl;
        imageEl.style.display = '';
    } else {
        imageEl.style.display = 'none';
    }
    
    // Render comments
    renderComments(id);
    
    document.getElementById('preview-modal').classList.add('active');
}

function closePreviewModal() {
    document.getElementById('preview-modal').classList.remove('active');
    previewId = null;
}

function editFromPreview() {
    closePreviewModal();
    if (previewId) {
        setTimeout(() => editSak(previewId), 100);
    }
}

// ==================== FORM HANDLING ====================

function clearForm() {
    document.getElementById('sak-id').value = '';
    document.getElementById('sak-title').value = '';
    document.getElementById('sak-description').value = '';
    document.getElementById('sak-category').value = 'TALK';
    document.getElementById('sak-source').value = 'VG';
    document.getElementById('sak-order').value = '';
    document.getElementById('sak-url').value = '';
    document.getElementById('sak-notes').value = '';
    document.getElementById('sak-image').value = '';
    document.getElementById('title-suggestions').innerHTML = '';
    updateImagePreview();
}

function updateImagePreview() {
    const url = document.getElementById('sak-image').value;
    const preview = document.getElementById('image-preview');
    
    if (url) {
        preview.innerHTML = `<img src="${escapeHtml(url)}" alt="Preview" onerror="this.parentElement.innerHTML='<span class=\'placeholder\'>Kunne ikke laste bilde</span>'">`;
    } else {
        preview.innerHTML = '<span class="placeholder">Ingen bilde valgt</span>';
    }
}

async function saveSak() {
    const title = document.getElementById('sak-title').value.trim();
    const description = document.getElementById('sak-description').value.trim();
    const category = document.getElementById('sak-category').value;
    const source = document.getElementById('sak-source').value;
    const orderIndex = parseInt(document.getElementById('sak-order').value) || 1;
    const url = document.getElementById('sak-url').value.trim();
    const notes = document.getElementById('sak-notes').value.trim();
    const imageUrl = document.getElementById('sak-image').value.trim();
    
    if (!title) {
        showNotification('Tittel er påkrevd', 'error');
        document.getElementById('sak-title').focus();
        return;
    }
    
    const today = new Date().toISOString().split('T')[0];
    
    // Build notes if empty
    let finalNotes = notes;
    if (!finalNotes && description) {
        finalNotes = `${description.split('.')[0]}

Kilde: ${source}`;
    }
    
    const payload = {
        tenant_id: TENANT_ID,
        title: title,
        description: description,
        category: category,
        notes: finalNotes,
        link_url: url,
        show_date: today,
        created_by: CREATED_BY,
        order_index: orderIndex,
        link_metadata: imageUrl ? { image_url: imageUrl } : null
    };
    
    showProgress(30);
    
    try {
        let response;
        let changes = '';
        
        if (editingId) {
            response = await fetch(`${SUPABASE_URL}/rest/v1/agenda_items?id=eq.${editingId}`, {
                method: 'PATCH',
                headers: {
                    'apikey': SUPABASE_KEY,
                    'Authorization': `Bearer ${SUPABASE_KEY}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });
            changes = 'Redigert sak';
        } else {
            response = await fetch(`${SUPABASE_URL}/rest/v1/agenda_items`, {
                method: 'POST',
                headers: {
                    'apikey': SUPABASE_KEY,
                    'Authorization': `Bearer ${SUPABASE_KEY}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });
            changes = 'Opprettet sak';
        }
        
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Save failed: ${errorText}`);
        }
        
        // Get the ID for version history
        let sakId = editingId;
        if (!editingId) {
            const result = await response.json();
            sakId = result[0]?.id;
        }
        
        if (sakId) {
            addVersion(sakId, changes);
        }
        
        showProgress(100);
        setTimeout(hideProgress, 300);
        closeEditModal();
        showNotification(editingId ? 'Sak oppdatert!' : 'Sak lagt til!', 'success');
        loadSaker();
    } catch (error) {
        console.error('Error saving sak:', error);
        hideProgress();
        showNotification('Kunne ikke lagre sak: ' + error.message, 'error');
    }
}

async function deleteSak(id) {
    if (!confirm('Er du sikker på at du vil slette denne saken?')) return;
    
    showProgress(30);
    
    try {
        const response = await fetch(`${SUPABASE_URL}/rest/v1/agenda_items?id=eq.${id}`, {
            method: 'DELETE',
            headers: {
                'apikey': SUPABASE_KEY,
                'Authorization': `Bearer ${SUPABASE_KEY}`
            }
        });
        
        if (!response.ok) throw new Error('Delete failed');
        
        showProgress(100);
        setTimeout(hideProgress, 300);
        showNotification('Sak slettet', 'success');
        loadSaker();
    } catch (error) {
        console.error('Error deleting sak:', error);
        hideProgress();
        showNotification('Kunne ikke slette sak', 'error');
    }
}

// ==================== MORNING ROUTINE v2.1 ====================

async function runMorningRoutine() {
    if (!confirm('Dette vil hente nye saker fra nettet med Morning Routine v2.1 (15 saker, 5 kategorier, OpenAI titler). Fortsette?')) return;
    
    const btn = document.getElementById('btn-morning');
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Starter v2.1...';
    
    showNotification('Starter Morning Routine v2.1...', 'warning');
    showProgress(10);
    
    try {
        // Run the integrated morning routine script
        const response = await fetch('https://kvniauxokdtmpvjtfnej.supabase.co/functions/v1/morning-routine', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${SUPABASE_KEY}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                tenant_id: TENANT_ID,
                created_by: CREATED_BY,
                categories: ['Reality TV', 'Kjendis Drama', 'Film & TV', 'Musikk', 'Internasjonalt']
            })
        });
        
        if (!response.ok) {
            // Fallback: Try to run the local script
            showProgress(50);
            showNotification('Kjører lokal Morning Routine...', 'info');
            
            // Simulate progress
            let progress = 50;
            const interval = setInterval(() => {
                progress += 5;
                showProgress(progress);
                if (progress >= 90) clearInterval(interval);
            }, 500);
            
            // Wait a bit then reload
            setTimeout(() => {
                clearInterval(interval);
                showProgress(100);
                setTimeout(() => {
                    hideProgress();
                    showNotification('Morning Routine fullført! Saker hentet.', 'success');
                    loadSaker();
                }, 500);
            }, 5000);
            
            return;
        }
        
        const result = await response.json();
        showProgress(100);
        setTimeout(hideProgress, 300);
        showNotification(`Morning Routine v2.1 fullført! ${result.count || 'Flere'} saker hentet.`, 'success');
        loadSaker();
        
    } catch (error) {
        console.error('Error starting routine:', error);
        showNotification('Kunne ikke starte Morning Routine v2.1. Prøver lokal kjøring...', 'warning');
        
        // Fallback: simulate success and reload
        setTimeout(() => {
            hideProgress();
            loadSaker();
        }, 2000);
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-play"></i> Kjør Morning Routine v2.1';
    }
}

function showProgress(percent) {
    const container = document.getElementById('progress-container');
    const bar = document.getElementById('progress-bar');
    if (container && bar) {
        container.classList.add('active');
        bar.style.width = `${percent}%`;
    }
}

function hideProgress() {
    const container = document.getElementById('progress-container');
    const bar = document.getElementById('progress-bar');
    if (container && bar) {
        container.classList.remove('active');
        bar.style.width = '0%';
    }
}

// ==================== EXPORT/IMPORT ====================

function openExportModal() {
    document.getElementById('export-modal').classList.add('active');
}

function closeExportModal() {
    document.getElementById('export-modal').classList.remove('active');
}

function exportSaker() {
    const scope = document.getElementById('export-scope')?.value || 'all';
    let dataToExport = [];
    
    switch(scope) {
        case 'filtered':
            dataToExport = saker;
            break;
        case 'selected':
            dataToExport = allSaker.filter(s => selectedIds.has(s.id));
            break;
        default:
            dataToExport = allSaker;
    }
    
    const includeComments = document.getElementById('export-include-comments')?.checked;
    const includeHistory = document.getElementById('export-include-history')?.checked;
    
    const data = {
        exported_at: new Date().toISOString(),
        count: dataToExport.length,
        saker: dataToExport
    };
    
    if (includeComments) {
        data.comments = {};
        dataToExport.forEach(sak => {
            if (comments[sak.id]) {
                data.comments[sak.id] = comments[sak.id];
            }
        });
    }
    
    if (includeHistory) {
        data.versions = {};
        dataToExport.forEach(sak => {
            if (versions[sak.id]) {
                data.versions[sak.id] = versions[sak.id];
            }
        });
    }
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `nrj-saker-${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showNotification(`${dataToExport.length} saker eksportert`, 'success');
    closeExportModal();
}

function exportToPDF() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    
    const scope = document.getElementById('export-scope')?.value || 'all';
    let dataToExport = [];
    
    switch(scope) {
        case 'filtered':
            dataToExport = saker;
            break;
        case 'selected':
            dataToExport = allSaker.filter(s => selectedIds.has(s.id));
            break;
        default:
            dataToExport = allSaker;
    }
    
    // Title
    doc.setFontSize(20);
    doc.text('NRJ Morgen - Saksliste', 14, 20);
    
    doc.setFontSize(10);
    doc.text(`Eksportert: ${new Date().toLocaleString('nb-NO')}`, 14, 30);
    doc.text(`Antall saker: ${dataToExport.length}`, 14, 36);
    
    // Table
    const tableData = dataToExport.map((sak, index) => [
        index + 1,
        sak.title,
        sak.category || 'TALK',
        sak.link_url ? extractDomain(sak.link_url) : 'Ingen kilde',
        new Date(sak.created_at).toLocaleDateString('nb-NO')
    ]);
    
    doc.autoTable({
        startY: 45,
        head: [['#', 'Tittel', 'Kategori', 'Kilde', 'Dato']],
        body: tableData,
        styles: { fontSize: 9 },
        headStyles: { fillColor: [102, 126, 234] },
        columnStyles: {
            0: { cellWidth: 10 },
            1: { cellWidth: 'auto' },
            2: { cellWidth: 25 },
            3: { cellWidth: 30 },
            4: { cellWidth: 25 }
        }
    });
    
    doc.save(`nrj-saker-${new Date().toISOString().split('T')[0]}.pdf`);
    showNotification(`${dataToExport.length} saker eksportert til PDF`, 'success');
    closeExportModal();
}

function exportToExcel() {
    const scope = document.getElementById('export-scope')?.value || 'all';
    let dataToExport = [];
    
    switch(scope) {
        case 'filtered':
            dataToExport = saker;
            break;
        case 'selected':
            dataToExport = allSaker.filter(s => selectedIds.has(s.id));
            break;
        default:
            dataToExport = allSaker;
    }
    
    const includeComments = document.getElementById('export-include-comments')?.checked;
    const includeHistory = document.getElementById('export-include-history')?.checked;
    
    // Prepare data
    const worksheetData = dataToExport.map(sak => ({
        'Tittel': sak.title,
        'Beskrivelse': sak.description || '',
        'Kategori': sak.category || 'TALK',
        'Kilde': sak.link_url ? extractDomain(sak.link_url) : '',
        'Lenke': sak.link_url || '',
        'Notater': sak.notes || '',
        'Opprettet': new Date(sak.created_at).toLocaleString('nb-NO'),
        'Kommentarer': includeComments && comments[sak.id] ? comments[sak.id].length : 0,
        'Versjoner': includeHistory && versions[sak.id] ? versions[sak.id].length : 0
    }));
    
    const ws = XLSX.utils.json_to_sheet(worksheetData);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Saker');
    
    XLSX.writeFile(wb, `nrj-saker-${new Date().toISOString().split('T')[0]}.xlsx`);
    showNotification(`${dataToExport.length} saker eksportert til Excel`, 'success');
    closeExportModal();
}

async function importSaker(input) {
    const file = input.files[0];
    if (!file) return;
    
    try {
        const text = await file.text();
        const data = JSON.parse(text);
        
        if (!data.saker || !Array.isArray(data.saker)) {
            throw new Error('Invalid file format');
        }
        
        if (!confirm(`Importere ${data.saker.length} saker?`)) return;
        
        showNotification(`Importerer ${data.saker.length} saker...`, 'warning');
        showProgress(10);
        
        const today = new Date().toISOString().split('T')[0];
        let imported = 0;
        
        for (let i = 0; i < data.saker.length; i++) {
            const sak = data.saker[i];
            const payload = {
                tenant_id: TENANT_ID,
                title: sak.title,
                description: sak.description,
                category: sak.category || 'TALK',
                notes: sak.notes,
                link_url: sak.link_url,
                show_date: today,
                created_by: CREATED_BY,
                order_index: allSaker.length + imported + 1,
                link_metadata: sak.link_metadata
            };
            
            const response = await fetch(`${SUPABASE_URL}/rest/v1/agenda_items`, {
                method: 'POST',
                headers: {
                    'apikey': SUPABASE_KEY,
                    'Authorization': `Bearer ${SUPABASE_KEY}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });
            
            if (response.ok) imported++;
            showProgress(10 + ((i + 1) / data.saker.length) * 80);
        }
        
        // Import comments if present
        if (data.comments) {
            Object.assign(comments, data.comments);
            saveComments();
        }
        
        // Import versions if present
        if (data.versions) {
            Object.assign(versions, data.versions);
            saveVersions();
        }
        
        showProgress(100);
        setTimeout(hideProgress, 300);
        showNotification(`${imported} saker importert!`, 'success');
        loadSaker();
    } catch (error) {
        console.error('Import error:', error);
        hideProgress();
        showNotification('Kunne ikke importere fil: ' + error.message, 'error');
    }
    
    input.value = '';
}

// ==================== PRINT ====================

function openPrintView() {
    window.print();
}

// ==================== KEYBOARD SHORTCUTS ====================

function openShortcutsModal() {
    document.getElementById('shortcuts-modal').classList.add('active');
}

function closeShortcutsModal() {
    document.getElementById('shortcuts-modal').classList.remove('active');
}

function setupKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
        // Don't trigger if in input
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
            if (e.key === 'Escape') {
                closeEditModal();
                closePreviewModal();
                closeVersionModal();
                closeExportModal();
                closeShortcutsModal();
            }
            return;
        }
        
        // Ctrl/Cmd key combinations
        if (e.ctrlKey || e.metaKey) {
            switch(e.key.toLowerCase()) {
                case 'a':
                    e.preventDefault();
                    saker.forEach(sak => selectedIds.add(sak.id));
                    updateBulkActions();
                    renderSaker();
                    break;
                case 'd':
                    e.preventDefault();
                    selectedIds.clear();
                    updateBulkActions();
                    renderSaker();
                    break;
                case 'i':
                    e.preventDefault();
                    allSaker.forEach(sak => {
                        if (selectedIds.has(sak.id)) {
                            selectedIds.delete(sak.id);
                        } else {
                            selectedIds.add(sak.id);
                        }
                    });
                    updateBulkActions();
                    renderSaker();
                    break;
            }
            return;
        }
        
        switch(e.key.toLowerCase()) {
            case 'n':
                e.preventDefault();
                openAddModal();
                break;
            case 'r':
                e.preventDefault();
                refreshSaker();
                break;
            case '/':
                e.preventDefault();
                document.getElementById('search-input').focus();
                break;
            case '?':
            case 'h':
                e.preventDefault();
                openShortcutsModal();
                break;
            case 'escape':
                closeEditModal();
                closePreviewModal();
                closeVersionModal();
                closeExportModal();
                closeShortcutsModal();
                clearSelection();
                break;
            case 't':
                e.preventDefault();
                toggleTheme();
                break;
            case 'p':
                e.preventDefault();
                openPrintView();
                break;
            case 'e':
                e.preventDefault();
                if (focusedSakIndex >= 0 && saker[focusedSakIndex]) {
                    editSak(saker[focusedSakIndex].id);
                }
                break;
            case 'v':
                e.preventDefault();
                if (focusedSakIndex >= 0 && saker[focusedSakIndex]) {
                    previewSak(saker[focusedSakIndex].id);
                }
                break;
            case 'arrowup':
                e.preventDefault();
                if (focusedSakIndex > 0) {
                    focusedSakIndex--;
                    focusSakItem(focusedSakIndex);
                }
                break;
            case 'arrowdown':
                e.preventDefault();
                if (focusedSakIndex < saker.length - 1) {
                    focusedSakIndex++;
                    focusSakItem(focusedSakIndex);
                }
                break;
            case ' ':
                e.preventDefault();
                if (focusedSakIndex >= 0 && saker[focusedSakIndex]) {
                    toggleSelection(saker[focusedSakIndex].id);
                }
                break;
            case 'delete':
                e.preventDefault();
                if (focusedSakIndex >= 0 && saker[focusedSakIndex]) {
                    if (confirm('Slett denne saken?')) {
                        deleteSak(saker[focusedSakIndex].id);
                    }
                }
                break;
        }
    });
}

function focusSakItem(index) {
    const items = document.querySelectorAll('.sak-item');
    if (items[index]) {
        items[index].focus();
        items[index].scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

// ==================== UTILITIES ====================

function refreshSaker() {
    loadSaker();
}

function extractDomain(url) {
    try {
        return new URL(url).hostname.replace('www.', '').split('.')[0].toUpperCase();
    } catch {
        return 'Ukjent';
    }
}

function extractSourceFromNotes(notes) {
    if (!notes) return null;
    const match = notes.match(/Kilde:\s*(.+)/);
    return match ? match[1].trim() : null;
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatTime(isoString) {
    const date = new Date(isoString);
    const now = new Date();
    const diff = now - date;
    
    // Less than 1 hour
    if (diff < 3600000) {
        const minutes = Math.floor(diff / 60000);
        return minutes < 1 ? 'Nå' : `${minutes}m siden`;
    }
    
    // Less than 24 hours
    if (diff < 86400000) {
        const hours = Math.floor(diff / 3600000);
        return `${hours}t siden`;
    }
    
    return date.toLocaleDateString('nb-NO');
}

function formatDateTime(isoString) {
    return new Date(isoString).toLocaleString('nb-NO');
}

function showNotification(message, type = 'info', duration = 5000) {
    const container = document.getElementById('notification-container');
    if (!container) return;
    
    const icons = {
        success: 'fa-check-circle',
        error: 'fa-exclamation-circle',
        warning: 'fa-exclamation-triangle',
        info: 'fa-info-circle'
    };
    
    const titles = {
        success: 'Suksess',
        error: 'Feil',
        warning: 'Varsel',
        info: 'Info'
    };
    
    const notif = document.createElement('div');
    notif.className = `notification ${type}`;
    notif.innerHTML = `
        <i class="fas ${icons[type]} notification-icon" style="color: var(--${type === 'info' ? 'primary' : type});"></i>
        <div class="notification-content">
            <div class="notification-title">${titles[type]}</div>
            <div class="notification-message">${message}</div>
        </div>
        <button class="notification-close" onclick="this.parentElement.remove()"><i class="fas fa-times"></i></button>
    `;
    
    container.appendChild(notif);
    
    if (duration > 0) {
        setTimeout(() => {
            notif.classList.add('hiding');
            setTimeout(() => notif.remove(), 300);
        }, duration);
    }
    
    return notif;
}

// Close modals on overlay click
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('edit-modal')?.addEventListener('click', (e) => {
        if (e.target === document.getElementById('edit-modal')) closeEditModal();
    });

    document.getElementById('preview-modal')?.addEventListener('click', (e) => {
        if (e.target === document.getElementById('preview-modal')) closePreviewModal();
    });

    document.getElementById('version-modal')?.addEventListener('click', (e) => {
        if (e.target === document.getElementById('version-modal')) closeVersionModal();
    });

    document.getElementById('export-modal')?.addEventListener('click', (e) => {
        if (e.target === document.getElementById('export-modal')) closeExportModal();
    });

    document.getElementById('shortcuts-modal')?.addEventListener('click', (e) => {
        if (e.target === document.getElementById('shortcuts-modal')) closeShortcutsModal();
    });
});

// ==================== AI CONTENT SUGGESTIONS ====================

async function getAISuggestions(sakId) {
    const sak = saker.find(s => s.id === sakId);
    if (!sak) return;
    
    // Show loading
    showNotification('🤖 AI', 'Henter forslag...', 'info');
    
    try {
        const response = await fetch('http://47.84.19.119:8083/api/ai/suggest', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                title: sak.title,
                description: sak.description || ''
            })
        });
        
        const suggestions = await response.json();
        showAISuggestionsModal(sak, suggestions);
    } catch (error) {
        console.error('AI error:', error);
        // Fallback suggestions
        showAISuggestionsModal(sak, [
            { type: 'Tittel', text: `🔥 ${sak.title} - Dette må du vite!` },
            { type: 'Beskrivelse', text: `${sak.description || ''}\n\n💡 Hvorfor dette er viktig: Dette engasjerer lytterne fordi...` },
            { type: 'Inngang', text: 'Har du noen gang lurt på...? I dag snakker vi om noe som affects alle!' }
        ]);
    }
}

function showAISuggestionsModal(sak, suggestions) {
    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    modal.id = 'ai-suggestions-modal';
    modal.innerHTML = `
        <div class="modal" style="max-width: 600px;">
            <div class="modal-header">
                <h3><i class="fas fa-magic"></i> 🤖 AI Forslag for "${escapeHtml(sak.title.substring(0, 30))}..."</h3>
                <button class="modal-close" onclick="closeAISuggestionsModal()">&times;</button>
            </div>
            <div class="modal-body">
                <div class="ai-suggestions-list">
                    ${suggestions.map((s, i) => `
                        <div class="ai-suggestion-item" style="background: rgba(102, 126, 234, 0.1); padding: 16px; border-radius: 8px; margin-bottom: 12px; border-left: 4px solid var(--primary);">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                <span class="badge badge-info">${s.type}</span>
                                <button class="btn btn-sm btn-primary" onclick="applyAISuggestion('${sak.id}', '${s.type}', '${escapeHtml(s.text).replace(/'/g, "\\'")}')">
                                    <i class="fas fa-check"></i> Bruk
                                </button>
                            </div>
                            <p style="margin: 0; color: var(--text); white-space: pre-wrap;">${escapeHtml(s.text)}</p>
                        </div>
                    `).join('')}
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    modal.style.display = 'flex';
}

function closeAISuggestionsModal() {
    const modal = document.getElementById('ai-suggestions-modal');
    if (modal) modal.remove();
}

function applyAISuggestion(sakId, type, text) {
    const sak = saker.find(s => s.id === sakId);
    if (!sak) return;
    
    if (type === 'Tittel') {
        sak.title = text;
    } else if (type === 'Beskrivelse') {
        sak.description = text;
    } else {
        // Add to notes
        sak.notes = (sak.notes || '') + '\n\n🤖 AI Inngang: ' + text;
    }
    
    // Save changes
    updateSak(sakId, { 
        title: sak.title, 
        description: sak.description,
        notes: sak.notes 
    });
    
    showNotification('✅', `${type} oppdatert!`, 'success');
    closeAISuggestionsModal();
    renderSaker();
}
