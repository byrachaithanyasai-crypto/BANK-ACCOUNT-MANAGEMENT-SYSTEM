from pydantic import BaseModel, condecimal
from datetime import datetime
from typing import Optional

class TransactionBase(BaseModel):
    account_id: int
    transaction_type: str
    amount: condecimal(max_digits=15, decimal_places=2)
    status: str = "COMPLETED"
    reference_number: Optional[str] = None
    description: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    transaction_id: int
    transaction_date: datetime
    
    class Config:
        from_attributes = True
