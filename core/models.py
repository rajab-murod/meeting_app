import enum
from sqlalchemy import Column, Integer, Boolean, String, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship

from app.database import Base


class EduYear(Base):
    name = Column(String, nullable=False)
    meetings = relationship("Meeting", back_populates="edu_year")


class Subject(Base):
    name = Column(String, nullable=False)
    
    issues = relationship("Issue", back_populates="subject")


class Meeting(Base):
    name = Column(String, nullable=False)
    life_time = Column(DateTime, nullable=False)
    input_time = Column(DateTime, nullable=False)
    is_confirm = Column(Boolean, default=False)
    edu_year_id = Column(Integer, ForeignKey("eduyears.id"), nullable=True)

    edu_year = relationship("EduYear", back_populates="meetings")
    issues = relationship("Issue", back_populates="meeting")
    
    att_dances = relationship("Attendance", back_populates="meeting")
    votes = relationship("Vote", back_populates="meeting")
    questions = relationship("Question", back_populates="meeting")


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

    user = relationship("User", back_populates="issues")
    meeting = relationship("Meeting", back_populates="issues")
    subject = relationship("Subject", back_populates="issues")

    info_issues = relationship("InfoIssue", back_populates="issue")
    votes = relationship("Vote", back_populates="issue")
    questions = relationship("Question", back_populates="issue")


class InfoIssue(Base):
    issue_id = Column(Integer, ForeignKey("issues.id"))
    content = Column(Text)
    file_path = Column(String, nullable=True, default=None)

    issue = relationship("Issue", back_populates="info_issues")


class Attendance(Base):
    meeting_id = Column(Integer, ForeignKey("meetings.id"), nullable = False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable = False)
    date = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="att_dances")
    meeting = relationship("Meeting", back_populates="att_dances")


class VoteStatus(enum.Enum):
    DISAGREE = "disagree"
    AGREE = "agree"
    NEUTRAL = "neutral"

    # Optional: Map keys to human-readable labels
    @classmethod
    def labels(cls):
        return {
            cls.DISAGREE: "Qarshi",
            cls.AGREE: "Rozi",
            cls.NEUTRAL: "Betaraf",
        }

class VoteType(enum.Enum):
    AGENDA = "agenda"
    ISSUE = "issue"

    # Optional: Map keys to human-readable labels
    @classmethod
    def labels(cls):
        return {
            cls.AGENDA: "Kun tartibi",
            cls.ISSUE: "Masala",
        }
  

class Vote(Base):
    meeting_id = Column(Integer, ForeignKey("meetings.id"), nullable=False)
    issue_id = Column(Integer, ForeignKey("issues.id"), nullable=True, default=None)
    user_id = Column(Integer, ForeignKey("users.id"), nullable = False)
    status = Column(Enum(VoteStatus, native_enum=False), nullable=False)
    vote_type = Column(Enum(VoteType, native_enum=False), nullable=False)

    user = relationship("User", back_populates="votes")
    meeting = relationship("Meeting", back_populates="votes")
    issue = relationship("Issue", back_populates="votes")


class Question(Base):
    meeting_id = Column(Integer, ForeignKey("meetings.id"), nullable = False)
    issue_id = Column(Integer, ForeignKey("issues.id"), nullable = False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable = False)
    text = Column(Text)

    user = relationship("User", back_populates="questions")
    meeting = relationship("Meeting", back_populates="questions")
    issue = relationship("Issue", back_populates="questions")