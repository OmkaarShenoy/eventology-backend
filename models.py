# models.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Enum as SQLAEnum, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from enum import Enum
from datetime import datetime

Base = declarative_base()

class RoleEnum(str, Enum):
    participant = "participant"
    organizer = "organizer"

class User(Base):
    __tablename__ = 'users'
    user_id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    role = Column(SQLAEnum(RoleEnum), nullable=False)
    total_points = Column(Integer, default=0)
    organized_events = relationship('Event', back_populates='organizer')
    participant_checkins = relationship("CheckIn", back_populates="participant", foreign_keys="CheckIn.user_id")
    organizer_checkins = relationship("CheckIn", back_populates="organizer", foreign_keys="CheckIn.checked_in_by")

class Event(Base):
    __tablename__ = 'events'
    event_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    event_name = Column(String, nullable=False)
    description = Column(Text)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    location = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.user_id'), nullable=False)
    
    organizer = relationship('User', back_populates='organized_events')
    subevents = relationship('Subevent', back_populates='event', cascade="all, delete-orphan")

class Subevent(Base):
    __tablename__ = 'subevents'
    subevent_id = Column(Integer, primary_key=True, index=True)
    subevent_name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    event_id = Column(Integer, ForeignKey('events.event_id'), nullable=False)
    points = Column(Integer, default=0)
    date = Column(DateTime, nullable=True)
    time = Column(Time, nullable=True)  # Ensure this is of type Time
    
    event = relationship('Event', back_populates='subevents')
    checkins = relationship("CheckIn", back_populates="subevent")

class CheckIn(Base):
    __tablename__ = 'checkins'
    checkin_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey('users.user_id'), nullable=False)
    subevent_id = Column(Integer, ForeignKey('subevents.subevent_id'), nullable=False)
    checkin_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    checked_in_by = Column(String, ForeignKey('users.user_id'), nullable=False)
    points = Column(Integer, default=0)
    
    # Relationships
    participant = relationship(
        "User",
        back_populates="participant_checkins",
        foreign_keys=[user_id]
    )
    organizer = relationship(
        "User",
        back_populates="organizer_checkins",
        foreign_keys=[checked_in_by]
    )
    subevent = relationship("Subevent", back_populates="checkins")

class LeaderboardEntry(Base):
    __tablename__ = 'leaderboard_entries'
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey('events.event_id'), nullable=False)
    user_id = Column(String, ForeignKey('users.user_id'), nullable=False)
    points = Column(Integer, nullable=False)
    
    event = relationship('Event')
    user = relationship('User')