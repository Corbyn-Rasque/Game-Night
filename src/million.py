from faker import Faker
from random_username.generate import generate_username as gen_u
from src.api import users, events, brackets
from timeit import default_timer as timer

def mill_users(amount:int):
    fake = Faker()
    unames = gen_u(amount)
    names = [fake.name().split() for i in range(amount)]
    user_list = []
    for i in range(amount):
        user_list.append(
            users.User(username=unames[i], first=names[i][0], last=names[i][1])
        )
    return user_list

s = timer()
player_ids = []
n = 10
while len(player_ids) < n:
    new_users = mill_users(n-len(player_ids))
    player_ids.extend(users.create_user(new_users))

huge_event = events.Event(host="CorbynR", name="The Tournament to End All Tournaments", type="Gaming", start = "2024-11-08T22:44:47.327Z", stop="2025-01-01T22:44:47.327Z",location="Colosseum in Rome, Italy",max_attendees = 1000000)
event_info = events.create_event(huge_event)

huge_bracket = brackets.Bracket(name="The World's Biggest Bracket EVER!!", event_id= event_info['event_id'], game_id = 7, time="2024-11-09T22:44:47.327Z", num_players = 1000000)
bracket_info = brackets.create_bracket(huge_bracket)

events.join_event(event_info['event_id'], player_ids)
brackets.add_user(bracket_info['id'], player_ids)

