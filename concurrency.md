# Concurrency Issues

## Lost Update
### 2 Winners declared for the same bracket in the same match at the same time
If 2 different valid winners are declared at the exact same time, one would successfully update and the other would be lost. Since there is a select statement that gets the correct match, and it checks that there is no winner yet, it could potentially get the match with no winner on both, update on one, and then try to update again but it gets lost. 

##