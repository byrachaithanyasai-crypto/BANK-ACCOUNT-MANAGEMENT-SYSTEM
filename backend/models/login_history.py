from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP, ForeignKey
from database.connection import Base
from datetime import datetime

class LoginHistory(Base):
    __tablename__ = "LOGIN_HISTORY"
    
    history_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("USER_ACCOUNT.user_id"), nullable=False)
    login_time = Column(TIMESTAMP, default=datetime.utcnow)
    ip_address = Column(String(45))
    status = Column(Enum('SUCCESS', 'FAILED'), nullable=False)
