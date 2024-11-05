from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import datetime
from sqlalchemy import text
from src import database as db

router = APIRouter(
    prefix="/events",
    tags=["events"],
    dependencies=[Depends(auth.get_api_key)],
)

# MAKE SURE TO USE UTC TIME!!!

# Test date functionality with URL. Verify format that it's being received in works,
# and that query parameters are also working properly, as well.

class Event(BaseModel):
    event_name: str
    time: datetime.datetime  # Ensure this is UTC
    type: str
    active: str
    max_attendees: int
    location: str


# Create new event
@router.post("/")
def create_event(event: Event):
    create_event = text('''INSERT INTO events (name, date_time, active, type, max_attendees, location) 
                           VALUES (:event_name, :time, :active, :type, :max_attendees, :location)
                           RETURNING id''')

    with db.engine.begin() as connection:
        event_id = connection.execute(create_event, dict(event)).scalar_one_or_none()

    return event_id if event_id else {}


# Get event details by event id
@router.get("/")
def get_event_by_id(event: int):
    event_query = text('''SELECT name, type, active, location, max_attendees, date_time
                          FROM events
                          WHERE id = :event_id''')

    with db.engine.begin() as connection:
        result = connection.execute(event_query, {"event_id": event}).mappings().all()
    
    return result if result else {}


# Get event details by date
@router.get("/")
def get_event_by_date(date: datetime.datetime = datetime.datetime.today()):
    event_query = text('''SELECT name, type, active, location, max_attendees, date_time
                          FROM events
                          WHERE (date_time - date(':year.:month.:day')) < '1 Day' ''')
    
    with db.engine.begin() as connection:
        result = connection.execute(event_query, {"year": date.year, "month": date.month, "day": date.day}).mappings().all()
    
    return result if result else {}


# Cancel an event
@router.delete("/")
def cancel_event(event: int):
    cancel_event = text('''UPDATE events
                           SET cancelled = TRUE
                           WHERE id = :event_id''')
    
    with db.engine.begin() as connection:
        connection.execute(cancel_event, {"event_id": event})

    return "OK"


# event_id = create_event(Event(event_name='Tetris Tournament', time=datetime.datetime(2024, 12, 1), type='Tetris', active='Upcoming', max_attendees=100, location='CSL Lab'))
# print(get_event(event_id))
# print(cancel_event(event_id))