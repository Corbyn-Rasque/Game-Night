from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import datetime
from sqlalchemy import text
from src import database as db
from src.api import users as users

router = APIRouter(
    prefix="/events",
    tags=["events"],
    dependencies=[Depends(auth.get_api_key)],
)

class Event(BaseModel):
    host : str
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
    
    event_host = text(''' INSERT INTO user_events (user_id, event_id)
                          SELECT users.id, :event_id FROM users 
                          WHERE username = :username ''')

    with db.engine.begin() as connection:
        event_id = connection.execute(create_event, dict(event)).scalar_one_or_none()
        connection.execute(event_host, {"event_id": event_id, "username" : event.host})


    return {"event_id" : event_id} if event_id else {}


@router.post("/{event_id}")
def join_event(username: str, event_id: int):

    join = text(''' INSERT INTO user_events (user_id, event_id)
                    SELECT users.id, :event_id FROM users 
                    WHERE username = :username ''')

    with db.engine.begin() as connection:
        connection.execute(join, {"event_id": event_id, "username" : username})

    return {"Success" : event_id} if event_id else {}

# Get event details by date 
@router.get("")
def get_event(name: str = None, username: str = None, type: str = None, start: datetime.datetime = None, stop: datetime.datetime = None):
    event_query = '''SELECT id, name, type, location, max_attendees, start, stop, cancelled
                     FROM events
                     WHERE (STRPOS(name, :name) > 0 OR :name is NULL)
                        AND (STRPOS(type, :type) > 0 OR :type is NULL)'''

    username_query = '''SELECT events.id, name, type, location, max_attendees, start, stop
                        FROM events
                        JOIN user_events ON user_events.event_id = id
                        JOIN users ON users.id = user_events.user_id
                        WHERE (STRPOS(name, :name) > 0 OR :name is NULL)
                        AND (STRPOS(type, :type) > 0 OR :type is NULL)
                        AND users.username = :username'''

    if username: final = username_query
    else: final = event_query


    if bool(start) ^ bool(stop):
        final += '\nAND ((start >= :start OR stop >= :start) OR (start <= :stop OR stop <= :stop))'
    elif bool(start) and bool(stop):
        final += '\nAND ((start BETWEEN :start AND :stop) OR (stop BETWEEN :start AND :stop))'

    with db.engine.begin() as connection:
        result = connection.execute(text(final),
                                    {"name": name, "username": username, "type": type, "start": start, "stop": stop}).mappings().all()

    return result if result else {}


# Get event details by event id
@router.get("/{event_id}")
def get_event_by_id(event_id: int):
    """returns detailed information about a specific event """
    event_query = text('''SELECT id, name, type, start, stop, location, max_attendees, cancelled
                          FROM events
                          WHERE id = :event_id''')

    with db.engine.begin() as connection:
        result = connection.execute(event_query, {"event_id": event_id}).mappings().all()
    
    return result if result else {}


@router.get("/{event_id}/users")
def get_event_attendees(event_id: int):
    user_query = text('''SELECT users.username AS username, users.first, users.last
                         FROM events
                         JOIN event_attendance ON event_attendance.event_id = id
                         JOIN users ON users.id = event_attendance.user_id
                         WHERE event_id = :event_id''')

    with db.engine.begin() as connection:
        results = connection.execute(user_query, {"event_id": event_id}).mappings().all()

    return results


@router.get("/{event_id}/brackets")
def get_event_brackets(event_id: int):
    bracket_query = text('''SELECT id, name, event_id, game_id, time, match_size, num_players
                            FROM brackets
                            WHERE event_id = :event_id''')
    
    with db.engine.begin() as connection:
        results = connection.execute(bracket_query, {"event_id": event_id}).mappings().all()

    return results


# Cancel an event
@router.patch("/{event_id}")
def cancel_event(event: int):
    cancel_event = text('''UPDATE events
                           SET cancelled = TRUE
                           WHERE id = :event_id''')
    
    with db.engine.begin() as connection:
        connection.execute(cancel_event, {"event_id": event})

    return "OK"
