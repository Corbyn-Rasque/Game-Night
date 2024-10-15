# Example Flows
## Tyler 'Ninja' Blevins as a gaming event host
Tyler 'Ninja' Blevins wants to go to a Fortnite tournament to scout the competition and confirm that he has world class skills. He first checks to see if there is any upcoming tournaments.(GET events/?active=upcoming&game=fortnite). He sees that there isn't any going on at the moment, so decides to make a new event and add a new category to our games list. 

- He starts by making a new event by calling @post /events and passing event name, time, type, max_attendees, location(Fortnite_Tournament_1, 2024-10-15T06:12:23+00:00, Gaming, 100). Tyler gets an event with id 842. 

- Next, Mr. Blevins creates a new bracket for his event with @post /brackets and passing bracket name, start time, game, capacity, and cost to enter(Fortnite_Bracket_1, 2024-10-15T06:12:23+00:00, Fortnite, 100, 0). The bracket has an id of 244.

- When prompted to add the game for the bracket, Tyler adds fortnite to our list of games through @post /games and passing the game's name, platform, publisher, release year, and player amount(Fortnite, PC, Epic_Games, 2017, 4). This creates a new game with an id of 54 which is passed to the bracket creation. 

Now Tyler is ready to see how good his skills are. Unfortunately, he quickly found out he was not as good as he thought and turned towards content creation where he has become very successful. 

## Joseph 'Mang0' Marquez wants to study up on matchups
Joseph 'Mang0' Marquez is a pro Super Smash Bros. Melee player that wants to get better. However, Mang0 has forgotten what brackets he has been a part of and the matches that he played in those brackets. He uses our API to find this information.

- First, Mang0 goes to his user profile which shows all the previous events he has attended (not shown in API but will be added at some point). This is done with a call to @get /events?active=past&type=gaming.

- Mang0 recognizes one of the events (with event_id = 23423) and clicks on it to see the bracket which is done with @get /brackets/23423 

- He finds the Super Smash Bros. Melee bracket and clicks it to see the matches that took place. This is done through the call @get /brackets/23423/matches.

- He now can see that he won some matches against lesser known players but lost to his rival, Zain, in a 3-0 blowout. 

Now Mang0 knows he needs to practice playing against Zain's character, Marth. He will lock in and train for the next tournament. 