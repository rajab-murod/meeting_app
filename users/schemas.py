from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ProfileBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileBase):
    pass


class ProfileResponse(ProfileBase):
    id: int
    user_id: int
    updated_at: datetime

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=50)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    password: Optional[str] = Field(..., min_length=6, max_length=50)
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    profile: Optional[ProfileResponse] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
