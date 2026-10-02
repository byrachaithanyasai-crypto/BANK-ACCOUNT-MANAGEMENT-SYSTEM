import urllib.request
import urllib.error
import json

def get_token(username, password):
    data = json.dumps({'username': username, 'password': password}).encode('utf-8')
    req = urllib.request.Request('http://127.0.0.1:8000/api/auth/login', data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode())
            return res_data['access_token']
    except urllib.error.HTTPError as e:
        return None

t_admin = get_token('admin', 'admin123')
t_manager = get_token('manager', 'manager123')
t_employee = get_token('employee', 'employee123')

def test_endpoint(token, method, endpoint, payload=None):
    headers = {'Authorization': 'Bearer ' + token}
    data = None
    if payload:
        data = json.dumps(payload).encode('utf-8')
        headers['Content-Type'] = 'application/json'
    req = urllib.request.Request(f'http://127.0.0.1:8000{endpoint}', data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as response:
            return response.status
    except urllib.error.HTTPError as e:
        return e.code

print("--- ACCOUNTS GET ---")
print(f"Admin: {test_endpoint(t_admin, 'GET', '/api/accounts')}")
print(f"Manager: {test_endpoint(t_manager, 'GET', '/api/accounts')}")
print(f"Employee: {test_endpoint(t_employee, 'GET', '/api/accounts')}")

print("--- BRANCHES GET ---")
print(f"Manager branches GET: {test_endpoint(t_manager, 'GET', '/api/branches')}")

print("--- ACCOUNTS PUT ---")
payload = {"status": "ACTIVE"}
print(f"Manager Edit: {test_endpoint(t_manager, 'PUT', '/api/accounts/1', payload)}")
print(f"Employee Edit: {test_endpoint(t_employee, 'PUT', '/api/accounts/1', payload)}")

print("--- ACCOUNTS POST ---")
payload_post = {"customer_id": 1, "branch_id": 1, "account_number": "TEST", "account_type": "SAVINGS", "balance": 100, "status": "ACTIVE", "opened_date": "2026-01-01"}
print(f"Manager Create: {test_endpoint(t_manager, 'POST', '/api/accounts', payload_post)}")
print(f"Employee Create: {test_endpoint(t_employee, 'POST', '/api/accounts', payload_post)}")

print("--- ACCOUNTS DELETE ---")
print(f"Manager Delete: {test_endpoint(t_manager, 'DELETE', '/api/accounts/1')}")
print(f"Employee Delete: {test_endpoint(t_employee, 'DELETE', '/api/accounts/1')}")

print("--- RESTRICTED ENDPOINTS ---")
print(f"Manager on /api/employees: {test_endpoint(t_manager, 'GET', '/api/employees')}")
print(f"Employee on /api/employees: {test_endpoint(t_employee, 'GET', '/api/employees')}")
