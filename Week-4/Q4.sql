-- LeetCode 176: Second Highest Salary
-- SQL Solution (MySQL)

SELECT
    (SELECT DISTINCT salary
     FROM Employee
     ORDER BY salary DESC
     LIMIT 1 OFFSET 1) AS SecondHighestSalary;
