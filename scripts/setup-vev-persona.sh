#!/bin/bash
# Setup script for Vev Persona Enforcer

cat >> ~/.bashrc << 'EOF'

# ============================================
# VEV PERSONA ENFORCER - Auto-loaded
# ============================================

# Enforce Vev persona (identity, personality, SOUL.md)
vev-persona() {
    cd /root/.openclaw/workspace/scripts && python3 vev-persona-enforcer.py 2>/dev/null
}
export -f vev-persona

# Full Vev initialization (master + persona + context + proactive)
vev-init() {
    echo "════════════════════════════════════════════════════════════════"
    echo "🚀 VEV FULL INITIALIZATION"
    echo "════════════════════════════════════════════════════════════════"
    echo ""
    
    # Step 0: Master Architecture
    echo "📋 Step 0/4: Loading system architecture..."
    if [ -f "/root/.openclaw/workspace/SYSTEM_ARCHITECTURE.md" ]; then
        echo "   ✅ System architecture loaded"
        echo "   📊 Components: Voice Chat, Auto-Responder, Pre-flight, Skills"
    fi
    echo ""
    
    # Step 1: Persona
    echo "🎭 Step 1/4: Loading persona from SOUL.md..."
    vev-persona
    echo ""
    
    # Step 2: Context  
    echo "🧠 Step 2/4: Loading system context..."
    cd /root/.openclaw/workspace/scripts && python3 vev-preflight.py 2>/dev/null
    echo ""
    
    # Step 3: Proactive
    echo "🔔 Step 3/4: Checking proactive suggestions..."
    cd /root/.openclaw/workspace/scripts && python3 vev-proactive-suggest.py 2>/dev/null
    echo ""
    
    echo "════════════════════════════════════════════════════════════════"
    echo "✅ VEV IS READY - Architecture + Persona + Context + Awareness"
    echo "════════════════════════════════════════════════════════════════"
    echo ""
}
export -f vev-init

# Auto-run full initialization on every new shell
vev-init
EOF

echo "✅ Vev Persona Enforcer er nå lagt til!"
echo ""
echo "NYE KOMMANDOER:"
echo "   vev-persona  - Husk hvem jeg er (Vev!)"
echo "   vev-init     - Full initialisering (persona + kontekst + proactive)"
echo "   vev          - Master control meny"
echo ""
echo "Dette kjører AUTOMATISK ved hver ny session:"
echo "   1. Laster SOUL.md (hvem er Vev)"
echo "   2. Laster kontekst (skills, minner, systemer)"
echo "   3. Sjekker proactive forslag"
echo ""
echo "Kjør 'source ~/.bashrc' for å aktivere nå!"
