from sqlalchemy import Column, Integer, String, Date, Text, Enum
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
