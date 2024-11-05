from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import datetime
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/teams",
    tags=["teams"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.get("/{bracket_id}")
def get_teams(bracket_id: int):
    with db.engine.begin() as conn:
        result = conn.execute(sqlalchemy.text("""
                    SELECT teams.id as team_id 
                    FROM teams 
                    WHERE bracket_id = :b_id"""), {"b_id": bracket_id}).mappings().all()

    return result if result else []


class Team(BaseModel):
    bracket_id: int
    team_name:str

@router.post("/")
def create_team(new_team: Team):
    with db.engine.begin() as conn:
        team_id = conn.execute(sqlalchemy.text("""
                    INSERT INTO teams (bracket_id, team_name) 
                    VALUES (:bracket_id,:team_name) 
                    ON CONFLICT (team_name) DO NOTHING
                    RETURNING id"""),dict(new_team)).scalar_one_or_none()

    if team_id is None:
        # try getting new event info again
        return {"team_id": None}
    else:
        return {"team_id": team_id}
