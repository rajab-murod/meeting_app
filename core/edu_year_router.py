from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.schemas import EduYearResponse, EduYearCreate
from core import models
from app.database import get_db
from baseviews.modelviews import ModelViewSet


edu_year_router = APIRouter(prefix="/edu_year", tags=["edu_year"])


class EduYearViewSet(ModelViewSet):
    def __init__(self, db: Session):
        super().__init__(db, model = models.EduYear)


@edu_year_router.get("/", response_model=List[EduYearResponse])
def list_edu_year(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return EduYearViewSet(db=db).list(skip=skip, limit=limit)


@edu_year_router.get("/{id}/", response_model=EduYearResponse)
def get_edu_year(id: int, db: Session = Depends(get_db)):
    return EduYearViewSet(db=db).get(obj_id=id)


@edu_year_router.post("/create/", response_model=EduYearResponse, status_code=201)
def create_edu_year(new_data: EduYearCreate, db: Session = Depends(get_db)):
    return EduYearViewSet(db=db).create(data=new_data.model_dump())


@edu_year_router.put("/update/{id}/", response_model=EduYearResponse)
def update_edu_year(id: int, new_data: EduYearCreate, db: Session = Depends(get_db)):
    return EduYearViewSet(db=db).update(obj_id=id, data=new_data.model_dump(exclude_unset=True))


@edu_year_router.delete("/delete/{id}/")
def delete_edu_year(id: int, db: Session = Depends(get_db)):
    return EduYearViewSet(db=db).delete(obj_id=id)
