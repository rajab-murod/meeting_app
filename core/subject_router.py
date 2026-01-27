from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core import models, schemas
from app.database import get_db
from baseviews.modelviews import ModelViewSet

subject_router = APIRouter(prefix="/subjects", tags=["subjects"])

class SubjectViewSet(ModelViewSet):
    def __init__(self, db):
        super().__init__(db, model = models.Subject)


@subject_router.get("/", response_model=List[schemas.SubjectResponse])
def list_subject(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return SubjectViewSet(db).list()


@subject_router.get("/{id}/", response_model=schemas.SubjectResponse)
def get_subject(id: int, db: Session = Depends(get_db)):
    return SubjectViewSet(db).get(obj_id=id)


@subject_router.post("/create/", response_model=schemas.SubjectResponse, status_code=201)
def create_subject(new_data: schemas.SubjectCreate, db: Session = Depends(get_db)):
    return SubjectViewSet(db).create(new_data.model_dump())


@subject_router.patch("/update/{id}/", response_model=schemas.SubjectResponse)
def update_subject(id: int, new_data: schemas.SubjectCreate, db: Session = Depends(get_db)):
    return SubjectViewSet(db).update(obj_id=id, data=new_data.model_dump(exclude_unset=True))


@subject_router.delete("/delete/{id}/")
def delete_subject(id: int, db: Session = Depends(get_db)):
    return SubjectViewSet(db).delete(obj_id=id)