# CSC 365 Thanksgiving Party
Professor Pierce wants to host a Thanksgiving house party for his students, but is lost on where to start. He knows of Game Night, a gaming-oriented party planning app, and is inspired to create ans event through the app to help coordinate everything. He wants everyone who wants to go to be able to register through the app, and wants people to be able to bring snacks and food, and to be able to see what other people are bringing and and how many of those things.

- He starts by creating a new event by calling @post /events and passing event name, time, type, active, max_attendees, & location. (Arcane Alchemy Summit, 2024-11-27T01:00:00+00:00, Dining, Upcoming, len(class)*2, Pierce Palace). Professor Pierce receives an event with id 420.

- Next, a new bracket is created for the event with @post /brackets, passing bracket name, start time, event type, capacity, and cost (Arcane Alchemy Summit, 2024-11-27T01:00:00+00:00, Party, len(class), 0). The bracket has an id of 420.

- Students will be able to find the event using @get /events/Party and perusing the list of active events through the interface, after the json file containing the names of all active events of Party type are returned. Users will be able to add themselves as long as there is still room available.

- Professor Pierce can add all of the foods and drinks he would like to supply, or would like for people to supply, by using @post /items to add all of the items he would like by providing name, type of object, quantity available and quantity requested, as well as cost if he'd like people to pitch in for anything. He accidentally adds an extra RED_POTION_100 to the request (even though Thanksgiving is on Edgeday, where no one's buying [100, 000, 000, 000] type potions), so he uses the @delete /items/{item_id} by clicking the delete button on the page that makes the request, and it's removed after the item ID is sent in the background.

The professor then checks all of the gets the Thanksgiving catalog and sees if anyone else has added anything using the @get /items endpoint, and sees a list of all items and potions that have been added, and is happy to see that everyone has brought the *perfect* mix of potions for the party.

## Test Results

### Event Creation

#### Request
```
curl -X 'POST' \
'https://brackish.onrender.com/events/' \
-H 'accept: application/json' \
-H 'access_token: f616b86c09e0ee3f524a5bf4c9c6109d' \
-H 'Content-Type: application/json' \
-d '{
"event_name": "Arcane Alchemy Summit",
"time": "2024-11-16T15:00:00.000Z",
"type": "Party",
"active": "Upcoming",
"max_attendees": 70,
"location": "Pierce Palace"
}'
```

#### Response
```
{ "event_id": 420 }
```

### Bracket Creation
#### Request
```
curl -X 'POST' \
'https://brackish.onrender.com/brackets/' \
-H 'accept: application/json' \
-H 'access_token: f616b86c09e0ee3f524a5bf4c9c6109d' \
-H 'Content-Type: application/json' \
-d '{
"name": "Attendees",
"date_time": "2024-11-16T16:00:00Z",
"game": "Dinner",
"capacity": 70,
"cost": 0
}'
```

#### Response
```
{ "bracket_id": 420 }
```

### Party Finding

#### Request
```
curl -X 'GET' \
'https://brackish.onrender.com/events?name=Alchemy&stop=2024-11-30T00%3A00%3A00Z' \
-H 'accept: application/json' \
-H 'access_token: f616b86c09e0ee3f524a5bf4c9c6109d'
```

#### Response
```
{
"name": "Arcane Alchemy Summit",
"type": "Party",
"location": "Pierce Palace",
"max_attendees": 70,
"start": "2024-11-16T15:00:00",
"stop": "2024-11-16T18:00:00"
}
```

### Item Request

#### Request
```
curl -X 'POST' \
'https://brackish.onrender.com/items/16/requests' \
-H 'accept: application/json' \
-H 'access_token: f616b86c09e0ee3f524a5bf4c9c6109d' \
-H 'Content-Type: application/json' \
-d '{
"name": "RED_POTION_100",
"type": "Potion",
"quantity": 70,
"payment": 50
}'
```

#### Response
```
"OK"
```

### Item Contributions

#### Request
```
curl -X 'POST' \
'https://brackish.onrender.com/items/16/contributions/user/jackalnom' \
-H 'accept: application/json' \
-H 'access_token: f616b86c09e0ee3f524a5bf4c9c6109d' \
-H 'Content-Type: application/json' \
-d '{
"name": "RED_POTION_100",
"type": "Potion",
"quantity": 70,
"payment": 50
}'
```

#### Response
```
"OK"
```

### Remove Item Contribution

#### Request
```
curl -X 'DELETE' \
'https://brackish.onrender.com/items/16/contributions/jackalnom/RED_POTION_100' \
-H 'accept: application/json' \
-H 'access_token: f616b86c09e0ee3f524a5bf4c9c6109d'
```

#### Response
```
"OK"
```

### Remove Item Request

#### Request
```
curl -X 'DELETE' \
'https://brackish.onrender.com/items/16/requests/RED_POTION_100' \
-H 'accept: application/json' \
-H 'access_token: f616b86c09e0ee3f524a5bf4c9c6109d'
```

#### Response
```
"OK"
```

### Get Event Contributions

#### Request
```
curl -X 'GET' \
'https://brackish.onrender.com/items/16/contributions/' \
-H 'accept: application/json' \
-H 'access_token: f616b86c09e0ee3f524a5bf4c9c6109d'
```

#### Response
```
"OK"
```


# Joseph 'Mang0' Marquez wants to study up on matchups

Joseph 'Mang0' Marquez is a pro Super Smash Bros. Melee player that wants to get better. However, Mang0 has forgotten what brackets he has been a part of and the matches that he played in those brackets. He uses our API to find this information.

- First, Mang0 goes to his user profile which shows all the previous events he has attended (not shown in API but will be added at some point). This is done with a call to @get /events?active=past&type=gaming.

- Mang0 recognizes one of the events (with event_id = 23423) and clicks on it to see the bracket which is done with @get /brackets/23423 

- He finds the Super Smash Bros. Melee bracket and clicks it to see the matches that took place. This is done through the call @get /brackets/23423/matches.

- He now can see that he won some matches against lesser known players but lost to his rival, Zain, in a 3-0 blowout. 

Now Mang0 knows he needs to practice playing against Zain's character, Marth. He will lock in and train for the next tournament. 


## Testing results

### 

###

###

###