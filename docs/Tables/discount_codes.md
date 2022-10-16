# ![logo](../Images/table.svg) discount_codes

[Start](../start.md)>discount_codes

## [](#Description) Description

> Discount Codes Used for Each Order

## [](#Columns) Columns _`5`_

|Key|Name|Data Type|Length|Precision|Scale|Not Null|Description
|---|---|---|---|---|---|---|---
|[![Primary Key PK_DiscountCodes](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_DiscountCodes](../Images/Cluster.svg)](#Indexes)|order_id|bigint|8|19|0|True|Order ID discount code applied to|
|[![Indexes IDX_DiscountCodes_order_id](../Images/index.svg)](#Indexes)|processed_at|datetime|8|23|3|True|Date the order was processed|
|[![Primary Key PK_DiscountCodes](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_DiscountCodes](../Images/Cluster.svg)](#Indexes)|code|nvarchar|255|0|0|True|Discount code|
||amount|money|8|19|4|True|Amount of discount code|
||type|nvarchar|255|0|0|True|Type of Discount Code|

## [](#Indexes) Indexes

|Key|Name|Columns|Unique|
|:---:|---|---|---|
||IDX_DiscountCodes_order_id|processed_at|False|
|[![Primary Key PK_DiscountCodes](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_DiscountCodes](../Images/Cluster.svg)](#Indexes)|PK_DiscountCodes|order_id, code|True|

___
