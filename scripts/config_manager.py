#!/usr/bin/env python3
"""
BAARLICLAW CONFIGURATION MANAGER
Centralized configuration and credential management for all NRJ Morgen scripts
"""

import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any

# ============================================================================
# PATHS
# ============================================================================

WORKSPACE_ROOT = Path("/root/.openclaw/workspace")
CREDENTIALS_DIR = WORKSPACE_ROOT / ".credentials"
SCRIPTS_DIR = WORKSPACE_ROOT / "scripts"
LOGS_DIR = WORKSPACE_ROOT / "brain" / "logs"

# ============================================================================
# SUPABASE CONFIG
# ============================================================================

SUPABASE_URL = "https://kvniauxokdtmpvjtfnej.supabase.co"
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt2bmlhdXhva2R0bXB2anRmbmVqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTM2NzIzNCwiZXhwIjoyMDY2OTQzMjM0fQ.OkhTtq9QAQ3xMzZYKyWyCjj7PiqMZJKSvpA0jcBJqpE"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt2bmlhdXhva2R0bXB2anRmbmVqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEzNjcyMzQsImV4cCI6MjA2Njk0MzIzNH0.eE7WGqD6b9Rk-2RqTXlg5XaqONpQTzXL1O5DMaLy5Yw"
TENANT_ID = "a0000000-0000-0000-0000-000000000001"
CREATED_BY = "10aa1508-6d52-490c-8ae5-fa3da9a152c4"

# ============================================================================
# EXTERNAL API KEYS (from .credentials/)
# ============================================================================

def load_env_file(filepath: Path) -> Dict[str, str]:
    """Load environment variables from a file."""
    env_vars = {}
    if filepath.exists():
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip().strip('"').strip("'")
    return env_vars


def get_credential(key: str, env_file: str = "live-search.env") -> Optional[str]:
    """
    Get credential from environment or credentials file.
    
    Priority:
    1. Environment variable
    2. .credentials/{env_file}
    3. .credentials/nrj-morgen.env
    4. Return None
    """
    # Check environment first
    if key in os.environ:
        return os.environ[key]
    
    # Check credentials files
    for cred_file in [env_file, "nrj-morgen.env", "telegram-bot.env"]:
        filepath = CREDENTIALS_DIR / cred_file
        if filepath.exists():
            env_vars = load_env_file(filepath)
            if key in env_vars:
                return env_vars[key]
    
    return None


# Lazy-loaded credentials
class Credentials:
    """Lazy credential loader with caching."""
    
    _cache: Dict[str, str] = {}
    
    @classmethod
    def get(cls, key: str) -> Optional[str]:
        if key not in cls._cache:
            cls._cache[key] = get_credential(key)
        return cls._cache[key]
    
    @classmethod
    def clear_cache(cls):
        cls._cache.clear()
    
    # Common credentials as properties
    @property
    def brave_api_key(self) -> Optional[str]:
        return self.get('BRAVE_API_KEY')
    
    @property
    def openai_api_key(self) -> Optional[str]:
        return self.get('OPENAI_API_KEY')
    
    @property
    def elevenlabs_api_key(self) -> Optional[str]:
        return self.get('ELEVENLABS_API_KEY')
    
    @property
    def telegram_bot_token(self) -> Optional[str]:
        return self.get('TELEGRAM_BOT_TOKEN')
    
    @property
    def telegram_chat_id(self) -> Optional[str]:
        return self.get('TELEGRAM_CHAT_ID')
    
    @property
    def openrouter_api_key(self) -> Optional[str]:
        return self.get('OPENROUTER_API_KEY')
    
    @property
    def gmail_app_password(self) -> Optional[str]:
        return self.get('GMAIL_APP_PASSWORD')
    
    @property
    def github_token(self) -> Optional[str]:
        return self.get('GITHUB_TOKEN')
    
    @property
    def netlify_token(self) -> Optional[str]:
        return self.get('NETLIFY_AUTH_TOKEN')


credentials = Credentials()

# ============================================================================
# API CONFIGURATIONS
# ============================================================================

API_CONFIG = {
    'brave': {
        'base_url': 'https://api.search.brave.com/res/v1',
        'timeout': 15,
        'rate_limit_per_minute': 100,
    },
    'openai': {
        'base_url': 'https://api.openai.com/v1',
        'timeout': 120,
        'image_model': 'gpt-image-1',
        'chat_model': 'gpt-4o-mini',
    },
    'elevenlabs': {
        'base_url': 'https://api.elevenlabs.io/v1',
        'timeout': 60,
        'voice_id': '4kCDY3HJwvO7Zp3con83',  # Sebastian - Norwegian
        'model': 'eleven_flash_v2_5',
    },
    'telegram': {
        'base_url': 'https://api.telegram.org/bot',
        'timeout': 30,
    },
    'supabase': {
        'url': SUPABASE_URL,
        'service_key': SUPABASE_SERVICE_KEY,
        'timeout': 15,
        'max_retries': 3,
    },
}

# ============================================================================
# MORNING ROUTINE CONFIG
# ============================================================================

MORNING_ROUTINE_CONFIG = {
    'num_articles': 15,
    'categories': ['Reality TV', 'Kjendis', 'Film & TV', 'Musikk', 'Internasjonalt'],
    'max_per_category': 3,
    'max_age_hours': 48,
    'sources': [
        'vg.no/rampelys',
        'tv2.no/underholdning',
        'nettavisen.no/kjendis',
        'seher.no',
        'dagbladet.no/kjendis',
    ],
    'exclude_keywords': [
        'krig', 'terror', 'drap', 'voldtekt', 'tragedie',
        'politikk', 'regjering', 'storting'
    ],
    'image_generation': {
        'enabled': True,
        'model': 'gpt-image-1',
        'size': '1024x1024',
        'rate_limit_delay': 2.0,
    },
}

# ============================================================================
# DASHBOARD CONFIG
# ============================================================================

DASHBOARD_CONFIG = {
    'panel_id': '0b1f6b6b-3fde-434b-b7c8-dcf306beea72',
    'tenant_id': TENANT_ID,
    'created_by': CREATED_BY,
    'update_interval_hours': 24,
    'nielsen_api': {
        'base_url': 'https://eu-iport.nielsen-iwatch.com/api',
        'channel': 'NRJ',
    },
    'podtoppen': {
        'csv_url': 'https://podtoppen.tnslistene.no/export.php',
        'podcast_title': 'NRJ Morgen Podkast',
    },
}

# ============================================================================
# STORAGE BUCKETS
# ============================================================================

STORAGE_BUCKETS = {
    'media_library': 'media-library',
    'profile_pictures': 'profile-pictures',
    'podcast_clips': 'podcast-clips',
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def ensure_directories():
    """Ensure all required directories exist."""
    for directory in [CREDENTIALS_DIR, SCRIPTS_DIR, LOGS_DIR]:
        directory.mkdir(parents=True, exist_ok=True)


def validate_credentials(required: list) -> tuple[bool, list]:
    """
    Validate that required credentials are available.
    
    Returns:
        (is_valid, missing_keys)
    """
    missing = []
    for key in required:
        if not credentials.get(key):
            missing.append(key)
    return len(missing) == 0, missing


def print_config_status():
    """Print status of all configurations (safe - no secrets)."""
    print("=" * 70)
    print("CONFIGURATION STATUS")
    print("=" * 70)
    
    # Check credentials
    print("\nCredentials:")
    creds_to_check = [
        'BRAVE_API_KEY',
        'OPENAI_API_KEY',
        'ELEVENLABS_API_KEY',
        'TELEGRAM_BOT_TOKEN',
    ]
    for cred in creds_to_check:
        status = "✅" if credentials.get(cred) else "❌"
        print(f"  {status} {cred}")
    
    # Check directories
    print("\nDirectories:")
    for name, path in [
        ('Workspace', WORKSPACE_ROOT),
        ('Scripts', SCRIPTS_DIR),
        ('Logs', LOGS_DIR),
        ('Credentials', CREDENTIALS_DIR),
    ]:
        status = "✅" if path.exists() else "❌"
        print(f"  {status} {name}: {path}")
    
    print("\n" + "=" * 70)

# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    'WORKSPACE_ROOT',
    'CREDENTIALS_DIR',
    'SCRIPTS_DIR',
    'LOGS_DIR',
    'SUPABASE_URL',
    'SUPABASE_SERVICE_KEY',
    'TENANT_ID',
    'CREATED_BY',
    'credentials',
    'Credentials',
    'API_CONFIG',
    'MORNING_ROUTINE_CONFIG',
    'DASHBOARD_CONFIG',
    'STORAGE_BUCKETS',
    'ensure_directories',
    'validate_credentials',
    'print_config_status',
]

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print_config_status()
    
    # Example: Validate required credentials
    required = ['BRAVE_API_KEY', 'OPENAI_API_KEY']
    is_valid, missing = validate_credentials(required)
    
    if is_valid:
        print("\n✅ All required credentials found")
    else:
        print(f"\n❌ Missing credentials: {', '.join(missing)}")
        sys.exit(1)
