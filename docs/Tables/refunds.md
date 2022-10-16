# ![logo](../Images/table.svg) refunds

[Start](../start.md)>refunds

## [](#Description) Description

> Order Refunds

## [](#Columns) Columns _`3`_

|Key|Name|Data Type|Length|Precision|Scale|Not Null|Description
|---|---|---|---|---|---|---|---
|[![Primary Key PK_refund_id](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_refund_id](../Images/Cluster.svg)](#Indexes)|id|bigint|8|19|0|True|Refund ID|
|[![Indexes IDX_Refunds_created_at](../Images/index.svg)](#Indexes)|created_at|datetime|8|23|3|True|Datetime refund created|
||processed_at|datetime|8|23|3|True|Datetime refund processed|
||order_date|datetime|8|23|3|True|Datetime refunded order was placed|
|[![Indexes IDX_Refunds_order_id](../Images/index.svg)](#Indexes)|order_id|bigint|8|19|0|True|ID of order that was refunded|
||note|nvarchar||0|0|False|Notes included with refund|

## [](#Indexes) Indexes _`1`_

|Key|Name|Columns|Unique|
|:---:|---|---|---|
||IDX_Refunds_created_at|created_at|False|
||IDX_Refunds_order_id|order_id|False|
|[![Primary Key PK_refund_id](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_refund_id](../Images/Cluster.svg)](#Indexes)|PK_refund_id|id|True|

___
