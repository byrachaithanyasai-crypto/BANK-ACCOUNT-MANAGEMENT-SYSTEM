import urllib.request
import urllib.error
import json

BASE_URL = 'http://127.0.0.1:8000'

def test_login(username, password):
    data = json.dumps({'username': username, 'password': password}).encode('utf-8')
    req = urllib.request.Request(f'{BASE_URL}/api/auth/login', data=data, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())['access_token']

token = test_login('admin', 'admin123')

def get(endpoint):
    req = urllib.request.Request(f'{BASE_URL}{endpoint}', headers={'Authorization': f'Bearer {token}'})
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

summary = get('/api/dashboard/summary')
accounts = len(get('/api/accounts'))
customers = len(get('/api/customers'))

print(f"Summary Accounts: {summary['accounts']}, List: {accounts}")
print(f"Summary Customers: {summary['customers']}, List: {customers}")

if summary['accounts'] != accounts or summary['customers'] != customers:
    print("MISMATCH DETECTED")
else:
    print("COUNTS MATCH")

