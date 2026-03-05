#!/usr/bin/env python3
"""
Mission Control Backend API v2.0
Full funksjonalitet med Supabase-integrasjon
"""

import os
import sys
import json
import subprocess
import threading
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl

# Konfigurasjon
SUPABASE_URL = 'https://kvniauxokdtmpvjtfnej.supabase.co'
SUPABASE_SERVICE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt2bmlhdXhva2R0bXB2anRmbmVqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTM2NzIzNCwiZXhwIjoyMDY2OTQzMjM0fQ.OkhTtq9QAQ3xMzZYKyWyCjj7PiqMZJKSvpA0jcBJqpE'
TENANT_ID = 'a0000000-0000-0000-0000-000000000001'
API_PORT = 8081
WORKSPACE = "/root/.openclaw/workspace"
SCRIPTS_DIR = f"{WORKSPACE}/scripts"

class SupabaseClient:
    def __init__(self):
        self.base_url = SUPABASE_URL
        self.api_key = SUPABASE_SERVICE_KEY
    
    def request(self, endpoint, method='GET', data=None, params=None):
        url = f"{self.base_url}/rest/v1{endpoint}"
        if params:
            url += '?' + urllib.parse.urlencode(params)
        
        headers = {
            'apikey': self.api_key,
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'Prefer': 'return=representation'
        }
        
        req = urllib.request.Request(url, headers=headers, method=method)
        if data:
            req.data = json.dumps(data).encode('utf-8')
        
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                if response.status == 204:
                    return {'success': True}
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            raise Exception(f"HTTP {e.code}: {error_body}")
        except Exception as e:
            raise Exception(f"Request failed: {str(e)}")
    
    def get(self, endpoint, params=None):
        return self.request(endpoint, 'GET', params=params)
    
    def post(self, endpoint, data):
        return self.request(endpoint, 'POST', data=data)
    
    def patch(self, endpoint, data):
        return self.request(endpoint, 'PATCH', data=data)
    
    def delete(self, endpoint):
        return self.request(endpoint, 'DELETE')

supabase = SupabaseClient()

# Global state
morning_routine_status = {
    'running': False,
    'started_at': None,
    'progress': 0,
    'message': 'Idle',
    'last_result': None
}

class APIHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {args[0]}")
    
    def send_json_response(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, apikey')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, apikey')
        self.end_headers()
    
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)
        
        try:
            if path == '/api/health':
                self.send_json_response({'status': 'ok', 'timestamp': datetime.now().isoformat()})
            
            elif path == '/api/status':
                self.send_json_response(self.get_system_status())
            
            elif path == '/api/saker':
                date = query.get('date', [datetime.now().strftime('%Y-%m-%d')])[0]
                self.send_json_response(self.get_saker(date))
            
            elif path == '/api/saker/all':
                self.send_json_response(self.get_all_saker())
            
            elif path == '/api/podcast/episodes':
                self.send_json_response(self.get_podcast_episodes())
            
            elif path == '/api/nrj/stats':
                self.send_json_response(self.get_nrj_stats())
            
            elif path == '/api/routine/morning/status':
                self.send_json_response(morning_routine_status)
            
            elif path == '/api/cron/jobs':
                self.send_json_response(self.get_cron_jobs())
            
            elif path == '/api/logs':
                self.send_json_response(self.get_logs())
            
            else:
                self.send_json_response({'error': 'Not found'}, 404)
        
        except Exception as e:
            print(f"Error in GET {path}: {e}")
            self.send_json_response({'error': str(e)}, 500)
    
    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        
        content_length = int(self.headers.get('Content-Length', 0))
        body = {}
        if content_length > 0:
            try:
                body = json.loads(self.rfile.read(content_length).decode())
            except:
                pass
        
        try:
            if path == '/api/saker':
                self.send_json_response(self.create_sak(body), 201)
            
            elif path == '/api/routine/morning':
                self.send_json_response(self.run_morning_routine())
            
            elif path == '/api/saker/reorder':
                self.send_json_response(self.reorder_saker(body))
            
            else:
                self.send_json_response({'error': 'Not found'}, 404)
        
        except Exception as e:
            print(f"Error in POST {path}: {e}")
            self.send_json_response({'error': str(e)}, 500)
    
    def do_PATCH(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        
        content_length = int(self.headers.get('Content-Length', 0))
        body = {}
        if content_length > 0:
            try:
                body = json.loads(self.rfile.read(content_length).decode())
            except:
                pass
        
        try:
            if path.startswith('/api/saker/'):
                sak_id = path.split('/')[-1]
                self.send_json_response(self.update_sak(sak_id, body))
            
            else:
                self.send_json_response({'error': 'Not found'}, 404)
        
        except Exception as e:
            print(f"Error in PATCH {path}: {e}")
            self.send_json_response({'error': str(e)}, 500)
    
    def do_DELETE(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        
        try:
            if path.startswith('/api/saker/'):
                sak_id = path.split('/')[-1]
                self.send_json_response(self.delete_sak(sak_id))
            
            else:
                self.send_json_response({'error': 'Not found'}, 404)
        
        except Exception as e:
            print(f"Error in DELETE {path}: {e}")
            self.send_json_response({'error': str(e)}, 500)
    
    # ===== API METHODS =====
    
    def get_system_status(self):
        try:
            # Sjekk ulike systemkomponenter
            auto_exec = os.path.exists(f"{WORKSPACE}/.auto-exec-log")
            autonomous = os.path.exists(f"{WORKSPACE}/.autonomous-mode.pid")
            
            # Tell skills og scripts
            skills_dir = f"{WORKSPACE}/skills"
            skills_count = len([d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d))]) if os.path.exists(skills_dir) else 0
            
            scripts_count = len([f for f in os.listdir(SCRIPTS_DIR) if f.endswith(('.sh', '.py'))]) if os.path.exists(SCRIPTS_DIR) else 0
            
            return {
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'systems': {
                    'autoExec': 'active' if auto_exec else 'inactive',
                    'autonomousMode': 'active' if autonomous else 'inactive',
                    'api': 'active',
                    'supabase': 'connected'
                },
                'stats': {
                    'skills': skills_count,
                    'scripts': scripts_count
                }
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def get_saker(self, date):
        try:
            result = supabase.get('/agenda_items', {
                'tenant_id': f'eq.{TENANT_ID}',
                'show_date': f'eq.{date}',
                'order': 'order_index.asc'
            })
            return {'saker': result, 'count': len(result), 'date': date}
        except Exception as e:
            return {'error': str(e), 'saker': [], 'count': 0}
    
    def get_all_saker(self, days=30):
        try:
            from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            result = supabase.get('/agenda_items', {
                'tenant_id': f'eq.{TENANT_ID}',
                'show_date': f'gte.{from_date}',
                'order': 'show_date.desc'
            })
            return {'saker': result, 'count': len(result)}
        except Exception as e:
            return {'error': str(e)}
    
    def create_sak(self, data):
        try:
            sak = {
                'tenant_id': TENANT_ID,
                'title': data.get('title', 'Ny sak'),
                'description': data.get('description', ''),
                'category': data.get('category', 'TALK'),
                'show_date': data.get('show_date', datetime.now().strftime('%Y-%m-%d')),
                'link_url': data.get('link_url', ''),
                'notes': data.get('notes', ''),
                'is_pinned': data.get('is_pinned', False),
                'order_index': data.get('order_index', 0),
                'created_by': '10aa1508-6d52-490c-8ae5-fa3da9a152c4'
            }
            result = supabase.post('/agenda_items', sak)
            return {'success': True, 'sak': result}
        except Exception as e:
            return {'error': str(e)}
    
    def update_sak(self, sak_id, data):
        try:
            result = supabase.patch(f'/agenda_items?id=eq.{sak_id}', data)
            return {'success': True, 'sak': result}
        except Exception as e:
            return {'error': str(e)}
    
    def delete_sak(self, sak_id):
        try:
            supabase.delete(f'/agenda_items?id=eq.{sak_id}')
            return {'success': True, 'message': 'Sak slettet'}
        except Exception as e:
            return {'error': str(e)}
    
    def reorder_saker(self, data):
        try:
            order = data.get('order', [])
            for idx, sak_id in enumerate(order):
                supabase.patch(f'/agenda_items?id=eq.{sak_id}', {'order_index': idx})
            return {'success': True}
        except Exception as e:
            return {'error': str(e)}
    
    def get_podcast_episodes(self):
        try:
            # Prøv å hente fra podcast_episodes tabell
            result = supabase.get('/podcast_episodes', {
                'order': 'published_at.desc',
                'limit': 20
            })
            return {'episodes': result, 'count': len(result)}
        except Exception as e:
            # Fallback til agenda_items med podcast kategori
            try:
                result = supabase.get('/agenda_items', {
                    'tenant_id': f'eq.{TENANT_ID}',
                    'category': 'eq.PODCAST',
                    'order': 'created_at.desc',
                    'limit': 20
                })
                return {'episodes': result, 'count': len(result), 'source': 'agenda_items'}
            except:
                return {'error': str(e), 'episodes': []}
    
    def get_nrj_stats(self):
        try:
            # Hent siste radio-stats
            radio = supabase.get('/agenda_items', {
                'tenant_id': f'eq.{TENANT_ID}',
                'category': 'eq.STATS',
                'order': 'created_at.desc',
                'limit': 1
            })
            
            # Hent siste podcast-ranking
            podcast = supabase.get('/agenda_items', {
                'tenant_id': f'eq.{TENANT_ID}',
                'category': 'eq.PODCAST_RANKING',
                'order': 'created_at.desc',
                'limit': 1
            })
            
            return {
                'radio': radio[0] if radio else None,
                'podcast': podcast[0] if podcast else None
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_cron_jobs(self):
        # Returner mock data for nå - kan utvides med faktisk cron-lesing
        return {
            'jobs': [
                {'name': 'Morning Routine', 'schedule': 'Mon-Fri 06:00', 'status': 'active'},
                {'name': 'Dashboard Update', 'schedule': 'Wed 14:00', 'status': 'active'},
                {'name': 'Podcast Download', 'schedule': 'Daily 07:00', 'status': 'active'}
            ]
        }
    
    def get_logs(self):
        try:
            log_file = f"{WORKSPACE}/logs/api.log"
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    lines = f.readlines()[-50:]
                    return [{'message': line.strip(), 'timestamp': datetime.now().isoformat()} for line in lines if line.strip()]
            return []
        except Exception as e:
            return [{'message': str(e), 'timestamp': datetime.now().isoformat()}]
    
    def run_morning_routine(self):
        global morning_routine_status
        
        if morning_routine_status['running']:
            return {'status': 'already_running', 'message': 'Morning Routine kjører allerede'}
        
        thread = threading.Thread(target=self._execute_morning_routine)
        thread.daemon = True
        thread.start()
        
        return {'status': 'started', 'message': 'Morning Routine startet. Dette tar 2-3 minutter.'}
    
    def _execute_morning_routine(self):
        global morning_routine_status
        
        morning_routine_status['running'] = True
        morning_routine_status['started_at'] = datetime.now().isoformat()
        morning_routine_status['progress'] = 0
        morning_routine_status['message'] = 'Starter Morning Routine...'
        
        try:
            # Steg 1: Slett gamle saker
            morning_routine_status['progress'] = 10
            morning_routine_status['message'] = 'Sletter gamle saker...'
            today = datetime.now().strftime('%Y-%m-%d')
            try:
                supabase.delete(f'/agenda_items?tenant_id=eq.{TENANT_ID}&show_date=eq.{today}')
            except:
                pass
            
            # Steg 2: Kjør news search
            morning_routine_status['progress'] = 30
            morning_routine_status['message'] = 'Søker etter nyheter...'
            
            result = subprocess.run(
                ['python3', f'{SCRIPTS_DIR}/brave-news-search.py', '15'],
                capture_output=True,
                text=True,
                timeout=180
            )
            
            if result.returncode != 0:
                raise Exception(f'News search failed: {result.stderr}')
            
            # Steg 3: Parse og insert resultater
            morning_routine_status['progress'] = 70
            morning_routine_status['message'] = 'Legger til saker i databasen...'
            
            # Les resultat fra fil hvis den finnes
            result_file = '/tmp/morning-routine-v2-result.json'
            if os.path.exists(result_file):
                with open(result_file, 'r') as f:
                    data = json.load(f)
                    articles = data.get('top_15', [])
                    
                    for idx, article in enumerate(articles):
                        sak = {
                            'tenant_id': TENANT_ID,
                            'title': article.get('short_title', article.get('title', 'Ukjent')),
                            'description': article.get('description', ''),
                            'category': 'TALK',
                            'show_date': today,
                            'link_url': article.get('url', ''),
                            'notes': f"{article.get('description', '')[:300]}\n\nUnderholdningsverdi: {article.get('score', 70)}/100\nKilde: {article.get('category', 'Ukjent')}",
                            'link_metadata': json.dumps({
                                'source': article.get('source', ''),
                                'image_url': ''
                            }),
                            'order_index': idx,
                            'created_by': '10aa1508-6d52-490c-8ae5-fa3da9a152c4',
                            'is_pinned': False
                        }
                        try:
                            supabase.post('/agenda_items', sak)
                        except Exception as e:
                            print(f"Error inserting sak: {e}")
                
                morning_routine_status['progress'] = 100
                morning_routine_status['message'] = f'Fullført! {len(articles)} saker lagt til.'
                morning_routine_status['last_result'] = {
                    'count': len(articles),
                    'timestamp': datetime.now().isoformat()
                }
            else:
                morning_routine_status['message'] = 'Fullført, men ingen resultatfil funnet.'
                
        except Exception as e:
            morning_routine_status['message'] = f'Feil: {str(e)}'
            morning_routine_status['last_result'] = {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
        finally:
            morning_routine_status['running'] = False

def main():
    server = HTTPServer(('0.0.0.0', API_PORT), APIHandler)
    print(f"🚀 Mission Control API v2.0")
    print(f"📡 Port: {API_PORT}")
    print(f"🔗 Supabase: {SUPABASE_URL}")
    print(f"🎯 Ready for connections!")
    print("")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
        server.shutdown()

if __name__ == '__main__':
    main()
