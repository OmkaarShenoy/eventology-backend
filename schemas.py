# schemas.py

from typing import Optional, List
import enum
from datetime import datetime, time
from pydantic import BaseModel

# Enum for user roles
class RoleEnum(str, enum.Enum):
    participant = "participant"
    organizer = "organizer"

# Base User schema
class UserBase(BaseModel):
    email: str
    first_name: Optional[str]
    last_name: Optional[str]

# Schema for creating a user (input)
class UserCreate(UserBase):
    password: str
    role: RoleEnum

# Schema for returning user data (output)
class User(UserBase):
    user_id: str
    total_points: int
    role: RoleEnum

    class Config:
        orm_mode = True

# Token schemas for authentication
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class EventUpdate(BaseModel):
    event_name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    location: Optional[str] = None

# Subevent schemas
class SubeventBase(BaseModel):
    subevent_name: str
    description: Optional[str] = None
    points: int

    class Config:
        arbitrary_types_allowed = True  # Allow arbitrary types

class SubeventCreate(BaseModel):
    subevent_name: str
    description: str
    points: int
    datetime: datetime  # Unified datetime field

class Subevent(BaseModel):
    subevent_id: int
    subevent_name: str
    description: Optional[str]
    points: int
    datetime: datetime  # Make datetime optional
    event_id: int

    class Config:
        orm_mode = True


class Subevent(SubeventBase):
    subevent_id: int
    event_id: int

    class Config:
        orm_mode = True

# Event schemas
class EventBase(BaseModel):
    event_name: str
    description: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    location: Optional[str] = None

class EventCreate(EventBase):
    subevents: List[SubeventCreate] = []  # Forward reference

class Event(EventBase):
    event_id: int
    subevents: List[Subevent] = []

    class Config:
        orm_mode = True

# CheckIn schemas
class CheckInBase(BaseModel):
    user_id: str
    subevent_id: int
    checked_in_by: str
    points: int

class CheckInCreate(CheckInBase):
    pass

class CheckIn(CheckInBase):
    checkin_id: int
    checkin_time: datetime

    class Config:
        orm_mode = True

class CheckInRequest(BaseModel):
    subevent_id: int
    participant_email: str

# LeaderboardEntry schemas
class LeaderboardEntryBase(BaseModel):
    points: int

class LeaderboardEntry(LeaderboardEntryBase):
    id: int
    event_id: int
    user_id: str

    class Config:
        orm_mode = True

class LeaderboardEntryResponse(BaseModel):
    event_id: int
    points: int
    first_name: str
    last_name: str

    class Config:
        orm_mode = True

# To handle forward references
EventCreate.update_forward_refs()
Event.update_forward_refs()
SubeventCreate.update_forward_refs()
Subevent.update_forward_refs()