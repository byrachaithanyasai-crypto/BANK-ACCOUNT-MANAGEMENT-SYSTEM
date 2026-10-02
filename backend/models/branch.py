from sqlalchemy import Column, Integer, String, Text
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
