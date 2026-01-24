from sqlalchemy import Column, Integer, Boolean, String, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship

from database import Base


class EduYear(Base):
    name = Column(String, nullable=False)
    meetings = relationship("Meeting", back_populates="edu_year")


class Subject(Base):
    name = Column(String, nullable=False)


class Meeting(Base):
    name = Column(String, nullable=False)
    life_time = Column(DateTime, nullable=False)
    input_time = Column(DateTime, nullable=False)
    is_confirm = Column(Boolean, default=False)
    edu_year_id = Column(Integer, ForeignKey("eduyears.id"), nullable=True)
    edu_year = relationship("EduYear", back_populates="meetings")

import enum

class IssueStatus(enum.Enum):
    NEW = "new"
    ACCEPT = "accept"
    ENTERED = "entered"
    CANCEL = "cancel"

    # Optional: Map keys to human-readable labels
    @classmethod
    def labels(cls):
        return {
            cls.NEW: "Yangi",
            cls.ACCEPT: "Kotib qabul qildi",
            cls.ENTERED: "Kun tartibiga kiritildi",
            cls.CANCEL: "Rad etildi",
        }
    

class Issue(Base):
    title = Column(String, nullable=False)
    meeting_id = Column(Integer, ForeignKey("meetings.id"), nullable=True, default=None)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=True, default=None)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_confirm = Column(Boolean, default=False)
    expired = Column(DateTime, nullable=False)
    status = Column(Enum(IssueStatus, native_enum=False), default=IssueStatus.NEW, nullable=False)
    desc = Column(Text, nullable=True, default=None)

    # user = relationship("User", back_populates="issues")


# class InfoIssue(Base):
#     content = Column(String)


# class Attendance(Base):
#     pass


# class Vote(Base):
#     pass


# class Question(Base):
#     pass