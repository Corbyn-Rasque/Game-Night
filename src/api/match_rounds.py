from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import datetime
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/match_rounds",
    tags=["match_rounds"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.get("/{match_id}")
def get_rounds(match_id: int):
    with db.engine.begin() as conn:
        result = conn.execute(sqlalchemy.text("""
                    SELECT match_rounds.id as round_id 
                    FROM match_rounds
                    WHERE match_id = :m_id"""), {"m_id": match_id}).mappings().all()

    return result if result else []


class Round(BaseModel):
    match_id: int
    team_a_id: int
    team_b_id: int

@router.post("/")
def create_round(new_round: Round):
    with db.engine.begin() as conn:
        round_id = conn.execute(sqlalchemy.text("""
                        INSERT INTO match_rounds (match_id,team_a_id,team_b_id) 
                        VALUES (:match_id,:team_a_id,:team_b_id) 
                        RETURNING id"""),dict(new_round)).scalar_one_or_none()

    if round_id is None:
        # try getting new event info again
        return {"round_id": None}
    else:
        return {"round_id": round_id}


