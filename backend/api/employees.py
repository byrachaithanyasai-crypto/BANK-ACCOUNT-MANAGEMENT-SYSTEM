from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from models.employee import Employee
from schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from api.audit_helper import log_audit
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
    log_audit(db, current_user.user_id, 'CREATE', 'EMP', db_emp.employee_id)
    db.commit()
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
    log_audit(db, current_user.user_id, 'CREATE', 'EMP', db_emp.employee_id)
    db.commit()
    return db_emp

@router.delete("/{id}")
def delete_employee(id: int, db: Session = Depends(get_db), current_user = Depends(require_admin)):
    db_emp = db.query(Employee).filter(Employee.employee_id == id).first()
    if not db_emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    log_audit(db, current_user.user_id, 'DELETE', 'EMP', id)
    db.delete(db_emp)
    db.commit()
    return {"message": "Employee deleted"}
