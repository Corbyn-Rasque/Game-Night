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

    start_check = text('''  WITH num as (
                                SELECT count(1) as entrants FROM bracket_entrants
                                WHERE bracket_id = :bracket_id
                            ) 
                        UPDATE brackets SET started = TRUE, num_players = POW(2,CEIL(LOG(2,((SELECT entrants FROM num)))))
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
            if byed:
                connection.execute(winner_input,byed)
                connection.execute(clean_byes, {"bracket_id": bracket_id})

            print(result)
            return result

    except HTTPException as e:
        logger.error(f"Bracket information not valid")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error seeding bracket: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error seeding bracket")


@router.post("/{bracket_id}/round/")
def finish_round(bracket_id:int):
    exist_check = text('''  SELECT id as bid FROM brackets
                            WHERE id = :bracket_id
                            AND started = TRUE
                            AND winner_id is null''')

    bracket_done_check = text('''   select matches.id as mid from matches
                                    where bracket_id = :bracket_id
                                    and winner_id is null''')

    new_seeding = text('''  with old_matches as (
                            select matches.id as mid, winner_id from matches
                            where bracket_id = :bracket_id
                            and next_match is null
                            and winner_id is not null
                            )
                              insert into matches (bracket_id)
                              SELECT (:bracket_id) from
                              generate_series(1, (SELECT count(1)/2 FROM old_matches))
                            ;
                            with old_matches as (
                            select matches.id as mid, winner_id from matches
                            where bracket_id = :bracket_id
                            and next_match is null
                            and winner_id is not null
                            ),
                            new_matches_mirrored as(
                              (select matches.id as nmid from matches 
                              where bracket_id = :bracket_id
                              and winner_id is null
                              order by nmid asc)
                              union all
                              (select matches.id as nmid from matches 
                              where bracket_id = :bracket_id
                              and winner_id is null
                              order by nmid desc)
                            ),
                            new_matches_numbered as(
                              select nmid,
                              ROW_NUMBER() over (order by 1 asc) as row
                              FROM new_matches_mirrored
                            ),
                            to_advance as(
                            select mid, winner_id, player_seed as seed from match_players
                            JOIN old_matches on mid = match_id
                            group by mid, player_seed, winner_id
                            having player_seed <= (select count(1) FROM old_matches)
                            order by player_seed asc
                            )
                            select :bracket_id as bracket_id, nmid as match_id, winner_id, seed 
                            from new_matches_numbered
                            join to_advance on row = seed
                            order by seed asc''')

    match_player_insert = text('''  with next_round as(
                                        SELECT max(round) as round FROM match_players
                                        join matches on match_id = matches.id
                                        where player_id = :winner_id
                                        and bracket_id = :bracket_id
                                    )
                                    INSERT INTO match_players(match_id, player_id, player_seed, round)
                                    SELECT :match_id, :winner_id, :seed, round+1
                                    FROM next_round''')

    get_next_matches = text(''' SELECT match_id, matches.id as mid from match_players
                                join matches on player_id = winner_id
                                where bracket_id = :bracket_id
                                and round = 
                                (SELECT max(round) from match_players join matches on match_id = matches.id
                                WHERE bracket_id =:bracket_id)''')
    match_linking = text('''UPDATE matches SET next_match = :match_id
                            WHERE matches.id = :mid''')
    try:
        with db.engine.begin() as connection:
            exits = connection.execute(exist_check, {'bracket_id': bracket_id}).scalar()
            if not exits:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Valid bracket with info given not found. Try starting bracket or getting winner.')
            some_null = connection.execute(bracket_done_check,{"bracket_id": bracket_id}).all()
            if some_null:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Round is not finished')
            next_matches = connection.execute(new_seeding, {"bracket_id": bracket_id}).mappings().all()
            connection.execute(match_player_insert,next_matches)
            match_pairings = connection.execute(get_next_matches, {"bracket_id": bracket_id}).mappings().all()
            connection.execute(match_linking,match_pairings)
            return "OK"
    except HTTPException as e:
        logger.error(f"Bracket information not valid")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error finishing round: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error finishing round")

class MatchWon(BaseModel):
    won_by_id:int

@router.post("/{bracket_id}/winner")
def declare_winner(bracket_id:int, winner:MatchWon):
    update_check = text('''with bracket_check as (
                              SELECT id as bid FROM brackets
                              WHERE id = :bracket_id
                              AND started = TRUE
                            ),
                            match_check as (
                              select match_id as mid from bracket_check
                              join matches on bid = bracket_id
                              join match_players on matches.id = match_id
                              where winner_id is null 
                              and player_id = :won_by_id
                            )
                            update matches 
                            set winner_id = :won_by_id
                            where id = 
                            (select mid from match_check)
                            RETURNING id''')

    update_score = text('''UPDATE match_players SET score = 1
                            WHERE player_id = :won_by_id
                            and match_id = :match_id''')
    try:
        with db.engine.begin() as connection:
            exists = connection.execute(update_check,{"bracket_id":bracket_id}|dict(winner)).scalar()
            if not exists:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Winner or bracket info not valid')
            connection.execute(update_score,dict(winner)|{"match_id":exists})
            return "OK"
    except HTTPException as e:
        logger.error(f"Winner information not valid")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error updating winner: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error updating winner")



#remove_user(4,42)
#add_user(4, 43)
# test = SeedBounds(beginner_limit=0)
# start_bracket(54, test)
# won_test = MatchWon(won_by_id = 38)
# declare_winner(4,won_test)
#
# finish_round(54)


# new_match_inserts = text('''with bye_matches as (
#                                   select distinct match_id from match_players
#                                   join matches on match_id = matches.id
#                                   WHERE player_id is null
#                                   and bracket_id = :bracket_id
#                                 ),
#                                 byed_seeds as (
#                                   select match_id, min(player_seed) as min_seed from match_players
#                                   JOIN bye_matches using(match_id)
#                                   group by match_id
#                                 ),
#                                 bye_info as (
#                                   select :bracket_id as bracket_id, player_id, match_id, min_seed from byed_seeds
#                                   JOIN match_players using(match_id)
#                                   where player_seed = min_seed
#                                 )
#                                 INSERT INTO matches(bracket_id)
#                                 SELECT (:bracket_id)
#                                 FROM generate_series(1, :amount)
#                                 RETURNING id as match_id''')
#
#     match_linking = text('''WITH old_match_players as (
#                                 SELECT min(id) as match_id FROM matches
#                                 WHERE id < :match_id
#                                 AND next_match is null
#                             )
#                             UPDATE matches SET next_match = :match_id
#                             WHERE matches.id = (SELECT match_id from old_match_players)''')





#
# with old_matches as (
# select matches.id as mid from matches
# where bracket_id = 4
# and next_match is null
# )
# select match_id, player_seed from match_players
# JOIN old_matches on mid = match_id
# group by match_id, player_seed
# having player_seed <= (select count(1) FROM old_matches)