#!/usr/bin/env python3
"""
⚙️ BAARLICLAW CONFIGURATION MANAGER
Sentral konfigurasjons-håndtering med validering
"""

import sys
import os
import json
import yaml
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from pathlib import Path

sys.path.insert(0, '/root/.openclaw/workspace/scripts')

from baarliclaw_toolkit import setup_logging
from validation_toolkit import Validator
from date_toolkit import DateUtils
from cli_toolkit import TerminalUI, Colors

logger = setup_logging("config-manager")

class ConfigManager:
    """Konfigurasjons-håndtering"""
    
    def __init__(self, config_dir: str = "/tmp/configs"):
        self.config_dir = config_dir
        self.configs: Dict[str, Dict[str, Any]] = {}
        self.schemas: Dict[str, Dict[str, str]] = {}
        
        os.makedirs(config_dir, exist_ok=True)
        self.load_all()
    
    def load_all(self):
        """Last alle konfigurasjoner"""
        for filename in os.listdir(self.config_dir):
            filepath = os.path.join(self.config_dir, filename)
            name = Path(filename).stem
            
            try:
                if filename.endswith('.json'):
                    with open(filepath, 'r') as f:
                        self.configs[name] = json.load(f)
                elif filename.endswith(('.yaml', '.yml')):
                    with open(filepath, 'r') as f:
                        self.configs[name] = yaml.safe_load(f)
            except Exception as e:
                logger.error(f"Kunne ikke laste {filename}: {e}")
    
    def get(self, name: str, key: str = None, default: Any = None) -> Any:
        """Hent konfigurasjons-verdi"""
        if name not in self.configs:
            return default
        
        if key is None:
            return self.configs[name]
        
        # Støtte for nøstede nøkler (f.eks. "database.host")
        keys = key.split('.')
        value = self.configs[name]
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, name: str, key: str, value: Any):
        """Sett konfigurasjons-verdi"""
        if name not in self.configs:
            self.configs[name] = {}
        
        # Støtte for nøstede nøkler
        keys = key.split('.')
        config = self.configs[name]
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        self.save(name)
    
    def save(self, name: str, format: str = "json"):
        """Lagre konfigurasjon til fil"""
        if name not in self.configs:
            return
        
        filepath = os.path.join(self.config_dir, f"{name}.{format}")
        
        try:
            with open(filepath, 'w') as f:
                if format == "json":
                    json.dump(self.configs[name], f, indent=2)
                elif format in ("yaml", "yml"):
                    yaml.dump(self.configs[name], f, default_flow_style=False)
            
            logger.info(f"Konfigurasjon lagret: {filepath}")
        except Exception as e:
            logger.error(f"Kunne ikke lagre {filepath}: {e}")
    
    def validate(self, name: str, schema: Dict[str, str]) -> List[str]:
        """Valider konfigurasjon mot skjema"""
        errors = []
        
        if name not in self.configs:
            return [f"Konfigurasjon '{name}' finnes ikke"]
        
        config = self.configs[name]
        
        for key, expected_type in schema.items():
            value = self.get(name, key)
            
            if value is None:
                errors.append(f"Mangler påkrevd felt: {key}")
                continue
            
            # Sjekk type
            type_map = {
                'str': str,
                'int': int,
                'float': float,
                'bool': bool,
                'list': list,
                'dict': dict
            }
            
            if expected_type in type_map:
                if not isinstance(value, type_map[expected_type]):
                    errors.append(f"{key} må være {expected_type}, fikk {type(value).__name__}")
            
            # Spesial-validering
            if expected_type == 'email':
                result = Validator.email(str(value))
                if not result.valid:
                    errors.append(f"{key} er ikke en gyldig e-post")
            
            elif expected_type == 'url':
                result = Validator.url(str(value))
                if not result.valid:
                    errors.append(f"{key} er ikke en gyldig URL")
        
        return errors
    
    def create_default_configs(self):
        """Opprett standard-konfigurasjoner"""
        # System-konfig
        self.configs['system'] = {
            'name': 'BaarliClaw',
            'version': '10.0',
            'environment': 'production',
            'debug': False,
            'timezone': 'Europe/Oslo',
            'services': {
                'orchestrator': {'enabled': True, 'interval': 300},
                'monitor': {'enabled': True, 'interval': 60},
                'backup': {'enabled': True, 'interval': 3600},
            }
        }
        self.save('system')
        
        # API-konfig
        self.configs['api'] = {
            'host': '0.0.0.0',
            'port': 8080,
            'rate_limit': 100,
            'cors_enabled': True,
            'auth': {
                'required': True,
                'token_expiry': 3600
            }
        }
        self.save('api')
        
        # Database-konfig
        self.configs['database'] = {
            'type': 'sqlite',
            'path': '/tmp/baarliclaw.db',
            'backup_enabled': True,
            'backup_interval': 86400
        }
        self.save('database')
        
        logger.info("Standard-konfigurasjoner opprettet")
    
    def display_configs(self):
        """Vis alle konfigurasjoner"""
        print(f"\n{'='*70}")
        print(f"{Colors.CYAN}⚙️  CONFIGURATION MANAGER{Colors.RESET}")
        print(f"{'='*70}")
        print(f"Konfigurasjons-mappe: {self.config_dir}")
        print(f"Antall konfigurasjoner: {len(self.configs)}")
        print()
        
        for name, config in self.configs.items():
            print(f"📄 {name}:")
            self._print_config(config, indent=2)
            print()
        
        print(f"{'='*70}")
    
    def _print_config(self, config: Dict, indent: int = 0):
        """Hjelpefunksjon for å printe konfigurasjon"""
        for key, value in config.items():
            if isinstance(value, dict):
                print(" " * indent + f"{key}:")
                self._print_config(value, indent + 2)
            else:
                print(" " * indent + f"{key}: {value}")

def main():
    """Hovedfunksjon"""
    print("="*70)
    print("⚙️  CONFIGURATION MANAGER")
    print("="*70)
    
    manager = ConfigManager()
    
    # Opprett standard-konfigurasjoner
    print("\n📝 Oppretter standard-konfigurasjoner...")
    manager.create_default_configs()
    
    # Vis konfigurasjoner
    manager.display_configs()
    
    # Test validering
    print("\n🔍 Validerer konfigurasjoner...")
    schema = {
        'name': 'str',
        'version': 'str',
        'environment': 'str',
        'debug': 'bool',
    }
    
    errors = manager.validate('system', schema)
    if errors:
        print(f"  ⚠️  Validerings-feil:")
        for error in errors:
            print(f"     - {error}")
    else:
        print(f"  ✅ Alle konfigurasjoner validert")
    
    print("\n" + "="*70)
    print("✅ Configuration Manager klar!")
    print("="*70)

if __name__ == "__main__":
    main()
