from sqlalchemy import Column, Integer, String, Enum, Boolean, TIMESTAMP, ForeignKey
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
