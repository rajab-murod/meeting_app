from sqlalchemy import Column, Integer, Boolean, String

from database import Base


class EduYear(Base):
    name = Column(String, nullable=False)


# class Subject(Base):
#     name = Column(String, nullable=False)


# class Meeting(Base):
#     pass


# class Issue(Base):
#     name = Column(String)


# class InfoIssue(Base):
#     content = Column(String)


# class Attendance(Base):
#     pass


# class Vote(Base):
#     pass


# class Question(Base):
#     pass