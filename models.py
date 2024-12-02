from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Text, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()

class RoleEnum(enum.Enum):
    participant = "participant"
    organizer = "organizer"

class User(Base):
    __tablename__ = 'users'
    user_id = Column(String, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    total_points = Column(Integer, default=0)
    role = Column(Enum(RoleEnum), nullable=False)

    # Relationships
    # Relationship to check-ins where the user is the participant
    participant_checkins = relationship(
        "CheckIn",
        back_populates="participant",
        foreign_keys="CheckIn.user_id"
    )

    # Relationship to check-ins where the user is the organizer who checked in participants
    organizer_checkins = relationship(
        "CheckIn",
        back_populates="organizer",
        foreign_keys="CheckIn.checked_in_by"
    )

class Event(Base):
    __tablename__ = 'events'
    event_id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String, nullable=False)
    description = Column(Text)
    start_date = Column(Date)
    end_date = Column(Date)
    location = Column(String)

    subevents = relationship("Subevent", back_populates="event")

class Subevent(Base):
    __tablename__ = 'subevents'
    subevent_id = Column(Integer, primary_key=True, index=True)
    subevent_name = Column(String, nullable=False)
    description = Column(Text)
    event_id = Column(Integer, ForeignKey('events.event_id'))
    points = Column(Integer, default=0)
    date = Column(Date)
    time = Column(Time)

    event = relationship("Event", back_populates="subevents")
    checkins = relationship("CheckIn", back_populates="subevent")

class CheckIn(Base):
    __tablename__ = 'checkins'
    checkin_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey('users.user_id'))
    subevent_id = Column(Integer, ForeignKey('subevents.subevent_id'))
    checkin_time = Column(Date, default='CURRENT_TIMESTAMP')
    checked_in_by = Column(String, ForeignKey('users.user_id'))
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