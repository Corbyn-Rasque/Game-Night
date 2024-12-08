# Peer Review Responses

## Kai Swaggler

### [Code Review](https://github.com/Corbyn-Rasque/Game-Night/issues/2)

1. **Additional information returned for errors**

    This is something we've definitely started implementing a bit more later on as we went, and much of our new code has more detailed responses. We generally try to return object dictionaries, and have implemented [reponses codes](#response-codes) to indicate success or not, with some more detailed print statements when required. Things look a lot nicer now, and are easier to debug.

<a id = "response-codes" />

2. **Lack of [HTTP Response Codes](https://fastapi.tiangolo.com/tutorial/handling-errors/)**

   This is a great suggestion, and one that we didn't even realize was a thing until only recently when a few of us learned about RESTful design practices and response codes. Fortunately, this has now been implemented across all of our code.

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


<a id = "uniqueness-constraint-necessity" />

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

1. **Errors with COALESCE usage.**

    This has been corrected, per suggestion.
    https://github.com/Corbyn-Rasque/Game-Night/blob/09ebda9c85062ac86c5a20b3acd30b26baee4bf0/src/api/brackets.py#L39-L43

2. **Return issues should carry more helpful errors.**

    This has been corrected & response codes have bee implemented.
    https://github.com/Corbyn-Rasque/Game-Night/blob/09ebda9c85062ac86c5a20b3acd30b26baee4bf0/src/api/brackets.py#L53-L64

3. **`user_id` type mislabeled as `str` instead of `int`.**

    This has been corrected.
    https://github.com/Corbyn-Rasque/Game-Night/blob/09ebda9c85062ac86c5a20b3acd30b26baee4bf0/src/api/brackets.py#L136

4. **Missing cancelled field in Event base model.**

    This does not need to be on the Event base model for event creating & updating. The only time the cancelled field is required is for when the event is being cancelled, where you only need an event_id. It would otherwise be redundant, as it would never be true as the event is created.

5. **Events search edge case for dates missing**

    It's easy to miss, but the existence of start & end times are being XOR'd for comparison and AND'd for comparison. All cases are covered.

    https://github.com/Corbyn-Rasque/Game-Night/blob/09ebda9c85062ac86c5a20b3acd30b26baee4bf0/src/api/events.py#L119-L122


6. **HTTP Responses code implementation for Events.**

    See [earlier response](#response-codes).

7. **Suggestion to trim some redundant SQL off of two different queries for different purposes.**

    This is a great suggestion and something that I considered, but the existence of the WHERE clause makes it sos these two queries cannot be concatenated or cleaned up in a nice way. - Corbyn

8. **Concern about concatenating queries opening up risk of SQL Injection**

    While the code refered to here wouldn't allow for SQL Injection due to the way SQLAlchemy does parameter binding, the code has none-the-less be refactored to condense the query parts into a single query now.
    https://github.com/Corbyn-Rasque/Game-Night/blob/839e0df2d27cc44256a82290a2bad631a38a7cd0/src/api/games.py#L53-L67

9. **Returning a set of games, given multiple query matches, versus just a single game.**

    Implemented as requested, using ILIKE comparison operator and returning all matches instead of one.
    https://github.com/Corbyn-Rasque/Game-Night/blob/839e0df2d27cc44256a82290a2bad631a38a7cd0/src/api/games.py#L53-L67

10. **Add helper functions for removing one user contribution, or all user contributions**

    This is a good idea, however we found it simpler to handle by considering how users are removed from events.
    Only the single item removal endpoint remains.

11. **Add response codes to team deletion**

    Teams has been removed as an endpoint, due to an alternate implementation scheme.
    On response codes: see [earlier response](#response-codes).

12. **Potential issues with order of parameters passed in \[ ? \] to the `get_user()` function.**

    The `get_users()` function has been overhauled, and should address your concerns. As for the order of parameters passed, that would be a front end issue.
    https://github.com/Corbyn-Rasque/Game-Night/blob/839e0df2d27cc44256a82290a2bad631a38a7cd0/src/api/users.py#L41-L55

13. **Suggestion to return all relevant matching User Events, intead of closest match.**

    Implemented below, per suggestion.
    https://github.com/Corbyn-Rasque/Game-Night/blob/839e0df2d27cc44256a82290a2bad631a38a7cd0/src/api/users.py#L58-L71

### [Schema/API Design Comments](https://github.com/Corbyn-Rasque/Game-Night/issues/4)

1. **Custom responses for edge cases for things like the POST User endpoint.**

    See [earlier response](#response-codes).

2. **Input validation concerns for Event Status**

    On Event Type, see [earlier response](#value-constraints).

    For the `status` field you refer to, this has been done away with in favor of a different solution that was cleaner and a bit more implicit.

3. **For Teams, it should be specified how players are distributed.**

    The Teams endpoint has been deprecated in favor of a solution integrated with Brackets. This endpoint handles the scenario you talk about much closer to real life event brackets with byes/etc.

4. **Match state for tracking match progress**

    Sorry for the repetative answers, but we've implemented a solution within Brackets that tracks state implicitly through whether or not there's a winner for a specific bracket matchup.

5. **Response code recommendation for Item removal.**

    See [earlier response](#response-codes).

6. **Snake Case versus Camel Case consistency concerns across code.**

    See [earlier response](#code-formatting).

7. **Unnecessary uniqueness constraint on primary key id in Users**

    See [earlier response](#uniqueness-constraint-necessity).

8. **Concerns about accidentally deleting a row that is referenced somewhere else, and suggestion of using `ON DELETE RESTRICT`**

    `ON DELETE RESTRICT` is not necessary, since all columns have foreign key constraints. While we generally have `CASCADE` implemented in a functional way that works with our tables, even if this was not the case, the delete would simply fail due to the the constraint. The `RESTRICT` keyword is largely superfluous here.

9. **Error handling for cases where match_id doesn't exist yet.**

    In this case, the trigger function highlighted *only* runs when a match row has been inserted, guaranteeing that a corresponding match_id exists.

10. **Consider implementing indexes for queries that are often run, such as User queries.**

    This is honestly a great suggest, and something that we'll likely be implementing in Version 5.

11. **Suggestion to add restrictions for Game table entries.**

    See [earlier reponse](#value-constraints)

12. **Suggestion to use timestamp instead of date for the time column on the Brackets table.**

    Implemented as suggested.

### [Product Ideas](https://github.com/Corbyn-Rasque/Game-Night/issues/6)

1. Create a player performance analytics endpoint.

    I love love love this idea, but it would simply be too complex an endpoint to implement on top of creating the brackets system we are targeting to implement. While we can implement it this project, this would be a great idea to try for in the future! - Corbyn

2. Create an event sponsorshop endpoint.

    This would honestly be a fantastic idea, and wouldn't take too much tweaking to implement. In theory it can be done with our current code, since mulitplpe organizers can 'own' and event. A company could create an account and become an event host, and with a little front end code to display them properly it could be really snazzy!

## Samiksha Karimbil

### [Code Review](https://github.com/Corbyn-Rasque/Game-Night/issues/7)
### [Schema/API Design Comments](https://github.com/Corbyn-Rasque/Game-Night/issues/8)
### [Product Ideas](https://github.com/Corbyn-Rasque/Game-Night/issues/9)

## Ivana Thomas

### [Code Review](https://github.com/Corbyn-Rasque/Game-Night/issues/13)
### [Schema/API Design Comments](https://github.com/Corbyn-Rasque/Game-Night/issues/14)
### [Product Ideas](https://github.com/Corbyn-Rasque/Game-Night/issues/12)