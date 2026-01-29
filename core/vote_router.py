from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy import distinct, func
from sqlalchemy.orm import Session

from core import models, schemas
from app.database import get_db
from baseviews.modelviews import ModelViewSet

vote_router = APIRouter(prefix="/votes", tags=["votes"])

class VoteViewSet(ModelViewSet):
    def __init__(self, db):
        super().__init__(db, model = models.Vote)


@vote_router.get("/", response_model=List[schemas.VoteResponse])
def list_vote(db: Session = Depends(get_db),
               meeting_id: Optional[int] = None,
            issue_id: Optional[int] = None, skip: int = 0, limit: int = 200):
    if meeting_id and issue_id:
        return db.query(models.Vote).filter(models.Vote.meeting_id == meeting_id and models.Vote.issue_id == issue_id) \
            .offset(skip) \
            .limit(limit).all()
    return VoteViewSet(db).list(skip=skip, limit=limit)


@vote_router.get("/stats/", response_model=List[schemas.VoteStat])
def stat_by_meeting(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    query = (db.query(
        (models.Meeting.id).label('id'),
        (models.Meeting.name).label('name'),
        (models.Vote.status).label('status'),
        func.count(distinct(models.Vote.id)).label('vote_count'),
        func.count(distinct(models.Attendance.id)).label('att_count')
        )
        .outerjoin(models.Vote, models.Meeting.id == models.Vote.meeting_id)
        .outerjoin(models.Attendance, models.Meeting.id == models.Attendance.meeting_id)
        .group_by(models.Meeting.id, models.Meeting.name, models.Vote.status)
        .offset(skip).limit(limit).all()
        )
    return query


@vote_router.get("/{id}/", response_model=schemas.VoteResponse)
def get_vote(id: int, db: Session = Depends(get_db)):
    return VoteViewSet(db).get(obj_id=id)


@vote_router.post("/create/", response_model=schemas.VoteResponse, status_code=201)
def create_vote(new_data: schemas.VoteCreate, db: Session = Depends(get_db)):
    return VoteViewSet(db).create(new_data.model_dump())


@vote_router.patch("/update/{id}/", response_model=schemas.VoteResponse)
def update_vote(id: int, new_data: schemas.VoteUpdate, db: Session = Depends(get_db)):
    return VoteViewSet(db).update(obj_id=id, data=new_data.model_dump(exclude_unset=True))


@vote_router.delete("/delete/{id}/")
def delete_vote(id: int, db: Session = Depends(get_db)):
    return VoteViewSet(db).delete(obj_id=id)
