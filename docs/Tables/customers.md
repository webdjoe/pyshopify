# ![logo](../Images/table.svg) customers

[Start](../start.md)>customers

## [](#Description) Description

> Customer Details

## [](#Columns) Columns

|Key|Name|Data Type|Length|Precision|Scale|Not Null|Description
|---|---|---|---|---|---|---|---
|[![Primary Key PK_customers_id](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_customers_id](../Images/cluster.svg)](#Indexes)|id|bigint|8|19|0|True|Customer ID|
||updated_at|datetime|8|23|3|True|Customer last edited date|
||created_at|datetime|8|23|3|True|Customer created datetime|
||email|nvarchar|255|0|0|False|Customer email addresses|
||last_order_id|bigint|8|19|0|False|Customer last order placed ID|
||orders_count|int|4|10|0|True|Number of orders placed|
||total_spent|money|8|19|4|True|Total amount spent|
||tags|nvarchar||0|0|False|Customer tags|
||city|nvarchar|255|0|0|False|Customer city|
||province|nvarchar|255|0|0|False|Customer state/province|
||country|nvarchar|255|0|0|False|Customer country|
||zip|nvarchar|255|0|0|False|Customer zip|

## [](#Indexes) Indexes

|Key|Name|Columns|Unique|
|---|---|---|---|
|[![Primary Key PK_ordercustid](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_ordercustid](../Images/cluster.svg)](#Indexes)|PK_customers_id|id|True|
___
