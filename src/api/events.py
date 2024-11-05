from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import datetime
import sqlalchemy
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

@router.post("/")
def create_events(new_event: Event):
    
    with db.engine.begin() as connection:
        event_id = connection.execute(sqlalchemy.text("""
        INSERT INTO events 
        (name, date_time, active, type, max_attendees, location) 
        VALUES (:event_name, :time, :active, :type, :max_attendees, :location) 
        RETURNING id
        """), new_event.dict()).scalar_one_or_none()

    if event_id is None:
        return {"event_id": None}
    else:
        return {"event_id": event_id}

@router.get("/{event_id}")
def get_event(event_id: int):

    with db.engine.begin() as connection:
        event_query = sqlalchemy.text("""
            SELECT 
            name, type, active, location, max_attendees, date_time
            FROM events
            WHERE id = :id """)
        result = connection.execute(event_query, {"id": event_id}).mappings().all()
    
    return result
