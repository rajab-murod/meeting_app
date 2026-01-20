from datetime import datetime
from pydantic import BaseModel

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
