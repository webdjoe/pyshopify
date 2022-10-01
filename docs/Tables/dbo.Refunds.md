# ![logo](../Images/table.svg) dbo.Refunds

[Start](../start.md)>dbo.Refunds

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

## [](#SqlScript) SQL Script

```SQL
CREATE TABLE dbo.Refunds (
  id bigint NOT NULL,
  created_at datetime NOT NULL,
  processed_at datetime NOT NULL,
  order_date datetime NOT NULL,
  order_id bigint NOT NULL,
  note nvarchar(max) NULL,
  CONSTRAINT PK_refund_id PRIMARY KEY CLUSTERED (id)
)
ON [PRIMARY]
TEXTIMAGE_ON [PRIMARY]
GO

CREATE INDEX IDX_Refunds_created_at
  ON dbo.Refunds (created_at)
  ON [PRIMARY]
GO

CREATE INDEX IDX_Refunds_order_id
  ON dbo.Refunds (order_id)
  ON [PRIMARY]
GO
```

___
