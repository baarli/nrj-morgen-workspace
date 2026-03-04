#!/usr/bin/env python3
"""
Benchmark Generator for Radio Theory
Genererer kreative, innovative segmentideer basert på radioteori
"""

import random
import argparse
import sys
from datetime import datetime

# Psykologiske triggere
TRIGGERS = {
    "fomo": {
        "name": "Fear Of Missing Out",
        "description": "Angsten for å gå glipp av noe",
        "hooks": [
            "Du vil ikke tro hva som skjedde...",
            "Bare de som lytter nå får høre dette...",
            "Dette har aldri skjedd før...",
            "Om 5 minutter skjer noe historisk..."
        ]
    },
    "schadenfreude": {
        "name": "Schadenfreude",
        "description": "Glede over andres uhell",
        "hooks": [
            "Vi ringte Marte og fortalte at hun hadde vunnet...",
            "Hør hva som skjedde da vi lurte sjefen...",
            "Denne walk of shame-historien er helt vill...",
            "Du vil grine av latter når du hører dette..."
        ]
    },
    "curiosity": {
        "name": "Nysgjerrighet",
        "description": "Behovet for å fylle kunnskapshull",
        "hooks": [
            "Det er én ting jeg aldri har fortalt...",
            "Hva skjer når du blander X og Y?",
            "Jeg fant noe rart i kjelleren...",
            "Kan du gjette hva som er i esken?"
        ]
    },
    "belonging": {
        "name": "Fellesskap",
        "description": "Behovet for å tilhøre en gruppe",
        "hooks": [
            "Alle som har kjørt E6 på en mandag vet...",
            "Vi i [by] har alle opplevd dette...",
            "Hvis du er født på 90-tallet vil du kjenne deg igjen...",
            "Bare ekte fans vil forstå denne referansen..."
        ]
    },
    "empathy": {
        "name": "Empati",
        "description": "Evnen til å føle med andre",
        "hooks": [
            "Da jeg mistet jobben min var det den verste dagen...",
            "Jeg gråt da jeg hørte denne historien...",
            "Hun har aldri fortalt dette til noen før...",
            "Dette er historien som fikk hele studio til å gråte..."
        ]
    }
}

# Benchmark-typer
BENCHMARK_TYPES = {
    "content": {
        "formats": [
            "Top 10 List",
            "Mystery Guest",
            "Truth or Dare",
            "Would You Rather",
            "Rate My...",
            "Guess The...",
            "Never Have I Ever",
            "Two Truths and a Lie",
            "The Confession",
            "The Reveal"
        ],
        "moods": ["funny", "emotional", "shocking", "heartwarming", "controversial"]
    },
    "interaction": {
        "formats": [
            "Phone Scam",
            "Text Line",
            "Poll Battle",
            "Shoutout",
            "Request Line",
            "Challenge Accepted",
            "The Bet",
            "Phone-a-Friend",
            "Listener Takeover",
            "Crowd Control"
        ],
        "moods": ["energetic", "competitive", "funny", "surprising", "engaging"]
    },
    "personality": {
        "formats": [
            "The Argument",
            "The Prank",
            "The Challenge",
            "The Experiment",
            "The Bet",
            "The Blind Test",
            "The Swap",
            "The Confession",
            "The Makeover",
            "The Investigation"
        ],
        "moods": ["dramatic", "funny", "risky", "personal", "adventurous"]
    }
}

# Twist-ideer
TWISTS = [
    "...men med en motsatt vri",
    "...men lytterne styrer utfallet",
    "...men alt er live og uplanlagt",
    "...men vi vet ikke hvem som deltar",
    "...men det er en hemmelig gjest involvert",
    "...men det skjer på en uventet lokasjon",
    "...men det er en tidsfrist",
    "...men det er en plot twist halvveis",
    "...men det er en straff for taperen",
    "...men vinneren bestemmer neste runde"
]

# Segment-struktur maler
STRUCTURES = {
    "short": {
        "duration": "3-5 minutter",
        "breakdown": {
            "hook": "15-20 sek",
            "setup": "30-45 sek",
            "execution": "2-3 min",
            "payoff": "30-45 sek",
            "reset": "10-15 sek"
        }
    },
    "medium": {
        "duration": "6-8 minutter",
        "breakdown": {
            "hook": "20-30 sek",
            "setup": "1-1.5 min",
            "execution": "4-5 min",
            "payoff": "45-60 sek",
            "reset": "15-20 sek"
        }
    },
    "long": {
        "duration": "10-12 minutter",
        "breakdown": {
            "hook": "30-45 sek",
            "setup": "1.5-2 min",
            "execution": "6-7 min",
            "payoff": "1-1.5 min",
            "reset": "20-30 sek"
        }
    }
}


def generate_benchmark(benchmark_type="content", mood=None, duration="medium", trigger=None):
    """Genererer en ny benchmark-idé"""
    
    # Velg tilfeldig hvis ikke spesifisert
    if not mood:
        mood = random.choice(BENCHMARK_TYPES[benchmark_type]["moods"])
    if not trigger:
        trigger = random.choice(list(TRIGGERS.keys()))
    
    format_name = random.choice(BENCHMARK_TYPES[benchmark_type]["formats"])
    twist = random.choice(TWISTS)
    hook = random.choice(TRIGGERS[trigger]["hooks"])
    structure = STRUCTURES[duration]
    
    # Generer navn
    benchmark_name = f"{format_name}: {mood.title()} Edition"
    
    # Bygg beskrivelse
    description = f"""
╔══════════════════════════════════════════════════════════════════╗
║  📻 NY BENCHMARK: {benchmark_name:<42} ║
╚══════════════════════════════════════════════════════════════════╝

🎯 KONSEPT:
   En {mood} {format_name.lower()}-segment {twist}

🧠 PSYKOLOGISK TRIGGER:
   {TRIGGERS[trigger]["name"]} - {TRIGGERS[trigger]["description"]}

🎣 HOOK (åpning):
   "{hook}"

⏱️  VARIGHET: {structure['duration']}

📋 STRUKTUR:
   • Hook:      {structure['breakdown']['hook']}  - Få oppmerksomhet
   • Setup:     {structure['breakdown']['setup']}  - Etabler kontekst
   • Execution: {structure['breakdown']['execution']}  - Hovedinnhold
   • Payoff:    {structure['breakdown']['payoff']}  - Konklusjon/belønning
   • Reset:     {structure['breakdown']['reset']}  - Tease neste

💡 PRODUKSJONSTIPS:
   1. Øv på hook til den sitter perfekt
   2. Ha en plan B hvis execution går skeis
   3. Forbered 3-4 payoff-alternativer
   4. Reset skal alltid tease neste segment

🎨 VARIASJONER:
   • Versjon A: Standard format
   • Versjon B: Med lytter-interaksjon
   • Versjon C: Med overraskelsesgjest
   • Versjon D: Med tidsbegrensning

📊 SUKSESSKRITERIER:
   ✅ Lyttere ringer/sender inn underveis
   ✅ Folk snakker om det etterpå
   ✅ Kan gjentas med nytt innhold
   ✅ Skaper "FOMO" for de som ikke hørte det

Generert: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    return description


def generate_multiple(count=3, benchmark_type="content"):
    """Genererer flere benchmarks"""
    output = []
    output.append("=" * 70)
    output.append("🎙️  RADIO BENCHMARK GENERATOR")
    output.append("   Kreative segmentideer basert på radioteori")
    output.append("=" * 70)
    output.append("")
    
    for i in range(count):
        output.append(generate_benchmark(
            benchmark_type=benchmark_type,
            mood=None,  # Tilfeldig
            duration=random.choice(["short", "medium", "long"]),
            trigger=None  # Tilfeldig
        ))
        output.append("")
        output.append("-" * 70)
        output.append("")
    
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description="Generer kreative radio/podcast benchmarks"
    )
    parser.add_argument(
        "--type", "-t",
        choices=["content", "interaction", "personality"],
        default="content",
        help="Type benchmark (default: content)"
    )
    parser.add_argument(
        "--mood", "-m",
        choices=["funny", "emotional", "shocking", "heartwarming", 
                 "controversial", "energetic", "competitive", "surprising",
                 "engaging", "dramatic", "risky", "personal", "adventurous"],
        help="Stemning/mood"
    )
    parser.add_argument(
        "--duration", "-d",
        choices=["short", "medium", "long"],
        default="medium",
        help="Segment-lengde (default: medium)"
    )
    parser.add_argument(
        "--trigger", "-tr",
        choices=list(TRIGGERS.keys()),
        help="Psykologisk trigger"
    )
    parser.add_argument(
        "--count", "-c",
        type=int,
        default=1,
        help="Antall benchmarks å generere (default: 1)"
    )
    parser.add_argument(
        "--output", "-o",
        help="Lagre til fil"
    )
    
    args = parser.parse_args()
    
    if args.count > 1:
        result = generate_multiple(args.count, args.type)
    else:
        result = generate_benchmark(
            benchmark_type=args.type,
            mood=args.mood,
            duration=args.duration,
            trigger=args.trigger
        )
    
    print(result)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"\n💾 Lagret til: {args.output}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
