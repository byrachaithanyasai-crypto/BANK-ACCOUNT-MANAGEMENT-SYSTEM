from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    kyc_status: str = "PENDING"
    date_of_birth: Optional[date] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    kyc_status: Optional[str] = None

class CustomerResponse(CustomerBase):
    customer_id: int
    
    class Config:
        from_attributes = True
