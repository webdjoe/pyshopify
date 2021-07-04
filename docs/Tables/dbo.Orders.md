[Start](../start.md)>[Tables](./Tables.md)>dbo.Orders

# ![logo](../Images/table.svg) dbo.Orders

## <a name="#Description"></a>Description
> Order Details
## <a name="#Columns"></a>Columns _`16`_
|Key|Name|Data Type|Length|Precision|Scale|Not Null|Description
|---|---|---|---|---|---|---|---
|[![Primary Key PK_OrderID](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_OrderID](../Images/Cluster.svg)](#Indexes)|id|bigint|8|19|0|True||||False|False|Order ID|
| |order_date|datetime|8|23|3|True|Order Date|
| |number|bigint|8|19|0|True|Order Number|
| |total_price|float|8|53|0|True|Order Total Price - including shipping, taxes & discounts|
| |subtotal_price|float|8|53|0|True|Order Subtotal - including discounts, not shipping or taxes|
| |total_weight|float|8|53|0|True|Order Weight|
| |total_tax|float|8|53|0|True|Total Tax|
| |total_discounts|float|8|53|0|False|Total Order Discounts|
| |total_line_items_price|float|8|53|0|False|Total Line Item Price per Order|
| |name|nvarchar|255|0|0|True|Order Name|
| |total_price_usd|float|8|53|0|True|Order total price|
| |order_number|bigint|8|19|0|False|Order Number|
| |processing_method|nvarchar|255|0|0|False|Payment Method|
| |source_name|nvarchar|255|0|0|False|Source of Order|
| |fulfillment_status|nvarchar|255|0|0|False|Fulfillment Status|
| |payment_gateway_names|nvarchar||0|0|False|Payment Gateway|
| |email|nvarchar|255|0|0|False| Customer Email|
| |updated_at|datetime|8|23|3|False|Last order update|

## <a name="#Indexes"></a>Indexes _`1`_
|Key|Name|Columns|Unique|Type|Description
|---|---|---|---|---|---
|[![Primary Key PK_OrderID](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_OrderID](../Images/Cluster.svg)](#Indexes)|PK_OrderID|id|True||Order ID Unique Key|

## <a name="#SqlScript"></a>SQL Script
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
  CONSTRAINT PK_OrderID PRIMARY KEY CLUSTERED (id)
)
ON [PRIMARY]
TEXTIMAGE_ON [PRIMARY]
GO
```

___