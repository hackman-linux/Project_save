# Run this script to diagnose CamPay API issues
# python manage.py shell < campay_diagnostic.py

import requests
from django.conf import settings
import json

print("=" * 60)
print("CamPay API Diagnostic Tool")
print("=" * 60)

config = settings.CAMPAY_CONFIG
base_url = config["BASE_URL"].rstrip('/')

print(f"\n1. Configuration Check:")
print(f"   Base URL: {base_url}")
print(f"   Environment: {config['ENVIRONMENT']}")
print(f"   Has API Key: {'Yes' if config.get('API_KEY') else 'No'}")
print(f"   Has Username: {'Yes' if config.get('USERNAME') else 'No'}")
print(f"   Has Password: {'Yes' if config.get('PASSWORD') else 'No'}")

# Test 1: Basic connectivity
print(f"\n2. Testing Basic Connectivity:")
try:
    response = requests.get(base_url, timeout=10)
    print(f"   ✅ Can reach {base_url}")
    print(f"   Status: {response.status_code}")
except requests.exceptions.ConnectionError as e:
    print(f"   ❌ Cannot connect to {base_url}")
    print(f"   Error: {e}")
    print(f"\n   Possible causes:")
    print(f"   - Wrong BASE_URL in settings")
    print(f"   - CamPay API is down")
    print(f"   - Network/firewall issue")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: Authentication endpoint
print(f"\n3. Testing Authentication Endpoint:")
if config.get('USERNAME') and config.get('PASSWORD'):
    try:
        auth_url = f"{base_url}/token/"
        payload = {
            "username": config['USERNAME'],
            "password": config['PASSWORD']
        }
        
        print(f"   URL: {auth_url}")
        print(f"   Payload: {json.dumps(payload, indent=6)}")
        
        response = requests.post(
            auth_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            if 'token' in data:
                print(f"   ✅ Authentication successful")
                print(f"   Token: {data['token'][:20]}...")
            else:
                print(f"   ⚠️ No token in response: {data}")
        else:
            print(f"   ❌ Authentication failed")
            print(f"   Response: {response.text[:300]}")
            
    except requests.exceptions.ConnectionError as e:
        print(f"   ❌ Connection error: {e}")
        print(f"\n   The server closed the connection!")
        print(f"   This usually means:")
        print(f"   1. Wrong endpoint URL")
        print(f"   2. Invalid SSL certificate")
        print(f"   3. Server rejecting the request")
    except Exception as e:
        print(f"   ❌ Error: {e}")
else:
    print(f"   ⚠️ No username/password configured")

# Test 3: Collect endpoint with API key
print(f"\n4. Testing Collect Endpoint:")
if config.get('API_KEY'):
    try:
        collect_url = f"{base_url}/collect/"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Token {config['API_KEY']}"
        }
        
        # Test with minimal data
        test_data = {
            "amount": "100",
            "from": "237600000000",
            "description": "Test",
            "external_reference": "test123"
        }
        
        print(f"   URL: {collect_url}")
        print(f"   Headers: Authorization: Token {config['API_KEY'][:20]}...")
        print(f"   Test Data: {json.dumps(test_data, indent=6)}")
        
        response = requests.post(
            collect_url,
            json=test_data,
            headers=headers,
            timeout=30
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:300]}")
        
        if response.status_code in [200, 201]:
            print(f"   ✅ Collect endpoint accessible")
        else:
            print(f"   ⚠️ Unexpected status code")
            
    except requests.exceptions.ConnectionError as e:
        print(f"   ❌ Connection error: {e}")
        print(f"\n   DIAGNOSIS:")
        print(f"   The API is rejecting your requests immediately.")
        print(f"   Check:")
        print(f"   1. Is your API_KEY correct?")
        print(f"   2. Is the BASE_URL correct? ({base_url})")
        print(f"   3. Should it be /api/collect/ instead of /collect/?")
    except Exception as e:
        print(f"   ❌ Error: {e}")
else:
    print(f"   ⚠️ No API key configured")

# Test 4: Alternative endpoints
print(f"\n5. Testing Alternative Endpoints:")
alternatives = [
    f"{base_url}/api/token/",
    f"{base_url}/api/collect/",
    f"{base_url.replace('/api', '')}/token/",
    f"{base_url.replace('/api', '')}/collect/"
]

for alt_url in alternatives:
    try:
        response = requests.get(alt_url, timeout=5)
        print(f"   {alt_url}: {response.status_code}")
    except:
        print(f"   {alt_url}: ❌ Failed")

print("\n" + "=" * 60)
print("Diagnostic Complete")
print("=" * 60)

# Recommendations
print("\n📋 Recommendations:")
print("1. Verify your BASE_URL in settings matches CamPay documentation")
print("2. Ensure your API_KEY or credentials are correct")
print("3. Check if you need /api/ prefix in URLs")
print("4. Contact CamPay support if connection keeps failing")
print("5. Check your Django logs for more details")