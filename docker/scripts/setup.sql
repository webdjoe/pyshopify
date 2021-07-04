USE master
GO

IF DB_NAME() <> N'master' SET NOEXEC ON

CREATE DATABASE shop_rest
GO

ALTER DATABASE shop_rest
  SET
    ANSI_NULL_DEFAULT OFF,
    ANSI_NULLS OFF,
    ANSI_PADDING OFF,
    ANSI_WARNINGS OFF,
    ARITHABORT OFF,
    AUTO_CLOSE OFF,
    AUTO_CREATE_STATISTICS ON,
    AUTO_SHRINK OFF,
    AUTO_UPDATE_STATISTICS ON,
    AUTO_UPDATE_STATISTICS_ASYNC OFF,
    COMPATIBILITY_LEVEL = 150,
    CONCAT_NULL_YIELDS_NULL OFF,
    CURSOR_CLOSE_ON_COMMIT OFF,
    CURSOR_DEFAULT GLOBAL,
    DATE_CORRELATION_OPTIMIZATION OFF,
    DB_CHAINING OFF,
    HONOR_BROKER_PRIORITY OFF,
    MULTI_USER,
    NESTED_TRIGGERS = ON,
    NUMERIC_ROUNDABORT OFF,
    PAGE_VERIFY CHECKSUM,
    PARAMETERIZATION SIMPLE,
    QUOTED_IDENTIFIER OFF,
    READ_COMMITTED_SNAPSHOT OFF,
    RECOVERY FULL,
    RECURSIVE_TRIGGERS OFF,
    TRANSFORM_NOISE_WORDS = OFF,
    TRUSTWORTHY OFF
    WITH ROLLBACK IMMEDIATE
GO

ALTER DATABASE shop_rest
  SET DISABLE_BROKER
GO



ALTER DATABASE shop_rest
  SET QUERY_STORE = OFF
GO

USE shop_rest
GO

IF DB_NAME() <> N'shop_rest' SET NOEXEC ON
GO

CREATE TABLE dbo.Orders (
  id bigint NOT NULL,
  order_date datetime NOT NULL,
  number bigint NOT NULL,
  total_price float NOT NULL,
  subtotal_price float NOT NULL,
  total_weight float NOT NULL,
  total_tax float NOT NULL,
  total_discounts float NULL,
  total_line_items_price float NULL,
  name nvarchar(255) NOT NULL,
  total_price_usd float NOT NULL,
  order_number bigint NULL,
  processing_method nvarchar(255) NULL,
  source_name nvarchar(255) NULL,
  fulfillment_status nvarchar(255) NULL,
  payment_gateway_names nvarchar(max) NULL,
  email nvarchar(255) NULL,
  updated_at datetime NULL,
  CONSTRAINT PK_OrderID PRIMARY KEY CLUSTERED (id)
)
ON [PRIMARY]
TEXTIMAGE_ON [PRIMARY]
GO

SET QUOTED_IDENTIFIER, ANSI_NULLS ON
GO

CREATE OR ALTER PROCEDURE dbo.orders_update

AS
BEGIN
	SET NOCOUNT ON;
	Merge [dbo].[Orders] TARGET
	USING [dbo].[tmp_tbl] SOURCE
	ON (TARGET.[id] = SOURCE.[id])


	WHEN MATCHED AND (SOURCE.updated_at <> TARGET.updated_at)
	THEN UPDATE SET
	TARGET.total_price = SOURCE.total_price,
	TARGET.total_tax = SOURCE.total_tax,
	TARGET.total_discounts = SOURCE.total_discounts,
	TARGET.total_line_items_price = SOURCE.total_line_items_price,
	TARGET.name = SOURCE.name,
	TARGET.total_price_usd = SOURCE.total_price_usd,
	TARGET.updated_at = SOURCE.updated_at,
	TARGET.fulfillment_status = SOURCE.fulfillment_status


	WHEN NOT MATCHED BY TARGET
	THEN INSERT (
	   id
	  ,order_date
      ,number
      ,total_price
      ,subtotal_price
      ,total_weight
      ,total_tax
      ,total_discounts
      ,total_line_items_price
      ,[name]
      ,total_price_usd
      ,order_number
      ,processing_method
      ,source_name
      ,fulfillment_status
      ,payment_gateway_names
	  ,email
	  ,updated_at)

	  VALUES ( SOURCE.id
      ,SOURCE.order_date
      ,SOURCE.number
      ,SOURCE.total_price
      ,SOURCE.subtotal_price
      ,SOURCE.total_weight
      ,SOURCE.total_tax
      ,SOURCE.total_discounts
      ,SOURCE.total_line_items_price
      ,SOURCE.[name]
      ,SOURCE.total_price_usd
      ,SOURCE.order_number
      ,SOURCE.processing_method
      ,SOURCE.source_name
      ,SOURCE.fulfillment_status
      ,SOURCE.payment_gateway_names
	  ,SOURCE.email
	  ,SOURCE.updated_at);





	  DROP TABLE dbo.tmp_tbl
END
GO

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

CREATE TABLE dbo.LineItems (
  id bigint NOT NULL,
  order_id bigint NOT NULL,
  order_date datetime NOT NULL,
  variant_id bigint NOT NULL,
  quantity int NOT NULL,
  price float NOT NULL,
  name nvarchar(255) NULL,
  product_id bigint NULL,
  sku nvarchar(255) NULL,
  title nvarchar(255) NULL,
  total_discount money NULL,
  variant_title nvarchar(255) NULL,
  CONSTRAINT PK_line_item_id PRIMARY KEY CLUSTERED (id)
)
ON [PRIMARY]
GO

CREATE OR ALTER PROCEDURE dbo.lineitems_update

AS
BEGIN
	SET NOCOUNT ON;

	INSERT INTO dbo.LineItems([id]
      ,[order_id]
      ,[order_date]
      ,[variant_id]
      ,[quantity]
      ,[price]
	  ,[name]
      ,[product_id]
      ,[sku]
      ,[title]
      ,[total_discount]
      ,[variant_title])

	  SELECT [id]
      ,tmp.[order_id]
      ,tmp.[order_date]
      ,tmp.[variant_id]
      ,tmp.[quantity]
      ,tmp.[price]
	  ,tmp.[name]
      ,tmp.[product_id]
      ,tmp.[sku]
      ,tmp.[title]
      ,tmp.[total_discount]
      ,tmp.[variant_title]

	  FROM tmp_tbl tmp
	  WHERE tmp.id NOT IN (SELECT id FROM dbo.LineItems)
	  DROP TABLE dbo.tmp_tbl
END
GO

CREATE TABLE dbo.DiscountCodes (
  order_id bigint NOT NULL,
  order_date datetime NOT NULL,
  code nvarchar(255) NOT NULL,
  amount money NOT NULL,
  type nvarchar(255) NOT NULL
)
ON [PRIMARY]
GO

CREATE OR ALTER PROCEDURE dbo.disccode_update

AS
BEGIN

	SET NOCOUNT ON;


	Merge [dbo].[DiscountCodes] TARGET
	USING [dbo].[tmp_tbl] SOURCE
	ON (TARGET.[order_id] = SOURCE.[order_id] AND TARGET.[code] = SOURCE.[code] AND TARGET.[amount] = SOURCE.[amount] AND TARGET.[type] = SOURCE.[type])

	WHEN NOT MATCHED BY TARGET
	THEN INSERT (
	   [order_id]
      ,[order_date]
      ,[code]
	  ,[amount]
	  ,[type]
      )
	  VALUES (
	   SOURCE.[order_id]
      ,SOURCE.[order_date]
      ,SOURCE.[code]
	  ,SOURCE.[amount]
	  ,SOURCE.[type]);

	  DROP TABLE dbo.tmp_tbl
END
GO

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


CREATE OR ALTER PROCEDURE dbo.discapp_update

AS
BEGIN

	SET NOCOUNT ON;


	Merge [dbo].[DiscountApps] TARGET
	USING [dbo].[tmp_tbl] SOURCE
	ON (TARGET.[order_id] = SOURCE.[order_id] AND TARGET.[title] = SOURCE.[title] AND TARGET.[value] = SOURCE.[value] AND TARGET.[value_type] = SOURCE.[value_type] AND TARGET.[allocation_method] = SOURCE.[allocation_method]
	AND SOURCE.[target_selection] = TARGET.[target_selection] AND SOURCE.[target_type] = TARGET.[target_type] AND SOURCE.[code] = TARGET.[code])

	WHEN NOT MATCHED BY TARGET
	THEN INSERT (
	   [order_id]
      ,[order_date]
      ,[type]
	  ,[title]
	  ,[description]
	  ,[value]
	  ,[value_type]
	  ,[allocation_method]
	  ,[target_selection]
	  ,[target_type]
	  ,[code]
      )
	  VALUES (
	   SOURCE.[order_id]
      ,SOURCE.[order_date]
      ,SOURCE.[type]
	  ,SOURCE.[title]
	  ,SOURCE.[description]
	  ,SOURCE.[value]
	  ,SOURCE.[value_type]
	  ,SOURCE.[allocation_method]
	  ,SOURCE.[target_selection]
	  ,SOURCE.[target_type]
	  ,SOURCE.[code]
	  );

	  DROP TABLE dbo.tmp_tbl
END
GO

CREATE TABLE dbo.Adjustments (
  id bigint NOT NULL,
  refund_id bigint NOT NULL,
  order_id bigint NOT NULL,
  amount float NOT NULL,
  tax_amount float NOT NULL,
  kind nvarchar(255) NULL,
  reason nvarchar(255) NULL,
  CONSTRAINT PK_adj_id PRIMARY KEY CLUSTERED (id)
)
ON [PRIMARY]
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

CREATE TABLE dbo.Refunds (
  id bigint NOT NULL,
  refund_date datetime NOT NULL,
  order_id bigint NOT NULL,
  CONSTRAINT PK_refund_id PRIMARY KEY CLUSTERED (id)
)
ON [PRIMARY]
GO


CREATE OR ALTER PROCEDURE dbo.refunds_update

AS
BEGIN

	SET NOCOUNT ON;

	INSERT INTO dbo.Refunds 	(
	   id, refund_date, order_id)

	  SELECT tmp.id, tmp.refund_date, tmp.order_id

	  FROM tmp_tbl tmp
	  WHERE tmp.id NOT IN (SELECT id FROM dbo.Refunds)
	  DROP TABLE dbo.tmp_tbl
END
GO

CREATE TABLE dbo.RefundLineItem (
  id bigint NOT NULL,
  refund_id bigint NOT NULL,
  order_id bigint NOT NULL,
  line_item_id bigint NOT NULL,
  variant_id bigint NOT NULL,
  quantity int NOT NULL,
  subtotal float NOT NULL,
  total_tax float NOT NULL,
  CONSTRAINT PK_refundlineitem_id PRIMARY KEY CLUSTERED (id)
)
ON [PRIMARY]
GO

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

CREATE TABLE [dbo].[ShipLines](
	[id] [bigint] NOT NULL,
	[carrier_identifier] [nvarchar](255) NULL,
	[code] [nvarchar](255) NULL,
	[delivery_category] [nvarchar](255) NULL,
	[ship_discount_price] [money] NULL,
	[ship_price] [money] NULL,
	[phone] [nvarchar](255) NULL,
	[requested_fulfillment_id] [nvarchar](255) NULL,
	[source] [nvarchar](255) NULL,
	[title] [nvarchar](255) NULL,
	[order_id] [bigint] NULL,
	[order_date] [datetime] NULL,
 CONSTRAINT [PK_ShipLines] PRIMARY KEY CLUSTERED
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

CREATE OR ALTER PROCEDURE [dbo].[shipline_update]

AS
BEGIN

    SET NOCOUNT ON;
    Merge [dbo].[ShipLines] TARGET
    USING [dbo].[tmp_tbl] SOURCE
    ON (TARGET.[id] = SOURCE.[id])

    WHEN NOT MATCHED BY TARGET
        THEN
        INSERT (
            -- Insert statements for procedure here

                 [id]
               , [carrier_identifier]
               , [code]
               , [delivery_category]
               , [ship_discount_price]
               , [ship_price]
               , [phone]
               , [requested_fulfillment_id]
               , [source]
               , [title]
               , [order_id]
               , [order_date])

        VALUES ( SOURCE.[id]
               , SOURCE.[carrier_identifier]
               , SOURCE.[code]
               , SOURCE.[delivery_category]
               , SOURCE.[ship_discount_price]
               , SOURCE.[ship_price]
               , SOURCE.[phone]
               , SOURCE.[requested_fulfillment_id]
               , SOURCE.[source]
               , SOURCE.[title]
               , SOURCE.[order_id]
               , SOURCE.[order_date]);
    DROP TABLE dbo.tmp_tbl
END
GO

SET NOEXEC OFF
GO