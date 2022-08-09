# ![logo](../Images/table.svg) dbo.Orders

[Start](../start.md)>dbo.Orders

## [](#Description) Description

> Order Details

## [](#Columns) Columns _`21`_

| Key                                                                                                                         | Name                   | Data Type | Length | Precision | Scale | Not Null | Description                                                 |
|-----------------------------------------------------------------------------------------------------------------------------|------------------------|-----------|--------|-----------|-------|----------|-------------------------------------------------------------|
| [![Primary Key PK_OrderID](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_OrderID](../Images/Cluster.svg)](#Indexes) | id                     | bigint    | 8      | 19        | 0     | True     | Order ID                                                    |
|                                                                                                                             | order_date             | datetime  | 8      | 23        | 3     | True     | Order Date                                                  |
|                                                                                                                             | number                 | bigint    | 8      | 19        | 0     | True     | Order Number                                                |
|                                                                                                                             | total_price            | float     | 8      | 53        | 0     | True     | Order Total Price - including shipping, taxes & discounts   |
|                                                                                                                             | subtotal_price         | float     | 8      | 53        | 0     | True     | Order Subtotal - including discounts, not shipping or taxes |
|                                                                                                                             | total_weight           | float     | 8      | 53        | 0     | True     | Order weight                                                |
|                                                                                                                             | total_tax              | float     | 8      | 53        | 0     | True     | Total Tax on Order                                          |
|                                                                                                                             | total_discounts        | float     | 8      | 53        | 0     | False    | Total Discounts applied                                     |
|                                                                                                                             | total_line_items_price | float     | 8      | 53        | 0     | False    | Total price of line item                                    |
|                                                                                                                             | name                   | nvarchar  | 255    | 0         | 0     | True     | Order name                                                  |
|                                                                                                                             | total_price_usd        | float     | 8      | 53        | 0     | True     | Order Total Price - including shipping, taxes & discounts   |
|                                                                                                                             | order_number           | bigint    | 8      | 19        | 0     | False    | Order Name without prefix                                   |
|                                                                                                                             | processing_method      | nvarchar  | 255    | 0         | 0     | False    | Payment method                                              |
|                                                                                                                             | source_name            | nvarchar  | 255    | 0         | 0     | False    | Source of sale                                              |
|                                                                                                                             | fulfillment_status     | nvarchar  | 255    | 0         | 0     | False    | Fulfillment status                                          |
|                                                                                                                             | payment_gateway_names  | nvarchar  |        | 0         | 0     | False    | Payment methods in comma separated string                   |
|                                                                                                                             | email                  | nvarchar  | 255    | 0         | 0     | False    | Email of customer                                           |
|                                                                                                                             | updated_at             | datetime  | 8      | 23        | 3     | False    | Order updated date                                          |
|                                                                                                                             | financial_status       | nvarchar  | 255    | 0         | 0     | False    | Financial status of order                                   |
|                                                                                                                             | customer_id            | bigint    | 8      | 19        | 0     | False    | Customer ID of order                                        |
|                                                                                                                             | tags                   | nvarchar  |        | 0         | 0     | False    | Tags in comma separated string                              |

## [](#Indexes) Indexes _`1`_

|Key|Name|Columns|Unique|Type|Description
|---|---|---|---|---|---
|[![Primary Key PK_OrderID](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_OrderID](../Images/Cluster.svg)](#Indexes)|PK_OrderID|id|True||Order ID Unique Key|

## [](#SqlScript) SQL Script

```SQL
CREATE TABLE dbo.Orders (
  id bigint NOT NULL,
  order_date datetime NOT NULL,
  number bigint NOT NULL,
  total_price float NOT NULL,
  subtotal_price float NOT NULL,
  total_weight float NOT NULL,
  total_tax float NOT NULL,
  total_discounts float NULL,
  total_line_items_price float NULL,
  name nvarchar(255) NOT NULL,
  total_price_usd float NOT NULL,
  order_number bigint NULL,
  processing_method nvarchar(255) NULL,
  source_name nvarchar(255) NULL,
  fulfillment_status nvarchar(255) NULL,
  payment_gateway_names nvarchar(max) NULL,
  email nvarchar(255) NULL,
  updated_at datetime NULL,
  financial_status nvarchar(255) NULL,
  customer_id bigint NULL,
  tags nvarchar(max) NULL,
  CONSTRAINT PK_OrderID PRIMARY KEY CLUSTERED (id)
)
ON [PRIMARY]
TEXTIMAGE_ON [PRIMARY]
GO
```

___
