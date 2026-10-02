import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.connection import engine, Base

import models
from api.customers import router as customers_router
from api.auth import router as auth_router
from api.transactions import router as transactions_router
from api.accounts import router as accounts_router
from api.employees import router as employees_router
from api.branches import router as branches_router
from api.dashboard import router as dashboard_router
from api.audit_logs import router as audit_logs_router

app = FastAPI(title="Bank Account Management API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "*")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(customers_router)
app.include_router(transactions_router)
app.include_router(accounts_router)
app.include_router(employees_router)
app.include_router(branches_router)
app.include_router(dashboard_router)
app.include_router(audit_logs_router)

@app.get('/health')
def health_check():
    return {'status': 'healthy'}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000)); uvicorn.run("main:app", host="0.0.0.0", port=port)


