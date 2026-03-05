#!/usr/bin/env python3
"""
Segment Timer for Radio
Beregner optimal segment-lengde basert på innhold og kontekst
"""

import argparse
import sys
from datetime import datetime


# Innholds-typer og deres optimale lengder
CONTENT_TYPES = {
    "interview": {
        "base_duration": 8,
        "factors": {
            "celebrity": -2,  # Kjendiser trenger mindre tid
            "expert": 2,      # Eksperter trenger mer tid
            "politician": 3,  # Politikere trenger mer tid
            "musician": 0,    # Musikk-intervju = standard
            "author": 2,      # Forfattere trenger tid til å forklare
        },
        "description": "Intervju med gjest"
    },
    "phone_in": {
        "base_duration": 6,
        "factors": {
            "advice": 2,      # Rådgivning tar tid
            "opinion": 0,     # Meningsutveksling = standard
            "story": 3,       # Historier trenger tid
            "game": -1,       # Spill går raskere
        },
        "description": "Telefon-inn fra lyttere"
    },
    "game_quiz": {
        "base_duration": 5,
        "factors": {
            "trivia": 0,      # Quiz = standard
            "physical": 3,    # Fysiske utfordringer tar tid
            "mental": 1,      # Mentale utfordringer
            "team": 2,        # Lag-aktiviteter
        },
        "description": "Spill eller quiz"
    },
    "news_feature": {
        "base_duration": 4,
        "factors": {
            "breaking": -1,   # Breaking news går raskt
            "investigative": 4, # Undersøkende tar tid
            "human_interest": 2, # Menneskelige historier
            "politics": 2,    # Politikk
        },
        "description": "Nyheter eller feature"
    },
    "prank": {
        "base_duration": 6,
        "factors": {
            "phone": 0,       # Telefon-prank = standard
            "in_person": 3,   # Personlig prank tar tid
            "reveal": 1,      # Avsløring
        },
        "description": "Prank eller practical joke"
    },
    "discussion": {
        "base_duration": 7,
        "factors": {
            "panel": 2,       # Panel-diskusjon
            "two_person": 0,  # To personer = standard
            "debate": 3,      # Debatt
        },
        "description": "Diskusjon eller debatt"
    },
    "storytelling": {
        "base_duration": 10,
        "factors": {
            "personal": 0,    # Personlig historie = standard
            "investigative": 5, # Undersøkende
            "comedic": -2,    # Komiske historier går raskere
        },
        "description": "Fortelling eller historie"
    },
    "music_feature": {
        "base_duration": 12,
        "factors": {
            "live_performance": 5, # Live musikk
            "interview_plus_music": 0, # Standard
            "countdown": -2,  # Countdown går raskere
        },
        "description": "Musikk-feature"
    }
}

# Oppmerksomhets-nivåer
ATTENTION_LEVELS = {
    "low": {
        "multiplier": 0.7,
        "description": "Bakgrunnslytting, lavt fokus"
    },
    "medium": {
        "multiplier": 1.0,
        "description": "Normal lytting, moderat fokus"
    },
    "high": {
        "multiplier": 1.3,
        "description": "Intens lytting, høyt fokus"
    }
}

# Tids-på-dagen faktorer
TIME_OF_DAY = {
    "morning": {
        "multiplier": 0.9,
        "description": "Morgen (06:00-10:00) - kort oppmerksomhet"
    },
    "midday": {
        "multiplier": 1.0,
        "description": "Midt på dagen (10:00-14:00) - normal"
    },
    "afternoon": {
        "multiplier": 1.1,
        "description": "Ettermiddag (14:00-18:00) - økende fokus"
    },
    "evening": {
        "multiplier": 1.2,
        "description": "Kveld (18:00-22:00) - høyt fokus"
    },
    "night": {
        "multiplier": 1.3,
        "description": "Natt (22:00-06:00) - intenst fokus"
    }
}


def calculate_segment_time(content_type, factor=None, attention="medium", time_of_day="midday"):
    """Beregner optimal segment-tid"""
    
    content = CONTENT_TYPES[content_type]
    base = content["base_duration"]
    
    # Legg til faktor hvis spesifisert
    factor_adjustment = 0
    if factor and factor in content["factors"]:
        factor_adjustment = content["factors"][factor]
    
    # Beregn justert tid
    adjusted = base + factor_adjustment
    
    # Multipliser med oppmerksomhet
    attention_mult = ATTENTION_LEVELS[attention]["multiplier"]
    
    # Multipliser med tids-på-dagen
    time_mult = TIME_OF_DAY[time_of_day]["multiplier"]
    
    # Final calculation
    final_time = adjusted * attention_mult * time_mult
    
    # Rund av til nærmeste halvtime
    final_time = round(final_time * 2) / 2
    
    # Min/max grenser
    final_time = max(3, min(final_time, 15))
    
    return {
        "base": base,
        "factor_adjustment": factor_adjustment,
        "attention_multiplier": attention_mult,
        "time_multiplier": time_mult,
        "final": final_time,
        "content_description": content["description"],
        "attention_description": ATTENTION_LEVELS[attention]["description"],
        "time_description": TIME_OF_DAY[time_of_day]["description"]
    }


def generate_timing_report(content_type, factor, attention, time_of_day):
    """Genererer en detaljert timing-rapport"""
    
    result = calculate_segment_time(content_type, factor, attention, time_of_day)
    
    report = f"""
╔══════════════════════════════════════════════════════════════════╗
║  ⏱️  SEGMENT TIMER - OPTIMAL TIDSBEREGNING                       ║
╚══════════════════════════════════════════════════════════════════╝

📋 INNHOLDSTYPE:
   {result['content_description']}
   Basertid: {result['base']} minutter

"""
    
    if factor:
        factor_name = factor.replace("_", " ").title()
        report += f"""🎯 FAKTOR:
   Type: {factor_name}
   Justering: {'+' if result['factor_adjustment'] > 0 else ''}{result['factor_adjustment']} minutter

"""
    
    report += f"""🧠 OPPMERKSOMHETSNIVÅ:
   {result['attention_description']}
   Multiplikator: {result['attention_multiplier']}x

🕐 TID PÅ DAGEN:
   {result['time_description']}
   Multiplikator: {result['time_multiplier']}x

{'='*70}

📊 BEREGNING:
   Basistid:           {result['base']:.1f} min
   Faktor-justering:   {result['factor_adjustment']:+.1f} min
   Subtotal:           {result['base'] + result['factor_adjustment']:.1f} min
   × Oppmerksomhet:    {result['attention_multiplier']}x
   × Tid på dagen:     {result['time_multiplier']}x
   {'='*50}
   🎯 ANBEFALT TID:    {result['final']:.1f} MINUTTER
{'='*70}

📋 STRUKTUR-FORSLAG ({result['final']:.0f} minutter):
"""
    
    # Generer struktur basert på total tid
    total_minutes = result['final']
    
    if total_minutes <= 5:
        report += """
   0:00-0:15  │ Hook (15 sek)          │ Få oppmerksomhet
   0:15-0:45  │ Setup (30 sek)         │ Etabler kontekst
   0:45-3:45  │ Execution (3 min)      │ Hovedinnhold
   3:45-4:30  │ Payoff (45 sek)        │ Konklusjon
   4:30-5:00  │ Reset (30 sek)         │ Tease neste
"""
    elif total_minutes <= 8:
        report += """
   0:00-0:20  │ Hook (20 sek)          │ Få oppmerksomhet
   0:20-1:20  │ Setup (1 min)          │ Etabler kontekst
   1:20-5:20  │ Execution (4 min)      │ Hovedinnhold
   5:20-6:20  │ Development (1 min)    │ Bygg opp til payoff
   6:20-7:20  │ Payoff (1 min)         │ Konklusjon/belønning
   7:20-8:00  │ Reset (40 sek)         │ Tease neste
"""
    else:
        report += """
   0:00-0:30  │ Hook (30 sek)          │ Få oppmerksomhet
   0:30-2:00  │ Setup (1.5 min)        │ Etabler kontekst
   2:00-3:30  │ Part 1 (1.5 min)       │ Første del av innhold
   3:30-4:00  │ Break/Tease (30 sek)   │ Kort pause
   4:00-7:00  │ Part 2 (3 min)         │ Hovedinnhold
   7:00-8:30  │ Development (1.5 min)  │ Bygg opp til payoff
   8:30-10:00 │ Payoff (1.5 min)       │ Konklusjon/belønning
   10:00-11:00│ Reset (1 min)          │ Tease neste
"""
    
    report += f"""

💡 PRODUKSJONSTIPS:
   • Øv på timing med stoppeklokke
   • Ha en "time keeper" i studio
   • Forbered en "early out" versjon (20% kortere)
   • Marker "must-make" punkter i manus
   • Bruk musikk til å time overganger

⚠️  ADVARSLER:
   • Aldri gå over 15 minutter uten reset
   • Hvis du er usikker: kjør kortere
   • Lyttere "tuner ut" etter 8 min uten variasjon
   • Ha alltid en plan B hvis segmentet dør

📊 STATISTIKK:
   • Gjennomsnittlig lytter-oppmerksomhet: 8-10 min
   • PPM-måling viser: reset hver 8. min = +23% retention
   • Morgenlyttere: 20% kortere oppmerksomhetsspenn
   • Kveldslyttere: 30% lengre oppmerksomhetsspenn

Beregnet: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    return report


def main():
    parser = argparse.ArgumentParser(
        description="Beregn optimal segment-tid for radio"
    )
    parser.add_argument(
        "--content-type", "-c",
        choices=list(CONTENT_TYPES.keys()),
        required=True,
        help="Type innhold"
    )
    parser.add_argument(
        "--factor", "-f",
        help="Spesifikk faktor (varierer etter innholdstype)"
    )
    parser.add_argument(
        "--attention", "-a",
        choices=["low", "medium", "high"],
        default="medium",
        help="Oppmerksomhetsnivå (default: medium)"
    )
    parser.add_argument(
        "--time-of-day", "-t",
        choices=["morning", "midday", "afternoon", "evening", "night"],
        default="midday",
        help="Tid på dagen (default: midday)"
    )
    parser.add_argument(
        "--output", "-o",
        help="Lagre til fil"
    )
    
    args = parser.parse_args()
    
    # Valider faktor hvis spesifisert
    if args.factor and args.factor not in CONTENT_TYPES[args.content_type]["factors"]:
        valid_factors = list(CONTENT_TYPES[args.content_type]["factors"].keys())
        print(f"Feil: Ugyldig faktor '{args.factor}'")
        print(f"Gyldige faktorer for {args.content_type}: {', '.join(valid_factors)}")
        return 1
    
    result = generate_timing_report(
        args.content_type,
        args.factor,
        args.attention,
        args.time_of_day
    )
    
    print(result)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"\n💾 Lagret til: {args.output}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
