from pydantic import BaseModel, condecimal
from datetime import date
from typing import Optional

class AccountBase(BaseModel):
    customer_id: int
    branch_id: int
    account_number: str
    account_type: str
    balance: condecimal(max_digits=15, decimal_places=2) = 0.00
    status: str = "ACTIVE"
    opened_date: date

class AccountCreate(AccountBase):
    pass

class AccountUpdate(BaseModel):
    account_type: Optional[str] = None
    balance: Optional[condecimal(max_digits=15, decimal_places=2)] = None
    status: Optional[str] = None

class AccountResponse(AccountBase):
    account_id: int
    
    class Config:
        from_attributes = True
