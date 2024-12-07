# models.py

from sqlalchemy import UniqueConstraint, Column, Integer, String, ForeignKey, DateTime, Text, Enum as SQLAEnum, Time
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
    leaderboard_entries = relationship('LeaderboardEntry', back_populates='event')  # Add this


class Subevent(Base):
    __tablename__ = 'subevents'
    subevent_id = Column(Integer, primary_key=True, index=True)
    subevent_name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    event_id = Column(Integer, ForeignKey('events.event_id'), nullable=False)
    __table_args__ = (UniqueConstraint('event_id', 'subevent_name', name='unique_event_subevent'),)
    points = Column(Integer, default=0)
    datetime = Column(DateTime, nullable=True)  # Change to nullable
    

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
    participant = relationship("User", foreign_keys=[user_id])
    organizer = relationship("User", foreign_keys=[checked_in_by])
    subevent = relationship("Subevent", back_populates="checkins")

class LeaderboardEntry(Base):
    __tablename__ = 'leaderboard_entries'
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey('events.event_id'), nullable=False)
    user_id = Column(String, ForeignKey('users.user_id'), nullable=False)
    points = Column(Integer, nullable=False)
    
    event = relationship('Event', back_populates='leaderboard_entries')  # Reverse relationship
    user = relationship('User')  # Assuming a simple relationship for user details
