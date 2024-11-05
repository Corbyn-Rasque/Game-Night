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
    best_of: int
    round:int
@router.post("/")
def create_match(new_match:Match,matches_amount: int):
    match_arr = []
    for i in range(matches_amount):
        match_arr.append(
            {
                "bracket_id": new_match.bracket_id,
                "best_of": new_match.best_of,
                "round": new_match.round,
            }
        )
    with db.engine.begin() as conn:
        result = conn.execute(sqlalchemy.text("""
                    INSERT INTO matches (bracket_id,best_of,round) 
                    VALUES (:bracket_id,:best_of,:round) 
                    RETURNING id"""),match_arr).fetchall()

    return result if result else []


test_match = Match(bracket_id = 4, best_of = 3, round = 1)
print(create_match(test_match,8))