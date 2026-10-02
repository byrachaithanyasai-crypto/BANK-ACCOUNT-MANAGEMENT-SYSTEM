from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database.connection import get_db
from models.user_account import UserAccount
from models.employee import Employee
from auth.jwt import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    
    user = db.query(UserAccount).filter(UserAccount.username == username).first()
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user account")
    
    return user

def require_admin(current_user: UserAccount = Depends(get_current_user)):
    if current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Not enough permissions. ADMIN role required.")
    return current_user

def require_manager(current_user: UserAccount = Depends(get_current_user)):
    if current_user.role not in ["ADMIN", "MANAGER"]:
        raise HTTPException(status_code=403, detail="Not enough permissions. MANAGER or ADMIN role required.")
    return current_user

def require_employee(current_user: UserAccount = Depends(get_current_user)):
    if current_user.role not in ["ADMIN", "MANAGER", "EMPLOYEE"]:
        raise HTTPException(status_code=403, detail="Not enough permissions.")
    return current_user
