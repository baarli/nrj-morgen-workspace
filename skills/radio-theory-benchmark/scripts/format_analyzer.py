#!/usr/bin/env python3
"""
Format Analyzer for Radio Shows
Analyserer show-formater og foreslår forbedringer
"""

import argparse
import sys
from datetime import datetime


def analyze_show_format(show_name, segments=4, duration_hours=4):
    """Analyserer et show-format og gir anbefalinger"""
    
    segment_minutes = (duration_hours * 60) // segments
    
    analysis = f"""
╔══════════════════════════════════════════════════════════════════╗
║  📊 FORMAT ANALYSIS: {show_name:<40} ║
╚══════════════════════════════════════════════════════════════════╝

📻 SHOW-INFORMASJON:
   Navn: {show_name}
   Varighet: {duration_hours} timer
   Antall segmenter: {segments}
   Gjennomsnittlig segment: {segment_minutes} minutter

📈 STRUKTUR-ANALYSE:
"""
    
    # Vurder segment-lengde
    if segment_minutes < 5:
        analysis += """
   ⚠️  ADVARSEL: Segmentene er svært korte!
       → Vurder å slå sammen segmenter for bedre flyt
       → Korte segmenter gir fragmentert lytter-opplevelse
"""
    elif segment_minutes < 10:
        analysis += """
   ✅ GODT: Segmentene er korte og konsise
       → Passer for nyheter og quick hits
       → Husk "tease-deliver-reset" pattern
"""
    elif segment_minutes <= 15:
        analysis += """
   ✅ OPTIMAL: Segmentene har god lengde
       → 10-15 min er sweet spot for engasjement
       → Gir nok tid til å utvikle innhold
"""
    else:
        analysis += """
   ⚠️  ADVARSEL: Segmentene er lange
       → Vurder å dele opp i sub-segmenter
       → Lange segmenter kan føre til "tuning out"
"""
    
    # Time-plan forslag
    analysis += f"""

🕐 FORESLÅTT TIME-PLAN ({duration_hours} timer):
"""
    
    for hour in range(duration_hours):
        start_time = f"{6 + hour:02d}:00" if show_name.lower().find("morgen") >= 0 else f"{14 + hour:02d}:00"
        
        if hour == 0:
            energy = "Hard start, høy energi"
        elif hour == duration_hours // 2:
            energy = "Prime time, maks energi"
        elif hour == duration_hours - 1:
            energy = "Wind down, lavere energi"
        else:
            energy = "Bygger momentum"
        
        analysis += f"""
   {start_time} - Time {hour + 1}:
       Energi: {energy}
       Segmenter: {segments // duration_hours} per time
       Fokus: {"Nyheter + trafikk" if hour == 0 else "Underholdning" if hour == duration_hours // 2 else "Interaksjon"}
"""
    
    # Benchmark-forslag
    analysis += """

🎯 BENCHMARK-FORSLAG:
"""
    
    benchmarks = [
        ("Telefonscam", "Klassisk, alltid populær", "High"),
        ("Mystery Guest", "Bygger nysgjerrighet", "Medium"),
        ("Listener Poll", "Høy interaksjon", "High"),
        ("Truth or Dare", "Personlig, engasjerende", "Medium"),
        ("Rate My...", "Lett å produsere", "Low"),
        ("The Challenge", "Krever forberedelse", "High"),
    ]
    
    for i, (name, desc, effort) in enumerate(benchmarks[:segments], 1):
        analysis += f"""
   {i}. {name}
      Beskrivelse: {desc}
      Produksjonsinnsats: {effort}
      Anbefalt tidspunkt: {"Start av show" if i == 1 else "Midt i show" if i == segments // 2 else "Slutten av show"}
"""
    
    # Forbedringsforslag
    analysis += """

💡 FORBEDRINGSFORSLAG:
"""
    
    suggestions = [
        "Legg til en 'must-listen' moment hvert 15. minutt",
        "Bruk 'tease-deliver-reset' i hvert segment",
        "Ha en fast 'feature' som går hver time (f.eks. 'Trafikk-trivia')",
        "Involver lyttere tidlig - første 30 minutter",
        "Slutt hver time med en 'cliffhanger' til neste",
        "Varier mellom 'talk' og 'action' segmenter",
        "Ha en 'host moment' - personlig historie per time",
        "Bruk 'reset' til å tease kommende gjester/features",
    ]
    
    for i, suggestion in enumerate(suggestions[:segments + 2], 1):
        analysis += f"""
   {i}. {suggestion}
"""
    
    # Energi-kurve
    analysis += f"""

📊 ENERGI-KURVE:
"""
    
    for hour in range(duration_hours):
        percentage = 100 - abs(hour - (duration_hours // 2)) * (50 // (duration_hours // 2 + 1))
        bar = "█" * (percentage // 10) + "░" * (10 - (percentage // 10))
        analysis += f"""
   Time {hour + 1}: {bar} {percentage}%
"""
    
    analysis += f"""

📋 SJEKKLISTE FOR IMPLEMENTERING:
   □ Definer 'hook' for hvert segment
   □ Planlegg 'payoff' for hvert segment
   □ Forbered backup-planer
   □ Test timing med stoppeklokke
   □ Ha system for lytter-interaksjon klar
   □ Forbered 'reset' som teaser neste segment
   □ Øv på overganger mellom segmenter

Analysert: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    return analysis


def compare_formats(show1, show2):
    """Sammenligner to show-formater"""
    
    comparison = f"""
╔══════════════════════════════════════════════════════════════════╗
║  📊 FORMAT COMPARISON                                              ║
╚══════════════════════════════════════════════════════════════════╝

📻 {show1} vs {show2}

{'='*70}

ASPEKT               | {show1[:20]:<20} | {show2[:20]:<20}
{'='*70}
Målgruppe            | [Analyseres]         | [Analyseres]
Tone                 | [Analyseres]         | [Analyseres]
Segment-lengde       | [Analyseres]         | [Analyseres]
Interaksjonsnivå     | [Analyseres]         | [Analyseres]
Musikkandel          | [Analyseres]         | [Analyseres]
Produksjonsverdi     | [Analyseres]         | [Analyseres]

{'='*70}

🎯 ANBEFALINGER:
   • Hent det beste fra begge formater
   • Kombiner {show1.split()[0]}s [styrke] med {show2.split()[0]}s [styrke]
   • Test A/B med lyttere

"""
    
    return comparison


def main():
    parser = argparse.ArgumentParser(
        description="Analyser radio show-formater"
    )
    parser.add_argument(
        "--show", "-s",
        required=True,
        help="Navn på showet som skal analyseres"
    )
    parser.add_argument(
        "--segments", "-seg",
        type=int,
        default=4,
        help="Antall segmenter (default: 4)"
    )
    parser.add_argument(
        "--duration", "-d",
        type=int,
        default=4,
        help="Varighet i timer (default: 4)"
    )
    parser.add_argument(
        "--compare", "-c",
        help="Sammenlign med et annet show"
    )
    parser.add_argument(
        "--output", "-o",
        help="Lagre til fil"
    )
    
    args = parser.parse_args()
    
    if args.compare:
        result = compare_formats(args.show, args.compare)
    else:
        result = analyze_show_format(args.show, args.segments, args.duration)
    
    print(result)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"\n💾 Lagret til: {args.output}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
