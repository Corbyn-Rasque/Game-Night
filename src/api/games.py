from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from src.api import auth
from sqlalchemy import text, exc
from src import database as db
from typing import Optional

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

@router.post("/", status_code = status.HTTP_201_CREATED)
def add_game(game: Game):
    insert_game =    '''INSERT INTO games (name, platform, publisher, release_year, player_count)
                        VALUES (:name, :platform, :publisher, :release_year, :player_count)
                        RETURNING id'''
    
    with db.engine.begin() as connection:
        try:
            game_id = connection.execute(text(insert_game), dict(game)).mappings().one()
            return game_id

        except exc.IntegrityError as e:
            error = str(e.orig)

            if 'games_pkey' in error:
                raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = 'Game already exists.')
            elif 'name' in error:
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'Name must not be default.')
            elif 'platform' in error:
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'Platform must not be default.')
            elif 'publisher' in error:
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'Publisher must not be default.')
            elif 'release_year' in error:
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'Release year must be zero or greater.')
            elif 'player_count' in error:
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'Player count must be one or more.')

        except exc.NoResultFound:
            raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = 'Error inserting game.')


@router.get("/{name}", status_code = status.HTTP_200_OK)
def get_game(name: str, platform: Optional[str] = None):

    name = f'%{name}%' if name else None
    platform = f'%{platform}%' if platform else None

    query =  '''SELECT id, name, platform, publisher, release_year, player_count
                FROM games
                WHERE name ILIKE :name AND (:platform IS NULL OR platform ILIKE :platform)'''
    
    with db.engine.begin() as connection:
        games = connection.execute(text(query), {"name": name, "platform": platform}).mappings().all()
    
    if not games: raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'No matching game found.')
    else: return games
