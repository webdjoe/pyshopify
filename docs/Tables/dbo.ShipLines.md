# ![logo](../Images/table.svg) dbo.ShipLines

[Start](../start.md)>[Tables](./Tables.md)>dbo.ShipLines

## [](#Description) Description

> Order shipping lines

## [](#Columns) Columns _`12`_

|Key|Name|Data Type|Length|Precision|Scale|Not Null|Description
|---|---|---|---|---|---|---|---
|[![Primary Key PK_ShipLines](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_ShipLines](../Images/Cluster.svg)](#Indexes)|id|bigint|8|19|0|True|Shipping line id|
| |carrier_identifier|nvarchar|255|0|0|False|Shipping carrier ID|
| |code|nvarchar|255|0|0|False|Shipping code|
| |delivery_category|nvarchar|255|0|0|False|Shipment delivery category|
| |ship_discount_price|money|8|19|4|False|Shipping discounted price|
| |ship_price|money|8|19|4|False|Shipping price|
| |phone|nvarchar|255|0|0|False|Shipping phone|
| |requested_fulfillment_id|nvarchar|255|0|0|False|Fulfillment ID|
| |source|nvarchar|255|0|0|False|Shipment source|
| |title|nvarchar|255|0|0|False|Shipping title|
| |order_id|bigint|8|19|0|False|Order ID|
| |order_date|datetime|8|23|3|False|Order_date|

## [](#Indexes) Indexes _`1`_

|Key|Name|Columns|Unique|Type|Description
|---|---|---|---|---|---
|[![Primary Key PK_ShipLines](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_ShipLines](../Images/Cluster.svg)](#Indexes)|PK_ShipLines|id|True|||

## [](#SqlScript) SQL Script

```SQL
CREATE TABLE dbo.ShipLines (
  id bigint NOT NULL,
  carrier_identifier nvarchar(255) NULL,
  code nvarchar(255) NULL,
  delivery_category nvarchar(255) NULL,
  ship_discount_price money NULL,
  ship_price money NULL,
  phone nvarchar(255) NULL,
  requested_fulfillment_id nvarchar(255) NULL,
  source nvarchar(255) NULL,
  title nvarchar(255) NULL,
  order_id bigint NULL,
  order_date datetime NULL,
  CONSTRAINT PK_ShipLines PRIMARY KEY CLUSTERED (id)
)
ON [PRIMARY]
GO
```

___
