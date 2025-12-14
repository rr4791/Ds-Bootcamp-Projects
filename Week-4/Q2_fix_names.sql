-- LeetCode 1667: Fix Names in a Table
-- SQL Solution (MySQL)

SELECT
    user_id,
    CONCAT(
        UPPER(LEFT(name, 1)),
        LOWER(SUBSTRING(name, 2))
    ) AS name
FROM Users
ORDER BY user_id;
