# ![logo](../Images/table.svg) line_items

[Start](../start.md)>line_items

## [](#Description) Description

> Line Item Product Details for Orders

## [](#Columns) Columns _`6`_

| Key                                                                                                                                   | Name           | Data Type | Length | Precision | Scale | Not Null | Description          |
|---------------------------------------------------------------------------------------------------------------------------------------|----------------|-----------|--------|-----------|-------|----------|----------------------|
|[![Primary Key PK_line_item_id](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_line_item_id](../Images/Cluster.svg)](#Indexes)|id|bigint|8|19|0|True|Line item ID|
|[![Indexes IDX_LineItems_order_id](../Images/index.svg)](#Indexes)|order_id|bigint|8|19|0|True|Order ID of line item|
|[![Indexes IDX_LineItems_processed_at](../Images/index.svg)](#Indexes)|processed_at|datetime|8|23|3|True|Date order was processed|
||variant_id|bigint|8|19|0|True|Product Variant ID of line item|
||quantity|int|4|10|0|True|Line item quantity |
||price|money|8|19|4|True|Line item price|
||name|nvarchar|255|0|0|False|Name of line item product|
||product_id|bigint|8|19|0|True|Product ID of line item|
||sku|nvarchar|255|0|0|False|Line item SKU|
||title|nvarchar|255|0|0|False|Product Title|
||total_discount|money|8|19|4|True|Total discount applied to product|
||variant_title|nvarchar|255|0|0|False|Line item product variant title |
||fulfillment_status|nvarchar|255|0|0|False|Fulfillment status of line item|

## [](#Indexes) Indexes _`1`_

|Key|Name|Columns|Unique|
|---|---|---|---|
||IDX_LineItems_order_id|order_id|False|
||IDX_LineItems_processed_at|processed_at|False|
|[![Primary Key PK_line_item_id](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_line_item_id](../Images/Cluster.svg)](#Indexes)|PK_line_item_id|id|True|

___
