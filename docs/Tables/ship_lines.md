# ![logo](../Images/table.svg) ship_lines

[Start](../start.md)> ship_lines

## [](#Description) Description

> Order shipping lines

## [](#Columns) Columns _`12`_

|Key|Name|Data Type|Length|Precision|Scale|Not Null|Description
|---|---|---|---|---|---|---|---
|[![Primary Key PK_ShipLines](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_ShipLines](../Images/Cluster.svg)](#Indexes)|id|bigint|8|19|0|True|Ship line ID|
|[![Indexes IDX_ShipLines](../Images/index.svg)](#Indexes)|processed_at|datetime|8|23|3|True|Datetime order was processed|
|[![Indexes IDX_ShipLines](../Images/index.svg)](#Indexes)|order_id|bigint|8|19|0|True|Order ID of shipping line|
||carrier_identifier|nvarchar|255|0|0|False|Shipping carrier ID|
||code|nvarchar|255|0|0|False|Shipping carrier code|
||delivery_category|nvarchar|255|0|0|False|Delivery type - pickup|
||discounted_price|money|8|19|4|True||
||price|money|8|19|4|True||
||phone|nvarchar|255|0|0|False||
||requested_fulfillment_service_id|nvarchar|255|0|0|False||
||source|nvarchar|255|0|0|False|Order of Item shipped|
||title|nvarchar|255|0|0|False|Title of shipping method|

## [](#Indexes) Indexes _`1`_

|Key|Name|Columns|Unique|
|---|---|---|---|
||IDX_ShipLines|order_id, processed_at|False|
|[![Primary Key PK_ShipLines](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_ShipLines](../Images/Cluster.svg)](#Indexes)|PK_ShipLines|id|True|

___
