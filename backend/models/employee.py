from sqlalchemy import Column, Integer, String, Date, ForeignKey
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
