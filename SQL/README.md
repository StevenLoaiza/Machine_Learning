# LeetCode Problems

## 196. Delete Duplicate Emails

Write a SQL query to delete all duplicate email entries in a table named Person, keeping only unique emails based on its smallest Id.

+----+------------------+ \
| Id | Email            | \
+----+------------------+ \
| 1  | john@example.com | \
| 2  | bob@example.com   | \
| 3  | john@example.com | \
+----+------------------+ \
Id is the primary key column for this table.
For example, after running your query, the above Person table should have the following rows:

+----+------------------+ \
| Id | Email            | \
+----+------------------+ \
| 1  | john@example.com | \
| 2  | bob@example.com   | \
+----+------------------+ \

Note:

Your output is the whole Person table after executing your sql. Use delete statement.

### Solution
```sql
# Write your MySQL query statement below
DELETE tbl1
    FROM 
        Person tbl1
    JOIN Person tbl2
    ON
        tbl1.Email = tbl2.Email 
        AND tbl1.Id > tbl2.Id
;
```
## 176. Second Highest Salary

Write a SQL query to get the second highest salary from the Employee table.

+----+-------+ \
| Id | Salary| \
+----+-------+ \
| 1  | 100   | \
| 2  | 200   | \
| 3  | 300   | \
+----+-------+ \

For example, given the above Employee table, the query should return 200 as the second highest salary. If there is no second highest salary, then the query should return null.

+----+------------------+ \
| SecondHighestSalary   | \
+----+------------------+ \
| 200                   | \
+----+------------------+ \

### Solution
```sql
SELECT IFNULL(
    (SELECT DISTINCT Salary
    FROM Employee
    ORDER BY Salary DESC
    LIMIT 1 OFFSET 1),
NULL)
as SecondHighestSalary;
```

## 175. Combine Two Tables

Table: Person

+-------------+---------+ \
| Column Name | Type    | \
+-------------+---------+ \
| PersonId    | int     | \
| FirstName   | varchar | \
| LastName    | varchar | \
+-------------+---------+ \
PersonId is the primary key column for this table.
Table: Address

+-------------+---------+ \
| Column Name | Type    | \
+-------------+---------+ \
| AddressId   | int     | \
| PersonId    | int     | \
| City        | varchar | \
| State       | varchar | \
+-------------+---------+ \
AddressId is the primary key column for this table.
 

Write a SQL query for a report that provides the following information for each person in the Person table, regardless if there is an address for each of those people:

### Solution
```sql
SELECT
    FirstName,
    LastName,
    City,
    State
FROM
    Person
LEFT JOIN Address
    ON Address.PersonId = Person.PersonId
;
```
## 1179. Reformat Department Table

+---------------+---------+ \
| Column Name   | Type    | \
+---------------+---------+ \
| id            | int     | \
| revenue       | int     | \ 
| month         | varchar | \
+---------------+---------+ \
(id, month) is the primary key of this table.
The table has information about the revenue of each department per month.
The month has values in ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"].

Write an SQL query to reformat the table such that there is a department id column and a revenue column for each month.

The query result format is in the following example:
Department table:
+------+---------+-------+ \
| id   | revenue | month | \
+------+---------+-------+ \
| 1    | 8000    | Jan   | \
| 2    | 9000    | Jan   | \
| 3    | 10000   | Feb   | \
| 1    | 7000    | Feb   | \
| 1    | 6000    | Mar   | \
+------+---------+-------+ 

Result table:
+------+-------------+-------------+-------------+-----+-------------+ \
| id   | Jan_Revenue | Feb_Revenue | Mar_Revenue | ... | Dec_Revenue | \
+------+-------------+-------------+-------------+-----+-------------+ \ 
| 1    | 8000        | 7000        | 6000        | ... | null        | \
| 2    | 9000        | null        | null        | ... | null        | \
| 3    | null        | 10000       | null        | ... | null        | \
+------+-------------+-------------+-------------+-----+-------------+ 

Note that the result table has 13 columns (1 for the department id + 12 for the months).

### Solution

```sql
SELECT 
    id, 
    SUM(CASE WHEN month = 'Jan' THEN revenue ELSE null END) AS Jan_Revenue,
    SUM(CASE WHEN month = 'Feb' THEN revenue ELSE null END) AS Feb_Revenue,
    SUM(CASE WHEN month = 'Mar' THEN revenue ELSE null END) AS Mar_Revenue,
    SUM(CASE WHEN month = 'Apr' THEN revenue ELSE null END) AS Apr_Revenue,
    SUM(CASE WHEN month = 'May' THEN revenue ELSE null END) AS May_Revenue,
    SUM(CASE WHEN month = 'Jun' THEN revenue ELSE null END) AS Jun_Revenue,
    SUM(CASE WHEN month = 'Jul' THEN revenue ELSE null END) AS Jul_Revenue,
    SUM(CASE WHEN month = 'Aug' THEN revenue ELSE null END) AS Aug_Revenue,
    SUM(CASE WHEN month = 'Sep' THEN revenue ELSE null END) AS Sep_Revenue,
    SUM(CASE WHEN month = 'Oct' THEN revenue ELSE null END) AS Oct_Revenue,
    SUM(CASE WHEN month = 'Nov' THEN revenue ELSE null END) AS Nov_Revenue,
    SUM(CASE WHEN month = 'Dec' THEN revenue ELSE null END) AS Dec_Revenue
FROM 
    Department
GROUP BY id;
```
