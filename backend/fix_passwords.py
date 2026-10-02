from database.connection import SessionLocal
from models.user_account import UserAccount
from auth.security import verify_password, get_password_hash

db = SessionLocal()
admin_user = db.query(UserAccount).filter(UserAccount.username == 'admin').first()
if admin_user:
    is_valid = verify_password('admin123', admin_user.password_hash)
    print(f"Is admin123 valid for current hash? {is_valid}")
    if not is_valid:
        print("Fixing admin password...")
        admin_user.password_hash = get_password_hash('admin123')
        db.commit()
        print("Fixed admin password.")

manager = db.query(UserAccount).filter(UserAccount.username == 'manager').first()
if manager:
    if not verify_password('manager123', manager.password_hash):
        print("Fixing manager password...")
        manager.password_hash = get_password_hash('manager123')
        db.commit()

employee = db.query(UserAccount).filter(UserAccount.username == 'employee').first()
if employee:
    if not verify_password('employee123', employee.password_hash):
        print("Fixing employee password...")
        employee.password_hash = get_password_hash('employee123')
        db.commit()

db.close()
