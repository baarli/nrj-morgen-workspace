#!/usr/bin/env python3
"""
Radio Stats Updater - Hent og oppdater radiotall og podtoppen-tall
for NRJ Morgen dashboard - MED EKTE DATA
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Legg til scrapers i path
sys.path.insert(0, '/root/.openclaw/workspace/scripts/scrapers')
sys.path.insert(0, '/root/.openclaw')

from skills_lib import SupabaseClient
from podtoppen_scraper import PodtoppenScraper
from nielsen_scraper import NielsenRadioScraper


class RadioStatsUpdater:
    """Hent og oppdater radiotall for NRJ Morgen - MED EKTE DATA"""
    
    def __init__(self):
        try:
            self.supabase = SupabaseClient()
        except:
            self.supabase = None
            print("⚠️  Supabase ikke tilgjengelig, bruker lokal lagring")
        
        self.podtoppen = PodtoppenScraper()
        self.nielsen = NielsenRadioScraper()
        self.local_dir = Path("/tmp/radio_stats")
        self.local_dir.mkdir(exist_ok=True)
    
    def update_podtoppen(self) -> bool:
        """Hent og oppdater Podtoppen-tall - EKTE DATA"""
        print("🎧 Henter EKTE data fra Podtoppen...")
        print("   Kilde: https://podtoppen.tnslistene.no/")
        
        stats = self.podtoppen.get_current_stats()
        
        if not stats:
            print("❌ Kunne ikke hente Podtoppen-data")
            return False
        
        print(f"   ✅ Rangering: #{stats['rank']}")
        print(f"   ✅ Lyttere: {stats['weekly_listeners']:,}")
        print(f"   ✅ Endring: {stats['weekly_change_percent']:+d}%")
        
        # Lagre data
        return self._save_stats("podtoppen", stats)
    
    def update_nielsen(self) -> bool:
        """Hent og oppdater Nielsen-tall"""
        print("📻 Henter radiotall...")
        print("   Kilde: Nielsen")
        
        stats = self.nielsen.get_stats(use_public_fallback=True)
        
        if not stats:
            print("❌ Kunne ikke hente Nielsen-data")
            return False
        
        if stats.get("source") == "nielsen_public_report":
            print("   ⚠️  Bruker offentlige markedstall")
            print("   📊 Nasjonal dekning: 84.1%")
            print("   📊 Daglig lyttere: 49%")
            print("   ℹ️  Stasjon-spesifikke tall krever iPort-tilgang")
        else:
            print(f"   ✅ Ukentlig rekkevidde: {stats.get('weekly_reach', 0):,}")
            print(f"   ✅ Markedsandel: {stats.get('market_share', 0)}%")
        
        # Lagre data
        return self._save_stats("nielsen", stats)
    
    def _save_stats(self, stats_type: str, data: dict) -> bool:
        """Lagre statistikk"""
        try:
            # 1. Lagre lokalt
            filename = self.local_dir / f"{stats_type}_{data.get('date', datetime.now().strftime('%Y-%m-%d'))}.json"
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"   💾 Lagret lokalt: {filename}")
            
            # 2. Prøv å lagre i Supabase
            if self.supabase:
                record = {
                    "title": f"📊 {stats_type.upper()} - {datetime.now().strftime('%d.%m.%Y')}",
                    "description": json.dumps(data, indent=2, ensure_ascii=False)[:500],
                    "category": "STATS",
                    "show_date": datetime.now().strftime("%Y-%m-%d"),
                    "notes": f"RADIO_STATS:{stats_type}\n{json.dumps(data, indent=2, ensure_ascii=False)}",
                    "is_pinned": False,
                    "order_index": 999
                }
                
                if self.supabase.insert("agenda_items", record):
                    print(f"   💾 Lagret i Supabase")
                else:
                    print(f"   ⚠️  Kunne ikke lagre i Supabase")
            
            return True
            
        except Exception as e:
            print(f"❌ Feil ved lagring: {e}")
            return False
    
    def generate_report(self) -> str:
        """Generer rapport fra lagrede data"""
        report = []
        report.append("="*60)
        report.append("📊 NRJ MORGEN STATISTIKK-RAPPORT")
        report.append("="*60)
        report.append(f"Generert: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
        report.append("")
        
        # Les Podtoppen-data
        podtoppen_files = sorted(self.local_dir.glob("podtoppen_*.json"))
        if podtoppen_files:
            with open(podtoppen_files[-1]) as f:
                pod_data = json.load(f)
            
            report.append("🎧 PODTOPPEN (SISTE UKE)")
            report.append("-"*40)
            report.append(f"Rangering: #{pod_data.get('rank', 'N/A')}")
            report.append(f"Ukentlige lyttere: {pod_data.get('weekly_listeners', 0):,}")
            report.append(f"Endring: {pod_data.get('weekly_change_percent', 0):+d}%")
            report.append(f"Kategori: {pod_data.get('category', 'N/A')}")
            report.append("")
        
        # Les Nielsen-data
        nielsen_files = sorted(self.local_dir.glob("nielsen_*.json"))
        if nielsen_files:
            with open(nielsen_files[-1]) as f:
                niel_data = json.load(f)
            
            report.append("📻 RADIOTALl (NIELSEN)")
            report.append("-"*40)
            if niel_data.get("weekly_reach"):
                report.append(f"Ukentlig rekkevidde: {niel_data['weekly_reach']:,}")
                report.append(f"Markedsandel: {niel_data.get('market_share', 0)}%")
            else:
                report.append(f"Nasjonal dekning: {niel_data.get('national_weekly_reach_percent', 84.1)}%")
                report.append(f"Daglig lyttere: {niel_data.get('national_daily_reach_percent', 49)}%")
                report.append("(Generelle markedstall - stasjon-spesifikk krever iPort)")
            report.append("")
        
        report.append("="*60)
        return "\n".join(report)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Oppdater radiotall for NRJ Morgen - EKTE DATA')
    parser.add_argument('--podtoppen', action='store_true', help='Oppdater Podtoppen-tall')
    parser.add_argument('--nielsen', action='store_true', help='Oppdater Nielsen-tall')
    parser.add_argument('--both', action='store_true', help='Oppdater begge')
    parser.add_argument('--report', action='store_true', help='Vis rapport')
    
    args = parser.parse_args()
    
    updater = RadioStatsUpdater()
    
    if args.podtoppen or args.both:
        updater.update_podtoppen()
    
    if args.nielsen or args.both:
        updater.update_nielsen()
    
    if args.report or not (args.podtoppen or args.nielsen or args.both):
        print(updater.generate_report())


if __name__ == '__main__':
    main()
