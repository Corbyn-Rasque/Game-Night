# Peer Review Responses

## Kai Swaggler

### [Code Review](https://github.com/Corbyn-Rasque/Game-Night/issues/2)

1. **Additional information returned for errors**

    This is something we've definitely started implementing a bit more later on as we went, and much of our new code has more detailed responses. We generally try to return object dictionaries, and have implemented [reponses codes](#response-codes) to indicate success or not, with some more detailed print statements when required. Things look a lot nicer now, and are easier to debug.

<a id = "response-codes" />

2. **Lack of [HTTP Response Codes](https://fastapi.tiangolo.com/tutorial/handling-errors/)**

   This is a great suggestion, and one that we didn't even realize was a thing until only recently when a few of us learned about RESTful design practices and response codes. Fortunately, this has now been implemented across much of our code, and is something we'll be continually working to add.

<a id = "return-statements" />

3. **Single return statement instead of multiple redundant statements**

    This is something we actually agreed on partway through the project, and the code you're seeig without unified return statements are actually parts of the code that were soon deprecated as we wrote new functionality for brackets & such in new places in the code.

4. **Using `generate_series` in [Postgres](https://www.postgresql.org/docs/current/functions-srf.html), instead of looping insert statements**

    Way ahead of you on this one! Not long after this code was submitted, we simple added a plpgsql trigger function on Supabase to generate the rows we needed on an insert into Brackets. No more looping inserts!

<a id = "code-formatting" />

5. **Code could be formatted using [Ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff) & [Black](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter)**

    Agreed—though with the brevity of this project, I think this is best left for a future endeavor, where this could be implemented from the beginning. Trying to implement this in the middle of the project, with all of the current branches currently being worked on, would create a number of merge conflicts that would need to be resolved.

6. **Remove commented code**

    Apologies for the amount of commented out code. It's a bad practice that I've had while writing code, creating 'code graveyards' of sort in case functionality needs to be reverted. This is something I've intentionally stopped doing as I move forwards. - Corbyn

7. **Formatting inconsistencies**

    This should ideally be addressed when implementing code formatting as you [mentioned above](#code-formatting).

### [Schema/API Design Comments](https://github.com/Corbyn-Rasque/Game-Night/issues/16)

#### Users

1. **GET `/users/` -> /users**

    Implemented below.
    https://github.com/Corbyn-Rasque/Game-Night/blob/e865807d653eb66c542b734aeae0592df26c9780/src/api/users.py#L11-L15

2. **GET `/users/{username}/` & GET `/users/{user_id}/` conflict.**

    Implemented below.
    https://github.com/Corbyn-Rasque/Game-Night/blob/e865807d653eb66c542b734aeae0592df26c9780/src/api/users.py#L34-L54

3. **Singular get_user() function that returns user based on `username` or `id`.**

    Implemented below.
    https://github.com/Corbyn-Rasque/Game-Night/blob/e865807d653eb66c542b734aeae0592df26c9780/src/api/users.py#L34-L54
    

4. **Duplicate uniqueness constraint in `Users` table.**

    While [this is duplicative](https://github.com/Corbyn-Rasque/Game-Night/blob/e865807d653eb66c542b734aeae0592df26c9780/schema.sql#22-#31), it both: doesn't affect functionality as it stands and would be hard to fix without first truncating or dropping tables to avoid foreign key constraints from other tables. Down the line this could be fixed, but we havea considerable amount of useful test data currently that we would like to keep using.

#### Events

1. **Event ownership confusion with `/users/{username}/events` endpoint address.**

    Implemented below.
    https://github.com/Corbyn-Rasque/Game-Night/blob/e865807d653eb66c542b734aeae0592df26c9780/src/api/events.py#L26-L41

<a id = "value-constraints" />

2. **Parameter constraints on the `Events` table or new [type](https://www.thegnar.com/blog/enum-types-in-postgres) to avoid invalid type.**

    We did not want to limit or have to enumerate every possible event type, given this service was intended to reach a very wide audience—gamer or otherwise. Some amount of checking could be later implemented through another function, but for now we'd rather leave options open.

#### Brackets

1. **Extra `/` on `/brackets/{bracket_id}/matches/{match_id}/players/`**

    Implemented below.
    https://github.com/Corbyn-Rasque/Game-Night/blob/b71e092e8da4612b510c8fb0fc69af8f6da91f40/src/api/brackets.py#L84

#### Games

1. **`/games` instead of `/games/`**

    Implemented below.
    https://github.com/Corbyn-Rasque/Game-Night/blob/b71e092e8da4612b510c8fb0fc69af8f6da91f40/src/api/games.py#L8-L12

2. **Parameter constraints on the `Games` table or new [type](https://www.thegnar.com/blog/enum-types-in-postgres) to avoid invalid type, and Game uniqueness**

    While we're very much of the same mind as with our [response](#value-constraints) to Event types, we've toyed around implementing some platform and restrictions. We haven't found a good solution to uniqueness constraints, though, given that the same game can be release multi-platform.

    https://github.com/Corbyn-Rasque/Game-Night/blob/b71e092e8da4612b510c8fb0fc69af8f6da91f40/src/api/games.py#L21-L50


3. **`player_count` utility as a column in the `Games` table.**

    While not implemented yet, we feel this could be useful in automatic bracket sizing down the line. It's also useful metadata for event planning & organizing, so we're leaving it for now.

4. **Openness of user game creation.**

    It's important to point out that this is only a back end implementation of an event organization service. With a front end and user authentication, game creation could be limited to Admins. Even if this was not the case, some amount of freedom for mischief (within reason) serves to lend towards making the platform feel fun & alive.

#### Items

1. **`/items/{event_id}/contributions` instead of `/items/{event_id}/contributions/`**

    Implemented below.
    https://github.com/Corbyn-Rasque/Game-Night/blob/b71e092e8da4612b510c8fb0fc69af8f6da91f40/src/api/items.py#L55


### [Product Ideas](https://github.com/Corbyn-Rasque/Game-Night/issues/17)

1. Making an endpoint to see all events by game may be interesting

    Implemented below.
    https://github.com/Corbyn-Rasque/Game-Night/blob/a1ea6d3882d9020ef0c1eb1de78d5b5700c90b54/src/api/events.py#L57-L91

2. Make an endpoint to delete a User.

    Implemented below.
    https://github.com/Corbyn-Rasque/Game-Night/blob/029c6e3c4b5dfa7f81c44d653f7067b98d6b50bf/src/api/users.py#L70-L82

3. Implement leaderboard system that shows how many brackets a user has won.

    This is a fantastic idea! We were so close to being able to implement something like this, but with limited time at the end and some very large, sweeping changes to the brackets system under the hood, we unfortunately weren't able to implement this. But everything is there to do it.

## Antony Tartakovskiy

### [Code Review](https://github.com/Corbyn-Rasque/Game-Night/issues/3)

1. 
2. 
3. 
4. 
5. 
6. 
7. 
8. 
9. 
10. 
11. 
12. 
13. 

### [Schema/API Design Comments](https://github.com/Corbyn-Rasque/Game-Night/issues/4)
### [Product Ideas](https://github.com/Corbyn-Rasque/Game-Night/issues/6)

## Samiksha Karimbil

### [Code Review](https://github.com/Corbyn-Rasque/Game-Night/issues/7)
### [Schema/API Design Comments](https://github.com/Corbyn-Rasque/Game-Night/issues/8)
### [Product Ideas](https://github.com/Corbyn-Rasque/Game-Night/issues/9)

## Ivana Thomas

### [Code Review](https://github.com/Corbyn-Rasque/Game-Night/issues/13)
### [Schema/API Design Comments](https://github.com/Corbyn-Rasque/Game-Night/issues/14)
### [Product Ideas](https://github.com/Corbyn-Rasque/Game-Night/issues/12)