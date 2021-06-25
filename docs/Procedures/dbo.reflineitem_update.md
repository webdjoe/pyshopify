[Start](../start.md)>[Procedures](Procedures.md)>dbo.reflineitem_update


# ![logo](../Images/procedure.svg) dbo.reflineitem_update

## <a name="#Description"></a>Description
> Merge Refunded Line Items with tmp_tbl generated from api call
## <a name="#SqlScript"></a>SQL Script
```SQL
SET QUOTED_IDENTIFIER, ANSI_NULLS ON
GO
-- =============================================
-- Author:	Joseph Trabulsy
-- Description:	Merge tmp_tbl with reflineitems
-- =============================================
CREATE OR ALTER PROCEDURE dbo.reflineitem_update 

AS
BEGIN
	SET NOCOUNT ON;

	INSERT INTO dbo.RefundLineItem ([id]
      ,[refund_id]
      ,[order_id]
      ,[line_item_id]
      ,[variant_id]
      ,[quantity]
      ,[subtotal]
      ,[total_tax])
	  
	  SELECT tmp.[id]
      ,tmp.[refund_id]
      ,tmp.[order_id]
      ,tmp.[line_item_id]
      ,tmp.[variant_id]
      ,tmp.[quantity]
      ,tmp.[subtotal]
      ,tmp.[total_tax]

	  FROM tmp_tbl tmp
	  WHERE tmp.id NOT IN (SELECT id FROM dbo.RefundLineItem)
	  DROP TABLE dbo.tmp_tbl
END
GO
```

___