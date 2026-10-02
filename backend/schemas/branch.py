from pydantic import BaseModel
from typing import Optional

class BranchBase(BaseModel):
    branch_code: str
    branch_name: str
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    phone: Optional[str] = None

class BranchCreate(BranchBase):
    pass

class BranchUpdate(BaseModel):
    branch_code: Optional[str] = None
    branch_name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    phone: Optional[str] = None

class BranchResponse(BranchBase):
    branch_id: int
    
    class Config:
        from_attributes = True
