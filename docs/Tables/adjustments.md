# ![logo](../Images/table.svg) adjustments

[Start](../start.md)>adjustments

## [](#Description) Description

> Adjustments on order for refunding shipping and refund discrepancies

## [](#Columns) Columns

|Key|Name|Data Type|Length|Precision|Scale|Not Null|Description
|---|---|---|---|---|---|---|---
|[![Primary Key PK_adj_id](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_adj_id](../Images/cluster.svg)](#Indexes)|id|bigint|8|19|0|True|Adjustment ID|
| |refund_id|bigint|8|19|0|True|Refund ID|
||refund_id|bigint|8|19|0|True|Refund ID of adjustment|
||processed_at|datetime|8|23|3|True|Datetime adjustment was processed|
||order_date|datetime|8|23|3|True|Datetime adjusted order was placed|
||order_id|bigint|8|19|0|True|Order ID of adjusted order|
||amount|money|8|19|4|True|Amount of adjustment|
||tax_amount|money|8|19|4|True|Tax amount adjusted|
||kind|nvarchar|255|0|0|False|Kind of adjustment|
||reason|nvarchar|255|0|0|False|Reason for adjustment|

## [](#Indexes) Indexes

|Key|Name|Columns|Unique|
|---|---|---|---|
|[![Primary Key PK_adj_id](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_adj_id](../Images/cluster.svg)](#Indexes)|PK_adj_id|id|True|
___
