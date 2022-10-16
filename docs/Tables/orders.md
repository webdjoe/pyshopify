# ![logo](../Images/table.svg) orders

[Start](../start.md)>orders

## [](#Description) Description

> Order Details

## [](#Columns) Columns _`16`_

| Key                                                                                                                         | Name                   | Data Type | Length | Precision | Scale | Not Null | Description                                                 |
|-----------------------------------------------------------------------------------------------------------------------------|------------------------|-----------|--------|-----------|-------|----------|-------------------------------------------------------------|
|[![Primary Key PK_OrderID](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_OrderID](../Images/Cluster.svg)](#Indexes)|id|bigint|8|19|0|True|Order ID|
||created_at|datetime|8|23|3|True|Datetime order was created|
||updated_at|datetime|8|23|3|True|Datetime order was updated|
|[![Indexes IDX_Orders_processed_at](../Images/index.svg)](#Indexes)|processed_at|datetime|8|23|3|True|Datetime order was processed - used for analytics|
||number|bigint|8|19|0|True|Numeric order number|
||total_weight|float|8|53|0|True|Total weight of items ordered|
||name|nvarchar|50|0|0|True|Order number and prefix|
||order_number|bigint|8|19|0|True|Padded number of order|
||processing_method|nvarchar|255|0|0|False|Charge processing method|
||source_name|nvarchar|50|0|0|False|The method which the order was placed|
||fulfillment_status|nvarchar|50|0|0|False|Tracking status of order|
||payment_gateway_names|nvarchar|255|0|0|False|Payment processing method|
||email|nvarchar|255|0|0|False|Email address of customer that placed order|
||financial_status|nvarchar|50|0|0|False|The status of the payment|
|[![Indexes IDX_Orders_customer_id](../Images/index.svg)](#Indexes)|customer_id|bigint|8|19|0|False|ID of customer that placed order|
||tags|nvarchar||0|0|False|Tags applied to the order|

## [](#Indexes) Indexes _`1`_

|Key|Name|Columns|Unique|
|:---:|---|---|---|
||IDX_Orders_customer_id|customer_id|False|
||IDX_Orders_processed_at|processed_at|False|
|[![Primary Key PK_OrderID](../Images/primarykey.svg)](#Indexes)[![Cluster Key PK_OrderID](../Images/Cluster.svg)](#Indexes)|PK_OrderID|id|True|

___
