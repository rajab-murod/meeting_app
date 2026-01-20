from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from database import get_db
from users.schemas import UserResponse, UserCreate, UserUpdate
from users import models

user_router = APIRouter(prefix='/users', tags=["users"])

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


@user_router.get("/{id}/", response_model=UserResponse)
def get_user(id: int, db:Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == id).first()
    if db_user:
        return db_user
    raise HTTPException(status_code=404, detail="User not found")


@user_router.get("/", response_model=List[UserResponse])
def list_all_user(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_user = db.query(models.User).offset(skip).limit(limit).all()
    return db_user


@user_router.post("/create/", response_model=UserResponse)
def create_user(new_user: UserCreate, db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.username == new_user.username).first()
    if user:
        raise HTTPException(status_code=400, detail="This username already exist.")

    hash_pass = pwd_context.hash(new_user.password)

    db_user = models.User(
        username = new_user.username,
        password = hash_pass,
    )

    if new_user.profile:
        db_user.profile = models.Profile(**new_user.profile.model_dump())

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@user_router.patch("/update/{id}/", response_model = UserResponse)
def update_user(id: int, new_user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == id).first()
    if db_user:
        new_data = new_user.model_dump(exclude_unset=True)
        if new_user.profile:
            for k, v in new_user.profile.model_dump(exclude_unset=True).items():
                setattr(db_user.profile, k, v)
            new_data.pop("profile")
            
        for k, v in new_data.items():
            setattr(db_user, k, v)
        db.commit()
        db.refresh(db_user)
    return db_user


@user_router.delete("/delete/{id}/", response_model=UserResponse)
def delete_user(id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return db_user
    raise HTTPException(status_code=404, detail="User not found")
