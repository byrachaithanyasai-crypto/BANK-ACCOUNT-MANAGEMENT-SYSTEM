from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from database.connection import get_db
from models.user_account import UserAccount
from models.employee import Employee
from models.login_history import LoginHistory
from models.audit_log import AuditLog
from schemas.auth import LoginRequest, Token
from auth.security import verify_password, get_password_hash
from auth.jwt import create_access_token
from auth.dependencies import get_current_user
from datetime import datetime

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/login", response_model=Token)
def login(request: Request, login_data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(UserAccount).filter(UserAccount.username == login_data.username).first()
    
    client_host = request.client.host if request.client else "Unknown"
    
    if not user or not verify_password(login_data.password, user.password_hash):
        if user:
            # Log failed attempt
            history = LoginHistory(user_id=user.user_id, status='FAILED', ip_address=client_host)
            db.add(history)
            db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is inactive")
        
    # Generate token
    access_token = create_access_token(data={"sub": user.username, "role": user.role})
    
    # Update last login
    user.last_login = datetime.utcnow()
    
    # Log successful login
    history = LoginHistory(user_id=user.user_id, status='SUCCESS', ip_address=client_host)
    db.add(history)
    
    # Audit logging
    audit = AuditLog(user_id=user.user_id, action="LOGIN", table_name="USER_ACCOUNT", record_id=user.user_id)
    db.add(audit)
    
    db.commit()
    
    return {"access_token": access_token, "token_type": "bearer", "user": {"username": user.username, "role": user.role}}

@router.get("/me")
def read_users_me(current_user: UserAccount = Depends(get_current_user), db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.employee_id == current_user.employee_id).first()
    return {
        "user_id": current_user.user_id,
        "username": current_user.username,
        "role": current_user.role,
        "employee_id": current_user.employee_id,
        "employee_name": f"{employee.first_name} {employee.last_name}" if employee else None,
        "branch_id": employee.branch_id if employee else None,
        "is_active": current_user.is_active,
        "last_login": current_user.last_login
    }

@router.post("/logout")
def logout():
    # Since JWT is stateless, the frontend must discard the token.
    # A true server-side invalidation would require a token blacklist table.
    return {"message": "Successfully logged out. Please discard your token."}

from pydantic import BaseModel
class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str

@router.post("/change-password")
def change_password(
    data: ChangePasswordRequest, 
    current_user: UserAccount = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    if not verify_password(data.current_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect current password")
    
    current_user.password_hash = get_password_hash(data.new_password)
    
    audit = AuditLog(user_id=current_user.user_id, action="UPDATE_PASSWORD", table_name="USER_ACCOUNT", record_id=current_user.user_id)
    db.add(audit)
    
    db.commit()
    return {"message": "Password updated successfully"}
