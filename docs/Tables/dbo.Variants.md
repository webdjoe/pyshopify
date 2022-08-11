# ![logo](../Images/table.svg) dbo.Products

[Start](../start.md)>dbo.Products

## [](#Description) Description

> Product listing data

## [](#Columns) Columns

|Key|Name|Data Type|Length|Precision|Scale|Not Null|Description
|---|---|---|---|---|---|---|---
|[![Primary Key PK_variants_id](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK__id](../Images/cluster.svg)](#Indexes)|id|bigint|8|19|0|True|Product Variant ID|
||product_id|bigint|8|19|0|True|Product ID|
||title|nvarchar|255|0|0|False|Variant Title|
||price|money|8|19|4|False|Variant Price|
||sku|nvarchar|255|0|0|False|Variant SKU|
||position|int|4|10|0|False|Variant Position|
||inventory_policy|nvarchar|255|0|0|False|Inventory policy for Out of Stock|
||compare_at_price|money|8|19|4|False|Compare at price|
||fulfillment_service|nvarchar|255|0|0|False|Variant Fulfillment Service|
||inventory_management|nvarchar|255|0|0|False|Variant inventory management system|
||option1|nvarchar|255|0|0|False|Variant Option 1 Title|
||option2|nvarchar|255|0|0|False|Variant Option 2 Title|
||option3|nvarchar|255|0|0|False|Variant Option 3 Title|
||created_at|datetimeoffset|10|34|7|False|Variant created date|
||updated_at|datetimeoffset|10|34|7|False|Variant updated date|
||barcode|bigint|8|19|0|False|Variant UPC|
||grams|int|4|10|0|False|variant weight in grams|
||image_id|bigint|8|19|0|False|variant image ID|
||weight|float|8|53|0|False|variant weight|
||weight_unit|nvarchar|50|0|0|False|variant unit of weight|
||inventory_item_id|bigint|8|19|0|False|inventory item ID|
||inventory_quantity|int|4|10|0|False|Quantity in inventory|
||old_inventory_quantity|int|4|10|0|False|Previous inventory quantity if updating|
||requires_shipping|bit|1|1|0|False|True if a physically shipped item|
||admin_graphql_api_id|nvarchar|255|0|0|False|Variant Graphql ID|

## [](#Indexes) Indexes

|Key|Name|Columns|Unique|Type|Description
|---|---|---|---|---|---
|[![Primary Key PK_Variants](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_Variants](../Images/cluster.svg)](#Indexes)|PK_Variants|id|True||Product Variant ID PK|

## [](#SqlScript) SQL Script

```SQL
CREATE TABLE dbo.Variants (
  id bigint NOT NULL,
  product_id bigint NOT NULL,
  title nvarchar(255) NULL,
  price money NULL,
  sku nvarchar(255) NULL,
  position int NULL,
  inventory_policy nvarchar(255) NULL,
  compare_at_price money NULL,
  fulfillment_service nvarchar(255) NULL,
  inventory_management nvarchar(255) NULL,
  option1 nvarchar(255) NULL,
  option2 nvarchar(255) NULL,
  option3 nvarchar(255) NULL,
  created_at datetimeoffset NULL,
  updated_at datetimeoffset NULL,
  barcode bigint NULL,
  grams int NULL,
  image_id bigint NULL,
  weight float NULL,
  weight_unit nvarchar(50) NULL,
  inventory_item_id bigint NULL,
  inventory_quantity int NULL,
  old_inventory_quantity int NULL,
  requires_shipping bit NULL,
  admin_graphql_api_id nvarchar(255) NULL,
  CONSTRAINT PK_Variants PRIMARY KEY CLUSTERED (id)
)
ON [PRIMARY]
GO
```

___
