#### Code Peer Review Response - Samiksha Karimbil

1. Consider wrapping gets in a try/except block to avoid issues with the database.

This was implemented for all database connections

2. Some of the endpoints return “OK”, such as the cancel event, request/contribute item or remove items endpoints. Consider standardizing the responses with JSON objects for consistency

JSON objects were added for consistency in endpoints

3. Consider using HTTP status codes for error handling along with descriptive messages

HTTP exceptions were added along with status codes and descriptive messages through the endpoints. 

4. In general, consider whether you want to reference a user through name or id. There are inconsistencies with that in some of the endpoints (add vs remove user, etc)

We'd like to allow users to change their usernames; therefore, using them as the primary key wouldn't be ineffective. It would be too difficult to change the Primary Keys for every table.

5. Lots of places with commented out code, generally makes code less visually appealing

Comments removed.

6. Consider print statements for logging purposes

Added print statements for all endpoints that modified the database. 

7. In get_event, not all cases for start and end time were considered, like if one of the times is not provided or if they are the same

Both of these edge cases respond fine to unit tests, and return appropriate results. If start and end times are the same, no events will return. If one is not provided, it searches around only the provided start or stop, with no limit in the other direction. This doesn't seem to be an issue from what I can see. 

8. SQL injections are a possibility with name, type, username or platform

All parameters in the endpoints use SQL parameter binding, [[https://observablehq.com/@calpoly-pierce/sql-security|which should prevent an injection attack]]. After reviewing, I'm not sure where this is a risk, but would be very interested to learn where specifically the concern is. 

9. There are 2 endpoints with the same function name (remove_user_contributions in items.py). Consider combining these endpoints where the request may contain the specific item, and remove all contributions if it doesn’t

Correct. We have since merged the two endpoints into one with optional parameters to increase readability. 

10. Consider documentation, each endpoint could have at least 1 line describing its purpose. This could be done with a docstring at the start of the function.

Added endpoint descriptions for readability 

11. Fields like username, event id, item name could all be validated to ensure correct data types and avoid invalid entries

Fixed every parameter that did explicitly define an appropriate data type. 

12. Instead of permanently deleting things like teams or items, consider adding in a deleted column to sort of ledgerize data and view history

Items are kept as a ledger already. For now, there isn't a benefit for maintaining a ledger of teams.