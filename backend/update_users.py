from database.connection import SessionLocal
from models.user_account import UserAccount

db = SessionLocal()

manager = db.query(UserAccount).filter(UserAccount.username == 'manager2').first()
if manager:
    manager.username = 'manager'
    db.commit()
    print("Migrated manager2 -> manager")

teller = db.query(UserAccount).filter(UserAccount.username == 'teller2').first()
if teller:
    teller.username = 'employee'
    db.commit()
    print("Migrated teller2 -> employee")

db.close()
