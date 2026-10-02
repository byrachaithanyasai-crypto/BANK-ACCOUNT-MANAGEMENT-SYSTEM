import urllib.request
import urllib.error
import json

data = json.dumps({'username': 'admin', 'password': 'admin123'}).encode('utf-8')
req = urllib.request.Request('http://127.0.0.1:8000/api/auth/login', data=data, headers={'Content-Type': 'application/json'})

try:
    with urllib.request.urlopen(req) as response:
        res_data = json.loads(response.read().decode())
        token = res_data['access_token']
        print("Token retrieved.")
        
        req2 = urllib.request.Request('http://127.0.0.1:8000/api/auth/me', headers={'Authorization': 'Bearer ' + token})
        with urllib.request.urlopen(req2) as res2:
            print("Me endpoint:", res2.read().decode())
except urllib.error.HTTPError as e:
    print("HTTP Status:", e.code)
    print("Response:", e.read().decode())
