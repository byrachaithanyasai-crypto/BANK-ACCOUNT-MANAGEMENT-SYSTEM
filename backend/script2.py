import os

schemas_dir = r'C:\Users\HAI\.gemini\antigravity\scratch\BANKX\backend\schemas'
api_dir = r'C:\Users\HAI\.gemini\antigravity\scratch\BANKX\backend\api'
os.makedirs(schemas_dir, exist_ok=True)
os.makedirs(api_dir, exist_ok=True)

schemas = {
    '__init__.py': '',
    'customer.py': '''from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    kyc_status: str = 'PENDING'
    date_of_birth: Optional[date] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    customer_id: int
    class Config:
        from_attributes = True
''',
    'auth.py': '''from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    username: str
    password: str
'''
}

apis = {
    '__init__.py': '',
    'customers.py': '''from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from models.customer import Customer
from schemas.customer import CustomerCreate, CustomerResponse

router = APIRouter(prefix="/api/customers", tags=["Customers"])

@router.get("/", response_model=list[CustomerResponse])
def get_customers(db: Session = Depends(get_db)):
    return db.query(Customer).all()

@router.post("/", response_model=CustomerResponse)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    db_customer = Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer
''',
    'auth.py': '''from fastapi import APIRouter
router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/login")
def login():
    return {"access_token": "fake-token", "token_type": "bearer"}
''',
    'transactions.py': '''from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from sqlalchemy import text
from pydantic import BaseModel
from decimal import Decimal

class TransactionRequest(BaseModel):
    account_id: int
    amount: Decimal
    description: str = ""

router = APIRouter(prefix="/api/transactions", tags=["Transactions"])

@router.post("/deposit")
def deposit(req: TransactionRequest, db: Session = Depends(get_db)):
    try:
        db.execute(text("CALL sp_deposit_money(:acc, :amt, :desc)"), 
            {"acc": req.account_id, "amt": req.amount, "desc": req.description})
        db.commit()
        return {"status": "success", "message": "Deposit successful"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/withdraw")
def withdraw(req: TransactionRequest, db: Session = Depends(get_db)):
    try:
        db.execute(text("CALL sp_withdraw_money(:acc, :amt, :desc)"), 
            {"acc": req.account_id, "amt": req.amount, "desc": req.description})
        db.commit()
        return {"status": "success", "message": "Withdrawal successful"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
'''
}

for filename, content in schemas.items():
    with open(os.path.join(schemas_dir, filename), 'w') as f:
        f.write(content)

for filename, content in apis.items():
    with open(os.path.join(api_dir, filename), 'w') as f:
        f.write(content)

print("Schemas and APIs created.")
