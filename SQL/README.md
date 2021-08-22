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

175. Combine Two Tables

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
