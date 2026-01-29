from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core import models, schemas
from app.database import get_db
from baseviews.modelviews import ModelViewSet

qsn_router = APIRouter(prefix="/questions", tags=["questions"])

class QuestionViewSet(ModelViewSet):
    def __init__(self, db):
        super().__init__(db, model = models.Question)


@qsn_router.get("/", response_model=List[schemas.QuestionResponse])
def list_question(db: Session = Depends(get_db), meeting_id: Optional[int] = None, skip: int = 0, limit: int = 200):
    if meeting_id:
        return db.query(models.Question).filter(models.Question.meeting_id == meeting_id) \
            .offset(skip) \
            .limit(limit).all()
    return QuestionViewSet(db).list(skip=skip, limit=limit)


@qsn_router.get("/{id}/", response_model=schemas.QuestionResponse)
def get_question(id: int, db: Session = Depends(get_db)):
    return QuestionViewSet(db).get(obj_id=id)


@qsn_router.post("/create/", response_model=schemas.QuestionResponse, status_code=201)
def create_question(new_data: schemas.QuestionCreate, db: Session = Depends(get_db)):
    return QuestionViewSet(db).create(new_data.model_dump())


@qsn_router.patch("/update/{id}/", response_model=schemas.QuestionResponse)
def update_question(id: int, new_data: schemas.QuestionUpdate, db: Session = Depends(get_db)):
    return QuestionViewSet(db).update(obj_id=id, data=new_data.model_dump(exclude_unset=True))


@qsn_router.delete("/delete/{id}/")
def delete_question(id: int, db: Session = Depends(get_db)):
    return QuestionViewSet(db).delete(obj_id=id)
