[Start](../start.md)>[Tables](./Tables.md)>dbo.LineItems

# ![logo](../Images/table.svg) dbo.LineItems

## <a name="#Description"></a>Description
> Line Items with Units Sold for Orders
## <a name="#Columns"></a>Columns _`6`_
|Key|Name|Data Type|Length|Precision|Scale|Not Null|Identity|Rule|Default|Computed|Persisted|Description
|---|---|---|---|---|---|---|---|---|---|---|---|---
|[![Primary Key PK_line_item_id](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_line_item_id](../Images/Cluster.svg)](#Indexes)|id|bigint|8|19|0|True||||False|False|Line Item ID|
||order_id|bigint|8|19|0|True||||False|False|Order ID|
||order_date|datetime|8|23|3|True||||False|False|Order Created Date|
||variant_id|bigint|8|19|0|True||||False|False|Unit variant ID|
||quantity|int|4|10|0|True||||False|False|Line Item Quantity|
||price|float|8|53|0|True||||False|False|Line Item Unit Price|

## <a name="#Indexes"></a>Indexes _`1`_
|Key|Name|Columns|Unique|Type|Description
|---|---|---|---|---|---
|[![Primary Key PK_line_item_id](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_line_item_id](../Images/Cluster.svg)](#Indexes)|PK_line_item_id|id|True||Line Item Primary Key|

## <a name="#SqlScript"></a>SQL Script
```SQL
CREATE TABLE dbo.LineItems (
  id bigint NOT NULL,
  order_id bigint NOT NULL,
  order_date datetime NOT NULL,
  variant_id bigint NOT NULL,
  quantity int NOT NULL,
  price float NOT NULL,
  CONSTRAINT PK_line_item_id PRIMARY KEY CLUSTERED (id)
)
ON [PRIMARY]
GO
```

___