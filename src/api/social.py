from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.api import auth
from sqlalchemy import text
from src import database as db

router = APIRouter(
    prefix="/social",
    tags=["social"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.post("/add")
def add_friend(user_id: int, friend_id: int):
    try: 
        insert_friend = """
                INSERT INTO user_friends  
                (user_id, friend_id)
                VALUES (:user, :friend)
                """
        with db.engine.begin() as connection:
            connection.execute(text(insert_friend), 
            [{"user":user_id, "friend":friend_id}])
    except Exception: 
        raise HTTPException(status_code=400, detail="Invalid User ID")
    print("friend added")
    return ("Friend Added")

@router.get("/friends")
def get_friends(user_id: int):
    try: 
        select_user = """
                SELECT friend_id, username
                    from user_friends
                    INNER JOIN users
                    ON users.id = user_friends.friend_id
                    WHERE user_id = :user
                """
        with db.engine.begin() as connection:
            result = connection.execute(text(select_user), 
            [{"user":user_id}]).fetchall()
    except Exception: 
        raise HTTPException(status_code=400, detail="Invalid User ID")
    print("Friends Selected: ")
    print(dict(result))
    return (dict(result))

@router.delete("/remove")
def remove_friend(user_id: int, friend_id : int):
    try:
        with db.engine.begin() as connection:
            remove_user = """
                    DELETE FROM user_friends
                    WHERE friend_id = :friend 
                    AND user_id = :user"""
            connection.execute(
                text(remove_user),
                [{"user":user_id, "friend":friend_id}])
    except Exception:
        raise HTTPException(status_code=400, detail="Error removing friend")
    print("removed friend :(")
    return (f"Removed user {friend_id}")

@router.get("/events")
def friend_events(user_id : int):
    events = {}
    try:
        query = """
                WITH friend_events AS (
                    SELECT 
                    events.id as id, array_agg(username) as friends_attending
                    from user_friends
                    INNER JOIN users
                    ON user_friends.friend_id = users.id
                    INNER JOIN event_attendance
                    ON event_attendance.user_id = user_friends.friend_id
                    INNER JOIN events
                    ON events.id = event_attendance.event_id
                    WHERE 
                    cancelled = false AND
                    user_friends.user_id = :user
                    GROUP BY events.id)
                SELECT *
                from friend_events
                INNER JOIN events
                ON events.id = friend_events.id
                ORDER BY cardinality(friends_attending) DESC"""
        with db.engine.begin() as connection:
            events = connection.execute(
                    text(query),
                    [{"user":user_id}]).mappings().all()
    except Exception:
        raise HTTPException(status_code=400, detail="Error retrieving friend events")
    print(f"Retrieving friend events for user id {user_id}")
    return(events)
