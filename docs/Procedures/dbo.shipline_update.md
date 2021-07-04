[Start](../start.md)>[Procedures](Procedures.md)>dbo.shipline_update

# ![logo](../Images/procedure.svg) dbo.shipline_update

## <a name="#Description"></a>Description
> Merge shipping lines table with return
## <a name="#SqlScript"></a>SQL Script

```SQL
SET QUOTED_IDENTIFIER, ANSI_NULLS ON
GO

CREATE OR ALTER PROCEDURE dbo.shipline_update 

AS
BEGIN
	SET NOCOUNT ON;
	Merge [dbo].[ShipLines] TARGET
	USING [dbo].[tmp_tbl] SOURCE
	ON (TARGET.[id] = SOURCE.[id])

	WHEN NOT MATCHED BY TARGET
	THEN INSERT (

	
	   [id]
      ,[carrier_identifier]
      ,[code]
      ,[delivery_category]
      ,[ship_discount_price]
      ,[ship_price]
      ,[phone]
      ,[requested_fulfillment_id]
      ,[source]
      ,[title]
      ,[order_id]
      ,[order_date])
	  
	  VALUES ( SOURCE.[id]
,SOURCE.[carrier_identifier]
,SOURCE.[code]
,SOURCE.[delivery_category]
,SOURCE.[ship_discount_price]
,SOURCE.[ship_price]
,SOURCE.[phone]
,SOURCE.[requested_fulfillment_id]
,SOURCE.[source]
,SOURCE.[title]
,SOURCE.[order_id]
,SOURCE.[order_date]);

	  


	  
	  DROP TABLE dbo.tmp_tbl
END
GO
```

___