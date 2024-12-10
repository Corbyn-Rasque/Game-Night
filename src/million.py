from faker import Faker
from random_username.generate import generate_username as gen_u
from src.api import users

def mill_users(amount:int):
    fake = Faker()
    unames = gen_u(amount)
    names = [fake.name().split() for i in range(amount)]
    user_list = []
    for i in range(amount):
        user_list.append(
            users.User(username=unames[i], firstname=names[i][0], lastname=names[i][1])
        )
    return user_list

new_users = mill_users(333333)

users.create_user(new_users)