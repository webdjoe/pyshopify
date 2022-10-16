# ![logo](../Images/table.svg) order_prices

[Start](../start.md)>order_prices

## [](#Description) Description

> Amounts charged for order.

## [](#Columns) Columns _`7`_

| Key | Name              | Data Type | Length | Precision | Scale | Not Null | Description                    |
|:---:|-------------------|-----------|--------|-----------|-------|----------|--------------------------------|
|[![Primary Key PK_OrderPrices_order_id](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_OrderPrices_order_id](../Images/Cluster.svg)](#Indexes)|order_id|bigint|8|19|0|True|Order ID for charges|
|[![Indexes UK_OrderPrices](../Images/index.svg)](#Indexes)|processed_at|datetime|8|23|3|True|Datetime order was processed|
||updated_at|datetime|8|23|3|True|Order last updated datetime|
||current_total_discounts|money|8|19|4|True|Total discount including refunds, adjustments and returns|
||current_total_price|money|8|19|4|True|Total price of order including refunds, adjustments and returns|
||current_subtotal_price|money|8|19|4|True|Price after discounts with refunds, adjustments and returns|
||current_total_tax|money|8|19|4|True|Total tax including refunds, adjustments and returns|
||subtotal_price|money|8|19|4|True|Price after discounts, not including tax, shipping, duties, tips|
||total_discounts|money|8|19|4|True|Total discounts applied|
||total_line_items_price|money|8|19|4|True|Sum of all line item prices|
||total_price|money|8|19|4|True|Sum of line item pricing, discounts, shipping, taxes and tips|
||total_tax|money|8|19|4|True|Total amount of tax charged|
||total_shipping_price|money|8|19|4|True|Price charged for shipping, excluding discounts & returns|
||taxes_included|bit|1|1|0|True|If taxes are included in subtotal|

## [](#Indexes) Indexes _`2`_

|Key|Name|Columns|Unique|
|:---:|---|---|---|
|[![Primary Key PK_OrderPrices_order_id](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_OrderPrices_order_id](../Images/Cluster.svg)](#Indexes)|PK_OrderPrices_order_id|order_id|True|
||UK_OrderPrices|processed_at|False|

___
