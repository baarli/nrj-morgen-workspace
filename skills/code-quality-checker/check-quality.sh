#!/bin/bash
#
# Code Quality Checker
# Systematisk kodekvalitetsjekk for workspace
#

set -e

# Konfigurasjon
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
RULES_DIR="$SCRIPT_DIR/rules"
REPORT_DIR="$WORKSPACE_DIR/brain/reports"
LOG_FILE="$REPORT_DIR/quality-check.log"

# Farger (disable for non-tty)
if [ -t 1 ]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    NC='\033[0m'
else
    RED=''
    GREEN=''
    YELLOW=''
    BLUE=''
    NC=''
fi

# Score tracking
TOTAL_FILES=0
TOTAL_SCORE=0
CRITICAL_ISSUES=0
WARNINGS=0
INFO_ISSUES=0

# Disable exit on error for arithmetic operations
set +e

# Resultater
declare -a FILE_RESULTS
declare -a ISSUES_LIST

# Global for score passing
LAST_SCORE=0

# Hjelp
show_help() {
    cat << EOF
Code Quality Checker

Bruk:
  check-quality.sh [OPTIONS] [FILE]

Options:
  -h, --help          Vis denne hjelpen
  -a, --all           Sjekk alle filer
  -r, --report        Generer rapport
  -t, --type TYPE     Sjekk kun spesifikk type (python|bash|html)
  -v, --verbose       Detaljert output
  -s, --score         Vis kun score

Eksempler:
  check-quality.sh script.py              Sjekk en fil
  check-quality.sh --all                  Sjekk alle filer
  check-quality.sh --type python          Sjekk alle Python-filer
  check-quality.sh --report               Generer full rapport
EOF
}

# Logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# Sjekk om Python er tilgjengelig
check_python() {
    if command -v python3 >/dev/null 2>&1; then
        PYTHON_CMD="python3"
    elif command -v python >/dev/null 2>&1; then
        PYTHON_CMD="python"
    else
        echo -e "${RED}Feil: Python ikke funnet${NC}"
        exit 1
    fi
}

# Analyser Python-fil
analyze_python() {
    local file="$1"
    local verbose="$2"
    local score=100
    local issues=()
    
    # Sjekk syntaks
    if ! $PYTHON_CMD -m py_compile "$file" 2>/dev/null; then
        issues+=("CRITICAL: Syntaksfeil")
        ((CRITICAL_ISSUES++))
        score=$((score - 30))
    fi
    
    # Sjekk docstrings
    local func_count=$($PYTHON_CMD -c "
import ast
with open('$file') as f:
    tree = ast.parse(f.read())
funcs = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
docstrings = [f for f in funcs if ast.get_docstring(f)]
print(len(funcs), len(docstrings))
" 2>/dev/null | awk '{print $1 - $2}')
    
    if [ -n "$func_count" ] && [ "$func_count" -gt 0 ]; then
        issues+=("WARNING: $func_count funksjoner uten docstring")
        ((WARNINGS++))
        score=$((score - func_count * 5))
    fi
    
    # Sjekk linjelengde
    local long_lines=$(grep -n '.>{100}' "$file" 2>/dev/null | wc -l)
    if [ "$long_lines" -gt 0 ]; then
        issues+=("INFO: $long_lines linjer > 100 tegn")
        ((INFO_ISSUES++))
        score=$((score - long_lines))
    fi
    
    # Sjekk filstørrelse
    local line_count=$(wc -l < "$file")
    if [ "$line_count" -gt 500 ]; then
        issues+=("WARNING: Filen er $line_count linjer (anbefalt: < 500)")
        ((WARNINGS++))
        score=$((score - 10))
    fi
    
    # Sjekk for TODO/FIXME
    local todos=$(grep -n -i "TODO\|FIXME\|XXX" "$file" 2>/dev/null | wc -l)
    if [ "$todos" -gt 0 ]; then
        issues+=("INFO: $todos TODO/FIXME funnet")
        ((INFO_ISSUES++))
    fi
    
    # Sørg for at score ikke går under 0
    if [ "$score" -lt 0 ]; then
        score=0
    fi
    
    # Output
    if [ "$verbose" = "true" ]; then
        echo -e "${BLUE}📄 $file${NC}"
        echo "   Linjer: $line_count | Score: $score/100"
        for issue in "${issues[@]}"; do
            if [[ $issue == CRITICAL* ]]; then
                echo -e "   ${RED}✗ $issue${NC}"
            elif [[ $issue == WARNING* ]]; then
                echo -e "   ${YELLOW}⚠ $issue${NC}"
            else
                echo -e "   ${BLUE}ℹ $issue${NC}"
            fi
        done
        echo ""
    fi
    
    # Lagre resultat
    FILE_RESULTS+=("$file:$score:${#issues[@]}")
    LAST_SCORE=$score
    return 0
}

# Analyser Bash-fil
analyze_bash() {
    local file="$1"
    local verbose="$2"
    local score=100
    local issues=()
    
    # Sjekk syntaks
    if ! bash -n "$file" 2>/dev/null; then
        issues+=("CRITICAL: Syntaksfeil")
        ((CRITICAL_ISSUES++))
        score=$((score - 30))
    fi
    
    # Sjekk shebang
    if ! head -1 "$file" | grep -q "^#!/bin/bash\|^#!/bin/sh"; then
        issues+=("WARNING: Mangler shebang (#!/bin/bash)")
        ((WARNINGS++))
        score=$((score - 10))
    fi
    
    # Sjekk for set -e
    if ! grep -q "set -e\|set -o errexit" "$file" 2>/dev/null; then
        issues+=("INFO: Vurder å legge til 'set -e' for feilhåndtering")
        ((INFO_ISSUES++))
        score=$((score - 5))
    fi
    
    # Sjekk for ubeskyttede variabler
    local unquoted=$(grep -n '\$[A-Z_]*[^"]' "$file" 2>/dev/null | grep -v '#' | wc -l)
    if [ "$unquoted" -gt 5 ]; then
        issues+=("INFO: $unquoted potensielt ubeskyttede variabler")
        ((INFO_ISSUES++))
        score=$((score - 5))
    fi
    
    # Sjekk linjelengde
    local long_lines=$(grep -n '.>{100}' "$file" 2>/dev/null | wc -l)
    if [ "$long_lines" -gt 0 ]; then
        issues+=("INFO: $long_lines linjer > 100 tegn")
        ((INFO_ISSUES++))
        score=$((score - long_lines))
    fi
    
    # Sørg for at score ikke går under 0
    if [ "$score" -lt 0 ]; then
        score=0
    fi
    
    # Output
    if [ "$verbose" = "true" ]; then
        echo -e "${BLUE}📄 $file${NC}"
        echo "   Score: $score/100"
        for issue in "${issues[@]}"; do
            if [[ $issue == CRITICAL* ]]; then
                echo -e "   ${RED}✗ $issue${NC}"
            elif [[ $issue == WARNING* ]]; then
                echo -e "   ${YELLOW}⚠ $issue${NC}"
            else
                echo -e "   ${BLUE}ℹ $issue${NC}"
            fi
        done
        echo ""
    fi
    
    # Lagre resultat
    FILE_RESULTS+=("$file:$score:${#issues[@]}")
    LAST_SCORE=$score
    return 0
}

# Analyser HTML-fil
analyze_html() {
    local file="$1"
    local verbose="$2"
    local score=100
    local issues=()
    
    # Sjekk DOCTYPE
    if ! head -5 "$file" | grep -qi "DOCTYPE"; then
        issues+=("WARNING: Mangler DOCTYPE deklarasjon")
        ((WARNINGS++))
        score=$((score - 10))
    fi
    
    # Sjekk for title
    if ! grep -q "<title>" "$file" 2>/dev/null; then
        issues+=("WARNING: Mangler <title> tag")
        ((WARNINGS++))
        score=$((score - 10))
    fi
    
    # Sjekk for viewport meta
    if ! grep -q "viewport" "$file" 2>/dev/null; then
        issues+=("INFO: Vurder å legge til viewport meta tag")
        ((INFO_ISSUES++))
        score=$((score - 5))
    fi
    
    # Sjekk filstørrelse
    local line_count=$(wc -l < "$file")
    if [ "$line_count" -gt 1000 ]; then
        issues+=("WARNING: HTML-fil er $line_count linjer (vurder å splitte)")
        ((WARNINGS++))
        score=$((score - 10))
    fi
    
    # Sørg for at score ikke går under 0
    if [ "$score" -lt 0 ]; then
        score=0
    fi
    
    # Output
    if [ "$verbose" = "true" ]; then
        echo -e "${BLUE}📄 $file${NC}"
        echo "   Linjer: $line_count | Score: $score/100"
        for issue in "${issues[@]}"; do
            if [[ $issue == CRITICAL* ]]; then
                echo -e "   ${RED}✗ $issue${NC}"
            elif [[ $issue == WARNING* ]]; then
                echo -e "   ${YELLOW}⚠ $issue${NC}"
            else
                echo -e "   ${BLUE}ℹ $issue${NC}"
            fi
        done
        echo ""
    fi
    
    # Lagre resultat
    FILE_RESULTS+=("$file:$score:${#issues[@]}")
    LAST_SCORE=$score
    return 0
}

# Finn alle filer av en type
find_files() {
    local type="$1"
    case "$type" in
        python)
            find "$WORKSPACE_DIR/scripts" "$WORKSPACE_DIR/skills" -name "*.py" -type f 2>/dev/null
            ;;
        bash)
            find "$WORKSPACE_DIR/scripts" -name "*.sh" -type f 2>/dev/null
            ;;
        html)
            find "$WORKSPACE_DIR" -name "*.html" -type f 2>/dev/null
            ;;
        *)
            find "$WORKSPACE_DIR/scripts" "$WORKSPACE_DIR/skills" \( -name "*.py" -o -name "*.sh" \) -type f 2>/dev/null
            ;;
    esac
}

# Generer rapport
generate_report() {
    local report_file="$REPORT_DIR/code-quality-$(date +%Y%m%d-%H%M%S).md"
    
    mkdir -p "$REPORT_DIR"
    
    cat > "$report_file" << EOF
# Code Quality Report

**Generert:** $(date '+%Y-%m-%d %H:%M:%S')  
**Workspace:** $WORKSPACE_DIR

## Sammendrag

| Metrikk | Verdi |
|---------|-------|
| Filer sjekket | $TOTAL_FILES |
| Gjennomsnittlig score | $TOTAL_SCORE/100 |
| Kritiske feil | $CRITICAL_ISSUES |
| Advarsler | $WARNINGS |
| Info | $INFO_ISSUES |

## Filer rangert etter kvalitet

EOF

    # Sorter resultater etter score
    IFS=$'\n' sorted=($(sort -t':' -k2 -n -r <<< "${FILE_RESULTS[*]}"))
    unset IFS
    
    echo "| Fil | Score | Issues |" >> "$report_file"
    echo "|-----|-------|--------|" >> "$report_file"
    
    for result in "${sorted[@]}"; do
        IFS=':' read -r file score issue_count <<< "$result"
        local basename=$(basename "$file")
        echo "| $basename | $score/100 | $issue_count |" >> "$report_file"
    done
    
    cat >> "$report_file" << EOF

## Anbefalinger

EOF

    if [ $CRITICAL_ISSUES -gt 0 ]; then
        echo "- 🔴 **Kritiske feil må fikses umiddelbart**" >> "$report_file"
    fi
    if [ $WARNINGS -gt 10 ]; then
        echo "- 🟡 **Mange advarsler - vurder opprydding**" >> "$report_file"
    fi
    if [ $TOTAL_SCORE -lt 80 ]; then
        echo "- 📊 **Gjennomsnittlig score under 80 - fokus på forbedring**" >> "$report_file"
    fi
    
    echo "" >> "$report_file"
    echo "---" >> "$report_file"
    echo "*Rapport generert av Code Quality Checker*" >> "$report_file"
    
    echo -e "${GREEN}✅ Rapport lagret: $report_file${NC}"
}

# Hovedfunksjon
main() {
    local check_all=false
    local generate_report_flag=false
    local file_type=""
    local verbose=false
    local score_only=false
    local target_file=""
    
    # Parse argumenter
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -a|--all)
                check_all=true
                shift
                ;;
            -r|--report)
                generate_report_flag=true
                shift
                ;;
            -t|--type)
                file_type="$2"
                shift 2
                ;;
            -v|--verbose)
                verbose=true
                shift
                ;;
            -s|--score)
                score_only=true
                shift
                ;;
            -*)
                echo -e "${RED}Ukjent option: $1${NC}"
                show_help
                exit 1
                ;;
            *)
                target_file="$1"
                shift
                ;;
        esac
    done
    
    # Opprett logg-mappe
    mkdir -p "$REPORT_DIR"
    
    echo -e "${BLUE}🔍 Code Quality Checker${NC}"
    echo "========================"
    echo ""
    
    # Sjekk Python
    check_python
    
    # Bestem hvilke filer som skal sjekkes
    local files_to_check=()
    
    if [ -n "$target_file" ]; then
        # Sjekk spesifikk fil
        if [ -f "$target_file" ]; then
            files_to_check+=("$target_file")
        else
            echo -e "${RED}Feil: Fil ikke funnet: $target_file${NC}"
            exit 1
        fi
    elif [ "$check_all" = true ] || [ "$generate_report_flag" = true ]; then
        # Sjekk alle filer
        while IFS= read -r file; do
            files_to_check+=("$file")
        done < <(find_files "$file_type")
    else
        show_help
        exit 0
    fi
    
    # Sjekk hver fil
    TOTAL_FILES=${#files_to_check[@]}
    
    if [ $TOTAL_FILES -eq 0 ]; then
        echo -e "${YELLOW}Ingen filer funnet å sjekke${NC}"
        exit 0
    fi
    
    echo "Sjekker $TOTAL_FILES filer..."
    echo ""
    
    for file in "${files_to_check[@]}"; do
        local ext="${file##*.}"
        local file_score=0
        
        case "$ext" in
            py)
                analyze_python "$file" "$verbose"
                file_score=$LAST_SCORE
                ;;
            sh)
                analyze_bash "$file" "$verbose"
                file_score=$LAST_SCORE
                ;;
            html)
                analyze_html "$file" "$verbose"
                file_score=$LAST_SCORE
                ;;
            *)
                echo -e "${YELLOW}⚠ Ukjent filtype: $file${NC}"
                continue
                ;;
        esac
        
        TOTAL_SCORE=$((TOTAL_SCORE + file_score))
    done
    
    # Beregn gjennomsnitt
    if [ $TOTAL_FILES -gt 0 ]; then
        TOTAL_SCORE=$((TOTAL_SCORE / TOTAL_FILES))
    fi
    
    # Vis sammendrag
    echo ""
    echo "========================"
    echo -e "${BLUE}📊 SAMMENDRAG${NC}"
    echo "========================"
    echo "Filer sjekket: $TOTAL_FILES"
    
    if [ $TOTAL_SCORE -ge 90 ]; then
        echo -e "Gjennomsnittlig score: ${GREEN}$TOTAL_SCORE/100${NC} 🌟"
    elif [ $TOTAL_SCORE -ge 70 ]; then
        echo -e "Gjennomsnittlig score: ${YELLOW}$TOTAL_SCORE/100${NC}"
    else
        echo -e "Gjennomsnittlig score: ${RED}$TOTAL_SCORE/100${NC}"
    fi
    
    if [ $CRITICAL_ISSUES -gt 0 ]; then
        echo -e "Kritiske feil: ${RED}$CRITICAL_ISSUES${NC}"
    fi
    if [ $WARNINGS -gt 0 ]; then
        echo -e "Advarsler: ${YELLOW}$WARNINGS${NC}"
    fi
    if [ $INFO_ISSUES -gt 0 ]; then
        echo -e "Info: ${BLUE}$INFO_ISSUES${NC}"
    fi
    
    # Generer rapport hvis ønsket
    if [ "$generate_report_flag" = true ]; then
        echo ""
        generate_report
    fi
    
    # Returner exit code basert på score
    if [ $CRITICAL_ISSUES -gt 0 ]; then
        exit 2
    elif [ $TOTAL_SCORE -lt 70 ]; then
        exit 1
    else
        exit 0
    fi
}

# Kjør hovedfunksjon
main "$@"
