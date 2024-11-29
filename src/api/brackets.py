from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from src.api import auth
import datetime
from sqlalchemy import text
from src import database as db
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/brackets",
    tags=["brackets"],
    dependencies=[Depends(auth.get_api_key)],
)

class Bracket(BaseModel):
    name: str
    event_id: int
    game_id: int
    time: datetime.datetime
    match_size: int
    num_players: int

class Match(BaseModel):
    id: int
    bracket_id: int
    next_match: int = None
    winner_id: int = None


@router.get("")
def get_bracket(name: str = None, event_id: int = None, game_id: int = None):
    get_brackets = text('''SELECT name, event_id, game_id, time, match_size, num_players
                           FROM brackets
                           WHERE name = COALESCE(:name, name)
                               AND event_id = COALESCE(:event_id, event_id)
                               AND game_id = COALESCE(:game_id, game_id)''')
    
    with db.engine.begin() as connection:
        results = connection.execute(get_brackets,
                                     {"name": name, "event_id": event_id, "game_id": game_id}).mappings().all()
        
    return results


@router.get("/{bracket_id}")
def get_bracket_by_id(bracket_id: int):
    get_bracket = text('''SELECT name, event_id, game_id, time, match_size, num_players
                          FROM brackets
                          WHERE id = :bracket_id''')
    
    with db.engine.begin() as connection:
        result = connection.execute(get_bracket, {"bracket_id": bracket_id}).mappings().one_or_none()

    return result


@router.get("/{bracket_id}/matches")
def get_matches(bracket_id: int):
    match_query = text('''SELECT id
                          FROM matches
                          WHERE bracket_id = :bracket_id''')
    
    with db.engine.begin() as connection:
        results = connection.execute(match_query, {"bracket_id": bracket_id}).mappings().all()

    return results


@router.get("/{bracket_id}/players")
def get_players(bracket_id: int):
    bracket_players_query = text('''SELECT DISTINCT player_id
                                    FROM match_players
                                    JOIN matches ON matches.id = match_players.match_id
                                    WHERE bracket_id = :bracket_id''')
    
    with db.engine.begin() as connection:
        results = connection.execute(bracket_players_query, {"bracket_id": bracket_id}).mappings().all()

    return results


@router.get("/{bracket_id}/matches/{match_id}/players/")
def get_match_players(bracket_id: int, match_id: int):
    match_users_query = text('''SELECT DISTINCT match_players.player_id
                                FROM matches
                                JOIN match_players ON match_players.match_id = :match_id
                                WHERE bracket_id = :bracket_id''')
    
    with db.engine.begin() as connection:
        results = connection.execute(match_users_query, 
                                     {"bracket_id": bracket_id, "match_id": match_id}).mappings().all()

    return results


@router.post("")
def create_bracket(bracket: Bracket):
    create_bracket = text('''INSERT INTO brackets (name, event_id, game_id, time, match_size, num_players)
                             VALUES (:name, :event_id, :game_id, :time, :match_size, :num_players)
                             RETURNING id''')
    
    with db.engine.begin() as connection:
        result = connection.execute(create_bracket, dict(bracket)).mappings().one_or_none()

    return result

@router.post("/{bracket_id}/matches/{match_id}/players/{user_id}")
def add_user(bracket_id: int, match_id: int, user_id: str):
    add_user = text('''INSERT INTO match_players (match_id, player_id)
                       VALUES (:match_id, :user_id)''')
    
    with db.engine.begin() as connection:
        connection.execute(add_user, {"match_id": match_id, "user_id": user_id})

    return "OK"


@router.delete("/{bracket_id}/matches/{match_id}/players/{user_id}")
def remove_user(bracket_id: int, match_id: int, user_id: int):
    remove_user = text('''DELETE FROM match_players
                          WHERE (match_id, player_id) IN ((:match_id, :user_id))''')

    with db.engine.begin() as connection:
        connection.execute(remove_user, {"match_id": match_id, "user_id": user_id})

    return "OK"


@router.delete("/{bracket_id}")
def remove_bracket(bracket_id: int):
    remove_bracket = text('''DELETE FROM brackets
                             WHERE id = :bracket_id''')
    
    with db.engine.begin() as connection:
        connection.execute(remove_bracket, {"bracket_id": bracket_id})

    return "OK"

class SeedBounds(BaseModel):
    beginner_limit: int

@router.post("/{bracket_id}/seeding")
def seed_bracket(bracket_id: int, bounds: SeedBounds):
    if bounds.beginner_limit <= 0:
        bounds.beginner_limit = 1
    bounds_dict = dict(bounds)
    id_check = text('''SELECT 1 FROM brackets WHERE id = :bracket_id''')

    player_winrates = text('''WITH bracket_players as (
                                    SELECT DISTINCT player_id
                                    FROM match_players
                                    JOIN matches ON matches.id = match_players.match_id
                                    WHERE bracket_id = :bracket_id
                                ),
                                scored_players as (
                                    SELECT player_id, (:beginner_limit*sum(score)+(count(1)))/(1+(:beginner_limit*(count(1)))) as seed_score 
                                    FROM bracket_players
                                    JOIN match_players using(player_id)
                                    GROUP BY player_id
                                    order by seed_score desc
                                )
                                SELECT :bracket_id as bracket_id, player_id,
                                ROW_NUMBER() over (order by seed_score desc) as seed
                                FROM scored_players
                                ''')

    insertion = text('''INSERT INTO bracket_seeds (bracket_id, player_id, seed)
                        VALUES (:bracket_id, :player_id, :seed)
                        ON CONFLICT (bracket_id, player_id) DO
                            UPDATE SET seed = :seed
                        RETURNING bracket_id, player_id, seed''')

    try:
        with db.engine.begin() as connection:
            exists = connection.execute(id_check, {"bracket_id": bracket_id}).scalar()
            if not exists:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Bracket not found')
            result = connection.execute(player_winrates, {"bracket_id": bracket_id} | bounds_dict).mappings().all()
            connection.execute(insertion, result)

            print(result)
            return result

    except HTTPException as e:
        logger.error(f"Bracket not found")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error seeding bracket: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error seeding bracket")

bounds = SeedBounds(beginner_limit=0)
seed_bracket(4,bounds)