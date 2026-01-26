import enum
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from core.models import IssueStatus

from users.schemas import UserResponse


class EduYearBase(BaseModel):
    name: str

class EduYearResponse(EduYearBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EduYearCreate(EduYearBase):
    pass


class SubjectBase(BaseModel):
    name: str

class SubjectResponse(SubjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SubjectCreate(SubjectBase):
    pass


class MeetingBase(BaseModel):
    name: str
    life_time: datetime
    input_time: datetime
    is_confirm: bool = False


class MeetingMonthlyCount(BaseModel):
    month: int
    count: int

class MeetingResponse(MeetingBase):
    id: int
    edu_year: EduYearResponse
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MeetingCreate(MeetingBase):
    edu_year_id: Optional[int] = None



class IssueBase(BaseModel):
    title: str
    user_id: int
    expired: datetime


class IssueResponse(IssueBase):
    id: int
    user: UserResponse
    meeting: MeetingResponse
    subject: SubjectResponse
    is_confirm: bool
    status: IssueStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class IssueCreate(IssueBase):
    pass


class IssueUpdate(IssueBase):
    meeting_id: int
    subject_id: int
    is_confirm: bool
    status: IssueStatus