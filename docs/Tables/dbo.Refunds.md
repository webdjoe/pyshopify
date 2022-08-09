# ![logo](../Images/table.svg) dbo.Refunds

[Start](../start.md)>dbo.Refunds

## [](#Description) Description

> Order Refunds

## [](#Columns) Columns _`3`_

|Key|Name|Data Type|Length|Precision|Scale|Not Null|Description
|---|---|---|---|---|---|---|---
|[![Primary Key PK_refund_id](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_refund_id](../Images/cluster.svg)](#Indexes)|id|bigint|8|19|0|True||||False|False|Refund ID|
| |refund_date|datetime|8|23|3|True|Refund Date|
| |order_id|bigint|8|19|0|True|Order ID|

## [](#Indexes) Indexes _`1`_

|Key|Name|Columns|Unique|Type
|---|---|---|---|---
|[![Primary Key PK_refund_id](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_refund_id](../Images/cluster.svg)](#Indexes)|PK_refund_id|id|True||Refund ID Unique PK|

## [](#SqlScript) SQL Script

```SQL
CREATE TABLE dbo.Refunds (
  id bigint NOT NULL,
  refund_date datetime NOT NULL,
  order_id bigint NOT NULL,
  CONSTRAINT PK_refund_id PRIMARY KEY CLUSTERED (id)
)
ON [PRIMARY]
GO
```

___
