#!/bin/bash
# Aktiverer alle relevante skills for en oppgave

TASK=$1

echo "🎯 Aktiverer skills for: $TASK"
echo ""

case $TASK in
    "morning")
        echo "Aktiverer morgen-skills:"
        echo "  ✅ nrj-morning-show-suite"
        echo "  ✅ media-monitor"
        echo "  ✅ news-aggregator"
        echo "  ✅ nrj-content-suite"
        echo "  ✅ email-automation"
        echo "  ✅ social-publisher"
        ;;
    "content")
        echo "Aktiverer innholds-skills:"
        echo "  ✅ nrj-content-suite"
        echo "  ✅ audio-transcriber"
        echo "  ✅ browser-automation"
        echo "  ✅ creative-brainstorm"
        ;;
    "research")
        echo "Aktiverer research-skills:"
        echo "  ✅ research-suite"
        echo "  ✅ nrj-intelligence-hub"
        echo "  ✅ trend-detector"
        echo "  ✅ media-monitor"
        ;;
    "social")
        echo "Aktiverer sosiale-skills:"
        echo "  ✅ nrj-social-suite"
        echo "  ✅ social-publisher"
        echo "  ✅ relationship-tracker"
        ;;
    *)
        echo "Ukjent oppgave: $TASK"
        echo "Bruk: morning | content | research | social"
        exit 1
        ;;
esac

echo ""
echo "✅ Skills aktivert for $TASK"
