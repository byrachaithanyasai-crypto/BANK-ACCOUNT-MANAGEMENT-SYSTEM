from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.connection import get_db
from models.audit_log import AuditLog
from schemas.audit_log import AuditLogResponse
from auth.dependencies import get_current_user, require_admin

router = APIRouter(prefix="/api/audit-logs", tags=["Audit Logs"])

@router.get("/", response_model=list[AuditLogResponse])
def get_audit_logs(db: Session = Depends(get_db), current_user = Depends(require_admin)):
    return db.query(AuditLog).order_by(AuditLog.action_timestamp.desc()).limit(100).all()
