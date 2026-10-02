from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Any

class AuditLogResponse(BaseModel):
    log_id: int
    user_id: Optional[int]
    action: str
    table_name: str
    record_id: Optional[int]
    old_value: Optional[Any]
    new_value: Optional[Any]
    action_timestamp: datetime
    
    class Config:
        from_attributes = True
