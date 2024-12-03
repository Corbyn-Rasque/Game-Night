from fastapi import HTTPException, APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import datetime
from sqlalchemy import text
from src import database as db

router = APIRouter(
    prefix="/teams",
    tags=["teams"],
    dependencies=[Depends(auth.get_api_key)],
)

class Team(BaseModel):
    id: int
    name:str

class Team_Player(BaseModel):
    team_id: int
    player_id: int


@router.get("/{team_id}/players", status_code=200)
def get_team_players(team_id: int):
    query_players = text('''SELECT player_id
                            FROM team_players
                            WHERE team_id = :team_id''')
    try:
        with db.engine.begin() as connection:
            results = connection.execute(query_players, {"team_id": team_id}).mappings().all()
        return results
    except Exception:
        raise HTTPException(status_code=400, detail="Error getting players")

@router.post("", status_code=201)
def create_team(name: str):
    add_team = text('''INSERT INTO teams (name)
                       VALUES (:name)
                       RETURNING id''')
    
    try:
        with db.engine.begin() as connection:
            result = connection.execute(add_team, {"name": name}).mappings().one()
        return result
    except Exception:
        raise HTTPException(status_code=400,detail="Error creating team")

@router.delete("/{team_id}",status_code=200)
def remove_team(team_id: int):
    remove_team = text('''DELETE FROM teams
                          WHERE id = :team_id''')
    
    try:
        with db.engine.begin() as connection:
            connection.execute(remove_team, {"team_id": team_id})
        return "OK"
        print(create_team("my favorite team :D"))
    except Exception:
        raise HTTPException(status_code=418, detail="Error deleting team")