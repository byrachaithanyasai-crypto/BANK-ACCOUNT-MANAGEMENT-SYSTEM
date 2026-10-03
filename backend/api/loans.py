from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from models.loan import Loan
from schemas.loan import LoanCreate, LoanUpdate, LoanResponse
from api.audit_helper import log_audit
from auth.dependencies import get_current_user, require_manager, require_admin

router = APIRouter(prefix="/api/loans", tags=["Loans"])

@router.get("/", response_model=list[LoanResponse])
def get_loans(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(Loan).all()

@router.get("/{id}", response_model=LoanResponse)
def get_loan(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    loan = db.query(Loan).filter(Loan.loan_id == id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan

@router.post("/", response_model=LoanResponse)
def create_loan(loan: LoanCreate, db: Session = Depends(get_db), current_user = Depends(require_manager)):
    db_loan = Loan(**loan.model_dump())
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    log_audit(db, current_user.user_id, 'CREATE', 'LOAN', db_loan.loan_id)
    db.commit()
    return db_loan

@router.put("/{id}", response_model=LoanResponse)
def update_loan(id: int, loan: LoanUpdate, db: Session = Depends(get_db), current_user = Depends(require_manager)):
    db_loan = db.query(Loan).filter(Loan.loan_id == id).first()
    if not db_loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    update_data = loan.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_loan, key, value)
    db.commit()
    db.refresh(db_loan)
    log_audit(db, current_user.user_id, 'UPDATE', 'LOAN', db_loan.loan_id)
    db.commit()
    return db_loan

@router.delete("/{id}")
def delete_loan(id: int, db: Session = Depends(get_db), current_user = Depends(require_admin)):
    db_loan = db.query(Loan).filter(Loan.loan_id == id).first()
    if not db_loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    log_audit(db, current_user.user_id, 'DELETE', 'LOAN', id)
    db.delete(db_loan)
    db.commit()
    return {"message": "Loan deleted successfully"}
