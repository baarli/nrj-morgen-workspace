#!/usr/bin/env python3
"""
Nielsen Radio Data Import - Håndter nedlastet spreadsheet fra Nielsen iPort

BRUK:
1. Logg inn på https://dashboard-eu-iport.nielsen-iwatch.com/norway_radio_reporting/
2. Last ned rapport som CSV/Excel
3. Lagre filen i /tmp/nielsen_download/
4. Kjør dette skriptet for å importere til Supabase

SUPPORTERTE FORMAT:
- CSV (.csv)
- Excel (.xlsx, .xls) - krever openpyxl
"""

import csv
import json
import os
import re
import urllib.request
from datetime import datetime
from pathlib import Path

# Supabase konfigurasjon
SUPABASE_URL = "https://kvniauxokdtmpvjtfnej.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt2bmlhdXhva2R0bXB2anRmbmVqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTM2NzIzNCwiZXhwIjoyMDY2OTQzMjM0fQ.OkhTtq9QAQ3xMzZYKyWyCjj7PiqMZJKSvpA0jcBJqpE"
TENANT_ID = "a0000000-0000-0000-0000-000000000001"
BAARLI_CLAW_ID = "10aa1508-6d52-490c-8ae5-fa3da9a152c4"

# Mappe for nedlastede filer
DOWNLOAD_DIR = Path("/tmp/nielsen_download")
DOWNLOAD_DIR.mkdir(exist_ok=True)


def find_downloaded_file():
    """Finn den nyeste Nielsen-filen i download-mappen"""
    
    supported_extensions = ['.csv', '.xlsx', '.xls']
    files = []
    
    for ext in supported_extensions:
        files.extend(DOWNLOAD_DIR.glob(f'*{ext}'))
    
    if not files:
        return None
    
    # Returner nyeste fil
    return max(files, key=lambda f: f.stat().st_mtime)


def parse_csv_file(filepath):
    """Parse CSV-fil fra Nielsen"""
    
    data = {
        "stations": [],
        "date_range": None,
        "source": "nielsen_csv_import"
    }
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
        
        if not rows:
            print("❌ CSV-filen er tom")
            return None
        
        # Analyser struktur
        print(f"📄 Fant {len(rows)} rader i CSV-filen")
        
        # Se etter NRJ-data
        nrj_data = None
        headers = None
        
        for i, row in enumerate(rows):
            # Sjekk om dette er header-raden
            if any('station' in str(cell).lower() or 'kanal' in str(cell).lower() for cell in row):
                headers = row
                print(f"   ✅ Header funnet på rad {i+1}: {headers}")
                continue
            
            # Se etter NRJ i raden
            for cell in row:
                if 'nrj' in str(cell).lower():
                    print(f"   ✅ NRJ funnet på rad {i+1}")
                    nrj_data = {
                        "row_index": i,
                        "raw_data": row,
                        "headers": headers
                    }
                    break
            
            if nrj_data:
                break
        
        # Hvis vi fant NRJ-data, prøv å parse tall
        if nrj_data and headers:
            station_data = {"name": "NRJ", "source": "nielsen_csv"}
            
            for i, (header, value) in enumerate(zip(headers, nrj_data["raw_data"])):
                header_lower = str(header).lower()
                
                # Ulike varianter av kolonnenavn
                if any(x in header_lower for x in ['weekly', 'ukentlig', 'reach', 'rekkevidde']):
                    try:
                        # Fjern tusenskilletegn og konverter til tall
                        clean_value = str(value).replace(' ', '').replace(',', '').replace('.', '')
                        station_data["weekly_reach"] = int(clean_value)
                    except:
                        station_data["weekly_reach"] = value
                
                elif any(x in header_lower for x in ['daily', 'daglig']):
                    try:
                        clean_value = str(value).replace(' ', '').replace(',', '').replace('.', '')
                        station_data["daily_reach"] = int(clean_value)
                    except:
                        station_data["daily_reach"] = value
                
                elif any(x in header_lower for x in ['share', 'andel', 'market']):
                    try:
                        clean_value = str(value).replace('%', '').replace(',', '.')
                        station_data["market_share"] = float(clean_value)
                    except:
                        station_data["market_share"] = value
                
                elif any(x in header_lower for x in ['time', 'tid', 'listening']):
                    station_data["avg_listening_time"] = value
            
            data["stations"].append(station_data)
        
        return data
        
    except Exception as e:
        print(f"❌ Feil ved parsing av CSV: {e}")
        return None


def parse_excel_file(filepath):
    """Parse Excel-fil fra Nielsen"""
    
    try:
        # Prøv å importere openpyxl
        import openpyxl
    except ImportError:
        print("❌ openpyxl ikke installert. Prøver å installere...")
        os.system("pip3 install openpyxl -q")
        try:
            import openpyxl
        except ImportError:
            print("❌ Kunne ikke installere openpyxl. Konverter filen til CSV manuelt.")
            return None
    
    try:
        workbook = openpyxl.load_workbook(filepath)
        sheet = workbook.active
        
        data = {
            "stations": [],
            "date_range": None,
            "source": "nielsen_excel_import"
        }
        
        # Finn header-rad og NRJ-data
        headers = None
        nrj_row = None
        
        for row in sheet.iter_rows(values_only=True):
            # Sjekk om dette er header
            if any('station' in str(cell).lower() or 'kanal' in str(cell).lower() for cell in row if cell):
                headers = row
                continue
            
            # Se etter NRJ
            for cell in row:
                if cell and 'nrj' in str(cell).lower():
                    nrj_row = row
                    break
            
            if nrj_row:
                break
        
        if nrj_row and headers:
            station_data = {"name": "NRJ", "source": "nielsen_excel"}
            
            for header, value in zip(headers, nrj_row):
                if not header or not value:
                    continue
                
                header_lower = str(header).lower()
                
                if any(x in header_lower for x in ['weekly', 'ukentlig', 'reach']):
                    try:
                        clean_value = str(value).replace(' ', '').replace(',', '')
                        station_data["weekly_reach"] = int(clean_value)
                    except:
                        station_data["weekly_reach"] = value
                
                elif any(x in header_lower for x in ['daily', 'daglig']):
                    try:
                        clean_value = str(value).replace(' ', '').replace(',', '')
                        station_data["daily_reach"] = int(clean_value)
                    except:
                        station_data["daily_reach"] = value
                
                elif any(x in header_lower for x in ['share', 'andel', 'market']):
                    try:
                        clean_value = str(value).replace('%', '').replace(',', '.')
                        station_data["market_share"] = float(clean_value)
                    except:
                        station_data["market_share"] = value
            
            data["stations"].append(station_data)
        
        return data
        
    except Exception as e:
        print(f"❌ Feil ved parsing av Excel: {e}")
        return None


def insert_to_supabase(data):
    """Insert parsed data til Supabase"""
    
    if not data or not data.get("stations"):
        print("❌ Ingen data å inserte")
        return False
    
    nrj = data["stations"][0]
    
    # Bygg title og description
    title = f"📻 Nielsen Radio Tall - NRJ {nrj.get('weekly_reach', 'N/A')} lyttere"
    
    description = f"""
    Ukentlig rekkevidde: {nrj.get('weekly_reach', 'N/A')} lyttere
    Daglig rekkevidde: {nrj.get('daily_reach', 'N/A')} lyttere
    Markedsandel: {nrj.get('market_share', 'N/A')}%
    Kilde: Nielsen iPort (importert fra fil)
    """
    
    notes = f"""📊 NIELSEN RADIO DATA - IMPORTERT FRA FIL

🎧 NRJ TALL:
• Ukentlig rekkevidde: {nrj.get('weekly_reach', 'N/A')} lyttere
• Daglig rekkevidde: {nrj.get('daily_reach', 'N/A')} lyttere
• Markedsandel: {nrj.get('market_share', 'N/A')}%
• Gjennomsnittlig lyttetid: {nrj.get('avg_listening_time', 'N/A')}

📁 IMPORT INFO:
• Kilde: {nrj.get('source', 'ukjent')}
• Importdato: {datetime.now().strftime('%Y-%m-%d %H:%M')}
• Datafil: {data.get('filename', 'ukjent')}

⚠️ VIKTIG:
Disse tallene er importert fra en manuelt nedlastet fil fra Nielsen iPort.
For automatisert import, kreves API-tilgang eller direkte database-integrasjon.
"""
    
    payload = {
        "title": title,
        "description": description,
        "notes": notes,
        "category": "TALK",
        "show_date": datetime.now().strftime("%Y-%m-%d"),
        "tenant_id": TENANT_ID,
        "created_by": BAARLI_CLAW_ID,
        "is_pinned": False,
        "order_index": 999
    }
    
    req = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/agenda_items",
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'apikey': SUPABASE_KEY,
            'Authorization': f'Bearer {SUPABASE_KEY}',
            'Content-Type': 'application/json',
            'Prefer': 'return=minimal'
        }
    )
    
    try:
        urllib.request.urlopen(req, timeout=10)
        print("✅ Data insertet til Supabase!")
        return True
    except Exception as e:
        print(f"❌ Feil ved insert: {e}")
        return False


def main():
    print("📻 NIELSEN RADIO DATA IMPORT")
    print("=" * 60)
    print()
    print(f"📁 Søker etter filer i: {DOWNLOAD_DIR}")
    print()
    
    # Finn nedlastet fil
    filepath = find_downloaded_file()
    
    if not filepath:
        print("❌ Ingen fil funnet!")
        print()
        print("INSTRUKSJONER:")
        print("1. Logg inn på https://dashboard-eu-iport.nielsen-iwatch.com/norway_radio_reporting/")
        print("2. Last ned rapport som CSV eller Excel")
        print(f"3. Lagre filen i: {DOWNLOAD_DIR}")
        print("4. Kjør dette skriptet igjen")
        print()
        print(f"For å opprette mappen:")
        print(f"  mkdir -p {DOWNLOAD_DIR}")
        return
    
    print(f"✅ Fant fil: {filepath.name}")
    print()
    
    # Parse fil basert på format
    if filepath.suffix.lower() == '.csv':
        print("📄 Parser CSV-fil...")
        data = parse_csv_file(filepath)
    elif filepath.suffix.lower() in ['.xlsx', '.xls']:
        print("📄 Parser Excel-fil...")
        data = parse_excel_file(filepath)
    else:
        print(f"❌ Ustøttet filformat: {filepath.suffix}")
        return
    
    if not data:
        print("❌ Kunne ikke parse filen")
        return
    
    # Legg til filnavn i data
    data["filename"] = filepath.name
    
    # Vis parsed data
    print()
    print("📊 PARSED DATA:")
    print("-" * 60)
    
    for station in data.get("stations", []):
        print(f"Stasjon: {station.get('name')}")
        print(f"  Ukentlig rekkevidde: {station.get('weekly_reach', 'N/A')}")
        print(f"  Daglig rekkevidde: {station.get('daily_reach', 'N/A')}")
        print(f"  Markedsandel: {station.get('market_share', 'N/A')}%")
    
    print()
    
    # Insert til Supabase
    print("💾 LAGRER TIL SUPABASE...")
    if insert_to_supabase(data):
        print()
        print("=" * 60)
        print("✅ IMPORT FULLFØRT!")
        print("=" * 60)
        print()
        print(f"📁 Originalfil: {filepath}")
        print("📊 Data lagret i Supabase (category=TALK)")
    else:
        print()
        print("⚠️  Kunne ikke lagre til Supabase")
        print(f"📁 Originalfil beholdt: {filepath}")


if __name__ == "__main__":
    main()
