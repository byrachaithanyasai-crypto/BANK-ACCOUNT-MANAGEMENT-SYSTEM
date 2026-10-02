from models.audit_log import AuditLog

def log_audit(db, user_id, action, table_name, record_id):
    audit = AuditLog(user_id=user_id, action=action, table_name=table_name, record_id=record_id)
    db.add(audit)
