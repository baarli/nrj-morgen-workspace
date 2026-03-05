#!/usr/bin/env python3
"""
⚙️ BAARLICLAW CONFIG TOOLKIT
Konfigurasjons-håndtering
"""

import os
import sys
import json
import yaml
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, '/root/.openclaw/workspace/scripts')
from baarliclaw_toolkit import setup_logging

logger = setup_logging("ConfigToolkit")

class ConfigManager:
    """Manage configuration files"""
    
    def __init__(self, config_dir: str = "./config"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self._configs: Dict[str, Dict] = {}
    
    def load(self, name: str) -> Dict[str, Any]:
        """Load configuration file"""
        if name in self._configs:
            return self._configs[name]
        
        # Try different formats
        for ext in ['.json', '.yaml', '.yml', '.conf']:
            filepath = self.config_dir / f"{name}{ext}"
            if filepath.exists():
                config = self._load_file(str(filepath))
                self._configs[name] = config
                return config
        
        # Return empty config
        return {}
    
    def _load_file(self, filepath: str) -> Dict:
        """Load a single config file"""
        ext = Path(filepath).suffix.lower()
        
        try:
            with open(filepath, 'r') as f:
                if ext == '.json':
                    return json.load(f)
                elif ext in ['.yaml', '.yml']:
                    try:
                        import yaml
                        return yaml.safe_load(f) or {}
                    except ImportError:
                        logger.error("PyYAML not installed")
                        return {}
                else:
                    # Parse as key=value
                    result = {}
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            result[key.strip()] = self._parse_value(value.strip())
                    return result
        except Exception as e:
            logger.error(f"Failed to load {filepath}: {e}")
            return {}
    
    def _parse_value(self, value: str) -> Any:
        """Parse config value"""
        # Try int
        try:
            return int(value)
        except:
            pass
        
        # Try float
        try:
            return float(value)
        except:
            pass
        
        # Try bool
        if value.lower() in ['true', 'yes', 'on']:
            return True
        if value.lower() in ['false', 'no', 'off']:
            return False
        
        # Return string (strip quotes)
        return value.strip('"\'')
    
    def save(self, name: str, config: Dict, format: str = "json"):
        """Save configuration"""
        filepath = self.config_dir / f"{name}.{format}"
        
        with open(filepath, 'w') as f:
            if format == 'json':
                json.dump(config, f, indent=2)
            elif format in ['yaml', 'yml']:
                try:
                    import yaml
                    yaml.dump(config, f, default_flow_style=False)
                except ImportError:
                    logger.error("PyYAML not installed")
            else:
                for key, value in config.items():
                    f.write(f"{key}={value}\n")
        
        self._configs[name] = config
        logger.info(f"Config saved: {filepath}")
    
    def get(self, name: str, key: str, default: Any = None) -> Any:
        """Get config value"""
        config = self.load(name)
        return config.get(key, default)
    
    def set(self, name: str, key: str, value: Any):
        """Set config value"""
        config = self.load(name)
        config[key] = value
        self.save(name, config)
    
    def list_configs(self) -> List[str]:
        """List available configs"""
        configs = []
        for f in self.config_dir.iterdir():
            if f.suffix in ['.json', '.yaml', '.yml', '.conf']:
                configs.append(f.stem)
        return configs

class EnvironmentConfig:
    """Load config from environment variables"""
    
    @staticmethod
    def load(prefix: str = "") -> Dict[str, Any]:
        """Load config from env vars"""
        config = {}
        
        for key, value in os.environ.items():
            if prefix and key.startswith(prefix):
                key = key[len(prefix):]
            
            # Convert to nested dict
            parts = key.lower().split('_')
            target = config
            for part in parts[:-1]:
                if part not in target:
                    target[part] = {}
                target = target[part]
            
            target[parts[-1]] = value
        
        return config
    
    @staticmethod
    def get(key: str, default: Any = None, 
            type_func: Optional[type] = None) -> Any:
        """Get environment variable"""
        value = os.environ.get(key)
        if value is None:
            return default
        
        if type_func:
            try:
                return type_func(value)
            except:
                return default
        
        return value

class ConfigValidator:
    """Validate configuration"""
    
    @staticmethod
    def validate(config: Dict, schema: Dict) -> List[str]:
        """Validate config against schema"""
        errors = []
        
        for key, rules in schema.items():
            if rules.get('required') and key not in config:
                errors.append(f"Missing required key: {key}")
                continue
            
            if key in config:
                value = config[key]
                
                # Type check
                expected_type = rules.get('type')
                if expected_type and not isinstance(value, expected_type):
                    errors.append(f"{key}: expected {expected_type.__name__}, got {type(value).__name__}")
                
                # Range check
                if 'min' in rules and value < rules['min']:
                    errors.append(f"{key}: value {value} < minimum {rules['min']}")
                
                if 'max' in rules and value > rules['max']:
                    errors.append(f"{key}: value {value} > maximum {rules['max']}")
        
        return errors

# === CONVENIENCE FUNCTIONS ===
def quick_config(name: str = "app") -> Dict:
    """Quick config load"""
    manager = ConfigManager()
    return manager.load(name)

def quick_env(prefix: str = "") -> Dict:
    """Quick env load"""
    return EnvironmentConfig.load(prefix)

def get_env(key: str, default: Any = None) -> Any:
    """Quick env get"""
    return EnvironmentConfig.get(key, default)

# === TESTING ===
if __name__ == "__main__":
    print("⚙️ BaarliClaw Config Toolkit - Testing")
    print("=" * 50)
    
    # Test config manager
    print("\n🧪 Testing Config Manager")
    
    # Create test config
    test_config = {
        "app_name": "TestApp",
        "debug": True,
        "port": 8080,
        "database": {
            "host": "localhost",
            "port": 5432
        }
    }
    
    manager = ConfigManager("/tmp/test_config")
    manager.save("test", test_config, "json")
    
    loaded = manager.load("test")
    print(f"✅ Loaded config: {loaded.get('app_name')}")
    print(f"✅ Nested value: {loaded.get('database', {}).get('host')}")
    
    # Test env config
    print("\n🧪 Testing Environment Config")
    
    os.environ['TEST_VAR'] = 'test_value'
    os.environ['TEST_NUMBER'] = '42'
    
    value = EnvironmentConfig.get('TEST_VAR')
    print(f"✅ String: {value}")
    
    number = EnvironmentConfig.get('TEST_NUMBER', type_func=int)
    print(f"✅ Number: {number}")
    
    # Test validator
    print("\n🧪 Testing Config Validator")
    
    schema = {
        'name': {'required': True, 'type': str},
        'port': {'required': True, 'type': int, 'min': 1, 'max': 65535},
        'debug': {'type': bool}
    }
    
    test_cfg = {'name': 'App', 'port': 8080}
    errors = ConfigValidator.validate(test_cfg, schema)
    print(f"✅ Validation errors: {errors}")
    
    # Cleanup
    import shutil
    shutil.rmtree("/tmp/test_config", ignore_errors=True)
    
    print("\n✅ Config Toolkit ready!")
