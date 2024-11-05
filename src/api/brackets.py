from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import datetime
from sqlalchemy import text
from src import database as db

router = APIRouter(
    prefix="/brackets",
    tags=["brackets"],
    dependencies=[Depends(auth.get_api_key)],
)

class Bracket(BaseModel):
    name: str
    date_time: datetime.datetime
    game: str
    capacity: int
    cost:float

@router.post("/")
def create_bracket(new_bracket: Bracket):

    with db.engine.begin() as connection:
        result = connection.execute(text("""
                    INSERT INTO brackets 
                    (name, date_time, game, capacity, cost) 
                    VALUES (:name, :date_time, :game, :capacity, :cost) 
                    RETURNING id """), dict(new_bracket)).scalar_one_or_none()
    if result is None:
        print("Bracket could not be created")
        return {"bracket_id": None}
    else:
        return {"bracket_id": result}

@router.get("/{event_id}")
def get_brackets(event_id: int):
    with db.engine.begin() as connection:
        result = connection.execute(text("""
                    SELECT id, name, active, game, capacity 
                    FROM brackets 
                    WHERE event_id = :e_id"""),{"e_id":event_id}).mappings().all()

    return result if result else []
