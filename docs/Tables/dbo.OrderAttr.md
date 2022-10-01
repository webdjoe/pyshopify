# ![logo](../Images/table.svg) dbo.OrderAttr

[Start](../start.md)>dbo.OrderAttr

## [](#Description) Description

> Attribution details for each order, such as campaign, source, and landing page.

## [](#Columns) Columns _`7`_

| Key | Name              | Data Type | Length | Precision | Scale | Not Null | Description                    |
|:---:|-------------------|-----------|--------|-----------|-------|----------|--------------------------------|
|[![Primary Key PK_OrderAttr_order_id](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_OrderAttr_order_id](../Images/Cluster.svg)](#Indexes)|order_id|bigint|8|19|0|True|Order ID |
|[![Indexes IDX_OrderAttr_processed_at](../Images/index.svg)](#Indexes)|processed_at|datetime|8|23|3|True|Datetime order was processed|
||landing_site|nvarchar||0|0|False|Landing page order originated on|
||referring_site|nvarchar||0|0|False|Site order was referred from|
||source_name|nvarchar||0|0|False|Name of source site order attributed to|
||source_identifier|nvarchar||0|0|False|Source ID of order|
||source_url|nvarchar||0|0|False|URL of order source|

## [](#Indexes) Indexes _`2`_

|Key|Name|Columns|Unique|
|:---:|---|---|---|
||IDX_OrderAttr_processed_at|processed_at|False|
|[![Primary Key PK_OrderAttr_order_id](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_OrderAttr_order_id](../Images/Cluster.svg)](#Indexes)|PK_OrderAttr_order_id|order_id|True|

## [](#SqlScript) SQL Script

```SQL
CREATE TABLE dbo.OrderAttr (
  order_id bigint NOT NULL,
  processed_at datetime NOT NULL,
  landing_site nvarchar(max) NULL,
  referring_site nvarchar(max) NULL,
  source_name nvarchar(max) NULL,
  source_identifier nvarchar(max) NULL,
  source_url nvarchar(max) NULL,
  CONSTRAINT PK_OrderAttr_order_id PRIMARY KEY CLUSTERED (order_id)
)
ON [PRIMARY]
TEXTIMAGE_ON [PRIMARY]
GO

CREATE INDEX IDX_OrderAttr_processed_at
  ON dbo.OrderAttr (processed_at)
  ON [PRIMARY]
GO
```

___
