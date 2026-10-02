import requests

token_res = requests.post('http://127.0.0.1:8000/api/auth/login', json={"username": "admin", "password": "admin123"})
if token_res.status_code == 200:
    token = token_res.json()['access_token']
    res = requests.get('http://127.0.0.1:8000/api/dashboard/summary', headers={"Authorization": f"Bearer {token}"})
    print(res.status_code)
    print(res.json())
else:
    print("Login failed")
