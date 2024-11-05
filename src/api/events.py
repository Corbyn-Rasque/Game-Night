from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import datetime
from sqlalchemy import text
from src import database as db

# MAKE SURE TO USE UTC TIME!!!

router = APIRouter(
    prefix="/events",
    tags=["events"],
    dependencies=[Depends(auth.get_api_key)],
)

class Event(BaseModel):
    event_name: str
    time: datetime.datetime  # Ensure this is UTC
    type: str
    active: str
    max_attendees: int
    location: str


# Create new event
@router.post("/")
def create_event(new_event: Event):
    create_event = text('''INSERT INTO events (name, date_time, active, type, max_attendees, location) 
                           VALUES (:event_name, :time, :active, :type, :max_attendees, :location)
                           RETURNING id''')

    with db.engine.begin() as connection:
        event_id = connection.execute(create_event, dict(new_event)).scalar_one_or_none()

    return event_id if event_id else {}


# Get event details by event id
@router.get("/{event_id}")
def get_event(event_id: int):
    event_query = text('''SELECT name, type, active, location, max_attendees, date_time
                        FROM events
                        WHERE id = :event_id''')

    with db.engine.begin() as connection:
        result = connection.execute(event_query, {"event_id": event_id}).mappings().all()
    
    return result


# Cancel an event
@router.post("/{event_id}")
def cancel_event(event_id: int):
    cancel_event = text('''UPDATE events
                           SET cancelled = TRUE
                           WHERE id = :event_id''')
    
    with db.engine.begin() as connection:
        connection.execute(cancel_event, {"event_id": event_id})

    return "OK"


# event_id = create_event(Event(event_name='Tetris Tournament', time=datetime.datetime(2024, 12, 1), type='Tetris', active='Upcoming', max_attendees=100, location='CSL Lab'))
# print(get_event(event_id))
# print(cancel_event(event_id))