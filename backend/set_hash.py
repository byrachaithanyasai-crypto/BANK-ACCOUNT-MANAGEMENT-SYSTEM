import models.branch
import models.employee
import models.user_account
import models.customer
import models.account
import models.transaction
import models.loan

from database.connection import get_db, SessionLocal
from models.user_account import UserAccount
from models.employee import Employee

db = SessionLocal()

emp = db.query(Employee).filter(Employee.employee_id == 1).first()
if not emp:
    print("Creating dummy employee 1")
    emp = Employee(employee_id=1, first_name="Admin", last_name="User", email="admin@bank.com", phone="123", position="Administrator", salary=100000)
    db.add(emp)
    db.commit()

user = db.query(UserAccount).filter(UserAccount.username == 'admin').first()
hashed = b'.76HMGleOkKSAWW.OuCl4GpkPOaZzJJW/4yaZrwFTPZ1JN.'.decode('utf-8')
if user:
    user.password_hash = hashed
    print("Updated admin password to admin123")
else:
    user = UserAccount(username='admin', password_hash=hashed, role='ADMIN', employee_id=1)
    db.add(user)
    print("Created admin user with password admin123")
db.commit()
