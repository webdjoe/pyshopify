[Start](../start.md)>[Procedures](Procedures.md)>dbo.adjustments_update

# ![logo](../Images/procedure.svg) dbo.adjustments_update

## <a name="#Description"></a>Description
> Update Adjustments from tmp_tbl generated from api
## <a name="#SqlScript"></a>SQL Script
```SQL
SET QUOTED_IDENTIFIER, ANSI_NULLS ON
GO

CREATE OR ALTER PROCEDURE dbo.adjustments_update 

AS
BEGIN
	SET NOCOUNT ON;

	INSERT INTO dbo.Adjustments([id]
      ,[refund_id]
      ,[order_id]
      ,[amount]
      ,[tax_amount]
      ,[kind]
      ,[reason])
	  
	  SELECT [id]
      ,tmp.[refund_id]
      ,tmp.[order_id]
      ,tmp.[amount]
      ,tmp.[tax_amount]
      ,tmp.[kind]
      ,tmp.[reason]

	  FROM tmp_tbl tmp
	  WHERE tmp.id NOT IN (SELECT id FROM dbo.Adjustments)
	  DROP TABLE dbo.tmp_tbl
END
GO
```

___