# ![logo](../Images/table.svg) dbo.RefundLineItem

[Start](../start.md)>[Tables](../Tables.md)>dbo.RefundLineItem

## [](#Description) Description

> Refunded Units

## [](#Columns) Columns _`8`_

|Key|Name|Data Type|Length|Precision|Scale|Not Null|Description
|---|---|---|---|---|---|---|---
|[![Primary Key PK_refundlineitem_id](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_refundlineitem_id](../Images/Cluster.svg)](#Indexes)|id|bigint|8|19|0|True|Refund Line Item ID|
| |refund_id|bigint|8|19|0|True|Refund ID|
| |order_id|bigint|8|19|0|True|Order ID|
| |line_item_id|bigint|8|19|0|True|Line Item ID|
| |variant_id|bigint|8|19|0|True|Line Item Variant ID|
| |quantity|int|4|10|0|True|Quantity Refunded|
| |subtotal|float|8|53|0|True|Refund Line Item Subtotal|
| |total_tax|float|8|53|0|True|Refund Line Item Tax|

## [](#Indexes) Indexes _`1`_

|Key|Name|Columns|Unique|Type|Description
|---|---|---|---|---|---
|[![Primary Key PK_refundlineitem_id](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_refundlineitem_id](../Images/Cluster.svg)](#Indexes)|PK_refundlineitem_id|id|True||Unique Refund Line Item ID PK|

## [](#SqlScript) SQL Script

```SQL
CREATE TABLE dbo.RefundLineItem (
  id bigint NOT NULL,
  refund_id bigint NOT NULL,
  order_id bigint NOT NULL,
  line_item_id bigint NOT NULL,
  variant_id bigint NOT NULL,
  quantity int NOT NULL,
  subtotal float NOT NULL,
  total_tax float NOT NULL,
  CONSTRAINT PK_refundlineitem_id PRIMARY KEY CLUSTERED (id)
)
ON [PRIMARY]
GO
```

___
