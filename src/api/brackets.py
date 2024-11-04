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
    bracket_dict = {
        "name": new_bracket.name,
        "date_time": new_bracket.date_time,
        "game": new_bracket.game,
        "capacity": new_bracket.capacity,
        "cost": new_bracket.cost,
    }

    with db.engine.begin() as connection:
        result = connection.execute(text("""
                    INSERT INTO brackets 
                    (name, date_time, game, capacity, cost) 
                    VALUES (:name, :date_time, :game, :capacity, :cost) 
                    RETURNING id """), bracket_dict).scalar_one_or_none()
    if result is None:
        print("Bracket could not be created")
        return {"bracket_id": None}
    else:
        return {"bracket_id": result}