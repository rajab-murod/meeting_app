from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.schemas import EduYearResponse, EduYearCreate
from core import models
from database import get_db

core_router = APIRouter(prefix="/meeting", tags=["meeting"])


@core_router.get("/edu_year/", response_model=List[EduYearResponse])
def get_edu_year(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return db.query(models.EduYear).offset(skip).limit(limit).all()


@core_router.get("/edu_year/{id}/", response_model=EduYearResponse)
def get_edu_year(id: int, db: Session = Depends(get_db)):
    db_year = db.query(models.EduYear).filter(models.EduYear.id == id).first()
    if db_year:
        return db_year
    raise HTTPException(status_code=404, detail="EduYear not found")


@core_router.post("/edu_year/create/", response_model=EduYearResponse, status_code=201)
def create_edu_year(edu_year: EduYearCreate, db: Session = Depends(get_db)):
    db_edu_year = models.EduYear(**edu_year.model_dump())
    db.add(db_edu_year)
    db.commit()
    db.refresh(db_edu_year)
    return db_edu_year


@core_router.put("/edu_year/update/{id}/", response_model=EduYearResponse)
def update_edu_year(id: int, edu_y: EduYearCreate, db: Session = Depends(get_db)):
    db_edu_year = db.query(models.EduYear).filter(models.EduYear.id == id).first()
    if db_edu_year:
        update_data = edu_y.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_edu_year, key, value)
        db.commit()
        db.refresh(db_edu_year)
    return db_edu_year


@core_router.delete("/edu_year/delete/{id}/", response_model=EduYearResponse)
def delete_edu_year(id: int, db: Session = Depends(get_db)):
    db_edu_year = db.query(models.EduYear).filter(models.EduYear.id == id).first()
    if db_edu_year:
        db.delete(db_edu_year)
        db.commit()
        return db_edu_year
    raise HTTPException(status_code=404, detail="EduYear not found")
