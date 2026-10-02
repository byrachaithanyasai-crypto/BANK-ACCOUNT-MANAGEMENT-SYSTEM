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

req = urllib.request.Request('http://127.0.0.1:8000/api/accounts/1', headers={'Authorization': 'Bearer ' + token})
try:
    with urllib.request.urlopen(req) as response:
        acc = json.loads(response.read().decode())
except urllib.error.HTTPError as e:
    print("GET error", e.read())
    exit(1)

# Mimic the frontend formData
formData = {
    "customer_id": acc["customer_id"],
    "branch_id": acc["branch_id"],
    "account_number": acc["account_number"],
    "account_type": "CHECKING",
    "balance": acc["balance"],
    "status": acc["status"],
    "opened_date": acc["opened_date"]
}

payload = {
    **formData,
    "customer_id": int(formData["customer_id"]),
    "branch_id": int(formData["branch_id"]),
    "balance": float(formData["balance"])
}

data = json.dumps(payload).encode('utf-8')
req2 = urllib.request.Request('http://127.0.0.1:8000/api/accounts/1', data=data, headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}, method='PUT')
try:
    with urllib.request.urlopen(req2) as response:
        print("PUT Response:", response.status)
except urllib.error.HTTPError as e:
    print("PUT error:", e.code, e.read().decode())
