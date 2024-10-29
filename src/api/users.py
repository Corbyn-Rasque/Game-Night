from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth

import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(auth.get_api_key)],
)

class User(BaseModel):
    username: str
    first_name: str
    last_name: str

@router.post("/users")
def create_user(new_user: User):
    new_user_dict = {
        "username": new_user.username,
        "first": new_user.first_name,
        "last": new_user.last_name,
    }
    with db.engine.begin() as connection:
        id = connection.execute(sqlalchemy.text("""
                INSERT INTO users (username, first, last) 
                VALUES (:username, :first, :last) 
                ON CONFLICT (username) 
                DO NOTHING 
                RETURNING id"""), new_user_dict).scalar_one_or_none()

    if id is None:
        #try getting new user info again
        return {"user_id": None}
    else:
        return {"user_id": id}

@router.get("/users/{username}/")
def get_user_by_username(username: str):
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text("""
                        SELECT id, username 
                        FROM users 
                        WHERE username = :username"""), {"username": username}).first()

    if result is None:
        print("No user with that username was found.")
        return None
    else:
        uid = result[0]
        uname = result[1]
        user_info = {"id": uid, "username": uname}
        return user_info

@router.get("/users/{user_ud}/")
def get_user_by_id(user_id: int):
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text("""
                    SELECT id, username 
                    FROM users 
                    WHERE id = :user_id"""), {"user_id": user_id}).first()

    if result is None:
        print("No user with that ID was found.")
        return None
    else:
        uid = result[0]
        uname = result[1]
        user_info = {"id": uid, "username": uname}
        return user_info