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

class Event(BaseModel):
    name: str
    type: str
    start: datetime.datetime    # UTC
    stop: datetime.datetime     # UTC
    location: str
    max_attendees: int


# Create new event
@router.post("")
def create_event(event: Event):
    create_event = text('''INSERT INTO events (name, type, start, stop, location, max_attendees) 
                           VALUES (:name, :type, :start, :stop, :location, :max_attendees)
                           RETURNING id''')

    with db.engine.begin() as connection:
        event_id = connection.execute(create_event, dict(event)).scalar_one_or_none()

    return event_id if event_id else {}

print(create_event(Event(name='New Years',type='Party', start=datetime.datetime(2025,1,1), stop=datetime.datetime(2025,1,2), location='Times Square', max_attendees=10000)))


# Get event details by date
@router.get("")
def get_event(name: str = None, start: datetime.datetime = None, stop: datetime.datetime = None):
    start = start if start else datetime.datetime.today()
    stop = stop if stop else start + datetime.timedelta(days = 7)
    
    name_and_date_query = text('''SELECT name, type, location, max_attendees, start, stop
                                  FROM events
                                  WHERE (STRPOS(name, :name) > 0 OR :name is NULL) AND ((start BETWEEN :start AND :stop) OR (stop BETWEEN :start AND :stop))''')
    
    with db.engine.begin() as connection:
        result = connection.execute(name_and_date_query, {"name": name, "start": start, "stop": stop}).mappings().all()
    
    return result if result else {}


# Get event details by event id
@router.get("/{event_id}")
def get_event_by_id(event_id: int):
    event_query = text('''SELECT name, type, start, stop, location, max_attendees
                          FROM events
                          WHERE id = :event_id''')

    with db.engine.begin() as connection:
        result = connection.execute(event_query, {"event_id": event_id}).mappings().all()
    
    return result if result else {}


# Cancel an event
@router.delete("/{event_id}")
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
# print(get_event_by_date(datetime.datetime(2024, 11, 5)))
# print(get_event(range = 12))
# print(get_event(name = 'Batman'))