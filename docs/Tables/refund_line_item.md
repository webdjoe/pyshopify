# ![logo](../Images/table.svg) refund_line_item

[Start](../start.md)>refund_line_item

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

___
