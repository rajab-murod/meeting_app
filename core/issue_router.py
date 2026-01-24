from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from core import models, schemas
from database import get_db
from baseviews.modelviews import ModelViewSet

issue_router = APIRouter(prefix="/issues", tags=["issues"])

class IssueViewSet(ModelViewSet):
    def __init__(self, db):
        super().__init__(db, model = models.Issue)


@issue_router.get("/", response_model=List[schemas.IssueResponse])
def list_issue(db: Session = Depends(get_db), skip: int = 0, limit: int = 200):
    
    return IssueViewSet(db).list(skip=skip, limit=limit)


@issue_router.get("/{id}/", response_model=schemas.IssueResponse)
def get_issue(id: int, db: Session = Depends(get_db)):
    return IssueViewSet(db).get(obj_id=id)


@issue_router.post("/create/", response_model=schemas.IssueResponse, status_code=201)
def create_issue(new_data: schemas.IssueCreate, db: Session = Depends(get_db)):
    return IssueViewSet(db).create(new_data.model_dump())


@issue_router.patch("/update/{id}/", response_model=schemas.IssueResponse)
def update_issue(id: int, new_data: schemas.IssueCreate, db: Session = Depends(get_db)):
    return IssueViewSet(db).update(obj_id=id, data=new_data.model_dump(exclude_unset=True))


@issue_router.delete("/delete/{id}/")
def delete_issue(id: int, db: Session = Depends(get_db)):
    return IssueViewSet(db).delete(obj_id=id)