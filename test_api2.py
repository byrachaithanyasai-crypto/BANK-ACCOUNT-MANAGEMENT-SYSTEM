import urllib.request
import json
import time

def test_login(username, password, expected_status):
    data = json.dumps({'username': username, 'password': password}).encode('utf-8')
    req = urllib.request.Request('http://127.0.0.1:8000/api/auth/login', data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as f:
            status = f.status
            if status == expected_status:
                print(f"[PASS] {username} -> {status}")
            else:
                print(f"[FAIL] {username} expected {expected_status}, got {status}")
    except urllib.error.HTTPError as e:
        status = e.code
        if status == expected_status:
            print(f"[PASS] {username} -> {status}")
        else:
            print(f"[FAIL] {username} expected {expected_status}, got {status}")
            print(e.read().decode('utf-8'))
    except Exception as e:
        print("Error:", e)

print("--- Auth Tests ---")
test_login("admin", "admin123", 200)
test_login("manager2", "manager123", 200)
test_login("teller2", "teller123", 200)
test_login("admin", "wrong", 401)
test_login("unknown", "unknown", 401)
