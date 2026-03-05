#!/usr/bin/env python3
"""
AI Content Suggestions API
Provides OpenAI-powered suggestions for improving sakslista items
"""

import json
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import urllib.error

# OpenAI API configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

class AIHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        if self.path == '/api/ai/suggest':
            self.handle_suggest()
        else:
            self.send_error(404)
    
    def handle_suggest(self):
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            title = data.get('title', '')
            description = data.get('description', '')
            
            # Generate suggestions using OpenAI
            suggestions = self.generate_suggestions(title, description)
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(suggestions).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def generate_suggestions(self, title, description):
        """Generate AI suggestions for content improvement"""
        
        # If no OpenAI key, return fallback suggestions
        if not OPENAI_API_KEY:
            return self.get_fallback_suggestions(title, description)
        
        try:
            prompt = f"""Gitt følgende sak for NRJ Morgen radio:
Tittel: {title}
Beskrivelse: {description}

Gi 3 konkrete forslag for å forbedre denne saken for radio:
1. En bedre tittel (mer spennende, action-orientert)
2. En bedre beskrivelse (mer engasjerende, 2-3 setninger)
3. En god inngang/åpning (spørsmål eller statement som fenger)

Svar i JSON format:
[{{"type": "Tittel", "text": "..."}}, {{"type": "Beskrivelse", "text": "..."}}, {{"type": "Inngang", "text": "..."}}]"""
            
            headers = {
                'Authorization': f'Bearer {OPENAI_API_KEY}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'model': 'gpt-4',
                'messages': [{'role': 'user', 'content': prompt}],
                'temperature': 0.7
            }
            
            req = urllib.request.Request(
                OPENAI_API_URL,
                data=json.dumps(payload).encode(),
                headers=headers,
                method='POST'
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode())
                content = result['choices'][0]['message']['content']
                return json.loads(content)
                
        except Exception as e:
            print(f"OpenAI error: {e}")
            return self.get_fallback_suggestions(title, description)
    
    def get_fallback_suggestions(self, title, description):
        """Fallback suggestions when OpenAI is not available"""
        return [
            {
                "type": "Tittel",
                "text": f"🔥 {title} - Dette må du vite!"
            },
            {
                "type": "Beskrivelse", 
                "text": f"{description}\n\n💡 Hvorfor dette er viktig: Dette engasjerer lytterne fordi..."
            },
            {
                "type": "Inngang",
                "text": "Har du noen gang lurt på...? I dag snakker vi om noe som affects alle!"
            }
        ]
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass

def main():
    port = 8083
    server = HTTPServer(('0.0.0.0', port), AIHandler)
    print(f"🤖 AI Content Suggestions API running on port {port}")
    server.serve_forever()

if __name__ == '__main__':
    main()
