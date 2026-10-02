from database.connection import SessionLocal
from models.user_account import UserAccount

db = SessionLocal()
admin_user = db.query(UserAccount).filter(UserAccount.username == 'admin').first()
print(f"Admin is_active: {admin_user.is_active}")
db.close()
