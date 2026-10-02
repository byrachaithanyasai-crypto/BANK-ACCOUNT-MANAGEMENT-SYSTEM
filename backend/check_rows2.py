from database.connection import SessionLocal
from models.user_account import UserAccount

db = SessionLocal()
users = db.query(UserAccount).all()
for u in users:
    print(f"ID: {u.user_id} | Username: '{u.username}' | Role: {u.role} | Active: {u.is_active} | Hash: {u.password_hash}")
db.close()
