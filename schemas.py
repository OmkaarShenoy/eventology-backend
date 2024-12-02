from typing import Optional, List
import enum
from datetime import date, time, datetime
from pydantic import BaseModel, ConfigDict

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

    model_config = ConfigDict(from_attributes=True)  # Updated configuration

# Token schemas for authentication
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Event schemas
class EventBase(BaseModel):
    event_name: str
    description: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]
    location: Optional[str]

class EventCreate(EventBase):
    pass

class Event(EventBase):
    event_id: int

    model_config = ConfigDict(from_attributes=True)  # Updated configuration

# Subevent schemas
class SubeventBase(BaseModel):
    subevent_name: str
    description: Optional[str]
    event_id: int
    points: int
    date: date
    time: time

class SubeventCreate(SubeventBase):
    pass

class Subevent(SubeventBase):
    subevent_id: int

    model_config = ConfigDict(from_attributes=True)  # Updated configuration

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

    model_config = ConfigDict(from_attributes=True)  # Updated configurationme