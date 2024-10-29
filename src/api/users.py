from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
from sqlalchemy import text
from src import database as db

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(auth.get_api_key)],
)

class User(BaseModel):
    username: str
    first: str
    last: str

@router.post("/users")
def create_user(user: User):
    add_user = text("""INSERT INTO users (username, first, last)
                       VALUES (:username, :first, :last)
                       ON CONFLICT (username) DO NOTHING
                       RETURNING id
                       """)

    with db.engine.begin() as connection:
        response = connection.execute(add_user, dict(user)).scalar_one_or_none()

    return dict(zip(["id"], [response]))

def get_user(parameter):
    id = parameter if isinstance(parameter, int) else None
    username = parameter if isinstance(parameter, str) else None

    get_user = text("""SELECT id, username
                       FROM users 
                       WHERE id = :id OR username = :username""")

    with db.engine.begin() as connection:
        result = connection.execute(get_user, {"id": id, "username": username}).mappings().first()

    return result if result else {}


@router.get("/users/{username}/")
def get_user_by_username(username: str):
    return get_user(username)


@router.get("/users/{user_id}/")
def get_user_by_id(id: int):
   return get_user(id)

    
# if __name__ == '__main__':
#     print(create_user(User(username = 'CorbynR', first = 'Corbyn', last = 'Rasque')))
#     print(get_user_by_username('Corbyn'))
#     print(get_user_by_id(0))


    # get_user = text("""SELECT id, username 
    #                    FROM users 
    #                    WHERE username = :username""")

    # with db.engine.begin() as connection:
    #     result = connection.execute(get_user, {"username": username}).first()



    # return dict(zip(["id", "username"], [result]))

        # get_id = text("""SELECT id, username 
    #                  FROM users 
    #                  WHERE id = :id""")

    # with db.engine.begin() as connection:
    #     result = connection.execute(get_id, {"user_id": id}).first()

    # return dict(zip(["id", "username"], [result]))