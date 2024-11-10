from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import datetime
from sqlalchemy import text
from src import database as db

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