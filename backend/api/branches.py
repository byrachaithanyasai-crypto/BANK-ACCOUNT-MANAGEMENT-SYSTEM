from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from models.branch import Branch
from schemas.branch import BranchCreate, BranchUpdate, BranchResponse
from api.audit_helper import log_audit
from auth.dependencies import get_current_user, require_admin

router = APIRouter(prefix="/api/branches", tags=["Branches"])

@router.get("/", response_model=list[BranchResponse])
def get_branches(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(Branch).all()

@router.post("/", response_model=BranchResponse)
def create_branch(br: BranchCreate, db: Session = Depends(get_db), current_user = Depends(require_admin)):
    db_br = Branch(**br.model_dump())
    db.add(db_br)
    db.commit()
    db.refresh(db_br)
    return db_br

@router.put("/{id}", response_model=BranchResponse)
def update_branch(id: int, br: BranchUpdate, db: Session = Depends(get_db), current_user = Depends(require_admin)):
    db_br = db.query(Branch).filter(Branch.branch_id == id).first()
    if not db_br:
        raise HTTPException(status_code=404, detail="Branch not found")
    for key, value in br.model_dump(exclude_unset=True).items():
        setattr(db_br, key, value)
    db.commit()
    db.refresh(db_br)
    return db_br
    
@router.delete("/{id}")
def delete_branch(id: int, db: Session = Depends(get_db), current_user = Depends(require_admin)):
    db_br = db.query(Branch).filter(Branch.branch_id == id).first()
    if not db_br:
        raise HTTPException(status_code=404, detail="Branch not found")
    log_audit(db, current_user.user_id, 'DELETE', 'BRANCH', id)
    db.delete(db_br)
    db.commit()
    return {"message": "Branch deleted"}

