from sqlalchemy import Column, Integer, String, DECIMAL, Date, Enum, ForeignKey, Numeric
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
