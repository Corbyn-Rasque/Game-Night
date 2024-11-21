# API Specification for Game Night

## 1. Users

### 1.1. Get User `/users/?username={username}&id={id}` (GET)

Fetches user information based on a provided `username` or `id`. If neither is provided, returns an empty object.

**Response**:

```json
{
  "id":"integer",
  "username":"string",
}
```

### 1.3. Create User – `/users` (POST)
Creates a new user that must have a unique username and will be given a unique id. The user's first and last name are needed.

**Request**:

```json
{
  "username":"string",
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