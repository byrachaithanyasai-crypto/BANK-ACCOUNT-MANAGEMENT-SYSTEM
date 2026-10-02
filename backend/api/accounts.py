from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from models.account import Account
from schemas.account import AccountCreate, AccountUpdate, AccountResponse
from api.audit_helper import log_audit
from auth.dependencies import get_current_user, require_manager, require_admin

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
    log_audit(db, current_user.user_id, 'CREATE', 'ACC', db_acc.account_id)
    db.commit()
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
    log_audit(db, current_user.user_id, 'CREATE', 'ACC', db_acc.account_id)
    db.commit()
    return db_acc

@router.delete("/{id}")
def delete_account(id: int, db: Session = Depends(get_db), current_user = Depends(require_admin)):
    db_acc = db.query(Account).filter(Account.account_id == id).first()
    if not db_acc:
        raise HTTPException(status_code=404, detail="Account not found")
    log_audit(db, current_user.user_id, 'DELETE', 'ACC', id)
    db.delete(db_acc)
    db.commit()
    return {"message": "Account deleted successfully"}

