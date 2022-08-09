# ![logo](../Images/table.svg) dbo.Customers

[Start](../start.md)>[Tables](./Tables.md)>dbo.Customers

## [](#Description) Description

> Customer Details

## [](#Columns) Columns

|Key|Name|Data Type|Length|Precision|Scale|Not Null|Description
|---|---|---|---|---|---|---|---
|[![Primary Key PK_customers_id](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_customers_id](../Images/Cluster.svg)](#Indexes)|id|bigint|8|19|0|True|Customer ID|
| |created_at|datetime|8|23|3|True|Customer created date|
| |updated_at|datetime|8|23|3|True|Customer last updated date|
| |email|nvarchar|255|0|0|False|Customer Email|
| |last_order_id|bigint|8|19|0|False|ID of last order placed|
| |orders_count|int|4|10|0|True|Customers Orders Count at updated date|
| |total_spent|money|8|19|4|True|Total Spent by Customer up to updated date|
| |tags|nvarchar|max|0|0|False|Customer tags|
| |city|nvarchar|255|0|0|False|Customer default city|
| |province|nvarchar|255|0|0|False|Customer default state/province|
| |zip|nvarchar|255|0|0|False|Customer default zip code|
| |country|nvarchar|255|0|0|False|Customer default country|

## [](#Indexes) Indexes

|Key|Name|Columns|Unique|Type|Description
|---|---|---|---|---|---
|[![Primary Key PK_ordercustid](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_ordercustid](../Images/Cluster.svg)](#Indexes)|PK_customers_id|id|True||Order ID unique PK|

## [](#SqlScript) SQL Script

```SQL
CREATE TABLE shop_rest.dbo.Customers (
  id BIGINT NOT NULL
 ,updated_at DATETIME NOT NULL
 ,created_at DATETIME NOT NULL
 ,email NVARCHAR(255) NULL
 ,last_order_id BIGINT NULL
 ,orders_count INT NOT NULL
 ,total_spent MONEY NOT NULL
 ,tags NVARCHAR(MAX) NULL
 ,city NVARCHAR(255) NULL
 ,province NVARCHAR(255) NULL
 ,country NVARCHAR(255) NULL
 ,zip NVARCHAR(255) NULL
 ,CONSTRAINT PK_Customers_id PRIMARY KEY CLUSTERED (id)
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
```

___
