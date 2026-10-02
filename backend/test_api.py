import requests

try:
    res = requests.post("http://127.0.0.1:8000/api/auth/login", json={"username": "admin", "password": "admin123"})
    print("Status:", res.status_code)
    print("Response:", res.text)
except Exception as e:
    print(f"Error: {e}")
