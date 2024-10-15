# API Specification for Game Night

## 1. Users [EVERYONE]

### 1.1. Get User – `/user/:{username}?/`

Retrieves the user at the specified username. Usernames will be unique to individuals, and only a single user with be returned.

**Response**:

```json
[
    {
      "first": "string",
      "last": "string",
    }
]
```

### 1.2. Create User – `/user`

**Response**:

```json
[
    {
      "username": 
    }
]
```

## 2. Events

### 2.1. Get Events `/events{?active,type}` (GET)
Retrieves any and all event(s) with the corresponding active status and/or type. If neither variable is undefined, it will return all events. 

**Response**
```json
[
  {
    "id":"int",
    "name":"string",
    "description":"string",
  }
]
```

### 2.2. Set Events `/events` (POST)
Creates a new event in the database.

**Request**
```json
[
  {
    "name":"string",
    "description":"string",
    "active":"string",  /*Past, Current, or Upcoming*/
    "type":"string", /*Movie, Video Game, Tabletop Game, etc.*/
    "max_attendees":"int"
  }
]
```
**Response**
```json
[
  {
    "success":"boolean"
  }
]
```

## 3. Brackets [OZCAR]

### 3.1 Get Brackets `/brackets`

### 3.2 Set Brackets `/brackets`

## 4. Games [ALAN]

### 4.1 Get Games `/games`

### 4.2 Set Games `/games`

## 5. Objects [CORBYN]

### 5.1 Get Objects `/objects`

### 5.2 Set Objects `/objects`