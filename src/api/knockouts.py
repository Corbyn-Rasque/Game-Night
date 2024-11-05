from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import datetime
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/knockouts",
    tags=["knockouts"],
    dependencies=[Depends(auth.get_api_key)],
)

class Knockout(BaseModel):
    match_a_id: int
    match_b_id: int

@router.post("/{bracket_id}")
def create_knockout(new_ko : Knockout, bracket_id : int):
    with db.engine.begin() as conn:
        ko_id = conn.execute(sqlalchemy.text("""
                        WITH match_insert AS(
                            INSERT INTO matches (bracket_id) 
                            VALUES (:bracket_id) 
                            RETURNING matches.id as inserted_match
                        )
                        INSERT INTO match_knockouts (match_id,winner_a_id, winner_b_id) 
                        SELECT inserted_match, (SELECT win_team_id FROM matches WHERE matches.id = :match_a_id), 
                        (SELECT win_team_id FROM matches WHERE matches.id = :match_b_id) from match_insert
                        RETURNING match_knockouts.id"""),dict(new_ko) | {"bracket_id":bracket_id}).scalar_one_or_none()

    if ko_id is None:
        # try getting new event info again
        return {"ko_id": None}
    else:
        return {"ko_id": ko_id}
