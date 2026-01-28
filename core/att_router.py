from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core import models, schemas
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
