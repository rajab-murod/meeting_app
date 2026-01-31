from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy import distinct, func
from sqlalchemy.orm import Session

from core import models, schemas
from users.models import User, Profile
from app.database import get_db
from baseviews.modelviews import ModelViewSet

att_router = APIRouter(prefix="/attendances", tags=["attendances"])

class AttendanceViewSet(ModelViewSet):
    def __init__(self, db):
        super().__init__(db, model = models.Attendance)


@att_router.get("/", response_model=List[schemas.AttendanceResponse])
def list_attendance(db: Session = Depends(get_db), meeting_id: Optional[int] = None, skip: int = 0, limit: int = 200):
    if meeting_id:
        return db.query(models.Attendance).filter(models.Attendance.meeting_id == meeting_id) \
            .offset(skip) \
            .limit(limit).all()
    return AttendanceViewSet(db).list(skip=skip, limit=limit)


@att_router.get("/stat_by_meeting/", response_model=List[schemas.AttStatByMeeting])
def stat_by_meeting(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    qt = (
        db.query(
            models.Meeting.id,
            models.Meeting.name,
            func.count(distinct(models.Attendance.id)).label('att_count')
            )
            .outerjoin(models.Attendance, models.Meeting.id == models.Attendance.meeting_id)
            .group_by(models.Meeting.id, models.Meeting.name)
            .offset(skip).limit(limit).all()
    )
    return qt


@att_router.get("/stat_by_meeting_detail/",response_model=List[schemas.AttStatByMeetingDetail])
def stat_by_meeting_detail(meeting_id: int, db: Session = Depends(get_db)):
    results = (
        db.query(
            (User.id).label('id'),
            (Profile.first_name).label('first_name'),
            (Profile.last_name).label('last_name'),
            (func.count(models.Attendance.id).label('count'))
        )
        .select_from(User)
        .outerjoin(Profile, User.id == Profile.user_id)
        .outerjoin(
            models.Attendance,
              (models.Attendance.user_id == User.id)
                & (models.Attendance.meeting_id == meeting_id)
                )
        .filter(User.is_active == True)
        .group_by(Profile.first_name, Profile.last_name, User.id)
        .order_by('count')
        .all()
    )

    return results


@att_router.get("/stat_by_edu_year/", response_model=schemas.AttStatByEduYear)
def stat_by_edu_year(edu_year_id: int, db: Session = Depends(get_db)):
    meeting_count = db.query(models.Meeting).filter(
        models.Meeting.edu_year_id == edu_year_id).count()
    results = (
        db.query(
            (User.id).label('id'),
            (Profile.first_name).label('first_name'),
            (Profile.last_name).label('last_name'),
            (func.count(distinct(models.Attendance.id)).label('count'))
        )
        .select_from(User)
        .outerjoin(Profile, User.id == Profile.user_id)
        .outerjoin(
            models.Attendance,
              (models.Attendance.user_id == User.id) )
        .filter(User.is_active == True)
        .group_by(Profile.first_name, Profile.last_name, User.id)
        .order_by('count')
        .all()
    )
    
    return {"total": meeting_count, "data": results}


@att_router.get("/{id}/", response_model=schemas.AttendanceResponse)
def get_attendance(id: int, db: Session = Depends(get_db)):
    return AttendanceViewSet(db).get(obj_id=id)


@att_router.post("/create/", response_model=schemas.AttendanceResponse, status_code=201)
def create_attendance(new_data: schemas.AttendanceCreate, db: Session = Depends(get_db)):
    return AttendanceViewSet(db).create(new_data.model_dump())


@att_router.patch("/update/{id}/", response_model=schemas.AttendanceResponse)
def update_attendance(id: int, new_data: schemas.AttendanceUpdate, db: Session = Depends(get_db)):
    return AttendanceViewSet(db).update(obj_id=id, data=new_data.model_dump(exclude_unset=True))


@att_router.delete("/delete/{id}/")
def delete_attendance(id: int, db: Session = Depends(get_db)):
    return AttendanceViewSet(db).delete(obj_id=id)
