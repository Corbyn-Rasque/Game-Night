from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from src.api import auth
import datetime
from sqlalchemy import text
from src import database as db
import math
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
    bracket.num_players = 1 if bracket.num_players <= 0 else 2**math.ceil(math.log2(bracket.num_players))
    create_bracket = text('''INSERT INTO brackets (name, event_id, game_id, time, num_players)
                             VALUES (:name, :event_id, :game_id, :time, :num_players)
                             RETURNING id''')
    with db.engine.begin() as connection:
        result = connection.execute(create_bracket, dict(bracket)).mappings().one_or_none()

    return result

@router.post("/{bracket_id}/players/{user_id}")
def add_user(bracket_id: int, user_id: str):
    add_user = text(''' INSERT INTO bracket_entrants (bracket_id, player_id)
                        SELECT :bracket_id, :user_id
                        FROM bracket_entrants
                        WHERE bracket_id = :bracket_id
                        HAVING count(*)<(SELECT num_players FROM brackets WHERE id =:bracket_id)
                        ON CONFLICT(bracket_id, player_id) DO NOTHING
                        RETURNING bracket_id, player_id''')
    
    with db.engine.begin() as connection:
        result = connection.execute(add_user, {"bracket_id": bracket_id, "user_id": user_id}).mappings().one_or_none()
    print(result)
    return "OK"


@router.delete("/{bracket_id}/players/{user_id}")
def remove_user(bracket_id: int, user_id: int):
    remove_user = text('''DELETE FROM bracket_entrants
                          WHERE (bracket_id, player_id) IN ((:bracket_id, :user_id))''')

    with db.engine.begin() as connection:
        connection.execute(remove_user, {"bracket_id": bracket_id, "user_id": user_id})

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

@router.post("/{bracket_id}/start")
def start_bracket(bracket_id: int, bounds: SeedBounds):
    if bounds.beginner_limit <= 0:
        bounds.beginner_limit = 1
    bounds_dict = dict(bounds)
    bracket_check = text('''SELECT 1 FROM brackets
                            WHERE id = :bracket_id''')

    start_check = text(''' UPDATE brackets SET started = TRUE 
                        WHERE id = :bracket_id
                        AND started = FALSE
                        RETURNING id''')

    player_matchups = text('''WITH bracket_players as (
                              SELECT DISTINCT player_id
                              FROM bracket_entrants
                              WHERE bracket_id = :bracket_id
                            ),
                            scored_players as (
                              SELECT player_id, coalesce((:beginner_limit*sum(score)+(count(1)))/(1+(:beginner_limit*(count(1)))),-22)::float as seed_score 
                              FROM bracket_players
                              LEFT JOIN match_players using(player_id)
                              GROUP BY player_id
                            ),
                            seeded_players as(
                              SELECT :bracket_id as bracket_id, player_id,
                              ROW_NUMBER() over (order by seed_score desc, player_id desc) as seed
                              FROM scored_players
                            ),
                            empties as (
                                SELECT gen,
                                COALESCE(bracket_id, :bracket_id) as bracket_id,
                                COALESCE(player_id, null) as player_id,
                                gen as seed,
                                ROW_NUMBER() over (order by gen desc) as opp_seed
                                FROM generate_series(1,(SELECT num_players FROM brackets WHERE id =:bracket_id)) as gen
                                LEFT JOIN seeded_players on gen = seed
                            ),
                            all_seeds as (
                                SELECT bracket_id, player_id, seed, opp_seed
                                FROM empties
                                ORDER BY seed
                            ),
                            all_matches as(
                                (SELECT id as match_id
                                FROM matches
                                WHERE bracket_id = :bracket_id
                                ORDER BY match_id desc)
                                UNION ALL
                                (SELECT id as match_id
                                FROM matches
                                WHERE bracket_id = :bracket_id
                                ORDER BY match_id asc)
                            ),
                            numbered_matches as (
                                SELECT match_id,
                                ROW_NUMBER() over (ORDER BY 1 asc) as row
                                FROM all_matches
                            )
                            SELECT match_id, player_id, seed 
                            FROM numbered_matches
                            JOIN all_seeds on seed = row
                            ORDER BY seed ASC''')

    match_insertion = text('''  WITH next_round as (
                                    SELECT 
                                    CASE WHEN :player_id is not null 
                                        THEN coalesce(max(round),0)+1
                                        ELSE (SELECT MAX(round) FROM match_players
                                                WHERE player_seed = (SELECT MIN(player_seed) FROM match_players)
                                             )
                                    END as round
                                    FROM match_players
                                    WHERE player_id = :player_id
                                )
                                INSERT INTO match_players(match_id, player_id, player_seed, round)
                                SELECT :match_id, :player_id, :seed, round
                                FROM next_round''')

    bye_info = text('''  with bye_matches as (
                              select distinct match_id from match_players
                              join matches on match_id = matches.id
                              WHERE player_id is null
                              and bracket_id = :bracket_id
                            ),
                            byed_seeds as (
                              select match_id, min(player_seed) as min_seed from match_players
                              JOIN bye_matches using(match_id)
                              group by match_id
                            )
                              select :bracket_id as bracket_id, player_id, match_id, min_seed from byed_seeds
                              JOIN match_players using(match_id)
                              where player_seed = min_seed
                              ORDER BY min_seed ASC
                            ''')

    winner_input = text(''' UPDATE matches SET winner_id = :player_id
                            WHERE matches.id = :match_id''')

    new_match_inserts = text('''with bye_matches as (
                                  select distinct match_id from match_players
                                  join matches on match_id = matches.id
                                  WHERE player_id is null
                                  and bracket_id = :bracket_id
                                ),
                                byed_seeds as (
                                  select match_id, min(player_seed) as min_seed from match_players
                                  JOIN bye_matches using(match_id)
                                  group by match_id
                                ),
                                bye_info as (
                                  select :bracket_id as bracket_id, player_id, match_id, min_seed from byed_seeds
                                  JOIN match_players using(match_id)
                                  where player_seed = min_seed
                                )
                                INSERT INTO matches(bracket_id)
                                SELECT (:bracket_id)
                                FROM generate_series(1, :amount)
                                RETURNING id as match_id''')

    match_linking = text('''WITH old_match_players as (
                                SELECT min(id) as match_id FROM matches
                                WHERE id < :match_id
                                AND next_match is null
                            )
                            UPDATE matches SET next_match = :match_id
                            WHERE matches.id = (SELECT match_id from old_match_players)''')

    clean_byes = text('''   WITH null_rows as (
                                SELECT match_players.id as mp_id FROM match_players
                                JOIN matches on match_id = matches.id
                                WHERE player_id is null
                                AND bracket_id = :bracket_id
                                AND round = 1
                            )          
                            DELETE FROM match_players
                            WHERE id in (SELECT mp_id FROM null_rows)
                            ''')

    try:
        with db.engine.begin() as connection:
            exists = connection.execute(bracket_check, {"bracket_id": bracket_id}).scalar()
            if not exists:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Bracket not found')
            toggled = connection.execute(start_check, {"bracket_id": bracket_id}).scalar()
            if not toggled:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Bracket already started')

            result = connection.execute(player_matchups, {"bracket_id": bracket_id} | bounds_dict).mappings().all()
            connection.execute(match_insertion,result)
            byed = connection.execute(bye_info, {"bracket_id": bracket_id}).mappings().all()
            connection.execute(winner_input,byed)
            new_match_ids = connection.execute(new_match_inserts, {"bracket_id": bracket_id,"amount":(len(byed)//2)+1}).mappings().all()
            new_match_ids.extend(list(reversed(new_match_ids)))
            new_match_id_list = list(dict(x) for x in new_match_ids)
            i = 0
            for match in new_match_id_list:
                match["player_id"] = byed[i]["player_id"] if i<len(byed) else None
                match["seed"] = i+1
                i += 1
            connection.execute(match_insertion, new_match_id_list)
            connection.execute(match_linking, new_match_id_list)
            connection.execute(clean_byes, {"bracket_id": bracket_id})
            print(result)
            return result

    except HTTPException as e:
        logger.error(f"Bracket information not valid")
        raise e
    # except Exception as e:
    #     logger.error(f"Unexpected error seeding bracket: {e}")
    #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error seeding bracket")

#remove_user(4,42)
#add_user(4, 43)
test = SeedBounds(beginner_limit=30)
start_bracket(4, test)