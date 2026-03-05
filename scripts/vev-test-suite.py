#!/usr/bin/env python3
"""
Vev Voice Chat Test Suite
Tester alle komponenter før deploy
"""
import os
import sys
import json
import requests
from datetime import datetime

WORKSPACE = "/root/.openclaw/workspace"

def log_test(test_name, status, details=""):
    """Log test result"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    status_icon = "✅" if status else "❌"
    print(f"[{timestamp}] {status_icon} {test_name}")
    if details:
        print(f"       {details}")
    return status

def test_voice_files():
    """Test that voice files exist"""
    print("\n🎙️  Testing Voice Files...")
    
    audio_dir = f"{WORKSPACE}/brain/projects/voice-chat/audio-emotional"
    tests = []
    
    # Check directory exists
    if os.path.exists(audio_dir):
        tests.append(log_test("Audio directory exists", True, audio_dir))
        
        # Check for emotion files
        emotions = ['excited', 'happy', 'serious', 'curious']
        for emotion in emotions:
            pattern = f"{audio_dir}/emotional_{emotion}_"
            files = [f for f in os.listdir(audio_dir) if f.startswith(f"emotional_{emotion}_")]
            if files:
                tests.append(log_test(f"{emotion.capitalize()} voice files", True, f"{len(files)} files"))
            else:
                tests.append(log_test(f"{emotion.capitalize()} voice files", False, "No files found"))
    else:
        tests.append(log_test("Audio directory exists", False, f"{audio_dir} not found"))
    
    return all(tests)

def test_conversation_history():
    """Test conversation history system"""
    print("\n💬 Testing Conversation History...")
    
    tests = []
    history_file = f"{WORKSPACE}/brain/conversations/telegram-history.json"
    
    if os.path.exists(history_file):
        try:
            with open(history_file) as f:
                data = json.load(f)
            tests.append(log_test("History file readable", True))
            
            if 'conversations' in data:
                tests.append(log_test("Conversations key exists", True))
            else:
                tests.append(log_test("Conversations key exists", False))
        except:
            tests.append(log_test("History file readable", False, "JSON parse error"))
    else:
        tests.append(log_test("History file exists", False))
    
    return all(tests)

def test_user_profiles():
    """Test user profile system"""
    print("\n👤 Testing User Profiles...")
    
    tests = []
    profiles_file = f"{WORKSPACE}/brain/conversations/user-profiles.json"
    
    if os.path.exists(profiles_file):
        try:
            with open(profiles_file) as f:
                data = json.load(f)
            tests.append(log_test("Profiles file readable", True))
            
            if 'users' in data:
                user_count = len(data['users'])
                tests.append(log_test("Users loaded", True, f"{user_count} users"))
            else:
                tests.append(log_test("Users key exists", False))
        except:
            tests.append(log_test("Profiles file readable", False, "JSON parse error"))
    else:
        tests.append(log_test("Profiles file exists", False))
    
    return all(tests)

def test_telegram_connection():
    """Test Telegram API connection"""
    print("\n📱 Testing Telegram Connection...")
    
    tests = []
    
    # Load credentials
    try:
        with open(f"{WORKSPACE}/.credentials/telegram-bot.env") as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, val = line.strip().split('=', 1)
                    os.environ[key] = val
        
        token = os.environ.get('TELEGRAM_BOT_TOKEN')
        if token:
            tests.append(log_test("Telegram token loaded", True))
            
            # Test API
            url = f"https://api.telegram.org/bot{token}/getMe"
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('ok'):
                        bot_name = data['result'].get('username', 'Unknown')
                        tests.append(log_test("Telegram API connection", True, f"@{bot_name}"))
                    else:
                        tests.append(log_test("Telegram API connection", False, "API error"))
                else:
                    tests.append(log_test("Telegram API connection", False, f"HTTP {response.status_code}"))
            except Exception as e:
                tests.append(log_test("Telegram API connection", False, str(e)))
        else:
            tests.append(log_test("Telegram token loaded", False))
    except Exception as e:
        tests.append(log_test("Credentials load", False, str(e)))
    
    return all(tests)

def test_elevenlabs_connection():
    """Test ElevenLabs API connection"""
    print("\n🔊 Testing ElevenLabs Connection...")
    
    tests = []
    
    try:
        with open(f"{WORKSPACE}/.credentials/elevenlabs.env") as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, val = line.strip().split('=', 1)
                    val = val.split('#')[0].strip()
                    os.environ[key] = val
        
        api_key = os.environ.get('ELEVENLABS_API_KEY')
        if api_key:
            tests.append(log_test("ElevenLabs API key loaded", True))
            
            # Test API
            url = "https://api.elevenlabs.io/v1/voices"
            headers = {"xi-api-key": api_key}
            try:
                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code == 200:
                    voices = response.json().get('voices', [])
                    tests.append(log_test("ElevenLabs API connection", True, f"{len(voices)} voices"))
                else:
                    tests.append(log_test("ElevenLabs API connection", False, f"HTTP {response.status_code}"))
            except Exception as e:
                tests.append(log_test("ElevenLabs API connection", False, str(e)))
        else:
            tests.append(log_test("ElevenLabs API key loaded", False))
    except Exception as e:
        tests.append(log_test("Credentials load", False, str(e)))
    
    return all(tests)

def test_systemd_service():
    """Test systemd service status"""
    print("\n⚙️  Testing Systemd Service...")
    
    tests = []
    
    import subprocess
    try:
        result = subprocess.run(
            ['systemctl', 'is-active', 'vev-telegram-responder.service'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            tests.append(log_test("Telegram responder service", True, "active"))
        else:
            tests.append(log_test("Telegram responder service", False, "inactive"))
    except Exception as e:
        tests.append(log_test("Systemd check", False, str(e)))
    
    return all(tests)

def main():
    print("=" * 60)
    print("🧪 VEV VOICE CHAT TEST SUITE")
    print("=" * 60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = []
    
    # Run all tests
    results.append(("Voice Files", test_voice_files()))
    results.append(("Conversation History", test_conversation_history()))
    results.append(("User Profiles", test_user_profiles()))
    results.append(("Telegram Connection", test_telegram_connection()))
    results.append(("ElevenLabs Connection", test_elevenlabs_connection()))
    results.append(("Systemd Service", test_systemd_service()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print("-" * 60)
    print(f"Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - Ready for deploy!")
        return 0
    else:
        print("⚠️  Some tests failed - Check logs above")
        return 1

if __name__ == "__main__":
    sys.exit(main())
