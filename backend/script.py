import os

base_dir = r'C:\Users\HAI\.gemini\antigravity\scratch\BANKX\backend\models'
os.makedirs(base_dir, exist_ok=True)

models = {
    '__init__.py': '',
    'customer.py': '''from sqlalchemy import Column, Integer, String, Date, Text, Enum
from sqlalchemy.orm import relationship
from database.connection import Base

class Customer(Base):
    __tablename__ = "CUSTOMER"
    customer_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=False)
    address = Column(Text)
    city = Column(String(50))
    state = Column(String(50))
    zip_code = Column(String(20))
    kyc_status = Column(Enum('PENDING', 'VERIFIED', 'REJECTED'), default='PENDING')
    date_of_birth = Column(Date)
    
    accounts = relationship("Account", back_populates="customer")
    loans = relationship("Loan", back_populates="customer")
''',
    'account.py': '''from sqlalchemy import Column, Integer, String, Decimal, Date, Enum, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from database.connection import Base

class Account(Base):
    __tablename__ = "ACCOUNT"
    account_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("CUSTOMER.customer_id"), nullable=False)
    branch_id = Column(Integer, ForeignKey("BRANCH.branch_id"), nullable=False)
    account_number = Column(String(20), unique=True, nullable=False)
    account_type = Column(Enum('SAVINGS', 'CHECKING', 'BUSINESS'), nullable=False)
    balance = Column(Numeric(15, 2), default=0.00)
    status = Column(Enum('ACTIVE', 'DORMANT', 'CLOSED', 'FROZEN'), default='ACTIVE')
    opened_date = Column(Date, nullable=False)
    
    customer = relationship("Customer", back_populates="accounts")
    branch = relationship("Branch", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")
''',
    'transaction.py': '''from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Numeric, Text, TIMESTAMP, func
from sqlalchemy.orm import relationship
from database.connection import Base

class Transaction(Base):
    __tablename__ = "TRANSACTION"
    transaction_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey("ACCOUNT.account_id"), nullable=False)
    transaction_type = Column(Enum('DEPOSIT', 'WITHDRAWAL', 'TRANSFER'), nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    transaction_date = Column(TIMESTAMP, server_default=func.now())
    status = Column(Enum('PENDING', 'COMPLETED', 'FAILED', 'REVERTED'), default='COMPLETED')
    reference_number = Column(String(50), unique=True)
    description = Column(Text)
    
    account = relationship("Account", back_populates="transactions")
''',
    'branch.py': '''from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from database.connection import Base

class Branch(Base):
    __tablename__ = "BRANCH"
    branch_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    branch_code = Column(String(20), unique=True, nullable=False)
    branch_name = Column(String(100), nullable=False)
    address = Column(Text)
    city = Column(String(50))
    state = Column(String(50))
    zip_code = Column(String(20))
    phone = Column(String(20))
    
    accounts = relationship("Account", back_populates="branch")
    employees = relationship("Employee", back_populates="branch")
''',
    'employee.py': '''from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database.connection import Base

class Employee(Base):
    __tablename__ = "EMPLOYEE"
    employee_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    branch_id = Column(Integer, ForeignKey("BRANCH.branch_id"))
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20))
    position = Column(String(50))
    hire_date = Column(Date)
    
    branch = relationship("Branch", back_populates="employees")
    user_account = relationship("UserAccount", back_populates="employee", uselist=False)
''',
    'loan.py': '''from sqlalchemy import Column, Integer, Enum, Date, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from database.connection import Base

class Loan(Base):
    __tablename__ = "LOAN"
    loan_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("CUSTOMER.customer_id"), nullable=False)
    branch_id = Column(Integer, ForeignKey("BRANCH.branch_id"), nullable=False)
    loan_type = Column(Enum('PERSONAL', 'HOME', 'AUTO', 'BUSINESS'), nullable=False)
    principal_amount = Column(Numeric(15, 2), nullable=False)
    interest_rate = Column(Numeric(5, 2), nullable=False)
    term_months = Column(Integer, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    status = Column(Enum('ACTIVE', 'CLOSED', 'DEFAULTED', 'PENDING'), default='PENDING')
    outstanding_balance = Column(Numeric(15, 2), nullable=False)
    
    customer = relationship("Customer", back_populates="loans")
''',
    'user_account.py': '''from sqlalchemy import Column, Integer, String, Enum, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from database.connection import Base

class UserAccount(Base):
    __tablename__ = "USER_ACCOUNT"
    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum('ADMIN', 'MANAGER', 'EMPLOYEE'), nullable=False)
    employee_id = Column(Integer, ForeignKey("EMPLOYEE.employee_id", ondelete="CASCADE"))
    is_active = Column(Boolean, default=True)
    last_login = Column(TIMESTAMP)
    
    employee = relationship("Employee", back_populates="user_account")
'''
}

for filename, content in models.items():
    with open(os.path.join(base_dir, filename), 'w') as f:
        f.write(content)

print("Models created.")
