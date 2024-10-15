# Example Flows
## Tyler Ninja Blevins as a gaming event host
Tyler Ninja Blevins wants to make a fortnite tournament to show off his world class skills. He first checks to see if there is any upcoming tournaments.(GET events/?active=upcoming&game=fortnite).He sees that there isn't any going on at the moment, so decides to make a new event and add a new category to our games list. 

- He starts by making a new event by calling @post /events and passing event name, time, type, max_attendees, location(Fortnite_Tournament_1, 2024-10-15T06:12:23+00:00, Gaming, 100). Tyler gets an event with id 842. 

- Next, Mr. Blevins creates a new bracket for his event with @post /brackets and passing bracket name, start time, game, capacity, and cost to enter(Fortnite_Bracket_1, 2024-10-15T06:12:23+00:00, Fortnite, 100, 0). The bracket has an id of 244.

- When prompted to add the game for the bracket, Tyler adds fortnite to our list of games through @post /games and passing the game's name, platform, publisher, release year, and player amount(Fortnite, PC, Epic_Games, 2017, 4). This creates a new game with an id of 54 which is passed to the bracket creation. 

- After all the competitors add themselves to the bracket (we still do not know how we want to do this), Tyler wants to see the bracket so he calls @get /brackets/244/matches.

Now Tyler is ready to show off his skills. Unfortunately, he quickly found out he was not as good as he thought and turned towards content creation where he has become very successful. 

## 