[Start](../start.md)>[Tables](./Tables.md)>dbo.Refunds

# ![logo](../Images/table.svg) dbo.Refunds

## <a name="#Description"></a>Description
> Order Refunds 
## <a name="#Columns"></a>Columns _`3`_
|Key|Name|Data Type|Length|Precision|Scale|Not Null|Identity|Rule|Default|Computed|Persisted|Description
|---|---|---|---|---|---|---|---|---|---|---|---|---
|[![Primary Key PK_refund_id](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_refund_id](../Images/Cluster.svg)](#Indexes)|id|bigint|8|19|0|True||||False|False|Refund ID|
||refund_date|datetime|8|23|3|True||||False|False|Refund Date|
||order_id|bigint|8|19|0|True||||False|False|Order ID|

## <a name="#Indexes"></a>Indexes _`1`_
|Key|Name|Columns|Unique|Type|Description
|---|---|---|---|---|---
|[![Primary Key PK_refund_id](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_refund_id](../Images/Cluster.svg)](#Indexes)|PK_refund_id|id|True||Refund ID Unique PK|

## <a name="#SqlScript"></a>SQL Script
```SQL
CREATE TABLE dbo.Refunds (
  id bigint NOT NULL,
  refund_date datetime NOT NULL,
  order_id bigint NOT NULL,
  CONSTRAINT PK_refund_id PRIMARY KEY CLUSTERED (id)
)
ON [PRIMARY]
GO
```

___