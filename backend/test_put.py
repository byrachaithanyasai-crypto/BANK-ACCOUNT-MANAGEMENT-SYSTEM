import urllib.request
import urllib.error
import json

BASE_URL = 'http://127.0.0.1:8000'

def test_login(username, password):
    data = json.dumps({'username': username, 'password': password}).encode('utf-8')
    req = urllib.request.Request(f'{BASE_URL}/api/auth/login', data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())['access_token']
    except Exception as e:
        print(f'Login failed: {e}')
        return None

token = test_login('admin', 'admin123')
if not token:
    exit(1)

def test_put(endpoint, payload):
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(f'{BASE_URL}{endpoint}', data=data, headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}, method='PUT')
    try:
        with urllib.request.urlopen(req) as response:
            print(f'PUT {endpoint}: {response.getcode()}')
            print(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f'PUT {endpoint}: {e.code}')
        print(e.read().decode())

# Let's test updating a customer with extra fields (like what frontend sends)
test_put('/api/customers/1', {'first_name': 'Test', 'last_name': 'Update', 'email': 'test@example.com', 'phone': '123', 'kyc_status': 'PENDING', 'extra_field': 'hello'})

