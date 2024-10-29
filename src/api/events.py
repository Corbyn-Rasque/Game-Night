import datetime
import sqlalchemy
from src import database as db

#@router.post("/events")
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
            return {"user_id": None}
        else:
            return {"user_id": event_id}

print(create_events("Fortnite Tournament 1",datetime.datetime.now(), "Gaming",100, "52-112 Science"))