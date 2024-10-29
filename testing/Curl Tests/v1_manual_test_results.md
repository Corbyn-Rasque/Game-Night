# Example Workflow
## Tyler 'Ninja' Blevins as a gaming event host
Tyler 'Ninja' Blevins wants to go to a Fortnite tournament to scout the competition and confirm that he has world class skills. He first checks to see if there is any upcoming tournaments.(GET events/?active=upcoming&game=fortnite). He sees that there isn't any going on at the moment, so decides to make a new event and add a new category to our games list. 

- He starts by making a new event by calling @post /events and passing event name, time, type, max_attendees, location(Fortnite_Tournament_1, 2024-10-15T06:12:23+00:00, Gaming, 100, Baker Building). Tyler gets an event with id 2. 

- Next, Mr. Blevins creates a new bracket for his event with @post /brackets and passing bracket name, start time, game, capacity, and cost to enter(Fortnite_Bracket_1, 2024-10-15T06:12:23+00:00, Fortnite, 100, 0). The bracket has an id of 3.

- When prompted to add the game for the bracket, Tyler adds fortnite to our list of games through @post /games and passing the game's name, platform, publisher, release year, and player amount(Fortnite, PC, Epic_Games, 2017, 4). This creates a new game with an id of 54 which is passed to the bracket creation.

Now Tyler is ready to show off his skills. Unfortunately, he quickly found out he was not as good as he thought and turned towards content creation where he has become very successful. 

# Testing results
 1. curl -X 'POST' \
  'https://brackish.onrender.com/events/events' \
  -H 'accept: application/json' \
  -H 'access_token: f616b86c09e0ee3f524a5bf4c9c6109d' \
  -H 'Content-Type: application/json' \
  -d '{
  "event_name": "Fortnite_Tournament_1",
  "time": "2024-10-15T06:12:23.468Z",
  "type": "Gaming",
  "max_attendees": 100,
  "location": "Baker Building"
}'
2. {
  "event_id": 2
}

1. curl -X 'POST' \
  'https://brackish.onrender.com/brackets/brackets' \
  -H 'accept: application/json' \
  -H 'access_token: f616b86c09e0ee3f524a5bf4c9c6109d' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Fortnite_Bracket_1",
  "date_time": "2024-10-15T06:12:13.172Z",
  "game": "Fortnite",
  "capacity": 100,
  "cost": 0
}'
2. {
  "bracket_id": 3
}

1. curl -X 'POST' \
  'https://brackish.onrender.com/games/games' \
  -H 'accept: application/json' \
  -H 'access_token: f616b86c09e0ee3f524a5bf4c9c6109d' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Fortnite",
  "platform": "XBOX",
  "publisher": "Epic Games",
  "release_year": 2015,
  "player_count": 100
}'
2. {
  "id": 6
}