[Start](../start.md)>[Tables](./Tables.md)>dbo.Adjustments

# ![logo](../Images/table.svg) dbo.Adjustments

## <a name="#Description"></a>Description
> Order Adjustments
## <a name="#Columns"></a>Columns
|Key|Name|Data Type|Length|Precision|Scale|Not Null|Identity|Rule|Default|Computed|Persisted|Description
|---|---|---|---|---|---|---|---|---|---|---|---|---
|[![Primary Key PK_adj_id](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_adj_id](../Images/Cluster.svg)](#Indexes)|id|bigint|8|19|0|True||||False|False|Adjustment ID|
||refund_id|bigint|8|19|0|True||||False|False|Refund ID|
||order_id|bigint|8|19|0|True||||False|False|Order ID|
||amount|float|8|53|0|True||||False|False|Adjustment Amount|
||tax_amount|float|8|53|0|True||||False|False|Adjusted Tax Amount|
||kind|nvarchar|255|0|0|False||||False|False|Kind of Adjustment|
||reason|nvarchar|255|0|0|False||||False|False|Reason for Adjustment|

## <a name="#Indexes"></a>Indexes
|Key|Name|Columns|Unique|Type|Description
|---|---|---|---|---|---
|[![Primary Key PK_adj_id](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_adj_id](../Images/Cluster.svg)](#Indexes)|PK_adj_id|id|True||Adjustment ID PK|

## <a name="#SqlScript"></a>SQL Script
```SQL
CREATE TABLE dbo.Adjustments (
  id bigint NOT NULL,
  refund_id bigint NOT NULL,
  order_id bigint NOT NULL,
  amount float NOT NULL,
  tax_amount float NOT NULL,
  kind nvarchar(255) NULL,
  reason nvarchar(255) NULL,
  CONSTRAINT PK_adj_id PRIMARY KEY CLUSTERED (id)
)
ON [PRIMARY]
GO
```

___
