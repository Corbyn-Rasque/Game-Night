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


# Get event details by date
@router.get("")
def get_event(name: str = None, username: str = None, type: str = None, start: datetime.datetime = None, stop: datetime.datetime = None):
    event_query = '''SELECT id, name, type, location, max_attendees, start, stop
                     FROM events
                     WHERE (STRPOS(name, :name) > 0 OR :name is NULL)
                        AND (STRPOS(type, :type) > 0 OR :type is NULL)'''

    username_query = '''SELECT id, name, type, location, max_attendees, start, stop
                        FROM events
                        JOIN user_events ON user_events.event_id = id
                        JOIN users ON users.id = user_events.user_id
                        WHERE (STRPOS(name, :name) > 0 OR :name is NULL)
                            AND (STRPOS(type, :type) > 0 OR :type is NULL)
                            AND users.username = :username'''

    if username: event_query = username_query

    if bool(start) ^ bool(stop):
        event_query += '\nAND ((start >= :start OR stop >= :start) OR (start <= :stop OR stop <= :stop))'
    elif bool(start) and bool(stop):
        event_query += '\nAND ((start BETWEEN :start AND :stop) OR (stop BETWEEN :start AND :stop))'

    with db.engine.begin() as connection:
        result = connection.execute(text(event_query),
                                    {"name": name, "username": username, "type": type, "start": start, "stop": stop}).mappings().all()
    
    return result if result else {}


# Get event details by event id
@router.get("/{event_id}")
def get_event_by_id(event_id: int):
    event_query = text('''SELECT id, name, type, start, stop, location, max_attendees
                          FROM events
                          WHERE id = :event_id''')

    with db.engine.begin() as connection:
        result = connection.execute(event_query, {"event_id": event_id}).mappings().all()
    
    return result if result else {}


@router.get("/{event_id}/users")
def get_event_users(event_id: int):
    user_query = text('''SELECT users.username AS name, users.first, users.last
                         FROM events
                         JOIN user_events ON user_events.event_id = id
                         JOIN users ON users.id = user_events.user_id
                         WHERE event_id = :event_id''')

    with db.engine.begin() as connection:
        results = connection.execute(user_query, {"event_id": event_id}).mappings().all()

    results = [users.User(**user) for user in results]

    return results


@router.get("{event_id}/brackets")
def get_event_brackets(event_id: int):
    bracket_query = text('''SELECT id, name, event_id, game_id, time, match_size, num_players
                            FROM brackets
                            WHERE event_id = :event_id''')
    
    with db.engine.begin() as connection:
        results = connection.execute(bracket_query, {"event_id": event_id}).mappings().all()

    return results


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