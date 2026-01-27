from sqlalchemy import Column, String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    profile = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    issues = relationship("Issue", back_populates="user")

    att_dances = relationship("Attendance", back_populates="user")


class Profile(Base):
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    user = relationship("User", back_populates="profile")
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)