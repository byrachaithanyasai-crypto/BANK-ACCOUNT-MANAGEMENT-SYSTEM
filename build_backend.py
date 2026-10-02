import os

def ensure_dir(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

def write_file(path, content):
    ensure_dir(path)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

schemas_account = '''
from pydantic import BaseModel, condecimal
from datetime import date
from typing import Optional

class AccountBase(BaseModel):
    customer_id: int
    branch_id: int
    account_number: str
    account_type: str
    balance: condecimal(max_digits=15, decimal_places=2) = 0.00
    status: str = "ACTIVE"
    opened_date: date

class AccountCreate(AccountBase):
    pass

class AccountUpdate(BaseModel):
    account_type: Optional[str] = None
    balance: Optional[condecimal(max_digits=15, decimal_places=2)] = None
    status: Optional[str] = None

class AccountResponse(AccountBase):
    account_id: int
    
    class Config:
        from_attributes = True
'''
write_file('backend/schemas/account.py', schemas_account)

schemas_customer = '''
from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    kyc_status: str = "PENDING"
    date_of_birth: Optional[date] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    kyc_status: Optional[str] = None

class CustomerResponse(CustomerBase):
    customer_id: int
    
    class Config:
        from_attributes = True
'''
write_file('backend/schemas/customer.py', schemas_customer)

schemas_transaction = '''
from pydantic import BaseModel, condecimal
from datetime import datetime
from typing import Optional

class TransactionBase(BaseModel):
    account_id: int
    transaction_type: str
    amount: condecimal(max_digits=15, decimal_places=2)
    status: str = "COMPLETED"
    reference_number: Optional[str] = None
    description: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    transaction_id: int
    transaction_date: datetime
    
    class Config:
        from_attributes = True
'''
write_file('backend/schemas/transaction.py', schemas_transaction)

schemas_employee = '''
from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class EmployeeBase(BaseModel):
    branch_id: Optional[int] = None
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    position: Optional[str] = None
    hire_date: Optional[date] = None

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    branch_id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    position: Optional[str] = None
    hire_date: Optional[date] = None

class EmployeeResponse(EmployeeBase):
    employee_id: int
    
    class Config:
        from_attributes = True
'''
write_file('backend/schemas/employee.py', schemas_employee)

schemas_branch = '''
from pydantic import BaseModel
from typing import Optional

class BranchBase(BaseModel):
    branch_code: str
    branch_name: str
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    phone: Optional[str] = None

class BranchCreate(BranchBase):
    pass

class BranchUpdate(BaseModel):
    branch_code: Optional[str] = None
    branch_name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    phone: Optional[str] = None

class BranchResponse(BranchBase):
    branch_id: int
    
    class Config:
        from_attributes = True
'''
write_file('backend/schemas/branch.py', schemas_branch)

schemas_audit = '''
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Any

class AuditLogResponse(BaseModel):
    log_id: int
    user_id: Optional[int]
    action: str
    table_name: str
    record_id: Optional[int]
    old_value: Optional[Any]
    new_value: Optional[Any]
    action_timestamp: datetime
    
    class Config:
        from_attributes = True
'''
write_file('backend/schemas/audit_log.py', schemas_audit)

api_accounts = '''
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from models.account import Account
from schemas.account import AccountCreate, AccountUpdate, AccountResponse
from auth.dependencies import get_current_user, require_manager

router = APIRouter(prefix="/api/accounts", tags=["Accounts"])

@router.get("/", response_model=list[AccountResponse])
def get_accounts(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(Account).all()

@router.get("/{id}", response_model=AccountResponse)
def get_account(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    acc = db.query(Account).filter(Account.account_id == id).first()
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")
    return acc

@router.post("/", response_model=AccountResponse)
def create_account(acc: AccountCreate, db: Session = Depends(get_db), current_user = Depends(require_manager)):
    db_acc = Account(**acc.model_dump())
    db.add(db_acc)
    db.commit()
    db.refresh(db_acc)
    return db_acc

@router.put("/{id}", response_model=AccountResponse)
def update_account(id: int, acc: AccountUpdate, db: Session = Depends(get_db), current_user = Depends(require_manager)):
    db_acc = db.query(Account).filter(Account.account_id == id).first()
    if not db_acc:
        raise HTTPException(status_code=404, detail="Account not found")
    update_data = acc.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_acc, key, value)
    db.commit()
    db.refresh(db_acc)
    return db_acc

@router.delete("/{id}")
def delete_account(id: int, db: Session = Depends(get_db), current_user = Depends(require_manager)):
    db_acc = db.query(Account).filter(Account.account_id == id).first()
    if not db_acc:
        raise HTTPException(status_code=404, detail="Account not found")
    db.delete(db_acc)
    db.commit()
    return {"message": "Account deleted successfully"}
'''
write_file('backend/api/accounts.py', api_accounts)

api_customers = '''
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from models.customer import Customer
from schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse
from auth.dependencies import get_current_user, require_manager

router = APIRouter(prefix="/api/customers", tags=["Customers"])

@router.get("/", response_model=list[CustomerResponse])
def get_customers(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(Customer).all()

@router.get("/{id}", response_model=CustomerResponse)
def get_customer(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    cust = db.query(Customer).filter(Customer.customer_id == id).first()
    if not cust:
        raise HTTPException(status_code=404, detail="Customer not found")
    return cust

@router.post("/", response_model=CustomerResponse)
def create_customer(cust: CustomerCreate, db: Session = Depends(get_db), current_user = Depends(require_manager)):
    db_cust = Customer(**cust.model_dump())
    db.add(db_cust)
    db.commit()
    db.refresh(db_cust)
    return db_cust

@router.put("/{id}", response_model=CustomerResponse)
def update_customer(id: int, cust: CustomerUpdate, db: Session = Depends(get_db), current_user = Depends(require_manager)):
    db_cust = db.query(Customer).filter(Customer.customer_id == id).first()
    if not db_cust:
        raise HTTPException(status_code=404, detail="Customer not found")
    update_data = cust.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_cust, key, value)
    db.commit()
    db.refresh(db_cust)
    return db_cust

@router.delete("/{id}")
def delete_customer(id: int, db: Session = Depends(get_db), current_user = Depends(require_manager)):
    db_cust = db.query(Customer).filter(Customer.customer_id == id).first()
    if not db_cust:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(db_cust)
    db.commit()
    return {"message": "Customer deleted successfully"}
'''
write_file('backend/api/customers.py', api_customers)

api_transactions = '''
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from models.transaction import Transaction
from models.account import Account
from schemas.transaction import TransactionCreate, TransactionResponse
from auth.dependencies import get_current_user, require_employee

router = APIRouter(prefix="/api/transactions", tags=["Transactions"])

@router.get("/", response_model=list[TransactionResponse])
def get_transactions(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(Transaction).order_by(Transaction.transaction_date.desc()).all()

@router.post("/", response_model=TransactionResponse)
def create_transaction(txn: TransactionCreate, db: Session = Depends(get_db), current_user = Depends(require_employee)):
    # Verify account
    acc = db.query(Account).filter(Account.account_id == txn.account_id).first()
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # Financial logic
    if txn.transaction_type == 'WITHDRAWAL' and acc.balance < txn.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")
        
    db_txn = Transaction(**txn.model_dump())
    db.add(db_txn)
    
    if txn.transaction_type == 'DEPOSIT':
        acc.balance += txn.amount
    elif txn.transaction_type == 'WITHDRAWAL':
        acc.balance -= txn.amount
        
    db.commit()
    db.refresh(db_txn)
    return db_txn
'''
write_file('backend/api/transactions.py', api_transactions)

api_employees = '''
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from models.employee import Employee
from schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from auth.dependencies import get_current_user, require_admin

router = APIRouter(prefix="/api/employees", tags=["Employees"])

@router.get("/", response_model=list[EmployeeResponse])
def get_employees(db: Session = Depends(get_db), current_user = Depends(require_admin)):
    return db.query(Employee).all()

@router.post("/", response_model=EmployeeResponse)
def create_employee(emp: EmployeeCreate, db: Session = Depends(get_db), current_user = Depends(require_admin)):
    db_emp = Employee(**emp.model_dump())
    db.add(db_emp)
    db.commit()
    db.refresh(db_emp)
    return db_emp

@router.put("/{id}", response_model=EmployeeResponse)
def update_employee(id: int, emp: EmployeeUpdate, db: Session = Depends(get_db), current_user = Depends(require_admin)):
    db_emp = db.query(Employee).filter(Employee.employee_id == id).first()
    if not db_emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    for key, value in emp.model_dump(exclude_unset=True).items():
        setattr(db_emp, key, value)
    db.commit()
    db.refresh(db_emp)
    return db_emp

@router.delete("/{id}")
def delete_employee(id: int, db: Session = Depends(get_db), current_user = Depends(require_admin)):
    db_emp = db.query(Employee).filter(Employee.employee_id == id).first()
    if not db_emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(db_emp)
    db.commit()
    return {"message": "Employee deleted"}
'''
write_file('backend/api/employees.py', api_employees)

api_branches = '''
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from models.branch import Branch
from schemas.branch import BranchCreate, BranchUpdate, BranchResponse
from auth.dependencies import get_current_user, require_admin

router = APIRouter(prefix="/api/branches", tags=["Branches"])

@router.get("/", response_model=list[BranchResponse])
def get_branches(db: Session = Depends(get_db), current_user = Depends(require_admin)):
    return db.query(Branch).all()

@router.post("/", response_model=BranchResponse)
def create_branch(br: BranchCreate, db: Session = Depends(get_db), current_user = Depends(require_admin)):
    db_br = Branch(**br.model_dump())
    db.add(db_br)
    db.commit()
    db.refresh(db_br)
    return db_br

@router.put("/{id}", response_model=BranchResponse)
def update_branch(id: int, br: BranchUpdate, db: Session = Depends(get_db), current_user = Depends(require_admin)):
    db_br = db.query(Branch).filter(Branch.branch_id == id).first()
    if not db_br:
        raise HTTPException(status_code=404, detail="Branch not found")
    for key, value in br.model_dump(exclude_unset=True).items():
        setattr(db_br, key, value)
    db.commit()
    db.refresh(db_br)
    return db_br
    
@router.delete("/{id}")
def delete_branch(id: int, db: Session = Depends(get_db), current_user = Depends(require_admin)):
    db_br = db.query(Branch).filter(Branch.branch_id == id).first()
    if not db_br:
        raise HTTPException(status_code=404, detail="Branch not found")
    db.delete(db_br)
    db.commit()
    return {"message": "Branch deleted"}
'''
write_file('backend/api/branches.py', api_branches)

api_dashboard = '''
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database.connection import get_db
from models.account import Account
from models.customer import Customer
from models.transaction import Transaction
from models.employee import Employee
from auth.dependencies import get_current_user

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("/summary")
def get_dashboard_summary(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    accounts = db.query(func.count(Account.account_id)).scalar()
    customers = db.query(func.count(Customer.customer_id)).scalar()
    transactions = db.query(func.count(Transaction.transaction_id)).scalar()
    employees = db.query(func.count(Employee.employee_id)).scalar()
    return {
        "accounts": accounts,
        "customers": customers,
        "transactions": transactions,
        "employees": employees
    }
'''
write_file('backend/api/dashboard.py', api_dashboard)

api_audit_logs = '''
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.connection import get_db
from models.audit_log import AuditLog
from schemas.audit_log import AuditLogResponse
from auth.dependencies import get_current_user, require_admin

router = APIRouter(prefix="/api/audit-logs", tags=["Audit Logs"])

@router.get("/", response_model=list[AuditLogResponse])
def get_audit_logs(db: Session = Depends(get_db), current_user = Depends(require_admin)):
    return db.query(AuditLog).order_by(AuditLog.action_timestamp.desc()).limit(100).all()
'''
write_file('backend/api/audit_logs.py', api_audit_logs)

# Update main.py
main_py = '''
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.connection import engine, Base

import models
from api.customers import router as customers_router
from api.auth import router as auth_router
from api.transactions import router as transactions_router
from api.accounts import router as accounts_router
from api.employees import router as employees_router
from api.branches import router as branches_router
from api.dashboard import router as dashboard_router
from api.audit_logs import router as audit_logs_router

app = FastAPI(title="Bank Account Management API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(customers_router)
app.include_router(transactions_router)
app.include_router(accounts_router)
app.include_router(employees_router)
app.include_router(branches_router)
app.include_router(dashboard_router)
app.include_router(audit_logs_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
'''
write_file('backend/main.py', main_py)

print("Backend API scaffolding complete.")
