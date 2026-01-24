from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from core import models, schemas
from database import get_db
from baseviews.modelviews import ModelViewSet

meeting_router = APIRouter(prefix="/meetings", tags=["meetings"])

class MeetingViewSet(ModelViewSet):
    def __init__(self, db):
        super().__init__(db, model = models.Meeting)


@meeting_router.get("/", response_model=List[schemas.MeetingResponse])
def list_meeting(db: Session = Depends(get_db), month: int = 1, skip: int = 0, limit: int = 200):
    qt = db.query(models.Meeting).filter(func.extract('month', models.Meeting.life_time) == month) \
    .offset(skip) \
    .limit(limit) \
    .all()
    return qt


@meeting_router.get("/stat_by_month/", response_model=List[schemas.MeetingMonthlyCount])
def stat_meeting(db: Session = Depends(get_db), skip: int = 0, limit: int = 200):
    query = (db.query(
        func.extract('month', models.Meeting.life_time).label('month'),
        func.count(models.Meeting.id).label('count')
        ).group_by('month').offset(skip).limit(limit).all())
    return query


@meeting_router.get("/{id}/", response_model=schemas.MeetingResponse)
def get_meeting(id: int, db: Session = Depends(get_db)):
    return MeetingViewSet(db).get(obj_id=id)


@meeting_router.post("/create/", response_model=schemas.MeetingResponse, status_code=201)
def create_meeting(new_data: schemas.MeetingCreate, db: Session = Depends(get_db)):
    return MeetingViewSet(db).create(new_data.model_dump())


@meeting_router.patch("/update/{id}/", response_model=schemas.MeetingResponse)
def update_meeting(id: int, new_data: schemas.MeetingCreate, db: Session = Depends(get_db)):
    return MeetingViewSet(db).update(obj_id=id, data=new_data.model_dump(exclude_unset=True))


@meeting_router.delete("/delete/{id}/")
def delete_meeting(id: int, db: Session = Depends(get_db)):
    return MeetingViewSet(db).delete(obj_id=id)