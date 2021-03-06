[Start](../start.md)>[Tables](./Tables.md)>dbo.DiscountApps

# ![logo](../Images/table.svg) dbo.DiscountApps

## <a name="#Description"></a>Description
> Discount applied to each order
## <a name="#Columns"></a>Columns _`11`_
|Key|Name|Data Type|Length|Precision|Scale|Not Null|Description
|---|---|---|---|---|---|---|---
| |order_id|bigint|8|19|0|True|Order ID|
| |order_date|datetime|8|23|3|True|Order Date|
| |type|nvarchar|255|0|0|False|Type of discount|
| |title|nvarchar|255|0|0|False|Title of discount|
| |description|nvarchar|255|0|0|False|Description of discount|
| |value|money|8|19|4|False|Value of discount|
| |value_type|nvarchar|255|0|0|False|Type of value|
| |allocation_method|nvarchar|255|0|0|False|Discount allocation method|
| |target_selection|nvarchar|255|0|0|False|Discount target|
| |target_type|nvarchar|255|0|0|False|Discount target type|
| |code|nvarchar|255|0|0|False|Discount code|

## <a name="#SqlScript"></a>SQL Script
```SQL
CREATE TABLE dbo.DiscountApps (
  order_id bigint NOT NULL,
  order_date datetime NOT NULL,
  type nvarchar(255) NULL,
  title nvarchar(255) NULL,
  description nvarchar(255) NULL,
  value money NULL,
  value_type nvarchar(255) NULL,
  allocation_method nvarchar(255) NULL,
  target_selection nvarchar(255) NULL,
  target_type nvarchar(255) NULL,
  code nvarchar(255) NULL
)
ON [PRIMARY]
GO

EXEC sys.sp_addextendedproperty N'MS_Description', N'Discount Applications for Each Order', 'SCHEMA', N'dbo', 'TABLE', N'DiscountApps'
GO
```

___