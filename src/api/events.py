from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth

import datetime
import sqlalchemy
from src import database as db


# MAKE SURE TO USE UTC TIME!!!

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(auth.get_api_key)],
)
@router.post("/events")
def create_events(event_name: str, time: datetime.datetime, type: str, max_attendees: int, location: str):

    event_dict = {
        "event_name": event_name,
        "time": time,
        "type": type,
        "max_att": max_attendees,
        "location": location
    }

    with db.engine.begin() as connection:
        event_id = connection.execute(sqlalchemy.text("""
                        INSERT INTO event 
                        (name, date_time, type, max_attendees, locations) 
                        VALUES (:event_name, :time, :type, :max_att, :location) 
                        RETURNING id"""),event_dict).scalar_one_or_none()

        if event_id is None:
            # try getting new event info again
            return {"event_id": None}
        else:
            return {"event_id": event_id}
