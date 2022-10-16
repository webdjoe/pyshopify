# ![logo](../Images/table.svg) products

[Start](../start.md)>products

## [](#Description) Description

> Product listing data

## [](#Columns) Columns

|Key|Name|Data Type|Length|Precision|Scale|Not Null|Description
|---|---|---|---|---|---|---|---
|[![Primary Key PK_products](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_products](../Images/Cluster.svg)](#Indexes)|id|bigint|8|19|0|True|Product ID|
||title|nvarchar|255|0|0|False|Product title|
||body_html|nvarchar||0|0|False|HTML of product description|
||vendor|nvarchar|255|0|0|False|Product vendor name|
||product_type|nvarchar|255|0|0|False|Product type|
||created_at|datetime|8|23|3|True|Datetime product created|
||handle|nvarchar|255|0|0|False|Handle for product URL|
||updated_at|datetime|8|23|3|True|Datetime product last updated|
||published_at|datetime|8|23|3|False|Datetime product was published live|
||template_suffix|nvarchar|255|0|0|False|template suffix of product web page|
||status|nvarchar|255|0|0|False|Status of product|
||published_scope|nvarchar|255|0|0|False|Product channel availability|
||tags|nvarchar||0|0|False|Product tags|
||admin_graphql_api_id|nvarchar|255|0|0|False|Graphql api ID|
||image_src|nvarchar|255|0|0|False|URL of product image|

## [](#Indexes) Indexes

|Key|Name|Columns|Unique|
|---|---|---|---|
|[![Primary Key PK_products](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_products](../Images/cluster.svg)](#Indexes)|PK_products_id|id|True|

___
