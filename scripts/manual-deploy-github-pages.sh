#!/bin/bash
# MANUELL DEPLOY TIL GITHUB PAGES
# Kjør dette scriptet for å deploye Mission Control til GitHub Pages

echo "🚀 Deployer Mission Control til GitHub Pages..."
echo ""

# Gå til github-pages mappen
cd /root/.openclaw/workspace/github-pages

# Sjekk at .netlify er fjernet
if [ -d ".netlify" ]; then
    echo "🗑️  Fjerner .netlify mappe (222MB)..."
    rm -rf .netlify
fi

# Legg til alle endringer
git add -A

# Commit
git commit -m "Deploy Mission Control - fjernet .netlify (222MB)" || echo "Ingen endringer å committe"

# Push til gh-pages
echo "📤 Pusher til GitHub..."
git push origin gh-pages

echo ""
echo "✅ Deploy fullført!"
echo "🔗 Sjekk: https://baarli.github.io/nrj-morgen-workspace/"
echo ""
echo "⚠️  Hvis push feiler pga autentisering:"
echo "   1. Gå til https://github.com/settings/tokens"
echo "   2. Generer nytt token (scope: repo)"
echo "   3. Kjør: gh auth login"
