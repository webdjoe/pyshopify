# ![logo](../Images/table.svg) dbo.DiscountApps

[Start](../start.md)>dbo.DiscountApps

## [](#Description) Description

> Discount applied to each order

## [](#Columns) Columns _`11`_

|Key|Name|Data Type|Length|Precision|Scale|Not Null|Description|
|---|---|---|---|---|---|---|---|
|[![Primary Key PK_DiscountApps](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_DiscountApps](../Images/Cluster.svg)](#Indexes)|id|bigint|8|19|0|True|Order ID combined with discount application index|
|[![Indexes IDX_DiscountApps_order_id](../Images/index.svg)](#Indexes)|order_id|bigint|8|19|0|True|Order ID discount applied to|
||processed_at|datetime|8|23|3|True|Datetime order was processed in UTC|
||type|nvarchar|255|0|0|True|Type of discount application|
||title|nvarchar|255|0|0|False|Title of Discount Applied|
||description|nvarchar|255|0|0|False|Description of Discount Applied|
||value|money|8|19|4|True|Value of Discount|
||value_type|nvarchar|255|0|0|False|Value type of discount percentage/dollar|
||allocation_method|nvarchar|255|0|0|False|Discount allocated across order/products/shipping|
||target_selection|nvarchar|255|0|0|False|Target of discount applied|
||target_type|nvarchar|255|0|0|False|Type of target discount applied to|
||code|nvarchar|255|0|0|False|Discount code if code was used|

## [](#Indexes) Indexes

|Key|Name|Columns|Unique|
|:---:|---|---|---|
||IDX_DiscountApps_order_id|order_id|False|
|[![Primary Key PK_DiscountApps](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_DiscountApps](../Images/Cluster.svg)](#Indexes)|PK_DiscountApps|id|True|

## [](#SqlScript) SQL Script

```SQL
CREATE TABLE dbo.DiscountApps (
  id bigint NOT NULL,
  order_id bigint NOT NULL,
  processed_at datetime NOT NULL,
  type nvarchar(255) NOT NULL,
  title nvarchar(255) NULL,
  description nvarchar(255) NULL,
  value money NOT NULL,
  value_type nvarchar(255) NULL,
  allocation_method nvarchar(255) NULL,
  target_selection nvarchar(255) NULL,
  target_type nvarchar(255) NULL,
  code nvarchar(255) NULL,
  CONSTRAINT PK_DiscountApps PRIMARY KEY CLUSTERED (id)
)
ON [PRIMARY]
GO

CREATE INDEX IDX_DiscountApps_order_id
  ON dbo.DiscountApps (order_id)
  ON [PRIMARY]
GO

```

___
