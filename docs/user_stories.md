# **Game Night**

User Stories  
---

1. As a competitive player, I want to find high level players so that I get good practice and become a better player.  
2. As a casual player, I want to play games with others looking to play for fun so that I can spend my free time having fun.   
3. As a beginner player, I want to find other beginners so that we can all learn to play the games together.   
4. As an event host, I want people to find my events easily so that I do not have to advertise by word of mouth or with a flier.   
5. As a tournament organizer, I want automatic seeding based on previous tournament results so that bracket making is easier.   
6. As someone without a car, I am looking for rides to stores so that I can buy things I need that I could not carry on the bus or walking.  
7. As someone who likes to take a lot of road trips, organizing people who want to go, who’s going in what car, and who’s bringing what, I would love an app that could do that, and a gaming slant would be cool for games in the car.  
8. As an event host, I want to be able to easily and quickly set up events that I have previously hosted so that I can host similar events repeatedly.   
9. As a player of a specific game, I want to have similar games recommended so that I can find new games to play and enjoy.   
10. As an on campus resident, I want to be in the loop of events going on in my community so that I can feel included in the community.  
11. As a movie connoisseur, I want to find and host movie nights where people can vote to decide what movie to watch so that I have a better idea of what everyone prefers to watch.   
12. As a Rizzy  individual i”m looking for some gyats in the vicinity to rizz up. On skibbidy. 

Possible Exceptions  
---

1. If a game/activity is entered by a host but not found in the section of popular games, they will get the option to add it through a custom entry box that will make that activity show up next time the host starts an event.   
2. If a new user lands on the starting page and did not set preferences, it would leave the list of recommended games empty and thus not recommend anything to them. In that scenario,  the user would be recommended the most popular games and activities.   
3. If the connection is poor and the user repeatedly tries to add, edit, or remove an event, there may be a number of sequential calls to add, update or remove a row from the database that may result in an error thrown or unexpected behavior (especially in updates).  
4. If the database is incorrectly set up, repeating an event may destructively edit past entries. Care should be taken in selecting primary or composite keys, and how events are connected & displayed.  
5. If searching for previous events, care should be taken to ensure repeated entries are still shown as a single listing or related listing to make search useful. Foreign keys may   
6. Adding the same user multiple times, the same items multiple times, etc may result in issues if unique primary keys are given to all entries. In some cases this may be desired with people with the same name, but other times this may result in duplicates. Some logic to compare contact details or other unique keys may help avoid this.  
7. A user typing in a specific game to add may encounter issues where the spelling of the title, spacings, or punctuation are different from the game in the database. Suggestions for game based on something like edit distance, or searching after a regex to get rid of some of the punctuation, for example, may lessen this issue.  
8. Two people may end up with an identical match-making rank after a number of games. Putting them in a rank may be a challenge,  as they may not end up facing one another (e.g. one is placed against a player above them and the other below). Using the number of games played as a tie-breaker would be effective in solving this, since someone who’s played more games than the other may have a more gradual skill curve, and should theoretically be placed against the lower player in that case.  
9. If a person is dropped from a seeded bracket and another person is to replace that person but their match-making rank is not the same, a prompt would be shown to the organizer asking if they want to seed the bracket again or just insert the new player.  
10. Two people both claim they won or lost (intentionally or otherwise). This case could be handled by having the host tie-break, DQ both, or set the final decision to a vote amongst all players.  
11. If a user attempts to use a username that is already in use, there will be suggested usernames that are not in use with the option of also trying a different name.  
12. If a tournament or bracket has more players than a power of two, the highest seeded players will start a round ahead to be higher in the bracket than the lower seeded players. The number of high seeded players to start ahead will be dependent on the total number of players in the bracket as well as what interval of powers of two the player amount is at.

