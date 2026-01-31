from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from core.models import IssueStatus, VoteStatus, VoteType

from users.schemas import UserResponse


class EduYearBase(BaseModel):
    name: str

class EduYearResponse(EduYearBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class EduYearCreate(EduYearBase):
    pass


class SubjectBase(BaseModel):
    name: str

class SubjectResponse(SubjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


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

    model_config = ConfigDict(from_attributes=True)


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

    model_config = ConfigDict(from_attributes=True)


class IssueCreate(IssueBase):
    pass


class IssueUpdate(IssueBase):
    meeting_id: int
    subject_id: int
    is_confirm: bool
    status: IssueStatus


class InfoIssueBase(BaseModel):
    content: str
    

class InfoIssueResponse(InfoIssueBase):
    id: int
    issue: IssueResponse
    file_path: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class InfoIssueCreate(InfoIssueBase):
    issue_id: int


class InfoIssueUpdate(InfoIssueBase):
    issue_id: int


class AttendanceBase(BaseModel):
    date: datetime
    

class AttendanceResponse(AttendanceBase):
    id: int
    user: UserResponse
    meeting: MeetingResponse
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AttStatByMeeting(BaseModel):
    id: int
    name: str
    att_count: int


class AttStatByMeetingDetail(BaseModel):
    id: int
    first_name: str
    last_name: str
    count: int


class AttStatByEduYear(BaseModel):
    total: int
    data: List[AttStatByMeetingDetail]


class AttendanceCreate(AttendanceBase):
    meeting_id: int
    user_id: int


class AttendanceUpdate(AttendanceBase):
    meeting_id: int
    user_id: int


class VoteStat(BaseModel):
    id: int
    name: str
    vote_count: int
    att_count: int
    status: Optional[str] = None


class VoteBase(BaseModel):
    vote_type: VoteType
    status: VoteStatus
    

class VoteResponse(VoteBase):
    id: int
    user: UserResponse
    meeting: MeetingResponse
    issue: IssueResponse
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class VoteCreate(VoteBase):
    meeting_id: int
    user_id: int
    issue_id: int | None = None
    


class VoteUpdate(VoteBase):
    meeting_id: int
    user_id: int
    issue_id: int | None = None



class QuestionBase(BaseModel):
    text: str
    

class QuestionResponse(QuestionBase):
    id: int
    user: UserResponse
    meeting: MeetingResponse
    issue: IssueResponse
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class QuestionCreate(QuestionBase):
    meeting_id: int
    user_id: int
    issue_id: int


class QuestionUpdate(QuestionBase):
    meeting_id: int
    user_id: int
    issue_id: int
