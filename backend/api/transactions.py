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
