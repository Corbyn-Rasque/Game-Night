from fastapi import HTTPException, APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
from sqlalchemy import text
from src import database as db
import sqlalchemy.exc 
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

@router.post("/", status_code=200)
def create_user(user: User):
    add_user = text('''INSERT INTO users (username, first, last)
                       VALUES (:username, :first, :last)
                       ON CONFLICT (username) DO NOTHING
                       RETURNING id''')

    try:
        with db.engine.begin() as connection:
            response = connection.execute(add_user, dict(user)).scalar_one_or_none()
        return dict(zip(["id"], [response]))
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=400,detail="User input violates an integrity constraint")
    except Exception:
        raise HTTPException(status_code=400,detail="Error creating user")


def get_user(parameter):
    id = parameter if isinstance(parameter, int) else None
    username = parameter if isinstance(parameter, str) else None
    get_user = text('''SELECT id, username
                       FROM users 
                       WHERE id = :id OR username = :username''')

    try: 
        with db.engine.begin() as connection:
            result = connection.execute(get_user, {"id": id, "username": username}).mappings().first()
        return result if result else {}
    except Exception:
        raise HTTPException(status_code=400,detail="Unexpected error retreiving user")

@router.get("/",status_code=200)
def get_user_info(username: Optional[str] = None, id: Optional[int] = None):
    if username:
        return get_user (username)
    elif id:
        return get_user (id)
    else:
        return {}

@router.get("/{username}/events", status_code=200)
def get_user_events(username: str):
    """ returns all events a user registered to participate in"""
    user_events = text('''SELECT events.id, events.name, events.type, events.location, events.max_attendees, events.start, events.stop
                          FROM event_attendance
                          JOIN events ON events.id = event_attendance.event_id
                          JOIN users ON users.id = event_attendance.user_id
                          WHERE users.username = :username''')
    
    try:
        with db.engine.begin() as connection:
            result = connection.execute(user_events, {"username": username}).mappings().all()
        return result
    except Exception:
        return HTTPException(status_code=400, detail="Unexpected error retrieving user events")