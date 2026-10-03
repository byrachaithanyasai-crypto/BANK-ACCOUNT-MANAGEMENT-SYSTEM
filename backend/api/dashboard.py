from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database.connection import get_db
from models.account import Account
from models.customer import Customer
from models.transaction import Transaction
from models.employee import Employee
from models.loan import Loan
from auth.dependencies import get_current_user

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("/summary")
def get_dashboard_summary(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # Base Counts
    accounts = db.query(func.count(Account.account_id)).scalar() or 0
    customers = db.query(func.count(Customer.customer_id)).scalar() or 0
    transactions = db.query(func.count(Transaction.transaction_id)).scalar() or 0
    employees = db.query(func.count(Employee.employee_id)).scalar() or 0
    
    # Financials
    total_balance = db.query(func.sum(Account.balance)).scalar() or 0
    avg_balance = db.query(func.avg(Account.balance)).scalar() or 0
    
    total_deposits = db.query(func.sum(Transaction.amount)).filter(Transaction.transaction_type == 'DEPOSIT').scalar() or 0
    total_withdrawals = db.query(func.sum(Transaction.amount)).filter(Transaction.transaction_type == 'WITHDRAWAL').scalar() or 0
    
    # Distribution for charts
    acct_types = db.query(Account.account_type, func.count(Account.account_id)).group_by(Account.account_type).all()
    account_distribution = [{"name": t[0], "value": t[1]} for t in acct_types]
    
    acct_statuses = db.query(Account.status, func.count(Account.account_id)).group_by(Account.status).all()
    status_distribution = [{"name": s[0], "value": s[1]} for s in acct_statuses]
    
    tx_types = db.query(Transaction.transaction_type, func.count(Transaction.transaction_id)).group_by(Transaction.transaction_type).all()
    transaction_distribution = [{"name": t[0], "value": t[1]} for t in tx_types]

    active_accounts = db.query(func.count(Account.account_id)).filter(Account.status == 'ACTIVE').scalar() or 0

    # Loans
    total_loans = db.query(func.count(Loan.loan_id)).scalar() or 0
    active_loans = db.query(func.count(Loan.loan_id)).filter(Loan.status == 'ACTIVE').scalar() or 0
    pending_loans = db.query(func.count(Loan.loan_id)).filter(Loan.status == 'PENDING').scalar() or 0
    total_loan_amount = float(db.query(func.sum(Loan.principal_amount)).scalar() or 0)

    return {
        "accounts": accounts,
        "customers": customers,
        "transactions": transactions,
        "employees": employees,
        "total_balance": float(total_balance),
        "average_balance": float(avg_balance),
        "total_deposits": float(total_deposits),
        "total_withdrawals": float(total_withdrawals),
        "active_accounts": active_accounts,
        "account_distribution": account_distribution,
        "status_distribution": status_distribution,
        "transaction_distribution": transaction_distribution,
        
        "total_loans": total_loans,
        "active_loans": active_loans,
        "pending_loans": pending_loans,
        "total_loan_amount": total_loan_amount
    }
