---
name: nrj-dashboard-system
description: Update NRJ Morgen Dashboard statistics panel with latest Nielsen radio and Podtoppen podcast data. Use when user asks to update NRJ dashboard, refresh radio stats, update podcast rankings, or fetch Nielsen/Podtoppen data for nrjmorgen.com. This is a SEPARATE system from the sakslista (agenda items) - it updates a specific dashboard panel with ID 0b1f6b6b-3fde-434b-b7c8-dcf306beea72.
---

# NRJ Dashboard System

## ⚠️ CRITICAL: This is NOT the sakslista!

This skill updates the **NRJ Statistikk panel** on the dashboard (nrjmorgen.com), NOT the daily agenda/sakslista.

## Panel Information

- **Panel ID:** `0b1f6b6b-3fde-434b-b7c8-dcf306beea72`
- **Location:** Dashboard (not sakslista)
- **Type:** `agenda_items` with `is_pinned: true`
- **Position:** Top of dashboard

## How to Update

```bash
cd /root/.openclaw/workspace/scripts
python3 update_nrj_dashboard.py
```

**ALWAYS use this script** - it updates the EXISTING panel.

**NEVER use:** `fetch_nrj_dashboard_stats.py` (creates NEW item in sakslista)

## Data Sources

### Nielsen Radio (API)
- **URL:** `https://eu-iport.nielsen-iwatch.com/api/Chart?dataid=8eb6daca-1266-4af8-8e8f-f39107dc63fb&publish_key=bd551853-f42b-4b86-813a-79faf3a718e9`
- **Latest available:** Week 7, 2026 (69,000 daily listeners)
- **Delay:** 1 week (published Wednesday/Thursday)
- **Format:** JSON

### Podtoppen Podcast (CSV)
- **URL:** `https://podtoppen.tnslistene.no/export.php`
- **Latest ranking:** #62 (16,470 unique listeners)
- **Updates:** Weekly (Wednesday)
- **Format:** CSV with semicolon, latin-1 encoding

## Current Data (as of 2026-02-24)

**📻 Nielsen Radio (Week 7, 2026):**
- Daily listeners: 69,000
- Average 2026: 58,857
- Trend: +9.5% from week 6

**🎧 Podtoppen Podcast:**
- Ranking: #62
- Unique listeners: 16,470
- Downloads: 33,405
- Publisher: Bauer Media

## Supabase Configuration

- **URL:** `https://kvniauxokdtmpvjtfnej.supabase.co`
- **Table:** `agenda_items`
- **Tenant ID:** `a0000000-0000-0000-0000-000000000001`
- **User ID:** `10aa1508-6d52-490c-8ae5-fa3da9a152c4` (BaarliClaw)
- **Panel ID:** `0b1f6b6b-3fde-434b-b7c8-dcf306beea72`

## What the Script Does

1. Finds existing panel by ID
2. Fetches latest Nielsen radio data
3. Fetches latest Podtoppen podcast data
4. Generates HTML for dashboard display
5. Updates existing panel (PATCH, not POST)

## Output

The dashboard panel shows:
- Radio stats with trend indicator
- Podcast ranking and listener counts
- Last updated timestamp
- Data source attribution

## Documentation

- Full docs: `/root/.openclaw/workspace/docs/NRJ_DASHBOARD_SYSTEM.md`
- Memory: `/root/.openclaw/workspace/MEMORY.md`
- Tools: `/root/.openclaw/workspace/TOOLS.md`

## Common Mistakes to Avoid

❌ Using `fetch_nrj_dashboard_stats.py` (creates new item)  
❌ Updating sakslista instead of dashboard panel  
❌ Forgetting panel ID  
❌ Not verifying data sources  

✅ Using `update_nrj_dashboard.py` (updates existing)  
✅ Targeting correct panel ID  
✅ Checking Nielsen has 1-week delay  
✅ Verifying Podtoppen updates weekly  
