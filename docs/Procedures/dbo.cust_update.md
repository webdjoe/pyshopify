[Start](../start.md)>[Procedures](Procedures.md)>dbo.cust_update


# ![logo](../Images/procedure.svg) dbo.cust_update

## <a name="#Description"></a>Description
> Update Customer Orders Table
## <a name="#SqlScript"></a>SQL Script
```SQL
SET QUOTED_IDENTIFIER, ANSI_NULLS ON
GO
CREATE OR ALTER PROCEDURE dbo.cust_update 

AS
BEGIN
	SET NOCOUNT ON;

	Merge [dbo].[OrderCustomers] TARGET
	USING [dbo].[tmp_tbl] SOURCE
	ON (TARGET.[order_id] = SOURCE.[order_id])

	WHEN NOT MATCHED BY TARGET
	THEN INSERT (
	[order_id]
      ,[order_date]
      ,[email]
	  ,[customer_id]
	  ,[orders_count]
	  ,[total_spent]
	  ,[created_at]
      )
	  VALUES (
	   SOURCE.[order_id]
      ,SOURCE.[order_date]
      ,SOURCE.[email]
      ,SOURCE.[customer_id]
      ,SOURCE.[orders_count]
      ,SOURCE.[total_spent]
      ,SOURCE.[created_at]
	  );
  
	  DROP TABLE dbo.tmp_tbl
END
GO
```

___