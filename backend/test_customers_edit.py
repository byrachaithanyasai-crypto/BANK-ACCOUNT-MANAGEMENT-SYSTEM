import urllib.request
import urllib.error
import json

def get_token(username, password):
    data = json.dumps({'username': username, 'password': password}).encode('utf-8')
    req = urllib.request.Request('http://127.0.0.1:8000/api/auth/login', data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())['access_token']
    except Exception: return None

token = get_token('admin', 'admin123')

req = urllib.request.Request('http://127.0.0.1:8000/api/customers/1', headers={'Authorization': 'Bearer ' + token})
try:
    with urllib.request.urlopen(req) as response:
        cust = json.loads(response.read().decode())
        print("GET CUST 1:", cust)
except urllib.error.HTTPError as e:
    print("GET error", e.read())
    exit(1)

# Mimic the frontend formData
payload = {
    "first_name": cust.get("first_name", ""),
    "last_name": cust.get("last_name", ""),
    "email": cust.get("email", ""),
    "phone": cust.get("phone", ""),
    "address": cust.get("address", ""),
    "city": cust.get("city", ""),
    "state": cust.get("state", ""),
    "zip_code": cust.get("zip_code", ""),
    "kyc_status": "VERIFIED"
}

data = json.dumps(payload).encode('utf-8')
req2 = urllib.request.Request('http://127.0.0.1:8000/api/customers/1', data=data, headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}, method='PUT')
try:
    with urllib.request.urlopen(req2) as response:
        print("PUT Response:", response.status)
except urllib.error.HTTPError as e:
    print("PUT error:", e.code, e.read().decode())
