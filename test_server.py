#!/usr/bin/env python3
"""
Test script to check what the web server returns
"""
import requests
import time

def test_endpoints():
    """Test various endpoints"""
    base_url = "http://localhost:8080"
    
    endpoints = [
        "/health",
        "/",
        "/api/status"
    ]
    
    print("🧪 Testing web server endpoints...")
    
    for endpoint in endpoints:
        try:
            url = base_url + endpoint
            print(f"\n📍 Testing: {url}")
            
            response = requests.get(url, timeout=10)
            print(f"   Status Code: {response.status_code}")
            print(f"   Content Type: {response.headers.get('content-type', 'Unknown')}")
            print(f"   Content Length: {len(response.text)} chars")
            
            if endpoint == "/health":
                print(f"   Response: {response.text}")
            elif response.status_code == 200:
                # For HTML responses, just show first 200 chars
                if 'text/html' in response.headers.get('content-type', ''):
                    print(f"   HTML Preview: {response.text[:200]}...")
                else:
                    print(f"   Response: {response.text[:500]}...")
            else:
                print(f"   Error Response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Error: {e}")
    
    print("\n✅ Endpoint testing complete!")

if __name__ == "__main__":
    # Wait a moment for server to be ready
    time.sleep(2)
    test_endpoints()