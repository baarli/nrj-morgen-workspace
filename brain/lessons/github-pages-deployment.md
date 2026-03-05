# LESSONS LEARNED: GitHub Pages Deployment

**Date:** 2026-03-05  
**Issue:** White screen on GitHub Pages

---

## 🔴 PROBLEM

Mission Control showed white screen after updates.

---

## 🔍 ROOT CAUSE ANALYSIS

### 1. Build Failure
- New code (Saksliste/Kanban) had import errors
- Build failed with: `Could not resolve "../lib/supabase"`
- Old working build was in `docs/` folder

### 2. Accidental Deletion
- During debugging, moved `docs/` to `docs_backup/`
- GitHub Pages serves from `docs/` folder on main branch
- Without `docs/`, GitHub Pages had no files to serve

### 3. Result
- GitHub Pages showed only HTML shell
- No JavaScript/CSS files found (404 errors)
- White screen because React couldn't mount

---

## ✅ SOLUTION

1. **Restored docs folder** from `docs_backup/`
2. **Committed all changes** including new code
3. **Pushed to GitHub** 
4. **GitHub Pages** now serves restored files

---

## 🛡️ PREVENTION MEASURES

### 1. Never Delete docs/ Without Backup
```bash
# WRONG: mv docs docs_backup  (breaks GitHub Pages)
# CORRECT: cp -r docs docs_backup  (keeps original)
```

### 2. Always Verify Build Before Deploy
```bash
npm run build
ls -la dist/  # Verify files exist
cp -r dist docs  # Only after successful build
```

### 3. Check File References
- Ensure all imports use correct paths
- Use `@/lib/supabase` alias instead of relative paths
- Verify vite.config.js has proper alias configuration

### 4. Test Before Push
```bash
# Local test
npm run preview

# Or check built files
npx serve docs
```

### 5. GitHub Pages Settings
- Source: Deploy from branch
- Branch: main /docs folder
- Must have index.html in docs/
- All assets must be in docs/

---

## 📋 DEPLOYMENT CHECKLIST

Before pushing to GitHub:

- [ ] `npm run build` succeeds
- [ ] `docs/` folder exists
- [ ] `docs/index.html` exists
- [ ] `docs/assets/` has JS/CSS files
- [ ] All images copied to docs/
- [ ] Test locally with `npx serve docs`
- [ ] Git commit includes docs/
- [ ] Push to origin main
- [ ] Wait 2-3 minutes for GitHub Pages update
- [ ] Test live URL

---

## 🚨 EMERGENCY RECOVERY

If white screen occurs:

```bash
# 1. Check if docs exists
ls docs/

# 2. If missing, restore from last known good
# Find in git history:
git log --oneline

# Checkout specific version of docs:
git checkout COMMIT_HASH -- docs/

# 3. Commit and push
git add docs/
git commit -m "Emergency restore of docs folder"
git push origin main
```

---

## 💡 KEY INSIGHTS

1. **GitHub Pages is static** - No server-side rendering
2. **docs/ folder is the entire site** - Must be complete
3. **Build must succeed** - Failed builds = broken site
4. **Always backup before moving** - `mv` is destructive
5. **Test incrementally** - Don't batch too many changes

---

**Lesson:** Never move/delete the docs folder without a backup copy. Always verify the build succeeds before deploying.
