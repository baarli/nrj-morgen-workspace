#!/bin/bash
#
# compliance-checker.sh
# Automatisk sjekk at alle aktiviteter følger PRINCIPLES.md
# Kjøres før og etter hver oppgave
#

set -e

WORKSPACE="/root/.openclaw/workspace"
PRINCIPLES="${WORKSPACE}/PRINCIPLES.md"
LOG_FILE="${WORKSPACE}/memory/compliance-log.md"
ERRORS=0

# Farger for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[COMPLIANCE]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    ((ERRORS++))
}

# Sjekk at PRINCIPLES.md finnes
check_principles_exist() {
    if [[ ! -f "$PRINCIPLES" ]]; then
        error "PRINCIPLES.md finnes ikke! Dette er kritisk."
        return 1
    fi
    log "✅ PRINCIPLES.md finnes"
}

# Sjekk at SOUL.md er i tråd med PRINCIPLES
check_soul_alignment() {
    local soul="${WORKSPACE}/SOUL.md"
    if [[ ! -f "$soul" ]]; then
        warn "SOUL.md finnes ikke"
        return 0
    fi
    
    # Sjekk at nøkkelord fra PRINCIPLES finnes i SOUL.md
    local keywords=("craft" "thoughtful" "autonomy" "trust" "memory" "communication")
    local found=0
    
    for keyword in "${keywords[@]}"; do
        if grep -qi "$keyword" "$soul"; then
            ((found++))
        fi
    done
    
    if [[ $found -ge ${#keywords[@]}/2 ]]; then
        log "✅ SOUL.md er i tråd med PRINCIPLES.md ($found/${#keywords[@]} nøkkelord)"
    else
        warn "SOUL.md kan være ute av tråd med PRINCIPLES.md ($found/${#keywords[@]} nøkkelord)"
    fi
}

# Sjekk at AGENTS.md er i tråd
check_agents_alignment() {
    local agents="${WORKSPACE}/AGENTS.md"
    if [[ ! -f "$agents" ]]; then
        warn "AGENTS.md finnes ikke"
        return 0
    fi
    
    # Sjekk at PRINCIPLES.md er referert
    if grep -q "PRINCIPLES.md" "$agents"; then
        log "✅ AGENTS.md refererer til PRINCIPLES.md"
    else
        error "AGENTS.md mangler referanse til PRINCIPLES.md"
    fi
}

# Sjekk at MEMORY.md er i tråd
check_memory_alignment() {
    local memory="${WORKSPACE}/MEMORY.md"
    if [[ ! -f "$memory" ]]; then
        warn "MEMORY.md finnes ikke"
        return 0
    fi
    
    # Sjekk at minnesystem er dokumentert
    if grep -q "Minnesystem\|System Memory\|Interaction Memory" "$memory"; then
        log "✅ MEMORY.md dokumenterer minnesystem"
    else
        warn "MEMORY.md mangler dokumentasjon av minnesystem"
    fi
}

# Sjekk at TOOLS.md er i tråd
check_tools_alignment() {
    local tools="${WORKSPACE}/TOOLS.md"
    if [[ ! -f "$tools" ]]; then
        warn "TOOLS.md finnes ikke"
        return 0
    fi
    
    # Sjekk at verktøy-filosofi er dokumentert
    if grep -q "Verktøy-filosofi\|Software is Craft" "$tools"; then
        log "✅ TOOLS.md dokumenterer verktøy-filosofi"
    else
        warn "TOOLS.md mangler verktøy-filosofi"
    fi
}

# Sjekk at auto-exec-enforcer finnes og er kjørbar
check_auto_exec() {
    local enforcer="${WORKSPACE}/scripts/auto-exec-enforcer.sh"
    if [[ ! -f "$enforcer" ]]; then
        error "auto-exec-enforcer.sh finnes ikke!"
        return 1
    fi
    
    if [[ ! -x "$enforcer" ]]; then
        chmod +x "$enforcer"
        log "Gjorde auto-exec-enforcer.sh kjørbar"
    fi
    
    log "✅ auto-exec-enforcer.sh finnes og er kjørbar"
}

# Sjekk at skills er i tråd med PRINCIPLES
check_skills_alignment() {
    local skills_dir="${WORKSPACE}/skills"
    if [[ ! -d "$skills_dir" ]]; then
        warn "skills/ mappe finnes ikke"
        return 0
    fi
    
    local skill_count=$(find "$skills_dir" -name "SKILL.md" | wc -l)
    local aligned_count=0
    
    for skill in "$skills_dir"/*/SKILL.md; do
        if [[ -f "$skill" ]]; then
            if grep -q "craft\|quality\|elegant\|thoughtful" "$skill"; then
                ((aligned_count++))
            fi
        fi
    done
    
    log "✅ $aligned_count/$skill_count skills er i tråd med PRINCIPLES.md"
}

# Logg resultat
log_result() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local status="✅ PASS"
    
    if [[ $ERRORS -gt 0 ]]; then
        status="❌ FAIL ($ERRORS feil)"
    fi
    
    # Append til logg
    echo -e "\n## $timestamp - $status" >> "$LOG_FILE"
    echo "- PRINCIPLES.md: ✅" >> "$LOG_FILE"
    echo "- Sjekket: SOUL.md, AGENTS.md, MEMORY.md, TOOLS.md, skills/" >> "$LOG_FILE"
    
    if [[ $ERRORS -gt 0 ]]; then
        echo "- **Feil funnet: $ERRORS**" >> "$LOG_FILE"
        echo "- Handling kreves!" >> "$LOG_FILE"
    fi
}

# Hovedfunksjon
main() {
    echo "=========================================="
    echo "🔍 COMPLIANCE CHECK - PRINCIPLES.md"
    echo "=========================================="
    echo ""
    
    # Sjekk alle komponenter
    check_principles_exist
    check_soul_alignment
    check_agents_alignment
    check_memory_alignment
    check_tools_alignment
    check_auto_exec
    check_skills_alignment
    
    echo ""
    echo "=========================================="
    
    if [[ $ERRORS -eq 0 ]]; then
        echo -e "${GREEN}✅ ALL SJEKKER BESTÅTT${NC}"
        echo "Systemet er i tråd med PRINCIPLES.md"
    else
        echo -e "${RED}❌ $ERRORS FEIL FUNNET${NC}"
        echo "Systemet har avvik fra PRINCIPLES.md"
        echo "Se detaljer ovenfor"
    fi
    
    echo "=========================================="
    
    # Logg resultat
    log_result
    
    return $ERRORS
}

# Kjør hovedfunksjon
main "$@"