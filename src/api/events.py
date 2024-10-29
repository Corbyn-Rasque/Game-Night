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
    time: datetime.datetime
    type: str
    max_attendees: int
    location: str

@router.post("/events")
def create_events(new_event: Event):

    with db.engine.begin() as connection:
        event_id = connection.execute(sqlalchemy.text("""
                        INSERT INTO events 
                        (name, date_time, type, max_attendees, locations) 
                        VALUES (:event_name, :time, :type, :max_attendees, :location) 
                        RETURNING id"""),dict(new_event)).scalar_one_or_none()

        if event_id is None:
            # try getting new event info again
            return {"event_id": None}
        else:
            return {"event_id": event_id}
