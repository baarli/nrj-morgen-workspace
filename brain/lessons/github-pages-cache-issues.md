# LESSONS LEARNED: GitHub Pages White Screen

**Date:** 2026-03-05  
**Issue:** White screen after every deploy  
**Root Cause:** GitHub Pages aggressive caching

---

## 🔴 THE PROBLEM

Every time we push to GitHub Pages:
1. New build is created in `docs/` folder
2. Push to GitHub
3. GitHub Pages shows **old** cached version
4. Old version points to `/src/main.jsx` (development)
5. **White screen** - no JavaScript loads

---

## 🔍 ROOT CAUSE

GitHub Pages has **aggressive caching**:
- index.html is cached at CDN level
- Can take 5-10 minutes to invalidate
- Sometimes requires manual cache clear
- Old references to `/src/main.jsx` persist

---

## ✅ SOLUTIONS IMPLEMENTED

### 1. .nojekyll File
```bash
touch docs/.nojekyll
```
- Prevents Jekyll processing
- Ensures files are served as-is

### 2. Cache-Control Headers in HTML
```html
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
<meta http-equiv="Pragma" content="no-cache" />
<meta http-equiv="Expires" content="0" />
```
- Tells browsers not to cache
- Forces fresh load each time

### 3. Full docs/ Recreation
```bash
rm -rf docs
cp -r dist docs
touch docs/.nojekyll
```
- Ensures clean state
- No stale files

### 4. Verify Before Push
```bash
# Check index.html points to correct assets
grep "src=" docs/index.html
# Should show: ./assets/index-XXXXXX.js

# NOT: /src/main.jsx
```

---

## 🛡️ PREVENTION CHECKLIST

Before every push:

- [ ] Delete old docs/ folder completely
- [ ] Copy fresh dist/ to docs/
- [ ] Add .nojekyll file
- [ ] Verify index.html has cache headers
- [ ] Verify script src points to ./assets/
- [ ] Commit and push
- [ ] Wait 2-3 minutes
- [ ] Test with hard refresh (Ctrl+Shift+R)
- [ ] If still white: add ?nocache=1 to URL

---

## 🚨 EMERGENCY FIX

If white screen after deploy:

```bash
# 1. Force cache clear via URL
# Add to URL: ?nocache=1

# 2. Or use incognito mode

# 3. Or manually trigger rebuild
git commit --allow-empty -m "Force rebuild"
git push
```

---

## 📋 UPDATED DEPLOY SCRIPT

```bash
#!/bin/bash
# deploy.sh - Safe GitHub Pages deploy

npm run build

# Clean docs completely
rm -rf docs

# Copy fresh build
cp -r dist docs

# Add cache-busting
touch docs/.nojekyll

# Add cache headers to index.html
sed -i 's/<meta name="description"/<meta http-equiv="Cache-Control" content="no-cache" \/>\n    <meta name="description"/' docs/index.html

# Verify
echo "Script src:"
grep "src=" docs/index.html

# Commit and push
git add docs/
git commit -m "Deploy $(date)"
git push

echo "✅ Deployed! Wait 2-3 minutes..."
```

---

## 💡 KEY INSIGHTS

1. **GitHub Pages CDN caches aggressively** - plan for it
2. **Always use .nojekyll** - prevents processing issues  
3. **Verify before push** - 10 seconds saves 10 minutes debugging
4. **Cache headers help** but aren't perfect
5. **Hard refresh is your friend** during testing

---

**Lesson:** Never assume push = immediate update. GitHub Pages needs time + cache busting.
