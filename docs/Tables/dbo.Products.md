# ![logo](../Images/table.svg) dbo.Products

[Start](../start.md)>dbo.Products

## [](#Description) Description

> Product listing data

## [](#Columns) Columns

|Key|Name|Data Type|Length|Precision|Scale|Not Null|Description
|---|---|---|---|---|---|---|---
|[![Primary Key PK_adj_id](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_adj_id](../Images/cluster.svg)](#Indexes)|id|bigint|8|19|0|True|Product ID|
||title|nvarchar|255|0|0|False|Product Title|
||body_html|nvarchar||0|0|False|HTML of product description|
||vendor|nvarchar|255|0|0|False|Product Vendor|
||product_type|nvarchar|255|0|0|False|Defined product type|
||created_at|datetimeoffset|10|34|7|True|Date product created|
||handle|nvarchar|255|0|0|False|Product URL Handle|
||updated_at|datetimeoffset|10|34|7|True|Product last updated|
||published_at|datetimeoffset|10|34|7|False|Date product was published|
||template_suffix|nvarchar|255|0|0|False|Liquid template for product|
||status|nvarchar|255|0|0|False|Active/Draft Status of Product|
||published_scope|nvarchar|255|0|0|False|Published scope - Global, Online Store, Google etc.|
||tags|nvarchar||0|0|False|Product Tags|
||admin_graphql_api_id|nvarchar|255|0|0|False|Graphql api id|
||image_src|nvarchar|255|0|0|False|Product image |

## [](#Indexes) Indexes

|Key|Name|Columns|Unique|Type|Description
|---|---|---|---|---|---
|[![Primary Key PK_products](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_products](../Images/cluster.svg)](#Indexes)|PK_products_id|id|True||Product ID PK|

## [](#SqlScript) SQL Script

```SQL
CREATE TABLE dbo.Products (
  id bigint NOT NULL,
  title nvarchar(255) NULL,
  body_html nvarchar(max) NULL,
  vendor nvarchar(255) NULL,
  product_type nvarchar(255) NULL,
  created_at datetimeoffset NOT NULL,
  handle nvarchar(255) NULL,
  updated_at datetimeoffset NOT NULL,
  published_at datetimeoffset NULL,
  template_suffix nvarchar(255) NULL,
  status nvarchar(255) NULL,
  published_scope nvarchar(255) NULL,
  tags nvarchar(max) NULL,
  admin_graphql_api_id nvarchar(255) NULL,
  image_src nvarchar(255) NULL,
  CONSTRAINT PK_products PRIMARY KEY CLUSTERED (id)
)
ON [PRIMARY]
TEXTIMAGE_ON [PRIMARY]
GO
```

___
