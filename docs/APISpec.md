# API Specification for Game Night

## 1. Users

### 1.1. Get User `/users/?username={username}&id={id}` (GET)

Fetches user information based on a provided `username` or `id`. If neither is provided, returns an empty object.

**Response**:

```json
{
  "id": "integer",
  "username": "string",
}
```

### 1.3. Create User – `/users` (POST)
Creates a new user that must have a unique username and will be given a unique id. The user's first and last name are needed.

**Request**:

```json
{
  "username": "string",
  "first": "string",
  "last": "string",
}
```

**Response**:
```json
{
  "success":"boolean"
}
```

## 2. Events

### 2.1. Get Event `/events{?active,type}` (GET)
Retrieves any and all event(s) with the corresponding active status and/or type. If neither variable is undefined, it will return all events. 

**Response**
```json
[
  {
    "id":"int",
    "active":"string",  /*Past, Current, or Upcoming*/
    "type":"string", /*Movie, Video Game, Tabletop Game, etc.*/
    "name":"string",
  }
]
```

### 2.2. Create Event `/events` (POST)
Creates a new event in the database.

**Request**
```json

{
  "name":"string",
  "date_time":"timestamp",
  "type":"string", /*Movie, Video Game, Tabletop Game, etc.*/
  "max_attendees":"int",
  "location":"string",
}

```
**Response**
```json

{
  "event_id" : "int"
}
```

## 3. Brackets

### 3.1 Get Bracket `/brackets/{event_id}` (GET)
Presents the bracket from a specific event.

**Response**:
```json
{
  "bracket_id":"int",
  "name":"string",
  "active":"string",  /*Past, Current, or Upcoming*/
  "game":"string",
  "capacity":"integer", /*Max number of users that can join the bracket*/
}
```

### 3.2 Create Brackets `/brackets` (POST)
Creates a new bracket and gives it a unique id.

**Request**:
```json
{
  "name":"string",
  "date_time":"timestamp",
  "game":"string", 
  "capacity":"integer",
  "cost":"float",
}
```

**Response**:
```json
{
  "success":"boolean",
}
```

### 3.3 Get All Matches in Bracket `/brackets/{bracket_id}/matches` (GET)
Retrieves all the matches in a bracket. Will give the match IDs along with info about that  match.

**Response**:
```json
[
  {
    "match_id":"integer",
    "teams":[    /*Can have many teams playing a match*/
      {
        "team_id":"integer",
        "players":[   /*Can have multiple players in a team*/
          {
            "user_id":"integer",
            "username":"string"
          },
          {...} 
        ]
      },
      {...}
    ]
  }
]
```

### 3.4 Get Match by id `/brackets/{bracket_id}/matches/{match_id}` (GET)
Retrieves a specific match in a specific bracket with all the information about that match.

**Response**:
```json
{
  "teams":[    /*Can have many teams playing a match*/
    {
      "team_id":"integer",
      "players":[   /*Can have multiple players in a team*/
        {
          "user_id":"integer",
          "username":"string"
        },
        {...} 
      ]
    },
    {...}
  ]
}
```

### 3.5 Start Bracket `/brackets/{bracket_id}/start` (POST) *COMPLEX ENDPOINT
Begins a bracket by creating all the matches needed appropriate to the number of players that actually entered the bracket. Works with non power of 2 numbers, for example you can start a bracket of 5 players and this endpoint will create an 8 player bracket (the next power of 2) where the remaining 3 players are byes for the top 3 seeded players. Seeding is also determined in this endpoint based on previous matches played. The endpoint automatically gives the players the bye and established matches for the first round of the bracket.

**Request**
```json
{
  "beginner_limit": "integer"   /*Will default to 1 for invalid values. Used for seeding formula*/
}
```

**Response**
```json
[
  {
    "bracket_id":"integer",
    "match_id": "integer",
    "player_id": "integer",
    "seed": "integer"
  },
  ... /*one for each player*/
]
```

### 3.6 Finish Round `/brackets/{bracket_id}/round` (POST) *COMPLEX ENPOINT
Advances the round of the given bracket. Will only advance if all matches in the current round of that bracket are complete. Does not work on brackets that have not been started.

**Response**
```json
"OK"
```

### 3.7 Declare Winner `/brackets/{bracket_id}/winner` (POST) *COMPLEX ENDPOINT
Inputs a winner into the correct match. It determines what the appropriate match is given the player and bracket. Will only work if the bracket is valid (exists and is started) and the player is still actually in the bracket (has not lost).

**Request**
```json
{
  "won_by_id": "integer"
}
```

**Response**
```json
"OK"
```

## 4. Games

### 4.1 Get Games `/games{?name,platform}` (GET)
Finds all games that have the specified criteria. If no criteria is given all games will be shown.

**Response**:
```json
{
  "id":"integer",
  "name":"string",
}
```

### 4.2 Create Game Entry `/games` (POST)
Creates a new game and gives it a unique id.

**Request**:
```json
{
  "name":"string",
  "platform":"string",
  "publisher":"string", 
  "release_year":"integer",
  "player_count":"integer",
}
```

**Response**:
```json
{
  "success":"boolean",
}
```

## 5. Objects

### 5.1. Get All Objects For Event `/items/{event_id}` (GET)
Returns a list of items associated with a specific event ID

**Response**
```json
[
  {
  "id":"int",
  "name":"string",
  "type":"string", /*Food, Supplies, Party Favors, etc.*/
  "quantity":"int",
  "requested":"int",
  "cost":"int",
  }
]
```

### 5.2. Get Object By ID `/items/{item_id}` (GET)
Retrieves the details of a specific item for actions like editing to happen.

**Response**
```json
{
  "id":"int",
  "name":"string",
  "type":"string", /*Food, Supplies, Party Favors, etc.*/
  "quantity":"int",
  "requested":"int",
  "cost":"int",
}
```

### 5.3. Add Object `/items` (POST)
Adds an item in the database that can then be associated with an event by the item ID.

**Request**:
```json
{
  "name":"string",
  "type":"string", /*Food, Supplies, Party Favors, etc.*/
  "quantity":"int",
  "requested":"int",
  "cost":"int",
}
```

**Response**
States 201

### 5.4. Remove Object `/items/{item}` (DELETE)
Removes an item from the database if user wants to remove it from an event.

**Response**
Status 204