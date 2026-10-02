from sqlalchemy import Column, Integer, Enum, Date, ForeignKey, Numeric
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
