# ![logo](../Images/table.svg) dbo.RefundLineItem

[Start](../start.md)>dbo.RefundLineItem

## [](#Description) Description

> Refunded Units

## [](#Columns) Columns _`8`_

|Key|Name|Data Type|Length|Precision|Scale|Not Null|Description
|---|---|---|---|---|---|---|---
|[![Primary Key PK_refundlineitem_id](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_refundlineitem_id](../Images/Cluster.svg)](#Indexes)|id|bigint|8|19|0|True|Refund line item ID|
||refund_id|bigint|8|19|0|True|Refund ID of line item|
|[![Indexes IDX_RefundLineItem_processed_at](../Images/index.svg)](#Indexes)|processed_at|datetime|8|23|3|True|Datetime line item was refunded|
||order_date|datetime|8|23|3|True|Datetime line item was ordered|
|[![Indexes IDX_RefundLineItem_order_id](../Images/index.svg)](#Indexes)|order_id|bigint|8|19|0|True|Order ID of refunded line item|
||line_item_id|bigint|8|19|0|True|Line Item ID of refunded line item|
||variant_id|bigint|8|19|0|True|Product variant ID of refunded line item|
||quantity|int|4|10|0|True|Quantity refunded|
||subtotal|money|8|19|4|True|Subtotal of refund|
||total_tax|money|8|19|4|True|Total tax refunded for line item|

## [](#Indexes) Indexes _`1`_

|Key|Name|Columns|Unique|
|:---:|---|---|---|
||IDX_RefundLineItem_order_id|order_id|False|
||IDX_RefundLineItem_processed_at|processed_at|False|
|[![Primary Key PK_refundlineitem_id](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_refundlineitem_id](../Images/Cluster.svg)](#Indexes)|PK_refundlineitem_id|id|True|

## [](#SqlScript) SQL Script

```SQL
CREATE TABLE dbo.RefundLineItem (
  id bigint NOT NULL,
  refund_id bigint NOT NULL,
  processed_at datetime NOT NULL,
  order_date datetime NOT NULL,
  order_id bigint NOT NULL,
  line_item_id bigint NOT NULL,
  variant_id bigint NOT NULL,
  quantity int NOT NULL,
  subtotal money NOT NULL,
  total_tax money NOT NULL,
  CONSTRAINT PK_refundlineitem_id PRIMARY KEY CLUSTERED (id)
)
ON [PRIMARY]
GO

CREATE INDEX IDX_RefundLineItem_order_id
  ON dbo.RefundLineItem (order_id)
  ON [PRIMARY]
GO

CREATE INDEX IDX_RefundLineItem_processed_at
  ON dbo.RefundLineItem (processed_at)
  ON [PRIMARY]
GO
```

___
