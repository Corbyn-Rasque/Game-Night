# Example Flows

## Tyler 'Ninja' Blevins as a gaming event host
Tyler 'Ninja' Blevins wants to go to a Fortnite tournament to scout the competition and confirm that he has world class skills. He first checks to see if there is any upcoming tournaments.(GET events/?active=upcoming&game=fortnite). He sees that there isn't any going on at the moment, so decides to make a new event and add a new category to our games list. 

- He starts by making a new event by calling @post /events and passing event name, time, type, max_attendees, location(Fortnite_Tournament_1, 2024-10-15T06:12:23+00:00, Gaming, 100). Tyler gets an event with id 842. 

- Next, Mr. Blevins creates a new bracket for his event with @post /brackets and passing bracket name, start time, game, capacity, and cost to enter(Fortnite_Bracket_1, 2024-10-15T06:12:23+00:00, Fortnite, 100, 0). The bracket has an id of 244.

- When prompted to add the game for the bracket, Tyler adds fortnite to our list of games through @post /games and passing the game's name, platform, publisher, release year, and player amount(Fortnite, PC, Epic_Games, 2017, 4). This creates a new game with an id of 54 which is passed to the bracket creation. 

- After all the competitors add themselves to the bracket (we still do not know how we want to do this), Tyler wants to see the bracket so he calls @get /brackets/244/matches.

Now Tyler is ready to show off his skills. Unfortunately, he quickly found out he was not as good as he thought and turned towards content creation where he has become very successful. 

## Joseph 'Mang0' Marquez wants to study up on matchups
Joseph 'Mang0' Marquez is a pro Super Smash Bros. Melee player that wants to get better. However, Mang0 has forgotten what brackets he has been a part of and the matches that he played in those brackets. He uses our API to find this information.

- First, Mang0 goes to his user profile which shows all the previous events he has attended (not shown in API but will be added at some point). This is done with a call to @get /events?active=past&type=gaming.

- Mang0 recognizes one of the events (with event_id = 23423) and clicks on it to see the bracket which is done with @get /brackets/23423 

- He finds the Super Smash Bros. Melee bracket and clicks it to see the matches that took place. This is done through the call @get /brackets/23423/matches.

- He now can see that he won some matches against lesser known players but lost to his rival, Zain, in a 3-0 blowout. 

Now Mang0 knows he needs to practice playing against Zain's character, Marth. He will lock in and train for the next tournament. 

## CSC 365 Thanksgiving Party
Professor Pierce wants to host a Thanksgiving house party for his students, but is lost on where to start. He knows of Game Night, a gaming-oriented party planning app, and is inspired to create and event through the app to help coordinate everything. He wants everyone who wants to go to be able to register through the app, and wants people to be able to bring snacks and food, and to be able to see what other people are bringing and and how many of those things.

- He starts by creating a new event by calling @post /events and passing event name, time, type, max_attendees, location(Pierce Palace, 2024-11-27T01:00:00+00:00, Dining, len(class)). Professor Pierce receives an event with id 420.

- Next, a new bracket is created for the event with @post /brackets, passing bracket name, start time, event type, capacity, and cost (Thanksgiving_Dinner, 2024-11-27T01:00:00+00:00, Party, len(class), 0). The bracket has an id of 420.

- Students will be able to find the event using @get /events/Party and perusing the list of active events through the interface, after the json file containing the names of all active events of Party type are returned. Users will be able to add themselves as long as there is still room available.

- Professor Pierce can add all of the foods and drinks he would like to supply, or would like for people to supply, by using @post /items to add all of the items he would like by providing name, type of object, quantity available and quantity requested, as well as cost if he'd like people to pitch in for anything. He accidentally adds an extra RED_POTION_100 to the request (even though Thanksgiving is on Edgeday, where no one's buying [100, 000, 000, 000] type potions), so he uses the @delete /items/{item_id} by clicking the delete button on the page that makes the request, and it's removed after the item ID is sent in the background.

The professor then checks all of the gets the Thanksgiving catalog and sees if anyone else has added anything using the @get /items endpoint, and sees a list of all items and potions that have been added, and is happy to see that everyone has brought the *perfect* mix of potions for the party.