from database.connection import SessionLocal
from models.user_account import UserAccount
from auth.security import get_password_hash

db = SessionLocal()
admin_user = db.query(UserAccount).filter(UserAccount.username == 'admin').first()
if admin_user:
    admin_user.password_hash = get_password_hash('admin123')
    admin_user.is_active = True
    db.commit()
    print("Fixed admin hash")

manager = db.query(UserAccount).filter(UserAccount.username == 'manager').first()
if manager:
    manager.password_hash = get_password_hash('manager123')
    manager.is_active = True
    db.commit()
    print("Fixed manager hash")

employee = db.query(UserAccount).filter(UserAccount.username == 'employee').first()
if employee:
    employee.password_hash = get_password_hash('employee123')
    employee.is_active = True
    db.commit()
    print("Fixed employee hash")

db.close()
