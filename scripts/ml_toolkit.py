#!/usr/bin/env python3
"""
🧠 BAARLICLAW ML TOOLKIT
Maskinlæring og AI-verktøy
"""

import os
import sys
import json
import math
from typing import List, Dict, Optional, Tuple, Any
from collections import defaultdict
from datetime import datetime, timedelta

sys.path.insert(0, '/root/.openclaw/workspace/scripts')
from baarliclaw_toolkit import setup_logging

logger = setup_logging("MLToolkit")

class SimpleClassifier:
    """Simple text classifier using bag-of-words"""
    
    def __init__(self):
        self.classes = defaultdict(lambda: defaultdict(int))
        self.class_counts = defaultdict(int)
        self.vocab = set()
        self.total_docs = 0
    
    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization"""
        # Lowercase and split
        words = text.lower().split()
        # Remove punctuation and short words
        words = [''.join(c for c in w if c.isalnum()) for w in words]
        words = [w for w in words if len(w) > 2]
        return words
    
    def train(self, text: str, label: str):
        """Train on a single document"""
        words = self._tokenize(text)
        
        for word in words:
            self.classes[label][word] += 1
            self.vocab.add(word)
        
        self.class_counts[label] += 1
        self.total_docs += 1
    
    def predict(self, text: str) -> Dict[str, float]:
        """Predict class probabilities"""
        words = self._tokenize(text)
        scores = {}
        
        for label in self.class_counts:
            # Prior probability
            score = math.log(self.class_counts[label] / self.total_docs)
            
            # Word probabilities (with smoothing)
            total_words = sum(self.classes[label].values())
            vocab_size = len(self.vocab)
            
            for word in words:
                count = self.classes[label].get(word, 0)
                # Laplace smoothing
                prob = (count + 1) / (total_words + vocab_size)
                score += math.log(prob)
            
            scores[label] = score
        
        # Convert to probabilities
        max_score = max(scores.values()) if scores else 0
        exp_scores = {k: math.exp(v - max_score) for k, v in scores.items()}
        total = sum(exp_scores.values())
        
        return {k: v/total for k, v in exp_scores.items()}

class RecommendationEngine:
    """Simple recommendation engine"""
    
    def __init__(self):
        self.user_items = defaultdict(set)
        self.item_users = defaultdict(set)
        self.item_features = {}
    
    def add_interaction(self, user_id: str, item_id: str):
        """Record user-item interaction"""
        self.user_items[user_id].add(item_id)
        self.item_users[item_id].add(user_id)
    
    def add_item_features(self, item_id: str, features: Dict[str, Any]):
        """Add features for an item"""
        self.item_features[item_id] = features
    
    def get_similar_users(self, user_id: str, n: int = 5) -> List[Tuple[str, float]]:
        """Find users with similar taste"""
        if user_id not in self.user_items:
            return []
        
        user_items = self.user_items[user_id]
        similarities = []
        
        for other_id, other_items in self.user_items.items():
            if other_id == user_id:
                continue
            
            # Jaccard similarity
            intersection = len(user_items & other_items)
            union = len(user_items | other_items)
            
            if union > 0:
                similarity = intersection / union
                if similarity > 0:
                    similarities.append((other_id, similarity))
        
        return sorted(similarities, key=lambda x: x[1], reverse=True)[:n]
    
    def recommend(self, user_id: str, n: int = 5) -> List[Tuple[str, float]]:
        """Recommend items for a user"""
        if user_id not in self.user_items:
            return []
        
        user_items = self.user_items[user_id]
        scores = defaultdict(float)
        
        # Collaborative filtering
        similar_users = self.get_similar_users(user_id, n=10)
        
        for similar_id, similarity in similar_users:
            for item_id in self.user_items[similar_id]:
                if item_id not in user_items:
                    scores[item_id] += similarity
        
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:n]
    
    def recommend_content_based(self, user_id: str, n: int = 5) -> List[Tuple[str, float]]:
        """Content-based recommendations"""
        if user_id not in self.user_items:
            return []
        
        user_items = self.user_items[user_id]
        
        # Aggregate features from user's items
        user_profile = defaultdict(float)
        for item_id in user_items:
            if item_id in self.item_features:
                for feature, value in self.item_features[item_id].items():
                    if isinstance(value, (int, float)):
                        user_profile[feature] += value
        
        # Normalize
        total = sum(user_profile.values())
        if total > 0:
            user_profile = {k: v/total for k, v in user_profile.items()}
        
        # Score all items
        scores = []
        for item_id, features in self.item_features.items():
            if item_id in user_items:
                continue
            
            score = 0
            for feature, value in features.items():
                if isinstance(value, (int, float)) and feature in user_profile:
                    score += user_profile[feature] * value
            
            scores.append((item_id, score))
        
        return sorted(scores, key=lambda x: x[1], reverse=True)[:n]

class TimeSeriesForecaster:
    """Simple time series forecasting"""
    
    def __init__(self):
        self.data = []
    
    def add_point(self, timestamp: datetime, value: float):
        """Add data point"""
        self.data.append((timestamp, value))
        self.data.sort(key=lambda x: x[0])
    
    def moving_average(self, window: int = 7) -> List[float]:
        """Calculate moving average"""
        if len(self.data) < window:
            return [v for _, v in self.data]
        
        values = [v for _, v in self.data]
        result = []
        
        for i in range(len(values)):
            if i < window - 1:
                result.append(sum(values[:i+1]) / (i+1))
            else:
                result.append(sum(values[i-window+1:i+1]) / window)
        
        return result
    
    def exponential_smoothing(self, alpha: float = 0.3) -> List[float]:
        """Exponential smoothing"""
        if not self.data:
            return []
        
        values = [v for _, v in self.data]
        result = [values[0]]
        
        for i in range(1, len(values)):
            smoothed = alpha * values[i] + (1 - alpha) * result[i-1]
            result.append(smoothed)
        
        return result
    
    def forecast(self, steps: int = 1) -> List[float]:
        """Simple forecast using trend"""
        if len(self.data) < 2:
            return [self.data[-1][1]] * steps if self.data else [0]
        
        values = [v for _, v in self.data]
        
        # Calculate trend
        n = len(values)
        x = list(range(n))
        
        x_mean = sum(x) / n
        y_mean = sum(values) / n
        
        numerator = sum((xi - x_mean) * (yi - y_mean) for xi, yi in zip(x, values))
        denominator = sum((xi - x_mean) ** 2 for xi in x)
        
        if denominator == 0:
            slope = 0
        else:
            slope = numerator / denominator
        
        intercept = y_mean - slope * x_mean
        
        # Forecast
        forecasts = []
        for i in range(steps):
            forecast = slope * (n + i) + intercept
            forecasts.append(forecast)
        
        return forecasts
    
    def detect_seasonality(self, period: int = 7) -> Optional[List[float]]:
        """Detect seasonal patterns"""
        if len(self.data) < period * 2:
            return None
        
        values = [v for _, v in self.data]
        
        # Calculate seasonal components
        seasonal = []
        for i in range(period):
            indices = list(range(i, len(values), period))
            if indices:
                avg = sum(values[j] for j in indices) / len(indices)
                seasonal.append(avg)
        
        # Normalize
        mean = sum(seasonal) / len(seasonal)
        seasonal = [s - mean for s in seasonal]
        
        return seasonal

class Clustering:
    """Simple clustering algorithms"""
    
    @staticmethod
    def kmeans(points: List[List[float]], k: int, max_iter: int = 100) -> Tuple[List[int], List[List[float]]]:
        """
        K-means clustering
        
        Returns:
            (assignments, centroids)
        """
        if not points or k <= 0 or k > len(points):
            return [], []
        
        # Initialize centroids randomly
        import random
        centroids = random.sample(points, k)
        
        for _ in range(max_iter):
            # Assign points to nearest centroid
            assignments = []
            for point in points:
                distances = [
                    sum((p - c) ** 2 for p, c in zip(point, centroid))
                    for centroid in centroids
                ]
                assignments.append(distances.index(min(distances)))
            
            # Update centroids
            new_centroids = []
            for i in range(k):
                cluster_points = [points[j] for j, a in enumerate(assignments) if a == i]
                if cluster_points:
                    new_centroid = [
                        sum(p[j] for p in cluster_points) / len(cluster_points)
                        for j in range(len(points[0]))
                    ]
                    new_centroids.append(new_centroid)
                else:
                    new_centroids.append(centroids[i])
            
            # Check convergence
            if new_centroids == centroids:
                break
            
            centroids = new_centroids
        
        return assignments, centroids

class Similarity:
    """Text and vector similarity functions"""
    
    @staticmethod
    def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        if len(vec1) != len(vec2):
            return 0.0
        
        dot = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot / (norm1 * norm2)
    
    @staticmethod
    def jaccard_similarity(set1: set, set2: set) -> float:
        """Calculate Jaccard similarity"""
        if not set1 and not set2:
            return 1.0
        
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        
        return intersection / union if union > 0 else 0.0
    
    @staticmethod
    def levenshtein_distance(s1: str, s2: str) -> int:
        """Calculate edit distance between two strings"""
        if len(s1) < len(s2):
            return Similarity.levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]

# === CONVENIENCE FUNCTIONS ===
def classify_text(text: str, classifier: SimpleClassifier) -> str:
    """Quick text classification"""
    probs = classifier.predict(text)
    return max(probs, key=probs.get) if probs else "unknown"

def find_similar_items(item_id: str, engine: RecommendationEngine, n: int = 5) -> List[str]:
    """Quick similar items"""
    # Find users who liked this item
    users = engine.item_users.get(item_id, set())
    
    # Find other items liked by same users
    similar = defaultdict(int)
    for user in users:
        for other_item in engine.user_items[user]:
            if other_item != item_id:
                similar[other_item] += 1
    
    return [item for item, _ in sorted(similar.items(), key=lambda x: x[1], reverse=True)[:n]]

def quick_forecast(values: List[float], steps: int = 1) -> List[float]:
    """Quick time series forecast"""
    forecaster = TimeSeriesForecaster()
    from datetime import datetime
    for i, v in enumerate(values):
        forecaster.add_point(datetime.now() + timedelta(days=i), v)
    return forecaster.forecast(steps)

# === TESTING ===
if __name__ == "__main__":
    print("🧠 BaarliClaw ML Toolkit - Testing")
    print("=" * 50)
    
    # Test classifier
    print("\n📊 Testing Classifier:")
    clf = SimpleClassifier()
    clf.train("Farmen er en populær realityserie", "reality")
    clf.train("Paradise Hotel har mye drama", "reality")
    clf.train("Spellemannprisen er en musikkpris", "musikk")
    clf.train("VG-lista viser populær musikk", "musikk")
    
    pred = clf.predict("Farmen Kjendis er på TV2")
    print(f"Prediction: {pred}")
    
    # Test recommendation
    print("\n🎯 Testing Recommendation Engine:")
    rec = RecommendationEngine()
    rec.add_interaction("user1", "farmen")
    rec.add_interaction("user1", "paradise_hotel")
    rec.add_interaction("user2", "farmen")
    rec.add_interaction("user2", "kompani_lauritzen")
    
    recommendations = rec.recommend("user1")
    print(f"Recommendations for user1: {recommendations}")
    
    # Test forecasting
    print("\n📈 Testing Time Series Forecaster:")
    ts = TimeSeriesForecaster()
    for i, v in enumerate([100, 105, 110, 108, 115, 120, 125]):
        ts.add_point(datetime.now() + timedelta(days=i), v)
    
    forecast = ts.forecast(3)
    print(f"Forecast next 3 days: {forecast}")
    
    # Test similarity
    print("\n🔗 Testing Similarity:")
    vec1 = [1, 2, 3]
    vec2 = [1, 2, 4]
    sim = Similarity.cosine_similarity(vec1, vec2)
    print(f"Cosine similarity: {sim:.3f}")
    
    print("\n✅ ML Toolkit ready!")
