# Mission Control - Test Checklist

## Pre-Test Setup
- [ ] Clear browser cache
- [ ] Clear localStorage
- [ ] Open browser console (F12)

## Login Test
- [ ] Navigate to https://baarli.github.io/mission-control-live/
- [ ] Enter password: kloakontroll2026
- [ ] Click login
- [ ] **Expected:** Dashboard loads, no console errors

## Navigation Test
- [ ] Click "📊 Dashboard"
- [ ] Click "📋 Saksliste"
- [ ] Click "🔍 Søk"
- [ ] Click "📈 Statistikk"
- [ ] **Expected:** Smooth transitions, no errors

## Saksliste Test
- [ ] Select a date
- [ ] Click refresh
- [ ] Click edit (✏️) on a sak
- [ ] Modify title
- [ ] Click save
- [ ] **Expected:** Changes saved, toast notification shown

## Search Test
- [ ] Go to "🔍 Søk"
- [ ] Enter search term: "Farmen"
- [ ] Select category: "Reality TV"
- [ ] Click search
- [ ] **Expected:** Results appear with scores

## Stats Test
- [ ] Go to "📈 Statistikk"
- [ ] **Expected:** Charts visible for radio and podcast
- [ ] Hover over chart points
- [ ] **Expected:** Tooltip shows values

## Theme Toggle Test
- [ ] Click 🌙/☀️ in header
- [ ] **Expected:** Theme changes, preference saved

## Onboarding Test
- [ ] Clear localStorage
- [ ] Refresh page
- [ ] **Expected:** Onboarding modal appears
- [ ] Click through all 5 steps
- [ ] **Expected:** Onboarding completes, no errors

## Error Handling Test
- [ ] Try to login with wrong password
- [ ] **Expected:** Error message shown
- [ ] Try to save empty sak title
- [ ] **Expected:** Validation error

## Console Check
- [ ] Open browser console
- [ ] Check for:
  - [ ] No red errors
  - [ ] No undefined variables
  - [ ] No failed network requests

## Mobile Test
- [ ] Open on mobile or resize browser
- [ ] **Expected:** Responsive layout works

---

## Sign-off

**Tester:** _______________  
**Date:** _______________  
**Result:** ☐ Pass / ☐ Fail  
**Notes:**
