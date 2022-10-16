# ![logo](../Images/table.svg) variants

[Start](../start.md)>variants

## [](#Description) Description

> Product listing data

## [](#Columns) Columns

|Key|Name|Data Type|Length|Precision|Scale|Not Null|Description
|---|---|---|---|---|---|---|---
|[![Primary Key PK_Variants](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_Variants](../Images/Cluster.svg)](#Indexes)|id|bigint|8|19|0|True|Variant ID|
||product_id|bigint|8|19|0|True|Product ID of variant|
||title|nvarchar|255|0|0|False|Variant title|
||price|money|8|19|4|False|Variant price|
||sku|nvarchar|255|0|0|False|Variant sku|
||position|int|4|10|0|False|Position of variant in product list|
||inventory_policy|nvarchar|255|0|0|False|Inventory tracking policy|
||compare_at_price|money|8|19|4|False|Compare at price|
||fulfillment_service|nvarchar|255|0|0|False|Service for fulfillment|
||inventory_management|nvarchar|255|0|0|False|Inventory management method|
||option1|nvarchar|255|0|0|False|Variant option 1|
||option2|nvarchar|255|0|0|False|Variant option 2|
||option3|nvarchar|255|0|0|False|Variant option 3|
||created_at|datetime|8|23|3|True|Date variant created|
||updated_at|datetime|8|23|3|True|Datetime variant last updated|
||barcode|bigint|8|19|0|False|Variant UPC|
||grams|int|4|10|0|False|Weight of variant in grams|
||image_id|bigint|8|19|0|False|Image ID of variant|
||weight|float|8|53|0|False|Weight in custom units|
||weight_unit|nvarchar|50|0|0|False|Unit of custom weight|
||inventory_item_id|bigint|8|19|0|False|ID of shopify inventory tracking|
||inventory_quantity|int|4|10|0|False|Amount in inventory|
||old_inventory_quantity|int|4|10|0|False|Amount prior to inventory update|
||requires_shipping|bit|1|1|0|False|Should item be shipped|
||admin_graphql_api_id|nvarchar|255|0|0|False|graphql api ID|

## [](#Indexes) Indexes

|Key|Name|Columns|Unique|
|:---:|---|---|---|
|[![Primary Key PK_Variants](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_Variants](../Images/Cluster.svg)](#Indexes)|PK_Variants|id|True|

___
