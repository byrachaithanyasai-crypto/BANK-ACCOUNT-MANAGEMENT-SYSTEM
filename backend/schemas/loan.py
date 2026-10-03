from pydantic import BaseModel, condecimal
from datetime import date
from typing import Optional

class LoanBase(BaseModel):
    customer_id: int
    branch_id: int
    loan_type: str
    principal_amount: condecimal(max_digits=15, decimal_places=2)
    interest_rate: condecimal(max_digits=5, decimal_places=2)
    term_months: int
    start_date: date
    end_date: Optional[date] = None
    status: str = "PENDING"
    outstanding_balance: condecimal(max_digits=15, decimal_places=2)
    loan_officer_id: Optional[int] = None

class LoanCreate(LoanBase):
    pass

class LoanUpdate(BaseModel):
    loan_type: Optional[str] = None
    principal_amount: Optional[condecimal(max_digits=15, decimal_places=2)] = None
    interest_rate: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    term_months: Optional[int] = None
    status: Optional[str] = None
    outstanding_balance: Optional[condecimal(max_digits=15, decimal_places=2)] = None
    loan_officer_id: Optional[int] = None

class LoanResponse(LoanBase):
    loan_id: int
    
    class Config:
        from_attributes = True
