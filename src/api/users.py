from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from src.api import auth
from sqlalchemy import text, exc
from src import database as db
from typing import Optional



router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(auth.get_api_key)],
)

class User(BaseModel):
    username: str
    first: str
    last: str

@router.post("", status_code = status.HTTP_201_CREATED)
def create_user(user: list[User]):
    temp_table = text('''   CREATE TEMPORARY TABLE temp_t(
                                username TEXT NOT NULL,
                                first TEXT NOT NULL,
                                last TEXT NOT NULL
                            )ON COMMIT DROP;
                            ''')

    temp_insert = text('''  INSERT INTO temp_t (username, first, last)
                            VALUES(:username,:first,:last)''')

    add_user =   '''INSERT INTO users (username, first, last)
                    SELECT username, first, last
                    FROM temp_t
                    ON CONFLICT (username) DO NOTHING
                    RETURNING id as user_id, username'''


    user = [dict(u) for u in user]

    with db.engine.begin() as connection:
        try:
            connection.execute(temp_table)
            connection.execute(temp_insert,user)
            response = connection.execute(text(add_user)).mappings().all()
            return response
        except exc.NoResultFound:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = 'User already exists.')
        except exc.IntegrityError as e:
            error = str(e.orig)
            if 'username' in error: raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'Cannot have default username.')
            elif 'first' in error:  raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'Cannot have first name.')
            elif 'last' in error:   raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'Cannot have last name.')


@router.get("", status_code = status.HTTP_200_OK)
def get_user(username: Optional[str] = None, id: Optional[int] = None):
    query =  '''SELECT id, username
                FROM users
                WHERE (:username IS NULL OR username = :username)
                    AND (:id IS NULL OR id = :id)'''

    with db.engine.begin() as connection:
        try: result = connection.execute(text(query), {"username": username, "id": id}).mappings().one()
        except exc.NoResultFound:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "No user found.")
        except exc.MultipleResultsFound:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'No search parameters provided.')
    
    return result


@router.get("/{username}/events", status_code = status.HTTP_200_OK)
def get_user_events(username: str):
    user_events =    '''SELECT events.id, events.name, events.type, events.location, events.max_attendees, events.start, events.stop
                        FROM event_attendance
                        JOIN events ON events.id = event_attendance.event_id
                        JOIN users ON users.id = event_attendance.user_id
                        WHERE users.username = :username'''
    
    with db.engine.begin() as connection:
        result = connection.execute(text(user_events), {"username": username}).mappings().all()

    if not result: HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "No events found.")

    return result


@router.patch("/{username}", status_code = status.HTTP_204_NO_CONTENT)
def deactivate_user(username: str):
    get_user(username)

    remove_user =   text('''UPDATE users
                            SET active = FALSE
                            WHERE username = :username AND active IS NOT FALSE''')
    
    with db.engine.begin() as connection:
        result = connection.execute(remove_user, {"username": username})
        if not result.rowcount: raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "User cannot be deactivated.")

# test_users = [User(username = 'tester333', first = 'john', last = 'doe')]
# create_user(test_users)