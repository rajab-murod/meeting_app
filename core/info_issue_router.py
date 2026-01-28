import os
import shutil
from typing import List, Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session

from core import models, schemas
from app.database import get_db
from baseviews.modelviews import ModelViewSet

info_issue_router = APIRouter(prefix="/info-issues", tags=["info-issues"])


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class InfoIssueViewSet(ModelViewSet):
    def __init__(self, db):
        super().__init__(db, model = models.InfoIssue)


@info_issue_router.get("/", response_model=List[schemas.InfoIssueResponse])
def list_info_issue(db: Session = Depends(get_db), issue_id: Optional[int] = None, skip: int = 0, limit: int = 200):
    if issue_id:
        return db.query(models.InfoIssue).filter(models.InfoIssue.issue_id == issue_id).offset(skip).limit(limit).all()
    return InfoIssueViewSet(db).list(skip=skip, limit=limit)


@info_issue_router.get("/{id}/", response_model=schemas.InfoIssueResponse)
def get_info_issue(id: int, db: Session = Depends(get_db)):
    return InfoIssueViewSet(db).get(obj_id=id)


@info_issue_router.post("/create/", response_model=schemas.InfoIssueResponse, status_code=201)
def create_info_issue(content: str = Form(...), issue_id: int = Form(...), file: UploadFile = File(None), db: Session = Depends(get_db)):
    file_location = ""
    
    if file:
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    
    db_info = models.InfoIssue(
    issue_id=issue_id, 
    content=content, 
    file_path=file_location
    )
    db.add(db_info)
    db.commit()
    db.refresh(db_info)
    return db_info
    

@info_issue_router.patch("/update/{id}/", response_model=schemas.InfoIssueResponse)
def update_info_issue(id: int, new_data: schemas.InfoIssueUpdate, db: Session = Depends(get_db)):
    return InfoIssueViewSet(db).update(obj_id=id, data=new_data.model_dump(exclude_unset=True))


@info_issue_router.delete("/delete/{id}/")
def delete_info_issue(id: int, db: Session = Depends(get_db)):
    return InfoIssueViewSet(db).delete(obj_id=id)

