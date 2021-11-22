# Data Science and Programming in Python

-- TODO Introduction
# <a id="toolkit"> Data Science Toolkit </a>

## <a id="sql"> Introduction to Structure Query Language </a>

### <a id="general"> General Layout </a>
Below we cover a few base components that make up a sql database:

1.	Schema: It is a container that stores collections of tables, procedures and metadata.
2.	Table: Structure data in a tabular form (such as an excel table).
    1.	Primary Key: It is a column that uniquely identifies each row.
    2.	Foreign Key: It is a column that maps a table to another through the relationship between primary key – foreign key.

![image](https://user-images.githubusercontent.com/46308439/131370112-f12d3ced-af70-4918-bbf9-83d44fc944ba.png)

### <a id="join"> Joins </a>

![image](https://user-images.githubusercontent.com/46308439/131388527-df52aa31-3e1b-422a-b4e1-d6598df45a0d.png)

Let assume we have two seperate tables with an (id) column and a (var) column. Our Goal is to Combine
the tables together.

| id|Val|
|---|---|
|  1| L1|
|  2| L2|
|  3| L3|   
|  4| L4|

| id|Val|
|---|---|
|  1| R1|
|  4| R2|
|  5| R3|
|  6| R4|

The left table column (id) is called a Primary Key, while the right column (id) is called the Foreign
Key . We use foreign keys and primary keys to connect rows in two different tables. One table's foreign
key holds the value of another table's primary key. The most common types of joins will be joining a foreign
key from one table with the primary key from another table.

Now we will use the Query INNER JOIN on both tables above. The INNER JOIN function will combine
the tables above, for the (id) values that are an exact match and discard the rest. The results would look
like this:
|id_L| L_Val| R_Val|
|----|------|------|
|1 |L1 |R1 |
|4 |L4 |R2 |

Given our example above, our SQL query would look like:

```sql
SELECT *
FROM 
  Left_Table
INNER JOIN Right.Table
  ON Left_Table.id=Right_Table.id
```

# <a id="simple">A Simple Approach</a>
A Brief Introduction to the world of Machine Learning. In this article we begin with two easy to understand supervised learning concepts [Linear Regressions & K- Nearest Neighborhood Method](https://github.com/StevenLoaiza/Machine_Learning/blob/master/Introduction/Machine%20Learning%20-%20A%20simple%20approach.ipynb)


# <a id="tree" href="https://github.com/StevenLoaiza/Machine_Learning/tree/master/Decision%20Trees"> Decision Trees</a>

This section is part of a larger effort to create a comprehensive compliation of lessons related to Data Science and Programming in Python.

The project "Decision Tree" hold 3 key lessons:
- Entropy and Information Gain
- Gini Impurity Measure
- Making Decisions with Trees

Each of the lessons above helps the reader decipher the inner workings of tree base algorithms. Keep in mind that this section is a introduction and will go over the building blocks of the algorithm.

# <a id="opti"> Optimization Methods </a>

## <a id="grad"> Gradient Descent </a>

![](https://github.com/StevenLoaiza/Machine_Learning/blob/master/optimize/gradient_animation.gif)

# <a id="deploy">Deployment - Modeling Services</a>

## <a id="k8s">Kubernetes</a>
### <a id="zero">Zero downtime deployment</a>
![](https://github.com/StevenLoaiza/Machine_Learning/blob/master/deployment/images/k8s_update.gif)
