from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel
from src.api import auth
import datetime
from sqlalchemy import text, exc
from src import database as db
from src.api import users as users
from typing import Optional

router = APIRouter(
    prefix="/events",
    tags=["events"],
    dependencies=[Depends(auth.get_api_key)],
)

class Event(BaseModel):
    host: str
    name: str
    type: str
    start: datetime.datetime
    stop: datetime.datetime
    location: str
    max_attendees: int


@router.post("", status_code = status.HTTP_201_CREATED)
def create_event(event: Event):
    create_event =   '''INSERT INTO events (name, type, start, stop, location, max_attendees) 
                        VALUES (:name, :type, :start, :stop, :location, :max_attendees)
                        RETURNING id'''
    
    event_host =    ''' INSERT INTO user_events (user_id, event_id)
                        SELECT users.id, :event_id FROM users 
                        WHERE username = :username
                        RETURNING user_id, event_id'''

    with db.engine.begin() as connection:
        try: new_event = connection.execute(text(create_event), dict(event)).mappings().one()
        except exc.IntegrityError as e:
            error = str(e.orig)

            if 'name' in error:
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'Cannot use default name.')
            elif 'type' in error:
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'Cannot use default type.')
            elif 'location' in error:
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'Cannot use default location.')
            elif 'max_attendees' in error:
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'Max attendees must be 1 or more.')

        except exc.NoResultFound: raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = 'Error creating event.')

        try:
            result = connection.execute(text(event_host), {"event_id": new_event['id'], "username" : event.host}).mappings().one()
            connection.commit()

            return result

        except exc.IntegrityError as e:
            connection.rollback()
            error = str(e.orig)

            if 'user_id' in error:      raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'Invalid username.')
            elif 'event_id' in error:   raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = 'Error creating event.')
        except exc.NoResultFound:
            connection.rollback()
            raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = 'Error creating event.')


class Attendee(BaseModel):
    username: str

@router.post("/{event_id}", status_code = status.HTTP_201_CREATED)
def join_event(event_id: int, users: list[Attendee]):

    users = [dict(e, event_id=event_id) for e in users]

    join =  ''' INSERT INTO event_attendance (user_id, event_id)
                SELECT users.id, :event_id FROM users 
                WHERE username = :username
                RETURNING user_id, event_id'''

    with db.engine.begin() as connection:
        try:
            connection.execute(text(join), users)
            connection.commit()

        except exc.IntegrityError as e:
            connection.rollback()
            error = str(e.orig)

            if 'event_id' in error:     raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'Invalid Event ID.')
            elif 'username' in error:   raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'Invalid Username.')
        except exc.NoResultFound:
            connection.rollback()
            raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = 'Error creating event.')


@router.get("", status_code = status.HTTP_200_OK)
def get_event(name: Optional[str] = None, username: Optional[str] = None, game: Optional[str] = None,
              type: Optional[str] = None, start: Optional[datetime.datetime] = None, stop: Optional[datetime.datetime] = None):
    event_query = '''SELECT events.id, events.name, games.name AS game, type, location, max_attendees, start, stop, cancelled
                     FROM events
                     JOIN brackets ON brackets.event_id = events.id
                     JOIN games ON games.id = brackets.game_id
                     WHERE (STRPOS(events.name, :name) > 0 OR :name is NULL)
                        AND (STRPOS(type, :type) > 0 OR :type is NULL)
                        AND (STRPOS(games.name, :game) > 0 OR :game is NULL)
                        AND events.cancelled = FALSE'''

    username_query = '''SELECT events.id, events.name, type, location, max_attendees, start, stop
                        FROM events
                        JOIN brackets ON brackets.event_id = events.id
                        JOIN games ON games.id = brackets.game_id
                        JOIN user_events ON user_events.event_id = events.id
                        JOIN users ON users.id = user_events.user_id
                        WHERE (STRPOS(events.name, :name) > 0 OR :name is NULL)
                            AND (STRPOS(type, :type) > 0 OR :type is NULL)
                            AND (STRPOS(games.name, :game) > 0 OR :game is NULL)
                            AND users.username = :username
                            AND events.cancelled = FALSE'''

    if username: query = username_query
    else: query = event_query


    if bool(start) ^ bool(stop):
        query += '\nAND ((start >= :start OR stop >= :start) OR (start <= :stop OR stop <= :stop))'
    elif bool(start) and bool(stop):
        query += '\nAND ((start BETWEEN :start AND :stop) OR (stop BETWEEN :start AND :stop))'

    with db.engine.begin() as connection:
        result = connection.execute(text(query),
                                {"name": name, "username": username, "game": game, "type": type, "start": start, "stop": stop}).mappings().all()
        
        if not result: raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'No matching events.')
        else: return result



@router.get("/{event_id}", status_code = status.HTTP_200_OK)
def get_event_by_id(event_id: int):
    event_query =    '''SELECT id, name, type, start, stop, location, max_attendees, cancelled
                        FROM events
                        WHERE id = :event_id'''

    with db.engine.begin() as connection:
        result = connection.execute(text(event_query), {"event_id": event_id}).mappings().all()
    
    if not result: raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'No matching events for event_id.')
    else: return result


@router.get("/{event_id}/users", status_code = status.HTTP_200_OK)
def get_event_attendees(event_id: int):
    user_query = '''SELECT users.username AS username, users.first, users.last
                    FROM events
                    JOIN event_attendance ON event_attendance.event_id = id
                    JOIN users ON users.id = event_attendance.user_id
                    WHERE event_id = :event_id'''

    with db.engine.begin() as connection:
        results = connection.execute(text(user_query), {"event_id": event_id}).mappings().all()

    if not results: raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'No users attending event.')
    else: return results


@router.get("/{event_id}/brackets", status_code = status.HTTP_200_OK)
def get_event_brackets(event_id: int):
    bracket_query =  '''SELECT id, name, event_id, game_id, time, match_size, num_players
                        FROM brackets
                        WHERE event_id = :event_id'''
    
    with db.engine.begin() as connection:
        results = connection.execute(text(bracket_query), {"event_id": event_id}).mappings().all()

    if not results: raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'No brackets found for event.')
    else: return results


@router.patch("/{event_id}", status_code = status.HTTP_204_NO_CONTENT)
def cancel_event(event_id: int):
    get_event_by_id(event_id)

    cancel_event =   '''UPDATE events
                        SET cancelled = TRUE
                        WHERE id = :event_id AND cancelled = FALSE
                        RETURNING id'''
    
    with db.engine.begin() as connection:
        try:
            connection.execute(text(cancel_event), {"event_id": event_id}).one()
            connection.commit()

        except exc.NoResultFound:
            connection.rollback()
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'Event already cancelled.')
