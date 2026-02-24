#!/usr/bin/env python3
"""
Mission Control API v2.0 - Test Suite
Run this to verify all API features are working
"""

import requests
import json
import sys
import time
import websocket
import threading

BASE_URL = "http://localhost:8081"
WS_URL = "ws://localhost:8082"

def test_endpoint(method, path, data=None, headers=None, expected_status=200):
    """Test an API endpoint"""
    url = f"{BASE_URL}{path}"
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=10)
        elif method == "PATCH":
            response = requests.patch(url, json=data, headers=headers, timeout=10)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, timeout=10)
        else:
            print(f"❌ Unknown method: {method}")
            return False
        
        success = response.status_code == expected_status
        status = "✓" if success else "❌"
        print(f"{status} {method} {path} - {response.status_code}")
        
        if not success:
            print(f"   Expected {expected_status}, got {response.status_code}")
            try:
                print(f"   Response: {response.json()}")
            except:
                print(f"   Response: {response.text[:200]}")
        
        return success, response
    except Exception as e:
        print(f"❌ {method} {path} - Error: {e}")
        return False, None

def test_public_endpoints():
    """Test public endpoints"""
    print("\n=== Public Endpoints ===")
    results = []
    
    results.append(test_endpoint("GET", "/api/health")[0])
    results.append(test_endpoint("GET", "/api/status")[0])
    
    return all(results)

def test_auth():
    """Test authentication"""
    print("\n=== Authentication ===")
    
    # Test login
    success, response = test_endpoint("POST", "/api/auth/login", 
        data={"username": "admin", "password": "admin"},
        expected_status=200)
    
    if not success:
        print("   Note: Login may fail if ADMIN_PASSWORD is not set to 'admin'")
        return None
    
    token = response.json().get("token")
    print(f"   Got token: {token[:20]}...")
    
    # Test verify
    headers = {"Authorization": f"Bearer {token}"}
    test_endpoint("GET", "/api/auth/verify", headers=headers)
    
    return token

def test_protected_endpoints(token):
    """Test protected endpoints"""
    if not token:
        print("\n=== Protected Endpoints (SKIPPED - no token) ===")
        return False
    
    print("\n=== Protected Endpoints ===")
    headers = {"Authorization": f"Bearer {token}"}
    results = []
    
    results.append(test_endpoint("GET", "/api/system/resources", headers=headers)[0])
    results.append(test_endpoint("GET", "/api/metrics", headers=headers)[0])
    results.append(test_endpoint("GET", "/api/logs", headers=headers)[0])
    results.append(test_endpoint("GET", "/api/config", headers=headers)[0])
    results.append(test_endpoint("GET", "/api/backups", headers=headers)[0])
    results.append(test_endpoint("GET", "/api/cron/jobs", headers=headers)[0])
    results.append(test_endpoint("GET", "/api/git/repos", headers=headers)[0])
    results.append(test_endpoint("GET", "/api/nrj/stats", headers=headers)[0])
    results.append(test_endpoint("GET", "/api/routine/morning/status", headers=headers)[0])
    
    return all(results)

def test_websocket():
    """Test WebSocket connection"""
    print("\n=== WebSocket ===")
    
    ws_results = {"connected": False, "received_message": False}
    
    def on_message(ws, message):
        print(f"✓ Received message: {message[:100]}...")
        ws_results["received_message"] = True
        ws.close()
    
    def on_error(ws, error):
        print(f"❌ WebSocket error: {error}")
    
    def on_close(ws, close_status_code, close_msg):
        print(f"✓ WebSocket closed")
    
    def on_open(ws):
        print("✓ WebSocket connected")
        ws_results["connected"] = True
        # Send a test message
        ws.send(json.dumps({"type": "test", "data": "hello"}))
    
    try:
        ws = websocket.WebSocketApp(WS_URL,
                                    on_open=on_open,
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close)
        
        # Run for 3 seconds
        wst = threading.Thread(target=ws.run_forever)
        wst.daemon = True
        wst.start()
        time.sleep(3)
        ws.close()
        
        return ws_results["connected"]
    except Exception as e:
        print(f"❌ WebSocket test failed: {e}")
        return False

def main():
    print("=" * 50)
    print("Mission Control API v2.0 - Test Suite")
    print("=" * 50)
    
    # Check if API is running
    try:
        requests.get(f"{BASE_URL}/api/health", timeout=2)
    except:
        print("\n❌ API is not running!")
        print("   Start it with: ./api-service.sh start")
        sys.exit(1)
    
    results = {}
    
    # Run tests
    results["public"] = test_public_endpoints()
    token = test_auth()
    results["protected"] = test_protected_endpoints(token)
    results["websocket"] = test_websocket()
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    
    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "❌ FAILED"
        print(f"{test_name.capitalize():20} {status}")
    
    all_passed = all(results.values())
    print("=" * 50)
    
    if all_passed:
        print("✓ All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed")
        sys.exit(1)

if __name__ == "__main__":
    main()