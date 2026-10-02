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

def test_put(endpoint, payload):
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(f'{BASE_URL}{endpoint}', data=data, headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}, method='PUT')
    try:
        with urllib.request.urlopen(req) as response:
            print(f'PUT {endpoint}: {response.getcode()}')
    except urllib.error.HTTPError as e:
        print(f'PUT {endpoint}: {e.code}')
        print(e.read().decode())

test_put('/api/accounts/1', {'balance': 1500.00})
test_put('/api/branches/1', {'branch_name': 'Downtown Branch Edit'})
test_put('/api/employees/1', {'first_name': 'Admin Edit'})

