#!/usr/bin/env python3
"""
📊 Recency Scoring for Morning Routine
"""
import math
from datetime import datetime

def calculate_recency_score(published_date):
    """Calculate recency score with exponential decay"""
    try:
        pub_date = datetime.fromisoformat(published_date.replace('Z', '+00:00'))
        now = datetime.now(pub_date.tzinfo)
        hours_old = (now - pub_date).total_seconds() / 3600
        score = 100 * math.exp(-hours_old / 24)
        return max(0, score)
    except:
        return 50

def calculate_source_authority(source):
    """Calculate source authority score"""
    authority_scores = {
        'vg.no': 100,
        'tv2.no': 95,
        'dagbladet.no': 90,
        'nrk.no': 95,
        'nettavisen.no': 80,
        'seher.no': 75,
        'dailymail.co.uk': 70,
        'tmz.com': 65,
    }
    return authority_scores.get(source, 50)
