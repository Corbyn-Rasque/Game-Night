from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.api import auth
from sqlalchemy import text
from src import database as db

router = APIRouter(
    prefix="/games",
    tags=["games"],
    dependencies=[Depends(auth.get_api_key)],
)

class Game(BaseModel):
    name: str
    platform: str
    publisher: str
    release_year: int
    player_count: int

@router.post("/")
def add_game(game: Game):
    add_game = text("""INSERT INTO games (name, platform, publisher, release_year, player_count)
                       VALUES (:name, :platform, :publisher, :release_year, :player_count)
                       ON CONFLICT(name, platform) DO NOTHING
                       RETURNING id
                       """)
    try:
        with db.engine.begin() as connection:
            response = connection.execute(add_game, dict(game)).scalar_one_or_none()
        return dict(zip(["id"], [response]))
    except Exception:
        raise HTTPException(status_code=400,detail="Unexpected error inserting game")

@router.get("/{name}")
def get_game(name: str, platform = None):
    get_game = """SELECT id 
                  FROM games
                  WHERE name = :name """
    
    with_platform = "AND platform = :platform" if platform else ""
    try:
        with db.engine.begin() as connection:
            result = connection.execute(text(get_game + with_platform), {"name": name, "platform": platform}).mappings().first()
        return result if result else {}
    except Exception:
        raise HTTPException(status_code=400,detail="Unexpected error getting game")