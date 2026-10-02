import urllib.request
import urllib.error
import json

def test_login(username, password):
    data = json.dumps({'username': username, 'password': password}).encode('utf-8')
    req = urllib.request.Request('http://127.0.0.1:8000/api/auth/login', data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode())
            print(f"{username} / {password} -> {response.status}")
            return res_data['access_token']
    except urllib.error.HTTPError as e:
        print(f"{username} / {password} -> {e.code}")
        return None

t1 = test_login('admin', 'admin123')
t2 = test_login('manager', 'manager123')
t3 = test_login('employee', 'employee123')
t4 = test_login('admin', 'wrongpass')

def test_role(token, endpoint):
    req = urllib.request.Request(f'http://127.0.0.1:8000{endpoint}', headers={'Authorization': 'Bearer ' + token})
    try:
        with urllib.request.urlopen(req) as response:
            return response.status
    except urllib.error.HTTPError as e:
        return e.code

print(f"Admin on /api/employees: {test_role(t1, '/api/employees')}")
print(f"Manager on /api/employees: {test_role(t2, '/api/employees')}")
print(f"Employee on /api/employees: {test_role(t3, '/api/employees')}")
