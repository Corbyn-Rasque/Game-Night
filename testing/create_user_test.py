from src.api import users
from src.api.users import User

new_username = "Ninja"
new_fname = "Tyler"
new_lname = "Blevins"
print(users.create_user(User(username=new_username, first=new_fname, last=new_lname)))
