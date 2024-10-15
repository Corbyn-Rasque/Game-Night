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

## 2. Events [NOAH]

### 2.1. Get Events `/events/:{start}?/:{end}?/:{genre}?` (GET)
Retrieves any event(s) in the specified range or genre. 

**Response**
```json
[
  {
    "event_type":"string",
    "duration":"int",
    "time":"DateTime",
    "location":"string",
    "description":"string",
    "max_participants":"int",
    "min_participants":"int",
  }
]
```

### 2.2. Set Events `/events` (POST)
Posts a new event to the database 

**Request**
```json
[
  {
    "event_type":"string",
    "duration":"int",
    "time":"DateTime",
    "location":"string",
    "description":"string",
    "max_participants":"int",
    "min_participants":"int",
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