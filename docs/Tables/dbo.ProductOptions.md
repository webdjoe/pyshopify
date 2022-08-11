# ![logo](../Images/table.svg) dbo.Products

[Start](../start.md)>dbo.Products

## [](#Description) Description

> Product listing data

## [](#Columns) Columns

|Key|Name|Data Type|Length|Precision|Scale|Not Null|Description
|---|---|---|---|---|---|---|---
[![Primary Key PK_Options](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_Options](../Images/cluster.svg)](#Indexes)|id|bigint|8|19|0|True|Product Option ID|
||product_id|bigint|8|19|0|True|Product ID associated with Option|
||name|nvarchar|100|0|0|False|Name of Product Option|
||position|int|4|10|0|False|Position of Option for Choosing Variant on Product Page|
||values|nvarchar||0|0|False|Variant IDs associated with Option|

## [](#Indexes) Indexes

|Key|Name|Columns|Unique|Type|Description
|---|---|---|---|---|---
|[![Primary Key PK_ProductOptions}](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_ProductOptions](../Images/cluster.svg)](#Indexes)|PK_ProductOptions|id|True||Product Options ID PK|

## [](#SqlScript) SQL Script

```SQL
CREATE TABLE shop_rest.dbo.ProductOptions (
  id BIGINT NOT NULL
 ,product_id BIGINT NOT NULL
 ,name NVARCHAR(100) NULL
 ,position INT NULL
 ,[values] NVARCHAR(MAX) NULL
 ,CONSTRAINT PK_ProductOptions_id PRIMARY KEY CLUSTERED (id)
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
```

___
