from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.responses import JSONResponse
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

    platforms = ['pc', 'playstation', 'xbox']
    if not isinstance(game.release_year, int) or game.release_year <= 0:
        response = "release_year should be a non negative Int"
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=response)
    if not isinstance(game.player_count, int) or game.player_count <= 0:
        response = "player_count should be a non negative Int"
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=response)
    
    if game.platform not in platforms:
        response = f"Platform must be one of the following: {platforms}"
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=response)
    

    add_game = text("""INSERT INTO games (name, platform, publisher, release_year, player_count)
                       VALUES (:name, :platform, :publisher, :release_year, :player_count)
                       RETURNING id
                       """)

    try :
        with db.engine.begin() as connection:
            game_id = connection.execute(add_game, dict(game)).scalar_one_or_none()
    except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while inserting: {str(e.args)}")

    print(f"{game.name} was successfully added to the list")

    return  {"id" : game_id}



@router.get("/{name}")
def get_game(name: str, platform = None):

    get_game = "SELECT id FROM games WHERE name = :name "
    with_platform = "AND platform = :platform" if platform else ""
    
    with db.engine.begin() as connection:
        result = connection.execute(text(get_game + with_platform), {"name": name, "platform": platform}).mappings().first()
    
    if not result:
        raise HTTPException(status_code=404, detail=f"Game: {name} was not found:")

    return result    
