-- LeetCode 1050: Actors and Directors Who Cooperated At Least Three Times
-- SQL Solution (MySQL)

SELECT
    actor_id,
    director_id
FROM ActorDirector
GROUP BY actor_id,_
