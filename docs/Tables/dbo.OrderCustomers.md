[Start](../start.md)>[Tables](./Tables.md)>dbo.OrderCustomers

# ![logo](../Images/table.svg) dbo.OrderCustomers

## <a name="#Description"></a>Description
> Customer Info based on Order ID
## <a name="#Columns"></a>Columns
|Key|Name|Data Type|Length|Precision|Scale|Not Null|Identity|Rule|Default|Computed|Persisted|Description
|---|---|---|---|---|---|---|---|---|---|---|---|---
|[![Primary Key PK_ordercustid](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_ordercustid](../Images/Cluster.svg)](#Indexes)|order_id|bigint|8|19|0|True||||False|False|Order ID|
||order_date|datetime|8|23|3|False||||False|False|Order Date|
||email|nvarchar|255|0|0|False||||False|False|Customer Email|
||customer_id|bigint|8|19|0|True||||False|False|Customer ID|
||orders_count|int|4|10|0|True||||False|False|Customers Orders Count at Current Order|
||total_spent|money|8|19|4|True||||False|False|Total Spent by Customer up to Current Order|
||created_at|datetime|8|23|3|True||||False|False|Customer created date|

## <a name="#Indexes"></a>Indexes
|Key|Name|Columns|Unique|Type|Description
|---|---|---|---|---|---
|[![Primary Key PK_ordercustid](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_ordercustid](../Images/Cluster.svg)](#Indexes)|PK_ordercustid|order_id|True||Order ID unique PK|

## <a name="#SqlScript"></a>SQL Script
```SQL
CREATE TABLE dbo.OrderCustomers (
  order_id bigint NOT NULL,
  order_date datetime NULL,
  email nvarchar(255) NULL,
  customer_id bigint NOT NULL,
  orders_count int NOT NULL,
  total_spent money NOT NULL,
  created_at datetime NOT NULL,
  CONSTRAINT PK_ordercustid PRIMARY KEY CLUSTERED (order_id)
)
ON [PRIMARY]
GO
```

___

