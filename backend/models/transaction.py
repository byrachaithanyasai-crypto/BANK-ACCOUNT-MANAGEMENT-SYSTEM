from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Numeric, Text, TIMESTAMP, func
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
