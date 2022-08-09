# ![logo](../Images/table.svg) dbo.DiscountCodes

[Start](../start.md)>[Tables](./Tables.md)>dbo.DiscountCodes

## [](#Description) Description

> Discount Codes In Use for Each Order

## [](#Columns) Columns _`5`_

|Key|Name|Data Type|Length|Precision|Scale|Not Null|Description
|---|---|---|---|---|---|---|---
| |order_id|bigint|8|19|0|True|Order ID|
| |order_date|datetime|8|23|3|True|Order Date|
| |code|nvarchar|255|0|0|True|Discount Code|
| |amount|money|8|19|4|True|Amount of discount|
| |type|nvarchar|255|0|0|True|Type of discount|

## [](#SqlScript) SQL Script

```SQL
CREATE TABLE dbo.DiscountCodes (
  order_id bigint NOT NULL,
  order_date datetime NOT NULL,
  code nvarchar(255) NOT NULL,
  amount money NOT NULL,
  type nvarchar(255) NOT NULL
)
ON [PRIMARY]
GO
```

___
