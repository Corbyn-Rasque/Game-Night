from faker import Faker
from random_username.generate import generate_username as gen_u
from src.api import users, events, brackets
from timeit import default_timer as timer
import math
from random import randint

def mill_users(amount:int):
    fake = Faker()
    unames = gen_u(amount)
    names = [fake.name().split() for i in range(amount)]
    user_list = []
    for i in range(amount):
        user_list.append(
            users.User(username=unames[i]+str((1,1000)), first=names[i][0], last=names[i][1])
        )
    return user_list

ts = 0
s = timer()
player_ids = []
n =
while len(player_ids) < n:
    new_users = mill_users(n-len(player_ids))
    player_ids.extend(users.create_user(new_users))
e = timer()
ts += e-s
print("users\t\t",e-s)
huge_event = events.Event(host=new_users[0].username, name="The Tournament to End All Tournaments", type="Gaming", start = "2024-11-08T22:44:47.327Z", stop="2025-01-01T22:44:47.327Z",location="Colosseum in Rome, Italy",max_attendees = 1000000)
event_info = events.create_event(huge_event)

huge_bracket = brackets.Bracket(name="The World's Biggest Bracket EVER!!", event_id= event_info['event_id'], game_id = 7, time="2024-11-09T22:44:47.327Z", num_players = 1000000)
bracket_info = brackets.create_bracket(huge_bracket)

s= timer()
events.join_event(event_info['event_id'], player_ids)
brackets.add_user(bracket_info['id'], player_ids)
e = timer()
ts += e-s
print("add users\t",e-s)

s = timer()
bracket_start_body = brackets.SeedBounds(beginner_limit = 1)
bracket_visualizer = brackets.start_bracket(bracket_info['id'], bracket_start_body)
e= timer()
ts += e-s
print("start\t\t",e-s)

# bracket has started I will now complete da bracket
s = timer()
near_pow = 2**math.ceil(math.log2(n))
num_winners = (2*n-near_pow)//2
winners = []
for i in range(num_winners):
    winners.append(brackets.MatchWon(won_by_id = bracket_visualizer[(len(bracket_visualizer)//2)-1-i]['player_id']))

brackets.declare_winner(bracket_info['id'], winners)

e = timer()
ts += e-s
print("winners\t\t",e-s)

# first round wins done
s=timer()
brackets.finish_round(bracket_info['id'])
e = timer()
ts += e-s
print("round\t\t",e-s)
print("total\t\t", ts)
near_pow = near_pow//2

while near_pow > 1:
    winners = []
    near_pow = near_pow//2
    for i in range(near_pow):
        winners.append(brackets.MatchWon(won_by_id = bracket_visualizer[i]['player_id']))
    brackets.declare_winner(bracket_info['id'], winners)
    if near_pow != 1:
        brackets.finish_round(bracket_info['id'])