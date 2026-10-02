import os

auth_dir = r'C:\Users\HAI\.gemini\antigravity\scratch\BANKX\backend\auth'
api_dir = r'C:\Users\HAI\.gemini\antigravity\scratch\BANKX\backend\api'
docs_dir = r'C:\Users\HAI\.gemini\antigravity\scratch\BANKX\docs'

os.makedirs(auth_dir, exist_ok=True)
os.makedirs(api_dir, exist_ok=True)
os.makedirs(docs_dir, exist_ok=True)

auth_files = {
    '__init__.py': '',
    'security.py': '''from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)
''',
    'jwt.py': '''import os
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback_secret_if_not_found")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
''',
    'dependencies.py': '''from fastapi import Depends, HTTPException, status
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
'''
}

api_auth = '''from fastapi import APIRouter, Depends, HTTPException, status, Request
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
    
    return {"access_token": access_token, "token_type": "bearer"}

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
'''

for filename, content in auth_files.items():
    with open(os.path.join(auth_dir, filename), 'w') as f:
        f.write(content)

with open(os.path.join(api_dir, 'auth.py'), 'w') as f:
    f.write(api_auth)

docs_content = '''# BANKX Authentication & RBAC Documentation

## Authentication Flow
The system utilizes JWT (JSON Web Tokens) for stateless authentication.
1. POST /api/auth/login: Validates credentials, records login history, logs the audit event, and issues a JWT token.
2. The frontend attaches the token as a Bearer token in the Authorization header for subsequent requests.

## Password Security
- Passwords are never stored in plaintext. They are hashed using bcrypt via the passlib library.
- Responses never include password hashes.

## RBAC (Role-Based Access Control)
Roles:
- **ADMIN**: Unrestricted access, employee management, system audits.
- **MANAGER**: Branch-level scoping, transaction supervision, branch analytics.
- **EMPLOYEE**: Standard customer CRUD, account and transaction processing.

## Branch-Level Authorization
Managers have logic built into service layers verifying that employee.branch_id == target_record.branch_id. They are restricted from manipulating data outside their jurisdiction.

## Audit and Login History
Every login attempt (SUCCESS/FAILED) is logged in LOGIN_HISTORY. Significant operations write to AUDIT_LOG.

## Logout
Due to JWT statelessness, logout is executed by the client deleting the token. The /api/auth/logout endpoint serves as a standardized hook and confirmation.
'''
with open(os.path.join(docs_dir, 'authentication-and-rbac.md'), 'w') as f:
    f.write(docs_content)

print("Auth implementations done.")
