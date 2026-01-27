from decouple import config
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from app.database import get_db
from users.schemas import UserResponse, UserCreate, UserUpdate, LoginRequest, Token
from users import models

user_router = APIRouter(prefix='/users', tags=["users"])

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login/")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
SECRET_KEY = config("SECRET_KEY")


def hash_password(password):
    return pwd_context.hash(password)


def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"{e}")
    
    user = db.query(models.User).get(int(user_id))

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.post("/login/", response_model=Token)
def user_login(data: LoginRequest, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.username == data.username).first()

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id)})

    return {"access_token": token, "token_type": "bearer"}


@user_router.get("/me/", response_model=UserResponse)
def get_me(current_user: models.User = Depends(get_current_user)):
    
    return current_user


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

    hash_pass = hash_password(new_user.password)

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
