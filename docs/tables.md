# ![logo](Images/folder.svg) Shopify Orders DB Documentation

## ![Table](Images/table.svg) **[Customers Table](Tables/Tables.md)**

| Name                                               | Description                                     |
|----------------------------------------------------|-------------------------------------------------|
| [dbo.Customers](Tables/dbo.Customers.md)           | Customer details                                |

## ![Table](Images/table.svg) **[Products & Inventory Tables](Tables/Tables.md)**

| Name                                               | Description                                     |
|----------------------------------------------------|-------------------------------------------------|
| [dbo.Products](Tables/dbo.Products.md)           | Product & Listing Data                                |
| [dbo.Variants](Tables/dbo.Variants.md)           | Product Variant details & Inventory                                |
| [dbo.ProductOptions](Tables/dbo.ProductOptions.md)           | Product & variant options configurations                          |

## ![Table](Images/table.svg) [Orders Tables](Tables/Tables.md)

| Name                                               | Description                                     |
|----------------------------------------------------|-------------------------------------------------|
| [dbo.Orders](Tables/dbo.Orders.md)                 | Order Details                                   |
| [dbo.OrderAttr](Tables/dbo.OrderAttr.md)           | Order source, campaign & attribution details    |
| [dbo.Adjustments](Tables/dbo.Adjustments.md)       | Order Refund Adjustments                        |
| [dbo.DateDimension](Tables/dbo.DateDimension.md)   | Date Dimension Table for Analysis               |
| [dbo.DiscountApps](Tables/dbo.DiscountApps.md)     | Discount Applications for Each Order            |
| [dbo.DiscountCodes](Tables/dbo.DiscountCodes.md)   | Discount Codes In Use for Each Order            |
| [dbo.LineItems](Tables/dbo.LineItems.md)           | Line Items with Units Sold for Orders           |
| [dbo.RefundLineItem](Tables/dbo.RefundLineItem.md) | Refunded Units                                  |
| [dbo.Refunds](Tables/dbo.Refunds.md)               | Order Refunds                                   |
| [dbo.ShipLines](Tables/dbo.ShipLines.md)           | Order shipping lines pricings method & discount |
