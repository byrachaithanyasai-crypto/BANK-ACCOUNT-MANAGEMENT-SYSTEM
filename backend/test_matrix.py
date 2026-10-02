import urllib.request
import urllib.error
import json

BASE_URL = 'http://127.0.0.1:8000'

def test_login(username, password):
    data = json.dumps({'username': username, 'password': password}).encode('utf-8')
    req = urllib.request.Request(f'{BASE_URL}/api/auth/login', data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            print(f'Login {username}/{password}: {response.getcode()}')
            return json.loads(response.read().decode())['access_token']
    except urllib.error.HTTPError as e:
        print(f'Login {username}/{password}: {e.code}')
        return None

def test_endpoint(token, method, endpoint):
    req = urllib.request.Request(f'{BASE_URL}{endpoint}', headers={'Authorization': f'Bearer {token}'}, method=method)
    try:
        with urllib.request.urlopen(req) as response:
            print(f'{method} {endpoint}: {response.getcode()}')
    except urllib.error.HTTPError as e:
        print(f'{method} {endpoint}: {e.code}')

print('--- AUTH MATRIX ---')
admin_token = test_login('admin', 'admin123')
manager_token = test_login('manager2', 'manager123')
teller_token = test_login('teller2', 'teller123')

test_login('admin', 'wrongpass')
test_login('manager2', 'wrongpass')

print('\n--- ROLE MATRIX ---')
print('ADMIN')
test_endpoint(admin_token, 'GET', '/api/dashboard/summary')
test_endpoint(admin_token, 'GET', '/api/employees')
test_endpoint(admin_token, 'GET', '/api/branches')

print('MANAGER')
test_endpoint(manager_token, 'GET', '/api/accounts')
test_endpoint(manager_token, 'GET', '/api/employees')
test_endpoint(manager_token, 'GET', '/api/branches')

print('EMPLOYEE')
test_endpoint(teller_token, 'GET', '/api/transactions')
test_endpoint(teller_token, 'GET', '/api/employees')

