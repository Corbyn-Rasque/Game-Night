from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import datetime
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/matches",
    tags=["matches"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.get("/{bracket_id}")
def get_matches(bracket_id: int):
    with db.engine.begin() as conn:
        result = conn.execute(sqlalchemy.text("""
                    SELECT matches.id as match_id 
                    FROM matches 
                    WHERE bracket_id = :b_id"""), {"b_id": bracket_id}).mappings().all()

    return result if result else []


class Match(BaseModel):
    bracket_id: int
    match_amount: int

@router.post("/")
def create_match(new_match:Match):
    match_arr = []
    for i in range(new_match.match_amount):
        match_arr.append(
            {
                "bracket_id": new_match.bracket_id,
            }
        )
    with db.engine.begin() as conn:
        conn.execute(sqlalchemy.text("""
                    INSERT INTO matches (bracket_id) 
                    VALUES (:bracket_id)"""),match_arr)

    return "OK"

