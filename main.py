from fastapi import FastAPI
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session, joinedload
from database import SessionLocal, engine
import models
import auth
import schemas  # Import schemas here
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional
import uuid
from fastapi.middleware.cors import CORSMiddleware
from typing import List  # Import List here
from datetime import timedelta
from passlib.context import CryptContext
import random

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React app origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
models.Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Register new user
@app.post("/register")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        user_id=str(uuid.uuid4()),
        email=user.email,
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role,
        total_points=0,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "your_secret_key_here"  # Replace with your actual secret key
ALGORITHM = "HS256"
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user

# Login and token generation
@app.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials"
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Include 'role' in the data dictionary
    access_token = auth.create_access_token(
    data={"sub": user.email, "role": user.role.value},  # Convert enum to string
    expires_delta=access_token_expires
)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/events", response_model=List[schemas.Event])
def read_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    events = db.query(models.Event).offset(skip).limit(limit).all()
    return events


@app.get("/users/me", response_model=schemas.User)
def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid authentication")
        user = get_user_by_email(db, email=email)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# Get details of a specific event
@app.get("/events/{event_id}", response_model=schemas.Event)
def get_event_details(
    event_id: int,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    event = db.query(models.Event).filter(models.Event.event_id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

# Get associated subevents for an event
@app.get("/events/{event_id}/subevents", response_model=List[schemas.Subevent])
def get_event_subevents(
    event_id: int,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    subevents = db.query(models.Subevent).filter(models.Subevent.event_id == event_id).all()
    return subevents

# Get leaderboard for an event
@app.get("/events/{event_id}/leaderboard", response_model=List[schemas.LeaderboardEntry])
def get_event_leaderboard(
    event_id: int,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    leaderboard = (
        db.query(models.LeaderboardEntry)
        .filter(models.LeaderboardEntry.event_id == event_id)
        .order_by(models.LeaderboardEntry.points.desc())
        .all()
    )
    return leaderboard


@app.get("/leaderboard", response_model=List[schemas.User])
def get_leaderboard(db: Session = Depends(get_db)):
    users = db.query(models.User).order_by(models.User.total_points.desc()).all()
    return users

@app.get("/my-events", response_model=List[schemas.Event])
def read_my_events(current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    print(current_user.role)
    # Adjust the role and permission logic as per your application's requirements
    if current_user.role != "organizer":
        raise HTTPException(status_code=403, detail="Not authorized to view these events.")
    print(current_user.user_id)
    events = db.query(models.Event).filter(models.Event.user_id == current_user.user_id).all()
    return events

@app.post("/events", response_model=schemas.Event)
def create_event(
    event: schemas.EventCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != models.RoleEnum.organizer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    # Generate a random integer within PostgreSQL's INTEGER range
    MAX_INT = 2147483647
    MIN_INT = -2147483648
    attempt = 0
    max_attempts = 5
    
    while attempt < max_attempts:
        event_id = random.randint(MIN_INT, MAX_INT)
        if not db.query(models.Event).filter(models.Event.event_id == event_id).first():
            break
        attempt += 1
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not generate a unique event ID. Please try again."
        )
    
    new_event = models.Event(
        event_id=event_id,
        event_name=event.event_name,
        description=event.description,
        start_date=event.start_date,
        end_date=event.end_date,
        location=event.location,
        user_id=current_user.user_id,
    )
    
    db.add(new_event)
    
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create event due to a database error."
        )
    
    db.refresh(new_event)
    
    # Create associated subevents
    for subevent in event.subevents:
        new_subevent = models.Subevent(
            subevent_name=subevent.subevent_name,
            description=subevent.description,
            points=subevent.points,
            date=subevent.date,
            time=subevent.time,
            event_id=new_event.event_id
        )
        db.add(new_subevent)
    db.commit()
    db.refresh(new_event)
    return new_event

@app.get("/subevents", response_model=List[schemas.Subevent])
def get_subevents(current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != 'organizer':
        raise HTTPException(status_code=403, detail="Not authorized")
    subevents = db.query(models.Subevent).filter(models.Subevent.organizer_id == current_user.user_id).all()
    return subevents

@app.post("/my-event/{event_id}/check-in")
# def check_in_participant(
#     subevent_id: int,
#     participant_email: str,
#     current_user: schemas.User = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     if current_user.role != 'organizer':
#         raise HTTPException(status_code=403, detail="Not authorized")
#     participant = get_user_by_email(db, email=participant_email)
#     if not participant:
#         raise HTTPException(status_code=404, detail="Participant not found")
#     # Add check-in logic here (e.g., create a CheckIn record)
#     # Update participant's points if necessary
#     return {"message": "Participant checked in successfully"}

@app.post("/events/{event_id}/subevents", response_model=schemas.Subevent)
def add_subevent(
    event_id: int,
    subevent: schemas.SubeventCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    event = db.query(models.Event).filter(models.Event.event_id == event_id, models.Event.user_id == current_user.user_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    if current_user.role != models.RoleEnum.organizer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to add subevents"
        )
    
    new_subevent = models.Subevent(
        subevent_name=subevent.subevent_name,
        description=subevent.description,
        points=subevent.points,
        date=subevent.date,
        time=subevent.time,
        event_id=event_id
    )
    
    db.add(new_subevent)
    db.commit()
    db.refresh(new_subevent)
    return new_subevent

@app.put("/events/{event_id}", response_model=schemas.Event)
def update_event(
    event_id: int,
    event_update: schemas.EventUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Fetch the event to update
    event = db.query(models.Event)\
              .options(joinedload(models.Event.subevents))\
              .filter(models.Event.event_id == event_id, models.Event.user_id == current_user.user_id)\
              .first()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    if current_user.role != models.RoleEnum.organizer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update events"
        )
    
    # Update event fields if provided
    for field, value in event_update.dict(exclude_unset=True).items():
        setattr(event, field, value)
    
    db.commit()
    db.refresh(event)
    return event