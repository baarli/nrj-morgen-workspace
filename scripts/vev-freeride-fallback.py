#!/usr/bin/env python3
"""
FreeRide Auto-Fallback System
Automatically switches to OpenRouter when rate limited
"""
import os
import json
import time
import requests
from datetime import datetime

class FreeRideFallback:
    """Automatic fallback to avoid rate limits"""
    
    def __init__(self):
        self.openrouter_key = os.getenv('OPENROUTER_API_KEY')
        self.primary_model = "kimi-coding/k2p5"
        self.fallback_models = [
            "openrouter/gpt-4o",
            "openrouter/claude-3-opus", 
            "openrouter/mistral-large"
        ]
        self.current_model = self.primary_model
        self.rate_limit_hits = 0
        
    def log(self, msg):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] {msg}")
        
    def check_rate_limit(self):
        """Check if we're hitting rate limits"""
        # This would check actual API response headers
        # For now, simulate based on request frequency
        return self.rate_limit_hits > 0
    
    def get_fallback_model(self):
        """Get next available fallback model"""
        if self.current_model == self.primary_model:
            return self.fallback_models[0]
        
        try:
            idx = self.fallback_models.index(self.current_model)
            if idx + 1 < len(self.fallback_models):
                return self.fallback_models[idx + 1]
        except ValueError:
            pass
            
        return self.fallback_models[0]  # Cycle back to first fallback
    
    def switch_model(self, reason="rate_limit"):
        """Switch to fallback model"""
        old_model = self.current_model
        self.current_model = self.get_fallback_model()
        
        self.log(f"🔄 Switched from {old_model} to {self.current_model}")
        self.log(f"   Reason: {reason}")
        
        return self.current_model
    
    def reset_to_primary(self):
        """Reset to primary model"""
        if self.current_model != self.primary_model:
            self.log(f"🔄 Reset to primary: {self.primary_model}")
            self.current_model = self.primary_model
            self.rate_limit_hits = 0
    
    def auto_execute(self, prompt, max_retries=3):
        """Execute with automatic fallback"""
        for attempt in range(max_retries):
            try:
                # Try current model
                result = self._call_model(self.current_model, prompt)
                
                # If successful and we were on fallback, consider resetting
                if self.current_model != self.primary_model and attempt == 0:
                    # Stay on fallback for now, reset later
                    pass
                    
                return result
                
            except Exception as e:
                self.log(f"⚠️  Attempt {attempt + 1} failed: {e}")
                
                if "rate limit" in str(e).lower():
                    self.rate_limit_hits += 1
                    if attempt < max_retries - 1:
                        self.switch_model("rate_limit")
                else:
                    raise
        
        raise Exception("All fallback models exhausted")
    
    def _call_model(self, model, prompt):
        """Call specific model"""
        if model.startswith("openrouter/"):
            return self._call_openrouter(model.replace("openrouter/", ""), prompt)
        else:
            # Primary model - use OpenClaw
            return self._call_openclaw(model, prompt)
    
    def _call_openrouter(self, model, prompt):
        """Call OpenRouter API"""
        headers = {
            "Authorization": f"Bearer {self.openrouter_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )
        
        if response.status_code == 429:
            raise Exception("Rate limit hit")
            
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    
    def _call_openclaw(self, model, prompt):
        """Call via OpenClaw"""
        # This would integrate with OpenClaw's API
        # For now, placeholder
        return f"[OpenClaw: {model}] {prompt}"

def main():
    fallback = FreeRideFallback()
    
    print("=" * 60)
    print("🚀 FREERIDE AUTO-FALLBACK SYSTEM")
    print("=" * 60)
    print()
    print(f"Primary: {fallback.primary_model}")
    print(f"Fallbacks: {', '.join(fallback.fallback_models)}")
    print(f"Current: {fallback.current_model}")
    print()
    
    # Test auto-switch
    print("Testing fallback system...")
    try:
        result = fallback.auto_execute("Hello, this is a test")
        print(f"✅ Success: {result[:50]}...")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
