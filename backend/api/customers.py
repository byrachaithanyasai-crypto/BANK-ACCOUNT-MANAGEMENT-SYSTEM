from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from models.customer import Customer
from schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse
from api.audit_helper import log_audit
from auth.dependencies import get_current_user, require_manager, require_admin

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
    log_audit(db, current_user.user_id, 'CREATE', 'CUST', db_cust.customer_id)
    db.commit()
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
    log_audit(db, current_user.user_id, 'CREATE', 'CUST', db_cust.customer_id)
    db.commit()
    return db_cust

@router.delete("/{id}")
def delete_customer(id: int, db: Session = Depends(get_db), current_user = Depends(require_admin)):
    db_cust = db.query(Customer).filter(Customer.customer_id == id).first()
    if not db_cust:
        raise HTTPException(status_code=404, detail="Customer not found")
    log_audit(db, current_user.user_id, 'DELETE', 'CUST', id)
    db.delete(db_cust)
    db.commit()
    return {"message": "Customer deleted successfully"}

