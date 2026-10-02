from sqlalchemy import Column, Integer, String, JSON, TIMESTAMP, ForeignKey
from database.connection import Base
from datetime import datetime

class AuditLog(Base):
    __tablename__ = "AUDIT_LOG"
    
    log_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("USER_ACCOUNT.user_id"), nullable=True)
    action = Column(String(50), nullable=False)
    table_name = Column(String(50), nullable=False)
    record_id = Column(Integer, nullable=True)
    old_value = Column(JSON, nullable=True)
    new_value = Column(JSON, nullable=True)
    action_timestamp = Column(TIMESTAMP, default=datetime.utcnow)
