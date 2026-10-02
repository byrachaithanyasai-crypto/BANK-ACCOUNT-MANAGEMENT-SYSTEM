import os

def insert_audit(filepath, entity_name, id_field):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Add import
    if "from api.audit_helper import log_audit" not in content:
        content = content.replace("from auth.dependencies import", "from api.audit_helper import log_audit\nfrom auth.dependencies import")
    
    # POST
    content = content.replace(f"db.refresh(db_{entity_name})", f"db.refresh(db_{entity_name})\n    log_audit(db, current_user.user_id, 'CREATE', '{entity_name.upper()}', db_{entity_name}.{id_field})\n    db.commit()")
    
    # PUT
    content = content.replace(f"db.refresh(db_{entity_name})\n    return db_{entity_name}", f"db.refresh(db_{entity_name})\n    log_audit(db, current_user.user_id, 'UPDATE', '{entity_name.upper()}', db_{entity_name}.{id_field})\n    db.commit()\n    return db_{entity_name}")
    
    # DELETE
    content = content.replace("db.delete(", f"log_audit(db, current_user.user_id, 'DELETE', '{entity_name.upper()}', id)\n    db.delete(")
    
    with open(filepath, 'w') as f:
        f.write(content)

insert_audit('backend/api/customers.py', 'cust', 'customer_id')
insert_audit('backend/api/accounts.py', 'acc', 'account_id')
insert_audit('backend/api/employees.py', 'emp', 'employee_id')
insert_audit('backend/api/branches.py', 'branch', 'branch_id')

