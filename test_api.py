import os
import sys

sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))

from fastapi.testclient import TestClient
from backend.main import app
from backend.database.connection import engine
from sqlalchemy import text

client = TestClient(app)

print("--- DB Connection Test ---")
with engine.connect() as conn:
    print(conn.execute(text("SELECT 1")).scalar())

def test_login(username, password, expected_status):
    resp = client.post("/api/auth/login", json={"username": username, "password": password})
    if resp.status_code == expected_status:
        print(f"[PASS] {username} -> {expected_status}")
    else:
        print(f"[FAIL] {username} expected {expected_status}, got {resp.status_code}")
        print(resp.json())

print("--- Auth Tests ---")
test_login("admin", "admin123", 200)
test_login("manager2", "manager123", 200)
test_login("teller2", "teller123", 200)
test_login("admin", "wrong", 401)
test_login("unknown", "unknown", 401)
