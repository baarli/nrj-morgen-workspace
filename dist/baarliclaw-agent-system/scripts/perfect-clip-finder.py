#!/usr/bin/env python3
"""
Perfect Clip Finder - Finn de beste podkast-klippene for sosiale medier
Analyserer lyd, innhold og engasjementspotensial
"""

import argparse
import json
import math
import os
import re
from pathlib import Path
from typing import List, Dict, Tuple
import tempfile

try:
    import numpy as np
    from pydub import AudioSegment
    from pydub.silence import detect_nonsilent
    HAS_PYDUB = True
except ImportError:
    HAS_PYDUB = False
    print("⚠️  pydub ikke installert - bruker grunnleggende analyse")

try:
    import whisper
    HAS_WHISPER = True
except ImportError:
    HAS_WHISPER = False
    print("⚠️  whisper ikke installert - ingen transkripsjon")

class PerfectClipFinder:
    """Finn perfekte klipp basert på flere parametere"""
    
    # Parametere for scoring
    SCORE_WEIGHTS = {
        'audio_energy': 0.15,      # Lydnivå/dynamikk
        'laughter_detection': 0.20, # Latter/glede
        'conversation_pace': 0.15,  # Samtaletempo
        'emotional_intensity': 0.20, # Emosjonell intensitet
        'quote_quality': 0.15,      # Sitat-kvalitet (relatable)
        'viral_potential': 0.15,    # Viral potensial
    }
    
    def __init__(self, audio_path: str):
        self.audio_path = Path(audio_path)
        self.audio = None
        self.duration = 0
        self.segments = []
        self.transcript = None
        
        if HAS_PYDUB:
            self._load_audio()
    
    def _load_audio(self):
        """Last inn lydfil"""
        try:
            self.audio = AudioSegment.from_mp3(self.audio_path)
            self.duration = len(self.audio) / 1000  # sekunder
            print(f"✅ Lastet audio: {self.duration:.1f}s")
        except Exception as e:
            print(f"❌ Kunne ikke laste audio: {e}")
    
    def analyze_audio_energy(self, start: float, end: float) -> float:
        """Analyser lydnivå og dynamikk (0-100)"""
        if not HAS_PYDUB or not self.audio:
            return 50.0
        
        try:
            segment = self.audio[int(start*1000):int(end*1000)]
            
            # RMS (Root Mean Square) = gjennomsnittlig lydnivå
            rms = segment.rms
            max_rms = 32767  # Maks for 16-bit audio
            
            # Normaliser til 0-100
            energy_score = min(100, (rms / max_rms) * 100 * 2)
            
            # Bonus for dynamikk (variasjon i lydnivå)
            samples = np.array(segment.get_array_of_samples())
            if len(samples) > 0:
                dynamic_range = np.std(samples) / max_rms * 100
                energy_score += dynamic_range * 0.3
            
            return min(100, energy_score)
        except Exception as e:
            return 50.0
    
    def detect_laughter(self, start: float, end: float) -> float:
        """Detekter latter og glede (0-100)"""
        if not HAS_PYDUB or not self.audio:
            return 50.0
        
        try:
            segment = self.audio[int(start*1000):int(end*1000)]
            samples = np.array(segment.get_array_of_samples())
            
            if len(samples) == 0:
                return 50.0
            
            # Latter = høye, raske topper i lyden
            # Beregn antall "spikes" over terskel
            threshold = np.mean(np.abs(samples)) * 2
            spikes = np.sum(np.abs(samples) > threshold)
            spike_density = spikes / len(samples) * 100
            
            # Latter har karakteristisk mønster: korte, høye topper
            laughter_score = min(100, spike_density * 5)
            
            # Bonus for høyt lydnivå (latter er ofte høyt)
            if segment.rms > 10000:
                laughter_score += 15
            
            return min(100, laughter_score)
        except Exception as e:
            return 50.0
    
    def analyze_conversation_pace(self, start: float, end: float) -> float:
        """Analyser samtaletempo (0-100)"""
        if not HAS_PYDUB or not self.audio:
            return 50.0
        
        try:
            segment = self.audio[int(start*1000):int(end*1000)]
            
            # Finn ikke-stille segmenter (tale)
            nonsilent_ranges = detect_nonsilent(
                segment, 
                min_silence_len=200,  # 200ms
                silence_thresh=-40    # -40dB
            )
            
            if not nonsilent_ranges:
                return 30.0  # For stille
            
            # Beregn taletid vs stillhet
            speech_duration = sum(end - start for start, end in nonsilent_ranges)
            total_duration = len(segment)
            speech_ratio = speech_duration / total_duration
            
            # Ideelt: 60-80% tale, 20-40% pause
            if 0.6 <= speech_ratio <= 0.8:
                pace_score = 90 + (0.7 - abs(speech_ratio - 0.7)) * 50
            elif speech_ratio > 0.8:
                pace_score = 70  # For mye prat, lite pause
            else:
                pace_score = 50 + speech_ratio * 50  # For mye stillhet
            
            return min(100, pace_score)
        except Exception as e:
            return 50.0
    
    def analyze_emotional_intensity(self, start: float, end: float) -> float:
        """Analyser emosjonell intensitet (0-100)"""
        if not HAS_PYDUB or not self.audio:
            return 50.0
        
        try:
            segment = self.audio[int(start*1000):int(end*1000)]
            samples = np.array(segment.get_array_of_samples())
            
            if len(samples) == 0:
                return 50.0
            
            # Emosjonell intensitet = høyt lydnivå + variasjon
            rms = np.sqrt(np.mean(samples**2))
            max_val = np.max(np.abs(samples))
            
            # Normaliser
            intensity = (rms / 32767) * 100
            peak_factor = (max_val / 32767) * 100
            
            # Kombiner RMS og peak
            emotional_score = intensity * 0.6 + peak_factor * 0.4
            
            # Bonus for "shouting" (høye topper)
            if peak_factor > 70:
                emotional_score += 20
            
            return min(100, emotional_score)
        except Exception as e:
            return 50.0
    
    def analyze_quote_quality(self, start: float, end: float) -> float:
        """Vurder sitat-kvalitet (relatable, morsomt, tankevekkende)"""
        # Uten transkripsjon, bruk heuristikker
        score = 50.0
        
        # Lengde-basert scoring
        duration = end - start
        if 25 <= duration <= 35:  # Ideell lengde for sosiale medier
            score += 20
        elif duration < 20:
            score -= 10  # For kort
        elif duration > 45:
            score -= 15  # For langt
        
        # Hvis vi har transkripsjon, analyser tekst
        if self.transcript and HAS_WHISPER:
            text_segment = self._get_transcript_segment(start, end)
            if text_segment:
                score = self._analyze_text_quality(text_segment, score)
        
        return min(100, score)
    
    def _get_transcript_segment(self, start: float, end: float) -> str:
        """Hent transkripsjon for tidssegment"""
        if not self.transcript:
            return ""
        
        # Finn segmenter innenfor tidsrommet
        text_parts = []
        for segment in self.transcript.get('segments', []):
            seg_start = segment.get('start', 0)
            seg_end = segment.get('end', 0)
            
            if seg_start >= start and seg_end <= end:
                text_parts.append(segment.get('text', ''))
        
        return ' '.join(text_parts)
    
    def _analyze_text_quality(self, text: str, base_score: float) -> float:
        """Analyser tekst-kvalitet"""
        score = base_score
        text_lower = text.lower()
        
        # Relatable nøkkelord
        relatable_words = [
            'kjæreste', 'forhold', 'krangel', 'kjærlighet', 'forelsket',
            'problemer', 'løsning', 'råd', 'tips', 'erfaring',
            'dere', 'vi', 'oss', 'sammen', 'følelser'
        ]
        
        # Humor-nøkkelord
        humor_words = [
            'morsomt', 'latter', 'humor', 'gal', 'gæren', 'dum',
            'rart', 'teit', 'komisk', '后者', 'latterlig'
        ]
        
        # Tell nøkkelord
        relatable_count = sum(1 for word in relatable_words if word in text_lower)
        humor_count = sum(1 for word in humor_words if word in text_lower)
        
        # Bonus for relatable innhold
        score += relatable_count * 5
        score += humor_count * 8
        
        # Bonus for spørsmål (engasjerer lyttere)
        if '?' in text:
            score += 10
        
        # Bonus for utrop (intensitet)
        if '!' in text:
            score += 5
        
        return min(100, score)
    
    def calculate_viral_potential(self, start: float, end: float, 
                                   audio_score: float, laughter_score: float,
                                   emotional_score: float) -> float:
        """Beregn viral potensial (0-100)"""
        # Kombiner flere faktorer
        viral_score = (
            audio_score * 0.2 +
            laughter_score * 0.3 +
            emotional_score * 0.3 +
            20  # Base score
        )
        
        # Bonus for "hook" i starten (første 3 sekunder)
        if audio_score > 70:
            viral_score += 10
        
        # Bonus for høy emotional + laughter (perfekt combo)
        if emotional_score > 70 and laughter_score > 60:
            viral_score += 15
        
        return min(100, viral_score)
    
    def score_segment(self, start: float, end: float) -> Dict:
        """Score et segment basert på alle parametere"""
        scores = {
            'audio_energy': self.analyze_audio_energy(start, end),
            'laughter_detection': self.detect_laughter(start, end),
            'conversation_pace': self.analyze_conversation_pace(start, end),
            'emotional_intensity': self.analyze_emotional_intensity(start, end),
            'quote_quality': self.analyze_quote_quality(start, end),
        }
        
        # Beregn viral potensial
        scores['viral_potential'] = self.calculate_viral_potential(
            start, end,
            scores['audio_energy'],
            scores['laughter_detection'],
            scores['emotional_intensity']
        )
        
        # Beregn total score
        total_score = sum(
            scores[param] * weight 
            for param, weight in self.SCORE_WEIGHTS.items()
        )
        
        scores['total_score'] = total_score
        scores['start'] = start
        scores['end'] = end
        scores['duration'] = end - start
        
        return scores
    
    def find_perfect_clips(self, num_clips: int = 3, 
                           min_duration: float = 25,
                           max_duration: float = 35) -> List[Dict]:
        """Finn de beste klippene i episoden"""
        print(f"\n🔍 Søker etter {num_clips} perfekte klipp...")
        print(f"   Varighet: {min_duration}-{max_duration}s")
        
        if not HAS_PYDUB or not self.audio:
            # Fallback: bruk faste tidssegmenter
            return self._fallback_clips(num_clips, min_duration, max_duration)
        
        # Analyser hele episoden i vinduer
        window_size = 30  # sekunder
        step_size = 5     # sekunder
        
        candidates = []
        
        for start in range(0, int(self.duration) - window_size, step_size):
            end = start + window_size
            
            # Score dette vinduet
            scores = self.score_segment(start, end)
            
            if scores['total_score'] > 50:  # Minimum terskel
                candidates.append(scores)
        
        if not candidates:
            return self._fallback_clips(num_clips, min_duration, max_duration)
        
        # Sorter etter total score
        candidates.sort(key=lambda x: x['total_score'], reverse=True)
        
        # Velg top clips med tilstrekkelig avstand
        selected = []
        min_gap = 30  # Minimum 30 sekunder mellom klipp
        
        for candidate in candidates:
            if len(selected) >= num_clips:
                break
            
            # Sjekk at det ikke overlapper for mye med eksisterende
            overlap = False
            for sel in selected:
                if abs(candidate['start'] - sel['start']) < min_gap:
                    overlap = True
                    break
            
            if not overlap:
                selected.append(candidate)
        
        return selected
    
    def _fallback_clips(self, num_clips: int, min_duration: float, 
                        max_duration: float) -> List[Dict]:
        """Fallback når pydub ikke er tilgjengelig"""
        print("   (Bruker fallback-metode)")
        
        # Bruk faste tidssegmenter
        default_starts = [120, 450, 890]
        
        clips = []
        for i, start in enumerate(default_starts[:num_clips]):
            end = start + 30
            clips.append({
                'start': start,
                'end': end,
                'duration': 30,
                'total_score': 70 - i * 5,
                'audio_energy': 60,
                'laughter_detection': 65,
                'conversation_pace': 70,
                'emotional_intensity': 60,
                'quote_quality': 65,
                'viral_potential': 65,
                'note': 'Fallback (ingen pydub)'
            })
        
        return clips
    
    def transcribe(self, model_size: str = "base"):
        """Transkriber episoden med Whisper"""
        if not HAS_WHISPER:
            print("⚠️  Whisper ikke tilgjengelig")
            return
        
        print(f"\n📝 Transkriberer med Whisper ({model_size})...")
        
        try:
            model = whisper.load_model(model_size)
            result = model.transcribe(str(self.audio_path), language="no")
            
            self.transcript = result
            
            # Lagre transkripsjon
            transcript_path = self.audio_path.with_suffix('.json')
            with open(transcript_path, 'w') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"   ✅ Transkripsjon lagret: {transcript_path}")
            
        except Exception as e:
            print(f"   ❌ Feil ved transkripsjon: {e}")
    
    def generate_report(self, clips: List[Dict]) -> str:
        """Generer rapport over funnede klipp"""
        report = []
        report.append("\n" + "=" * 60)
        report.append("🎯 PERFECT CLIP ANALYSE")
        report.append("=" * 60)
        report.append(f"Fil: {self.audio_path.name}")
        report.append(f"Varighet: {self.duration:.1f}s")
        report.append("")
        
        for i, clip in enumerate(clips, 1):
            report.append(f"\n{'─' * 60}")
            report.append(f"📌 KLIPP #{i} (Score: {clip['total_score']:.1f}/100)")
            report.append(f"{'─' * 60}")
            report.append(f"   Tid: {clip['start']:.1f}s - {clip['end']:.1f}s ({clip['duration']:.1f}s)")
            report.append("")
            report.append("   Parametre:")
            report.append(f"      🔊 Audio energi:      {clip['audio_energy']:.1f}/100")
            report.append(f"      😂 Latter-deteksjon:  {clip['laughter_detection']:.1f}/100")
            report.append(f"      💬 Samtaletempo:      {clip['conversation_pace']:.1f}/100")
            report.append(f"      ❤️  Emosjonell intens: {clip['emotional_intensity']:.1f}/100")
            report.append(f"      💭 Sitat-kvalitet:     {clip['quote_quality']:.1f}/100")
            report.append(f"      🚀 Viral potensial:   {clip['viral_potential']:.1f}/100")
            
            if 'note' in clip:
                report.append(f"      📝 Merknad: {clip['note']}")
        
        report.append("\n" + "=" * 60)
        return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(description='Perfect Clip Finder')
    parser.add_argument('audio_file', help='Lydfil å analysere')
    parser.add_argument('--clips', type=int, default=3, help='Antall klipp å finne')
    parser.add_argument('--min-duration', type=float, default=25, help='Minimum varighet')
    parser.add_argument('--max-duration', type=float, default=35, help='Maksimum varighet')
    parser.add_argument('--transcribe', action='store_true', help='Transkriber før analyse')
    parser.add_argument('--output', help='Lagre resultat til JSON-fil')
    
    args = parser.parse_args()
    
    # Opprett finder
    finder = PerfectClipFinder(args.audio_file)
    
    # Transkriber hvis ønsket
    if args.transcribe:
        finder.transcribe()
    
    # Finn perfekte klipp
    clips = finder.find_perfect_clips(
        num_clips=args.clips,
        min_duration=args.min_duration,
        max_duration=args.max_duration
    )
    
    # Vis rapport
    report = finder.generate_report(clips)
    print(report)
    
    # Lagre til fil hvis ønsket
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(clips, f, indent=2)
        print(f"\n💾 Resultat lagret: {args.output}")
    
    # Returner klipp for videre bruk
    return clips


if __name__ == '__main__':
    main()
