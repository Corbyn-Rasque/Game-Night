from src.api import users

new_username = "Ninja"
new_fname = "Tyler"
new_lname = "Blevins"
print(users.create_user(new_username, new_fname, new_lname))
