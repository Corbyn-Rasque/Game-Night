# Main Review Response

## Endpoint Testing

1. **POST `/teams` returns a list of an object instead of just an object**

    Teams has been depracated in favor of a different system, so the endpoint no longer exists.

2. **POST `/brackets` will 500 error with default parameters**

    Posting to the endpoint now handles default responses causing errors with event_id & game_id foreign key constraint violations. Proper responses codes are raised in either case, based on the which value was violated. Number of players if defaulted to 1 or a power or 2 if negative or zero values are given.

    A constraint has been added to the brackets table, such that 'string' is no longer a valid event name.

    Date constraints have not been touched, as we have chosen not to enforce event times. If someone wants to create a historical event or be silly, then can do so if they choose.

3. **Can’t get bracket id from GET /brackets and POST brackets fails so can’t test further**

    Fixed brackets search and added correct response codes. Name now allows for partial name search, though empty name searches return nothing. If no parameters are provided, 400 response. No results, 404 response.

## Code Review

### Brackets

1. **Endpoint names are too long, try simplifying by using request body**

    Endpoint names have been shortened.

2. **Validate id’s**

    Error handling has been implemented surrounding anything that has a foreign key to another table, such that a proper HTML response will be raised instead of resulting in an internal error. For when multiple statements are being called, commit() and rollback() were implemented to avoid concurrency issues.

3. **Standardize responses (either “OK” or rows); if OK, use status code instead**

    Proper response codes are now implemented across all Brackets endpoints. Default success status codes have been implemented that are sensical, and errors are handled for things like foreign key constraint violations and for empty responses. Try / Except blocks have been widely implemented where appropriate to provide these codes.

### Events

1. **Validate id’s**

    Additional constraints added to Events to prevent default values for type, name, & location, as well as for enforcing a max_attendees of more than zero. For when multiple statements are being called, commit() and rollback() were implemented to avoid concurrency issues.

2. **Standardize responses (either “OK” or rows); if OK, use status code instead**

    Proper response codes are now implemented across all Brackets endpoints. Default success status codes have been implemented that are sensical, and errors are handled for things like foreign key constraint violations and for empty responses. Try / Except blocks have been widely implemented where appropriate to provide these codes.

3. **`/{event_id}`: DELETE makes it like you are removing the event, consider using PATCH instead**

    Implemented as requested.

### Games

1. **`/` Has `ON CONFLICT DO NOTHING`, but just return error or status code instead**

    Endpoint has been since entirely refactored. Adding games now has constraints (see below), and proper response codes if the game is duplicative or can;t be inserted into the table.

2. **`/` Sanitize values like release year, name, platform, etc.**

    Added value constraints to name, platform, & publisher to prevent NULL or 'string' values. Year must be a positive number (0 included, math majors don't @me), and player_count must be 1 or more. Enums not used, because we intended for the platform to be quite open with what is and isn't considered a game. This may lead to some silliness, but that is honestly a positive. Some sanitizing would have to be done at scale for hateful words, but is beyond the scope of this project.

3. **`/{name}` Returns raw result or empty dictionary, use HTTPS code to report that a game is not found**

    Proper response codes implemented. Game now searches with partial matching. All matches are returned, though name & platform should still uniquely identify games, so single values should be returned if both are specified and there is a match. If no match, 404 is thrown.

### Items

1. **Optional but some endpoints are both updating and inserting, consider separating these for clarity**

    While this makes sense at in principle, it's largely just duplicating code. One post can handle both, and the assumption with posting is that the user currently wants to contribute X amount for Y item, regardless of what any previous value might have been. The user doesn't care what about previous values, and returning different values if updating versus insert could be easily implemented on the front end, depending on what's creating the post.

2. **Validate input like payment, quantity, etc.**

    Constraints added to the event_items and item_contributions table to handle this. Name and Type cannot be default values, quantity (both tables) must be one or more, and cost must be zero or more. Invalid username, event_id, item_name, or quantity are handled correctly with response codes.

3. **Standardize responses (either “OK” or rows); if OK, use status code instead**

    See above. Proper reponse codes implemented.

4. **`/{event_id}/contributions/{username}/{item_name}` Soft DELETE; use PATCH instead.**

    Implemented as described.

### Teams

1. **Standardize responses (either “OK” or rows); if OK, use status code instead**

    Teams endpoint has been entirely deprecated.

2. **Validate inputs**

    Teams endpoint has been entirely deprecated.

### Users

1. **Standardize responses (either “OK” or rows); if OK, use status code instead**

    All responses standardized with correct success response codes and sensical response codes for issues with input.

2. **Using two endpoints to access the same resource when you can use query parameters instead (ex: `/users?id={id}`)**

    Fixed, Optionals used for query parameters.

3. **Validate input such as username.**

    Username, First & Last all now have constraints created in the schema to prevent default username, first, or last name values from being used. Code has been updated to catch these error and provide a sensical response code. 