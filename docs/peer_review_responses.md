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

<a id = "commented-code" />

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

<a id = "leaderboard" />

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

<a id = "event-search-dates" />

5. **Events search edge case for dates missing**

    It's easy to miss, but the existence of start & end times are being XOR'd for comparison and AND'd for comparison. All cases are covered.

    https://github.com/Corbyn-Rasque/Game-Night/blob/09ebda9c85062ac86c5a20b3acd30b26baee4bf0/src/api/events.py#L119-L122


6. **HTTP Responses code implementation for Events.**

    See [earlier response](#response-codes).

7. **Suggestion to trim some redundant SQL off of two different queries for different purposes.**

    This is a great suggestion and something that I considered, but the existence of the WHERE clause makes it sos these two queries cannot be concatenated or cleaned up in a nice way. - Corbyn

<a id = "sql-injection" />

8. **Concern about concatenating queries opening up risk of SQL Injection**

    While the code refered to here wouldn't allow for SQL Injection due to the way SQLAlchemy does parameter binding, the code has none-the-less be refactored to condense the query parts into a single query now.
    https://github.com/Corbyn-Rasque/Game-Night/blob/839e0df2d27cc44256a82290a2bad631a38a7cd0/src/api/games.py#L53-L67

<a id = "game-search" />

9. **Returning a set of games, given multiple query matches, versus just a single game.**

    Implemented as requested, using ILIKE comparison operator and returning all matches instead of one.
    https://github.com/Corbyn-Rasque/Game-Night/blob/839e0df2d27cc44256a82290a2bad631a38a7cd0/src/api/games.py#L53-L67

<a id = "contribution-removal-duplication" />

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

<a id = "match-state" />

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

<a id = "player-performance-tracking" />

1. Create a player performance analytics endpoint.

    I love love love this idea, but it would simply be too complex an endpoint to implement on top of creating the brackets system we are targeting to implement. While we can implement it this project, this would be a great idea to try for in the future! - Corbyn

2. Create an event sponsorshop endpoint.

    This would honestly be a fantastic idea, and wouldn't take too much tweaking to implement. In theory it can be done with our current code, since mulitplpe organizers can 'own' and event. A company could create an account and become an event host, and with a little front end code to display them properly it could be really snazzy!

## Samiksha Karimbil

### [Code Review](https://github.com/Corbyn-Rasque/Game-Night/issues/7)

1. **Consider wrapping gets in a try/except block to avoid issues with the database.**

    See [earlier response](#response-codes).

2. **Some of the endpoints return “OK”, such as the cancel event, request/contribute item or remove items endpoints. Consider standardizing the responses with JSON objects for consistency.**

    See [earlier response](#response-codes).

3. **Consider using HTTP status codes for error handling along with descriptive messages.**

    See [earlier response](#response-codes).

<a id = "id-return" />

4. **In general, consider whether you want to reference a user through name or id. There are inconsistencies with that in some of the endpoints (add vs remove user, etc).**

    This advice is honestly really solid, and soemthing I've run into when doing another project that involved both front end and back end interacting with eachother. With this project, however, we don't really have a front end displaying data, so it's hard to tell whether using ID or Username would be more useful for getting data. If we evolve towards getting a front end set up, I think this would be very much worth revisiting. - Corbyn

5. **Lots of places with commented out code, generally makes code less visually appealing**

    See [earlier response](#commented-code)

6. **Consider print statements for logging purposes.**

    While this idea is great, we have switched tack a bit and have largely switched to use proper response codes to communicate success or failure.

7. **In get_event, not all cases for start and end time were considered, like if one of the times is not provided or if they are the same.**

    See [earlier response](#event-search-dates)

8. **SQL injections are a possibility with name, type, username or platform.**

    See [earlier response](#sql-injection)

9. **There are 2 endpoints with the same function name (remove_user_contributions in items.py). Consider combining these endpoints where the request may contain the specific item, and remove all contributions if it doesn’t.**

    See [earlier response](#contribution-removal-duplication)

10. **Consider documentation, each endpoint could have at least 1 line describing its purpose. This could be done with a docstring at the start of the function.**

    This is one area where we could have done a bit better. Without getting into it too much, most of our group has a professor that docs points for leaving any code comments, so this behavior has unfortunately spilled over onto this project. I will go through and try to update the docstrings for each endpoint though, as they are extremely useful for understanding what's going on in a veritale sea of endpoints.

<a id = "valid-value-constraints" />

11. **Fields like username, event id, item name could all be validated to ensure correct data types and avoid invalid entries.**

    Value constraints have been added across all tables to prevent default values and invalid numeric values.

12. **Instead of permanently deleting things like teams or items, consider adding in a deleted column to sort of ledgerize data and view history.**

    This suggestion is great, and is one we have implemented across Items, Events, and Users!

### [Schema/API Design Comments](https://github.com/Corbyn-Rasque/Game-Night/issues/8)

1. **If username must be unique, consider making that be the primary key of the user table.**

    See [earlier response](#uniqueness-constraint-necessity).

2. **The get_user_by_username and get_user_by_id endpoints seem redundant.**

    While on the outset these seem redundant, these are useful to use as helper functions for other functions. See below.
    https://github.com/Corbyn-Rasque/Game-Night/blob/839e0df2d27cc44256a82290a2bad631a38a7cd0/src/api/users.py#L74-L84

3. **If the ‘id’ column of games must be unique, consider having that alone be the primary key of the games table.**

    This is something we're definitely still debating over, but since we are still using the `name` and `platform` fields as a composite key to find games, we are simply keeping those as the primary composite key. The id column is simply there to make foreign keys a little less gross in other tables. But yes, this is somewhat duplicative.

4. **Ensure quantity of items is a valid non-negative value.**

    See [earlier response](#valid-value-constraints).

5. **Ensure the release_year column has valid year values that are non-negative and before current year.**

    See [earlier response](#valid-value-constraints).

6. **It doesn’t seem like users first and last name are being used, consider having a full name column for simplicity.**

    This is something that will ultimately depend on how a front end is written, but having first and last name separate is nice for having 'friendly' names to refer to users across the platform, without string tokenization required every time.

7. **Ensure that there are no duplicate brackets by having the event id and game id pair be unique.**

    This is already implemented as it stands.

8. **Some inconsistencies with naming conventions, stick to one type (lower case / camel case / snake case).**

    See [earlier response](#code-formatting).

9. **For the games table, platform, publisher, release_year and player_count don’t seem to be necessary information to store. Maybe it is nice for informational purposes, but in general seems to add no value to the API.**

    Respectfully, we disagree here. These are all important pieces of information needed for putting together a party, where people need to know what controllers or consoles to brings, or if they can even compete in the event. The value is more in displaying to the user, which would necessitate a front end to implement that. For now, the information lies dormant until something like that coalesces.

10. **Ensure start time of events is always before stop time.**

    This has been added as a constraint to the Events table.

11. **I don’t currently see any reference to teams anywhere in the API design outside teams.py.**

    This is largely a result of Teams heading towards deprecation at the time of this review, with dependencies being removed. Teams has now been fully deprecated. Sharp eye, though!

12. **Consider having event/bracket statuses, where it can say if the event or bracket match is in progress, completed or canceled.**

    See [earlier response](#match-state).

13. **Consider a table to standardize the possible event types.**

    See [earlier response](#value-constraints).

### [Product Ideas](https://github.com/Corbyn-Rasque/Game-Night/issues/9)

1. **Ranking system based on tournament outcome suggestion.**

    See [earlier response](#player-performance-tracking)

2. **Guest List implementation**

    This could be a really fun addition and would really enhance the app's overall appeal as an event organize above all else. At this point, getting Brackets set up has taken up a substantial chunk of time and we likely won't be able to implement this in time, but it's a great idea and wouldn't take too much effort to implement!

## Ivana Thomas

### [Code Review](https://github.com/Corbyn-Rasque/Game-Night/issues/13)

1. **When canceling an event, the event still shows up in `@GET/events/{event_id}` and looks the same as an active event. If a boolean is going to be used to handle cancellation, it would be good to return that to the user as well.**

    I honestly am not sure how that slipped through; thanks for pointing that out! A filter for cancelled events has been added to the Events search endpoint (see bellow)!
    https://github.com/Corbyn-Rasque/Game-Night/blob/e40e67747038c95e6ff85e7ff3baf0010bf6721b/src/api/events.py#L95-L115

2. **There could be more error handling: try/except or adding print statements to your render log.**

    See [earlier response](#response-codes).

3. **In items/contributions, for a reset from the user/event maybe remove the row instead of using a boolean? Or, could insert a negative quantity to simplify any aggregation that might be needed at some point?**

    For Item Contributions, we tried to pattern the table around a ledgerized system, where (similar to what you mention) we could aggregate the values to get a current answer at any given time. Given that, it's useful to keep around 'removed' contributions to retain a history of sorts, in case the user what's the undo the delete easily or see previous promises.

4. **For /events upon event creation, a more detailed response (so we know that the response is the event id).**

    See [earlier response](#response-codes).

5. **In `@POST/brackets`, the API Spec doesn’t match the request body in the deployed url. `event_id` is clear, but `game_id` is a little bit confusing.**

    This has been updated to be more clear. See below.
    https://github.com/Corbyn-Rasque/Game-Night/blob/e40e67747038c95e6ff85e7ff3baf0010bf6721b/src/api/brackets.py#L112-L132

6. **Despite use of `ON CONFLICT`, I was able to insert the exact same Fortnite entry into `games`, with the same platform, publisher, release year, and player count 4 times and got 4 separate ids.**

    This has been fixed in the latest update. See below.
    https://github.com/Corbyn-Rasque/Game-Night/blob/e40e67747038c95e6ff85e7ff3baf0010bf6721b/src/api/games.py#L22-L50

7. **Searching by Username only in `/events` results in a `500 internal server error`.**

    This has been fixed in the latest update. See below.
    https://github.com/Corbyn-Rasque/Game-Night/blob/e40e67747038c95e6ff85e7ff3baf0010bf6721b/src/api/games.py#L53-L67

8. **Creating a bracket for an event_id that doesn’t exist in `@POST/brackets` results in a `500 internal error`.**

    This has been fixed in the latest update. See below.
    https://github.com/Corbyn-Rasque/Game-Night/blob/e40e67747038c95e6ff85e7ff3baf0010bf6721b/src/api/brackets.py#L112-L132

9. **`@GET/users/{user_id}` is returning `{}`. Per API spec, it appears it should return username and id.**

    This has been fixed in the latest update. See below.
    https://github.com/Corbyn-Rasque/Game-Night/blob/e40e67747038c95e6ff85e7ff3baf0010bf6721b/src/api/users.py#L41-L55

10. **Super minor: datetime is imported into games, but not used**

    Superfluous datetime import has been removed! See below.
    https://github.com/Corbyn-Rasque/Game-Night/blob/e40e67747038c95e6ff85e7ff3baf0010bf6721b/src/api/games.py#L1-L7


### [Schema/API Design Comments](https://github.com/Corbyn-Rasque/Game-Night/issues/14)

1. **For teams, what if multiple teams have the same name? Is this something that is allowed, or should some checking be implemented?**

    While this might change in the future, for now we are allowing teams with the same name. Many time, team names are not super unique, so it would result in a lot of name collissions if we did.

2. **Additionally, there could be more integration of teams into the events/brackets. How many teams is an event allowed to have? In a bracket, must the players be on opposing teams?**

    This is something we've really wanted to do, but ultimately likely won't have time to implement. Bracket has been subversive in it's complexity, so automatic team seeding may have to wait for another day. It may also be a bit of a NP incomplete problem, but I'm not sure of that.

3. **In get_team_players, we are only returning a dictionary with the players ids, per the class Team_Player. It might be more helpful to also include and then return their name for human readability.**

    See [earlier response](#id-return).

4. **More could be done with payment on contribute_item– perhaps users could have a certain amount of money to spend?**

    This is a good idea, but forays too much into money management and away from the core aspects of the event planning idea for Game Night.

5. **For @POST/brackets, maybe there could be different endpoints for games vs events?**

    As it standard currently, you can implicitly differentiate between games & events by whether or not a bracket has been associated with the event.

<a id = "user-event-attendance" />

6. **In @POST/brackets/{bracket_id}/matches/ … match_id is unclear in the scope of hosting an event such as a party.**

    Agreed; originally the only way someone could attend an event was through a match. Now someone can directly attend an event, without needing to join a bracket.

7. **It also appears that there may not be a way to create a match.**

    This has been resolved through an overhaul of the Brackets & Match system in the time since.

8. **Implement a way for users to be associated with events, even if there is no matches or brackets for the event yet, especially in situations which may not require brackets/matches at all.**

    See [earlier response](#user-event-attendance).

9. **It might be useful to provide functionality to get all the games at once in @GET/games/{name} so a user could browse what games are already in the system instead of having to search for games.**

    See [earlier response](#game-search).

10. **Along the same lines of implementing the creation of matches, the winners of the match are already being stored! Something could be done with this, such as making a leaderboard or simply a GET for the endpoint.**

    See [earlier response](#leaderboard).

### [Product Ideas](https://github.com/Corbyn-Rasque/Game-Night/issues/12)

1. **A social aspect would be fun; users could add other users as a friend and join the same events/brackets as them.**

    Fantastic idea! This has been implemented!
    https://github.com/Corbyn-Rasque/Game-Night/blob/e40e67747038c95e6ff85e7ff3baf0010bf6721b/src/api/social.py

2. **A moderator endpoint could be useful for the gaming aspect of things, where a mode could be assigned to group to look out for cheating/etc.**

    That'd honestly be a super cool idea, especially for if the app every gets used for things like Dungeons & Dragons (TM) (don't want to anger the lawyers of Wizards of the Coast…). This idea is a bit much to implement for us this time around, but would be a great idea for the future!