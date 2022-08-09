# ![logo](../Images/table.svg) dbo.LineItems

[Start](../start.md)>[Tables](./Tables.md)>dbo.LineItems

## [](#Description) Description

> Line Items with Units Sold for Orders

## [](#Columns) Columns _`6`_

|Key|Name|Data Type|Length|Precision|Scale|Not Null|Description
|---|---|---|---|---|---|---|---
|[![Primary Key PK_line_item_id](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_line_item_id](../Images/Cluster.svg)](#Indexes)|id|bigint|8|19|0|True|Line Item ID|
| |order_id|bigint|8|19|0|True|Order ID|
| |order_date|datetime|8|23|3|True|Order Created Date|
| |variant_id|bigint|8|19|0|True|Unit variant ID|
| |quantity|int|4|10|0|True|Line Item Quantity|
| |price|float|8|53|0|True|Line Item Unit Price|
| |name|nvarchar|255|0|0|False|Variant Name|
| |product_id|bigint|8|19|0|False|Product ID|
| |sku|nvarchar|255|0|0|False|Product Variant SKU|
| |title|nvarchar|255|0|0|False|Product Title|
| |total_discount|money|8|19|4|False|Line item discount|
| |variant_title|nvarchar|255|0|0|False|Variant Title|

## [](#Indexes) Indexes _`1`_

|Key|Name|Columns|Unique|Type|Description
|---|---|---|---|---|---
|[![Primary Key PK_line_item_id](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_line_item_id](../Images/Cluster.svg)](#Indexes)|PK_line_item_id|id|True||Line Item Primary Key|

## [](#SqlScript) SQL Script

```SQL
CREATE TABLE dbo.LineItems (
  id bigint NOT NULL,
  order_id bigint NOT NULL,
  order_date datetime NOT NULL,
  variant_id bigint NOT NULL,
  quantity int NOT NULL,
  price float NOT NULL,
  name nvarchar(255) NULL,
  product_id bigint NULL,
  sku nvarchar(255) NULL,
  title nvarchar(255) NULL,
  total_discount money NULL,
  variant_title nvarchar(255) NULL,
  CONSTRAINT PK_line_item_id PRIMARY KEY CLUSTERED (id)
)
ON [PRIMARY]
GO
```

___
