# ![logo](Images/folder.svg) Shopify Orders DB Documentation

## ![Table](Images/table.svg) **[Customers Table](Tables/Tables.md)**

| Name                                               | Description                                     |
|----------------------------------------------------|-------------------------------------------------|
| [customers](Tables/customers.md)           | Customer details                                |

## ![Table](Images/table.svg) **[Products & Inventory Tables](Tables/Tables.md)**

| Name                                               | Description                                     |
|----------------------------------------------------|-------------------------------------------------|
| [products](Tables/products.md)           | Product & Listing Data                                |
| [variants](Tables/variants.md)           | Product Variant details & Inventory                                |
| [product_options](Tables/product_options.md)           | Product & variant options configurations                          |
|[inventory_levels](Tables/inventory_levels.md)|Inventory Levels for items at each inventory location|
|[inventory_locations](Tables/inventory_locations.md)|Inventory locations |

## ![Table](Images/table.svg) [Orders Tables](Tables/Tables.md)

| Name                                               | Description                                     |
|----------------------------------------------------|-------------------------------------------------|
| [orders](Tables/orders.md)                 | Order Details                                   |
| [order_attr](Tables/order_attr.md)           | Order source, campaign & attribution details    |
|[order_prices](Tables/order_prices.md)|Amounts charged for order|
| [adjustments](Tables/adjustments.md)       | Adjustments on order for refunding shipping and refund discrepancies                       |
| [date_dimension](Tables/date_dimension.md)   | Date Dimension Table for Analysis               |
| [discount_apps](Tables/discount_apps.md)     | Discount Applications for Each Order            |
| [discount_codes](Tables/discount_codes.md)   | Discount Codes In Use for Each Order            |
| [line_items](Tables/line_items.md)           | Line Items with Units Sold for Orders           |
| [refund_line_item](Tables/refund_line_item.md) | Refunded Units                                  |
| [refunds](Tables/refunds.md)               | Order Refunds                                   |
| [ship_lines](Tables/ship_lines.md)           | Order shipping lines pricings method & discount |
