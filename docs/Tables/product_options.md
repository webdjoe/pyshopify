# ![logo](../Images/table.svg) product_options

[Start](../start.md)>product_options

## [](#Description) Description

> Options associated with each product

## [](#Columns) Columns

|Key|Name|Data Type|Length|Precision|Scale|Not Null|Description
|---|---|---|---|---|---|---|---
[![Primary Key PK_Options](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_Options](../Images/cluster.svg)](#Indexes)|id|bigint|8|19|0|True|Product Option ID|
||product_id|bigint|8|19|0|True|Product ID associated with Option|
||name|nvarchar|100|0|0|False|Name of Product Option|
||position|int|4|10|0|False|Position of Option for Choosing Variant on Product Page|
||values|nvarchar||0|0|False|Variant IDs associated with Option|

## [](#Indexes) Indexes

|Key|Name|Columns|Unique|
|---|---|---|---|
|[![Primary Key PK_ProductOptions}](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_ProductOptions](../Images/cluster.svg)](#Indexes)|PK_ProductOptions|id|True|

___
