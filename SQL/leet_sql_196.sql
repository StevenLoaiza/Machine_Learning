# Write your MySQL query statement below
DELETE tbl1
    FROM 
        Person tbl1
    JOIN Person tbl2
    ON
        tbl1.Email = tbl2.Email 
        AND tbl1.Id > tbl2.Id
;
