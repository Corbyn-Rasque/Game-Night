# API Specification for Game Night

## 1. Users

### 1.1. Get User By username – `/users/{username}/` (GET)

Retrieves the user at the specified username. Usernames will be unique to individuals, and only a single user with be returned. 

**Response**:

```json
{
  "id":"integer",
  "username":"string",
}
```


### 1.2. Get User By id – `/users/{id}/` (GET)

Retrieves the user with the specified id.

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
[
  {
    "success":"boolean"
  }
]
```

## 3. Brackets

### 3.1 Get Bracket `/brackets/{id}`
Presets the bracket with the specified id.

**Response**:
```json
{
  "id":"int",
  "name":"string",
  "active":"string",  /*Past, Current, or Upcoming*/
  "game":"string",
  "capacity":"integer", /*Max number of users that can join the bracket*/
}
```

### 3.2 Set Brackets `/brackets`
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


## 4. Games [ALAN]

### 4.1 Get Games `/games`

### 4.2 Set Games `/games`

## 5. Objects [CORBYN]

### 5.1 Get Objects `/objects`

### 5.2 Set Objects `/objects`