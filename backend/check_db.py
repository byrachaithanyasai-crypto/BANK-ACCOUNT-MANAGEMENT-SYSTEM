from database.connection import SessionLocal
from models.user_account import UserAccount

db = SessionLocal()
admin_user = db.query(UserAccount).filter(UserAccount.username == 'admin').first()
if admin_user:
    print(f"Username: {admin_user.username}")
    print(f"Role: {admin_user.role}")
    print(f"Status: {getattr(admin_user, 'status', 'N/A')}")
    print(f"Has password_hash: {bool(admin_user.password_hash)}")
else:
    print("Admin user NOT FOUND")

manager = db.query(UserAccount).filter(UserAccount.username == 'manager').first()
print(f"Manager found: {bool(manager)}")

employee = db.query(UserAccount).filter(UserAccount.username == 'employee').first()
print(f"Employee found: {bool(employee)}")

db.close()
