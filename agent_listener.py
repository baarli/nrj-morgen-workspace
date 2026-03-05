#!/usr/bin/env python3
"""
BaarliClaw Agent Listener
Lytter på kommandoer fra Mission Control via Supabase Realtime
"""

import os
import sys
import json
import time
from datetime import datetime

# Konfigurasjon
SUPABASE_URL = "https://kvniauxokdtmpvjtfnje.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt2bmlhdXhva2R0bXB2anRmbmVqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTM2NzIzNCwiZXhwIjoyMDY2OTQzMjM0fQ.OkhTtq9QAQ3xMzZYKyWyCjj7PiqMZJKSvpA0jcBJqpE"

class AgentListener:
    def __init__(self):
        self.running = True
        self.last_check = datetime.now()
        
    def log(self, level, message, details=None):
        """Logg til konsoll og fil"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] [{level.upper()}] {message}")
        if details:
            print(f"  Details: {json.dumps(details, indent=2)}")
    
    def process_command(self, command):
        """Prosesser en kommando fra Mission Control"""
        cmd_id = command.get('id')
        cmd_type = command.get('command_type')
        cmd_data = command.get('command_data', {})
        
        self.log('info', f"Mottatt kommando: {cmd_type}", {'id': cmd_id, 'data': cmd_data})
        
        # Oppdater status til processing
        self.update_command_status(cmd_id, 'processing')
        
        try:
            # Håndter ulike kommando-typer
            if cmd_type == 'task':
                result = self.handle_task(cmd_data)
            elif cmd_type == 'query':
                result = self.handle_query(cmd_data)
            elif cmd_type == 'system':
                result = self.handle_system(cmd_data)
            elif cmd_type == 'config':
                result = self.handle_config(cmd_data)
            else:
                result = {'success': False, 'error': f'Ukjent kommando-type: {cmd_type}'}
            
            # Send svar
            self.send_response(cmd_id, 'result', result)
            self.update_command_status(cmd_id, 'completed', result=result)
            
        except Exception as e:
            error_msg = str(e)
            self.log('error', f"Feil ved prosessering: {error_msg}")
            self.send_response(cmd_id, 'error', {'error': error_msg})
            self.update_command_status(cmd_id, 'failed', error=error_msg)
    
    def handle_task(self, data):
        """Håndter oppgave-kommandoer"""
        task_name = data.get('task')
        self.log('info', f"Utfører oppgave: {task_name}")
        
        # TODO: Implementer faktisk oppgave-logikk
        return {
            'success': True,
            'task': task_name,
            'message': f'Oppgave {task_name} fullført'
        }
    
    def handle_query(self, data):
        """Håndter spørringer"""
        query_type = data.get('query')
        self.log('info', f"Behandler spørring: {query_type}")
        
        # TODO: Implementer spørrings-logikk
        return {
            'success': True,
            'query': query_type,
            'data': {}
        }
    
    def handle_system(self, data):
        """Håndter system-kommandoer"""
        action = data.get('action')
        self.log('info', f"System-handling: {action}")
        
        # TODO: Implementer system-handlinger
        return {
            'success': True,
            'action': action,
            'status': 'ok'
        }
    
    def handle_config(self, data):
        """Håndter konfigurasjons-endringer"""
        config_key = data.get('key')
        config_value = data.get('value')
        self.log('info', f"Oppdaterer config: {config_key}")
        
        # TODO: Implementer config-oppdatering
        return {
            'success': True,
            'key': config_key,
            'value': config_value
        }
    
    def update_command_status(self, cmd_id, status, result=None, error=None):
        """Oppdater status på en kommando i Supabase"""
        # TODO: Implementer via REST API
        self.log('debug', f"Oppdaterer status: {cmd_id} -> {status}")
    
    def send_response(self, cmd_id, response_type, data):
        """Send svar til Mission Control"""
        # TODO: Implementer via REST API
        self.log('debug', f"Sender svar: {cmd_id} -> {response_type}")
    
    def check_for_commands(self):
        """Sjekk etter nye kommandoer"""
        # TODO: Hent fra Supabase via REST API
        # For nå, simuler at vi sjekker
        pass
    
    def run(self):
        """Hovedløkke"""
        self.log('info', 'BaarliClaw Agent Listener startet')
        self.log('info', 'Venter på kommandoer fra Mission Control...')
        
        try:
            while self.running:
                self.check_for_commands()
                time.sleep(5)  # Sjekk hvert 5. sekund
                
        except KeyboardInterrupt:
            self.log('info', 'Avslutter...')
            self.running = False

if __name__ == '__main__':
    listener = AgentListener()
    listener.run()
