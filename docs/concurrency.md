# Concurrency Issues

## Lost Update
### 2 Winners declared for the same bracket in the same match at the same time
If 2 different valid winners are declared at the exact same time, one would successfully update and the other would be lost. Since there is a select statement that gets the correct match, and it checks that there is no winner yet, it could potentially get the match with no winner on both, update on one, and then try to update again but it gets lost. 

To address this, we ensured that the match winner is only updated within the same query as when it selects the correct match using CTEs which makes it atomic because its in the same query. Because only 1 update will go through now, the following query that updates the score will not run for both because it is dependent on the id returned by the initial update.

![Concurrency Case 1 Diagram](./images/case1.png)


##