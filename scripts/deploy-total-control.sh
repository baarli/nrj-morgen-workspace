#!/bin/bash
# Deploy Total Control Dashboard to GitHub Pages
# NOTE: Netlify disabled due to credit limit - using GitHub Pages instead

WORKSPACE="/root/.openclaw/workspace"
SOURCE_DIR="$WORKSPACE/mission-control/public"
GH_PAGES_DIR="$WORKSPACE/github-pages"

echo "🚀 Deploying Total Control Dashboard to GitHub Pages..."
echo ""

# Check if github-pages directory exists
if [ ! -d "$GH_PAGES_DIR" ]; then
    echo "❌ GitHub Pages directory not found!"
    echo "💡 Creating directory..."
    mkdir -p "$GH_PAGES_DIR"
    cd "$GH_PAGES_DIR"
    git init
    git remote add origin https://github.com/baarli/nrj-morgen-workspace.git
fi

# Sync files to github-pages
echo "📁 Syncing files..."
rsync -av --delete "$SOURCE_DIR/" "$GH_PAGES_DIR/" 2>&1 | tail -5

# Commit and push
echo ""
echo "📤 Committing and pushing to gh-pages branch..."
cd "$GH_PAGES_DIR"

# Fetch gh-pages branch if it exists
git fetch origin gh-pages 2>/dev/null || echo "No existing gh-pages branch"

# Create orphan branch if needed
git checkout --orphan gh-pages 2>/dev/null || git checkout gh-pages 2>/dev/null || true

# Remove all files from git (keep working tree)
git rm -rf . 2>/dev/null || true

# Add all files
git add -A

# Commit
git commit -m "Deploy Total Control Dashboard v3.0 - $(date '+%Y-%m-%d %H:%M:%S')" 2>&1 | tail -1 || echo "No changes to commit"

# Push to gh-pages branch
git push -f origin gh-pages 2>&1 | tail -5

echo ""
echo "✅ Deploy complete!"
echo "🔗 URL: https://baarli.github.io/nrj-morgen-workspace/"
