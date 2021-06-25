
# ![logo](Images/folder.svg) Shopify Orders DB Documentation

## <a name="#Description"></a>Documentation for storing Shopify order data in relational SQL Server database
>

### ![Table](Images/table.svg) [Tables](Tables/Tables.md)    

|Name|Description
|---|---
|[dbo.Adjustments](Tables/dbo.Adjustments.md)|Order Refund Adjustments|
|[dbo.DateDimension](Tables/dbo.DateDimension.md)|Date Dimension Table for Analysis|
|[dbo.LineItems](Tables/dbo.LineItems.md)|Line Items with Units Sold for Orders|
|[dbo.OrderCustomers](Tables/dbo.OrderCustomers.md)|Customer Info based on Order ID|
|[dbo.Orders](Tables/dbo.Orders.md)|Order Details|
|[dbo.RefundLineItem](Tables/dbo.RefundLineItem.md)|Refunded Units|
|[dbo.Refunds](Tables/dbo.Refunds.md)|Order Refunds |

### ![Procedure](Images/procedure.svg) [Stored Procedures](Procedures/Procedures.md)

|Name|Description
|---|---
|[dbo.adjustments_update](Procedures/dbo.adjustments_update.md)|Update Adjustments|
|[dbo.cust_update](Procedures/dbo.cust_update.md)|Update Customer Orders Table|
|[dbo.lineitems_update](Procedures/dbo.lineitems_update.md)|Update Line Items|
|[dbo.orders_update](Procedures/dbo.orders_update.md)|Merge Orders|
|[dbo.reflineitem_update](Procedures/dbo.reflineitem_update.md)|Merge Refunded Line Items|
|[dbo.refunds_update](Procedures/dbo.refunds_update.md)|Merge Refunds


