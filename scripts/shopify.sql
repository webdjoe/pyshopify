USE master
GO

IF DB_NAME() <> N'master' SET NOEXEC ON

--
-- Create database
--
PRINT (N'Create database [$(DBName)]')
GO
IF DB_ID('[$(DBName)]') IS NULL
BEGIN
  CREATE DATABASE [$(DBName)]
  PRINT (N'Alter database')
  ALTER DATABASE [$(DBName)]
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
      CONCAT_NULL_YIELDS_NULL OFF,
      CURSOR_CLOSE_ON_COMMIT OFF,
      CURSOR_DEFAULT GLOBAL,
      DATE_CORRELATION_OPTIMIZATION OFF,
      DB_CHAINING OFF,
      HONOR_BROKER_PRIORITY OFF,
      MULTI_USER,
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
  ALTER DATABASE [$(DBName)]
    SET ENABLE_BROKER
  ALTER DATABASE [$(DBName)]
    SET ALLOW_SNAPSHOT_ISOLATION OFF
  ALTER DATABASE [$(DBName)]
    SET QUERY_STORE = OFF
END
GO

PRINT (N'Create Login')
IF '$(DBUser)' <> 'sa' AND NOT EXISTS (SELECT * FROM sys.server_principals WHERE name = '($DBUser)')
CREATE LOGIN $(DBUser) WITH PASSWORD = N'$(DBPassword)'
GO

PRINT (N'Use database')
USE [$(DBName)]
GO

IF DB_NAME() <> N'$(DBName)' SET NOEXEC ON
GO

--
-- Create user
--
PRINT (N'Create user [$(DBUser)]')
GO
IF '$(DBUser)' <> 'sa' AND DATABASE_PRINCIPAL_ID(N'[$(DBUser)]') IS NULL
CREATE USER [$(DBUser)]
  FOR LOGIN [$(DBUser)]
GO

IF '$(DBUSER)' <> 'sa'
EXEC sp_addrolemember 'db_owner', '$(DBUser)'
GO

--
-- Create schema
--
PRINT (N'Create schema [$(SchemaName)]')
GO
IF '$(SchemaName)' <> 'dbo' AND SCHEMA_ID(N'[$(SchemaName)]') IS NULL
EXEC sp_executesql N'CREATE SCHEMA [$(SchemaName)] AUTHORIZATION [dbo]'
GO 

IF '$(SchemaName)' <> 'dbo' and '$(DBUser)' <> 'sa'
ALTER USER [$(DBUser)] WITH DEFAULT_SCHEMA = [$(SchemaName)]
GO

--
-- Create table [$(SchemaName)].[Variants]
--
PRINT (N'Create table [$(SchemaName)].[Variants]')
GO
IF OBJECT_ID(N'[$(SchemaName)].[Variants]', 'U') IS NULL
CREATE TABLE [$(SchemaName)].[Variants] (
  [id] [bigint] IDENTITY,
  [product_id] [bigint] NOT NULL,
  [created_at] [datetime] NOT NULL,
  [updated_at] [datetime] NOT NULL,
  [title] [nvarchar](255) NULL,
  [price] [money] NULL,
  [sku] [nvarchar](255) NULL,
  [position] [int] NULL,
  [inventory_policy] [nvarchar](255) NULL,
  [compare_at_price] [money] NULL,
  [fulfillment_service] [nvarchar](255) NULL,
  [inventory_management] [nvarchar](255) NULL,
  [option1] [nvarchar](255) NULL,
  [option2] [nvarchar](255) NULL,
  [option3] [nvarchar](255) NULL,
  [barcode] [bigint] NULL,
  [grams] [int] NULL,
  [image_id] [bigint] NULL,
  [weight] [float] NULL,
  [weight_unit] [nvarchar](50) NULL,
  [inventory_item_id] [bigint] NULL,
  [inventory_quantity] [int] NULL,
  [old_inventory_quantity] [int] NULL,
  [requires_shipping] [bit] NULL,
  [admin_graphql_api_id] [nvarchar](255) NULL,
  CONSTRAINT [PK_Variants] PRIMARY KEY CLUSTERED ([id])
)
ON [PRIMARY]
GO

--
-- Create table [$(SchemaName)].[ShipLines]
--
PRINT (N'Create table [$(SchemaName)].[ShipLines]')
GO
IF OBJECT_ID(N'[$(SchemaName)].[ShipLines]', 'U') IS NULL
CREATE TABLE [$(SchemaName)].[ShipLines] (
  [id] [bigint] IDENTITY,
  [processed_at] [datetime] NOT NULL,
  [order_id] [bigint] NOT NULL,
  [discounted_price] [money] NOT NULL,
  [price] [money] NOT NULL,
  [carrier_identifier] [nvarchar](255) NULL,
  [code] [nvarchar](255) NULL,
  [delivery_category] [nvarchar](255) NULL,
  [phone] [nvarchar](255) NULL,
  [requested_fulfillment_service_id] [nvarchar](255) NULL,
  [source] [nvarchar](255) NULL,
  [title] [nvarchar](255) NULL,
  CONSTRAINT [PK_ShipLines] PRIMARY KEY CLUSTERED ([id])
)
ON [PRIMARY]
GO

--
-- Create index [IDX_ShipLines] on table [$(SchemaName)].[ShipLines]
--
PRINT (N'Create index [IDX_ShipLines] on table [$(SchemaName)].[ShipLines]')
GO
IF NOT EXISTS (
  SELECT 1 FROM sys.indexes WITH (NOLOCK)
  WHERE name = N'IDX_ShipLines' AND object_id = OBJECT_ID(N'[$(SchemaName)].[ShipLines]'))
  AND EXISTS (
  SELECT 1 FROM sys.columns WITH (NOLOCK)
  WHERE name = N'order_id' AND object_id = OBJECT_ID(N'[$(SchemaName)].[ShipLines]'))
  AND EXISTS (
  SELECT 1 FROM sys.columns WITH (NOLOCK)
  WHERE name = N'processed_at' AND object_id = OBJECT_ID(N'[$(SchemaName)].[ShipLines]'))
CREATE INDEX [IDX_ShipLines]
  ON [$(SchemaName)].[ShipLines] ([order_id], [processed_at])
  ON [PRIMARY]
GO

--
-- Create table [Refunds]
--
PRINT (N'Create table [$(SchemaName)].[Refunds]')
GO
IF OBJECT_ID(N'[$(SchemaName)].[Refunds]', 'U') IS NULL
CREATE TABLE [$(SchemaName)].[Refunds] (
  [id] [bigint] IDENTITY,
  [created_at] [datetime] NOT NULL,
  [processed_at] [datetime] NOT NULL,
  [order_date] [datetime] NOT NULL,
  [order_id] [bigint] NOT NULL,
  [note] [nvarchar](max) NULL,
  CONSTRAINT [PK_refund_id] PRIMARY KEY CLUSTERED ([id])
)
ON [PRIMARY]
TEXTIMAGE_ON [PRIMARY]
GO

--
-- Create index [IDX_Refunds_created_at] on table [Refunds]
--
PRINT (N'Create index [IDX_Refunds_created_at] on table [$(SchemaName)].[Refunds]')
GO
IF NOT EXISTS (
  SELECT 1 FROM sys.indexes WITH (NOLOCK)
  WHERE name = N'IDX_Refunds_created_at' AND object_id = OBJECT_ID(N'[$(SchemaName)].[Refunds]'))
  AND EXISTS (
  SELECT 1 FROM sys.columns WITH (NOLOCK)
  WHERE name = N'created_at' AND object_id = OBJECT_ID(N'[$(SchemaName)].[Refunds]'))
CREATE INDEX [IDX_Refunds_created_at]
  ON [$(SchemaName)].[Refunds] ([created_at])
  ON [PRIMARY]
GO

--
-- Create index [IDX_Refunds_order_id] on table [Refunds]
--
PRINT (N'Create index [IDX_Refunds_order_id] on table [$(SchemaName)].[Refunds]')
GO
IF NOT EXISTS (
  SELECT 1 FROM sys.indexes WITH (NOLOCK)
  WHERE name = N'IDX_Refunds_order_id' AND object_id = OBJECT_ID(N'[$(SchemaName)].[Refunds]'))
  AND EXISTS (
  SELECT 1 FROM sys.columns WITH (NOLOCK)
  WHERE name = N'order_id' AND object_id = OBJECT_ID(N'[$(SchemaName)].[Refunds]'))
CREATE INDEX [IDX_Refunds_order_id]
  ON [$(SchemaName)].[Refunds] ([order_id])
  ON [PRIMARY]
GO

--
-- Create table [RefundLineItem]
--
PRINT (N'Create table [$(SchemaName)].[RefundLineItem]')
GO
IF OBJECT_ID(N'[$(SchemaName)].[RefundLineItem]', 'U') IS NULL
CREATE TABLE [$(SchemaName)].[RefundLineItem] (
  [id] [bigint] IDENTITY,
  [refund_id] [bigint] NOT NULL,
  [processed_at] [datetime] NOT NULL,
  [order_date] [datetime] NOT NULL,
  [order_id] [bigint] NOT NULL,
  [line_item_id] [bigint] NOT NULL,
  [variant_id] [bigint] NOT NULL,
  [quantity] [int] NOT NULL,
  [subtotal] [money] NOT NULL,
  [total_tax] [money] NOT NULL,
  CONSTRAINT [PK_refundlineitem_id] PRIMARY KEY CLUSTERED ([id])
)
ON [PRIMARY]
GO

--
-- Create index [IDX_RefundLineItem_order_id] on table [RefundLineItem]
--
PRINT (N'Create index [IDX_RefundLineItem_order_id] on table [$(SchemaName)].[RefundLineItem]')
GO
IF NOT EXISTS (
  SELECT 1 FROM sys.indexes WITH (NOLOCK)
  WHERE name = N'IDX_RefundLineItem_order_id' AND object_id = OBJECT_ID(N'[$(SchemaName)].[RefundLineItem]'))
  AND EXISTS (
  SELECT 1 FROM sys.columns WITH (NOLOCK)
  WHERE name = N'order_id' AND object_id = OBJECT_ID(N'[$(SchemaName)].[RefundLineItem]'))
CREATE INDEX [IDX_RefundLineItem_order_id]
  ON [$(SchemaName)].[RefundLineItem] ([order_id])
  ON [PRIMARY]
GO

--
-- Create index [IDX_RefundLineItem_processed_at] on table [RefundLineItem]
--
PRINT (N'Create index [IDX_RefundLineItem_processed_at] on table [$(SchemaName)].[RefundLineItem]')
GO
IF NOT EXISTS (
  SELECT 1 FROM sys.indexes WITH (NOLOCK)
  WHERE name = N'IDX_RefundLineItem_processed_at' AND object_id = OBJECT_ID(N'[$(SchemaName)].[RefundLineItem]'))
  AND EXISTS (
  SELECT 1 FROM sys.columns WITH (NOLOCK)
  WHERE name = N'processed_at' AND object_id = OBJECT_ID(N'[$(SchemaName)].[RefundLineItem]'))
CREATE INDEX [IDX_RefundLineItem_processed_at]
  ON [$(SchemaName)].[RefundLineItem] ([processed_at])
  ON [PRIMARY]
GO

--
-- Create table [Products]
--
PRINT (N'Create table [$(SchemaName)].[Products]')
GO
IF OBJECT_ID(N'[$(SchemaName)].[Products]', 'U') IS NULL
CREATE TABLE [$(SchemaName)].[Products] (
  [id] [bigint],
  [created_at] [datetime] NOT NULL,
  [updated_at] [datetime] NOT NULL,
  [title] [nvarchar](255) NULL,
  [body_html] [nvarchar](max) NULL,
  [vendor] [nvarchar](255) NULL,
  [product_type] [nvarchar](255) NULL,
  [handle] [nvarchar](255) NULL,
  [published_at] [datetime] NULL,
  [template_suffix] [nvarchar](255) NULL,
  [status] [nvarchar](255) NULL,
  [published_scope] [nvarchar](255) NULL,
  [tags] [nvarchar](max) NULL,
  [admin_graphql_api_id] [nvarchar](255) NULL,
  [image_src] [nvarchar](255) NULL,
  CONSTRAINT [PK_products] PRIMARY KEY CLUSTERED ([id])
)
ON [PRIMARY]
TEXTIMAGE_ON [PRIMARY]
GO

--
-- Create table [ProductOptions]
--
PRINT (N'Create table [$(SchemaName)].[ProductOptions]')
GO
IF OBJECT_ID(N'[$(SchemaName)].[ProductOptions]', 'U') IS NULL
CREATE TABLE [$(SchemaName)].[ProductOptions] (
  [id] [bigint] IDENTITY,
  [product_id] [bigint] NOT NULL,
  [name] [nvarchar](100) NULL,
  [position] [int] NULL,
  [values] [nvarchar](max) NULL,
  CONSTRAINT [PK_options] PRIMARY KEY CLUSTERED ([id])
)
ON [PRIMARY]
TEXTIMAGE_ON [PRIMARY]
GO

--
-- Create table [Orders]
--
PRINT (N'Create table [$(SchemaName)].[Orders]')
GO
IF OBJECT_ID(N'[$(SchemaName)].[Orders]', 'U') IS NULL
CREATE TABLE [$(SchemaName)].[Orders] (
  [id] [bigint] IDENTITY,
  [created_at] [datetime] NOT NULL,
  [updated_at] [datetime] NOT NULL,
  [processed_at] [datetime] NOT NULL,
  [number] [bigint] NOT NULL,
  [total_weight] [float] NOT NULL,
  [name] [nvarchar](50) NOT NULL,
  [order_number] [bigint] NOT NULL,
  [processing_method] [nvarchar](255) NULL,
  [source_name] [nvarchar](50) NULL,
  [fulfillment_status] [nvarchar](50) NULL,
  [payment_gateway_names] [nvarchar](255) NULL,
  [email] [nvarchar](255) NULL,
  [financial_status] [nvarchar](50) NULL,
  [customer_id] [bigint] NULL,
  [tags] [nvarchar](max) NULL,
  CONSTRAINT [PK_OrderID] PRIMARY KEY CLUSTERED ([id])
)
ON [PRIMARY]
TEXTIMAGE_ON [PRIMARY]
GO

--
-- Create index [IDX_Orders_customer_id] on table [Orders]
--
PRINT (N'Create index [IDX_Orders_customer_id] on table [$(SchemaName)].[Orders]')
GO
IF NOT EXISTS (
  SELECT 1 FROM sys.indexes WITH (NOLOCK)
  WHERE name = N'IDX_Orders_customer_id' AND object_id = OBJECT_ID(N'[$(SchemaName)].[Orders]'))
  AND EXISTS (
  SELECT 1 FROM sys.columns WITH (NOLOCK)
  WHERE name = N'customer_id' AND object_id = OBJECT_ID(N'[$(SchemaName)].[Orders]'))
CREATE INDEX [IDX_Orders_customer_id]
  ON [$(SchemaName)].[Orders] ([customer_id])
  ON [PRIMARY]
GO

--
-- Create index [IDX_Orders_processed_at] on table [Orders]
--
PRINT (N'Create index [IDX_Orders_processed_at] on table [$(SchemaName)].[Orders]')
GO
IF NOT EXISTS (
  SELECT 1 FROM sys.indexes WITH (NOLOCK)
  WHERE name = N'IDX_Orders_processed_at' AND object_id = OBJECT_ID(N'[$(SchemaName)].[Orders]'))
  AND EXISTS (
  SELECT 1 FROM sys.columns WITH (NOLOCK)
  WHERE name = N'processed_at' AND object_id = OBJECT_ID(N'[$(SchemaName)].[Orders]'))
CREATE INDEX [IDX_Orders_processed_at]
  ON [$(SchemaName)].[Orders] ([processed_at])
  ON [PRIMARY]
GO

--
-- Create table [OrderPrices]
--
PRINT (N'Create table [$(SchemaName)].[OrderPrices]')
GO
IF OBJECT_ID(N'[$(SchemaName)].[OrderPrices]', 'U') IS NULL
CREATE TABLE [$(SchemaName)].[OrderPrices] (
  [order_id] [bigint] IDENTITY,
  [processed_at] [datetime] NOT NULL,
  [updated_at] [datetime] NOT NULL,
  [current_total_discounts] [money] NOT NULL,
  [current_total_price] [money] NOT NULL,
  [current_subtotal_price] [money] NOT NULL,
  [current_total_tax] [money] NOT NULL,
  [subtotal_price] [money] NOT NULL,
  [total_discounts] [money] NOT NULL,
  [total_line_items_price] [money] NOT NULL,
  [total_price] [money] NOT NULL,
  [total_tax] [money] NOT NULL,
  [total_shipping_price] [money] NOT NULL,
  [taxes_included] [bit] NOT NULL,
  CONSTRAINT [PK_OrderPrices_order_id] PRIMARY KEY CLUSTERED ([order_id])
)
ON [PRIMARY]
GO

--
-- Create index [UK_OrderPrices] on table [OrderPrices]
--
PRINT (N'Create index [UK_OrderPrices] on table [$(SchemaName)].[OrderPrices]')
GO
IF NOT EXISTS (
  SELECT 1 FROM sys.indexes WITH (NOLOCK)
  WHERE name = N'UK_OrderPrices' AND object_id = OBJECT_ID(N'[$(SchemaName)].[OrderPrices]'))
  AND EXISTS (
  SELECT 1 FROM sys.columns WITH (NOLOCK)
  WHERE name = N'processed_at' AND object_id = OBJECT_ID(N'[$(SchemaName)].[OrderPrices]'))
CREATE INDEX [UK_OrderPrices]
  ON [$(SchemaName)].[OrderPrices] ([processed_at])
  ON [PRIMARY]
GO

--
-- Create table [OrderAttr]
--
PRINT (N'Create table [$(SchemaName)].[OrderAttr]')
GO
IF OBJECT_ID(N'[$(SchemaName)].[OrderAttr]', 'U') IS NULL
CREATE TABLE [$(SchemaName)].[OrderAttr] (
  [order_id] [bigint] IDENTITY,
  [processed_at] [datetime] NOT NULL,
  [landing_site] [nvarchar](max) NULL,
  [referring_site] [nvarchar](max) NULL,
  [source_name] [nvarchar](max) NULL,
  [source_identifier] [nvarchar](max) NULL,
  [source_url] [nvarchar](max) NULL,
  CONSTRAINT [PK_OrderAttr_order_id] PRIMARY KEY CLUSTERED ([order_id])
)
ON [PRIMARY]
TEXTIMAGE_ON [PRIMARY]
GO

--
-- Create index [IDX_OrderAttr_processed_at] on table [OrderAttr]
--
PRINT (N'Create index [IDX_OrderAttr_processed_at] on table [$(SchemaName)].[OrderAttr]')
GO
IF NOT EXISTS (
  SELECT 1 FROM sys.indexes WITH (NOLOCK)
  WHERE name = N'IDX_OrderAttr_processed_at' AND object_id = OBJECT_ID(N'[$(SchemaName)].[OrderAttr]'))
  AND EXISTS (
  SELECT 1 FROM sys.columns WITH (NOLOCK)
  WHERE name = N'processed_at' AND object_id = OBJECT_ID(N'[$(SchemaName)].[OrderAttr]'))
CREATE INDEX [IDX_OrderAttr_processed_at]
  ON [$(SchemaName)].[OrderAttr] ([processed_at])
  ON [PRIMARY]
GO

--
-- Create table [LineItems]
--
PRINT (N'Create table [$(SchemaName)].[LineItems]')
GO
IF OBJECT_ID(N'[$(SchemaName)].[LineItems]', 'U') IS NULL
CREATE TABLE [$(SchemaName)].[LineItems] (
  [id] [bigint] IDENTITY,
  [order_id] [bigint] NOT NULL,
  [processed_at] [datetime] NOT NULL,
  [variant_id] [bigint] NOT NULL,
  [quantity] [int] NOT NULL,
  [price] [money] NOT NULL,
  [product_id] [bigint] NOT NULL,
  [total_discount] [money] NOT NULL,
  [name] [nvarchar](255) NULL,
  [sku] [nvarchar](255) NULL,
  [title] [nvarchar](255) NULL,
  [variant_title] [nvarchar](255) NULL,
  [fulfillment_status] [nvarchar](255) NULL,
  CONSTRAINT [PK_line_item_id] PRIMARY KEY CLUSTERED ([id])
)
ON [PRIMARY]
GO

--
-- Create index [IDX_LineItems_order_id] on table [LineItems]
--
PRINT (N'Create index [IDX_LineItems_order_id] on table [$(SchemaName)].[LineItems]')
GO
IF NOT EXISTS (
  SELECT 1 FROM sys.indexes WITH (NOLOCK)
  WHERE name = N'IDX_LineItems_order_id' AND object_id = OBJECT_ID(N'[$(SchemaName)].[LineItems]'))
  AND EXISTS (
  SELECT 1 FROM sys.columns WITH (NOLOCK)
  WHERE name = N'order_id' AND object_id = OBJECT_ID(N'[$(SchemaName)].[LineItems]'))
CREATE INDEX [IDX_LineItems_order_id]
  ON [$(SchemaName)].[LineItems] ([order_id])
  ON [PRIMARY]
GO

--
-- Create index [IDX_LineItems_processed_at] on table [LineItems]
--
PRINT (N'Create index [IDX_LineItems_processed_at] on table [$(SchemaName)].[LineItems]')
GO
IF NOT EXISTS (
  SELECT 1 FROM sys.indexes WITH (NOLOCK)
  WHERE name = N'IDX_LineItems_processed_at' AND object_id = OBJECT_ID(N'[$(SchemaName)].[LineItems]'))
  AND EXISTS (
  SELECT 1 FROM sys.columns WITH (NOLOCK)
  WHERE name = N'processed_at' AND object_id = OBJECT_ID(N'[$(SchemaName)].[LineItems]'))
CREATE INDEX [IDX_LineItems_processed_at]
  ON [$(SchemaName)].[LineItems] ([processed_at])
  ON [PRIMARY]
GO

--
-- Create table [InventoryLocations]
--
PRINT (N'Create table [$(SchemaName)].[InventoryLocations]')
GO
IF OBJECT_ID(N'[$(SchemaName)].[InventoryLocations]', 'U') IS NULL
CREATE TABLE [$(SchemaName)].[InventoryLocations] (
  [id] [bigint] NOT NULL,
  [name] [nvarchar](255) NOT NULL,
  [address1] [nvarchar](255) NULL,
  [address2] [nvarchar](255) NULL,
  [city] [nvarchar](255) NULL,
  [country_code] [nvarchar](10) NULL,
  [province_code] [nvarchar](10) NULL,
  [updated_at] [datetime] NOT NULL,
  [zip] [nvarchar](50) NULL,
  [active] [bit] NOT NULL,
  CONSTRAINT [PK_InventoryLocations_id] PRIMARY KEY CLUSTERED ([id])
)
ON [PRIMARY]
GO

--
-- Create table [InventoryLevels]
--
PRINT (N'Create table [$(SchemaName)].[InventoryLevels]')
GO
IF OBJECT_ID(N'[$(SchemaName)].[InventoryLevels]', 'U') IS NULL
CREATE TABLE [$(SchemaName)].[InventoryLevels] (
  [inventory_item_id] [bigint] NOT NULL,
  [location_id] [bigint] NOT NULL,
  [available] [int] NULL,
  [updated_at] [datetime] NOT NULL,
  [admin_graphql_api_id] [nvarchar](255) NULL,
  CONSTRAINT [PK_InventoryLevels] PRIMARY KEY CLUSTERED ([inventory_item_id], [location_id])
)
ON [PRIMARY]
GO

--
-- Create table [DiscountCodes]
--
PRINT (N'Create table [$(SchemaName)].[DiscountCodes]')
GO
IF OBJECT_ID(N'[$(SchemaName)].[DiscountCodes]', 'U') IS NULL
CREATE TABLE [$(SchemaName)].[DiscountCodes] (
  [order_id] [bigint] NOT NULL,
  [processed_at] [datetime] NOT NULL,
  [code] [nvarchar](255) NOT NULL,
  [amount] [money] NOT NULL,
  [type] [nvarchar](255) NOT NULL,
  CONSTRAINT [PK_DiscountCodes] PRIMARY KEY CLUSTERED ([order_id], [code])
)
ON [PRIMARY]
GO

--
-- Create index [IDX_DiscountCodes_order_id] on table [DiscountCodes]
--
PRINT (N'Create index [IDX_DiscountCodes_order_id] on table [$(SchemaName)].[DiscountCodes]')
GO
IF NOT EXISTS (
  SELECT 1 FROM sys.indexes WITH (NOLOCK)
  WHERE name = N'IDX_DiscountCodes_order_id' AND object_id = OBJECT_ID(N'[$(SchemaName)].[DiscountCodes]'))
  AND EXISTS (
  SELECT 1 FROM sys.columns WITH (NOLOCK)
  WHERE name = N'processed_at' AND object_id = OBJECT_ID(N'[$(SchemaName)].[DiscountCodes]'))
CREATE INDEX [IDX_DiscountCodes_order_id]
  ON [$(SchemaName)].[DiscountCodes] ([processed_at])
  ON [PRIMARY]
GO

--
-- Create table [DiscountApps]
--
PRINT (N'Create table [$(SchemaName)].[DiscountApps]')
GO
IF OBJECT_ID(N'[$(SchemaName)].[DiscountApps]', 'U') IS NULL
CREATE TABLE [$(SchemaName)].[DiscountApps] (
  [id] [bigint] IDENTITY,
  [order_id] [bigint] NOT NULL,
  [processed_at] [datetime] NOT NULL,
  [type] [nvarchar](255) NOT NULL,
  [value] [money] NOT NULL,
  [title] [nvarchar](255) NULL,
  [description] [nvarchar](255) NULL,
  [value_type] [nvarchar](255) NULL,
  [allocation_method] [nvarchar](255) NULL,
  [target_selection] [nvarchar](255) NULL,
  [target_type] [nvarchar](255) NULL,
  [code] [nvarchar](255) NULL,
  CONSTRAINT [PK_DiscountApps] PRIMARY KEY CLUSTERED ([id])
)
ON [PRIMARY]
GO

--
-- Create index [IDX_DiscountApps_order_id] on table [DiscountApps]
--
PRINT (N'Create index [IDX_DiscountApps_order_id] on table [$(SchemaName)].[DiscountApps]')
GO
IF NOT EXISTS (
  SELECT 1 FROM sys.indexes WITH (NOLOCK)
  WHERE name = N'IDX_DiscountApps_order_id' AND object_id = OBJECT_ID(N'[$(SchemaName)].[DiscountApps]'))
  AND EXISTS (
  SELECT 1 FROM sys.columns WITH (NOLOCK)
  WHERE name = N'order_id' AND object_id = OBJECT_ID(N'[$(SchemaName)].[DiscountApps]'))
CREATE INDEX [IDX_DiscountApps_order_id]
  ON [$(SchemaName)].[DiscountApps] ([order_id])
  ON [PRIMARY]
GO

--
-- Create table [Customers]
--
PRINT (N'Create table [$(SchemaName)].[Customers]')
GO
IF OBJECT_ID(N'[$(SchemaName)].[Customers]', 'U') IS NULL
CREATE TABLE [$(SchemaName)].[Customers] (
  [id] [bigint] IDENTITY,
  [updated_at] [datetime] NOT NULL,
  [created_at] [datetime] NOT NULL,
  [orders_count] [int] NOT NULL,
  [total_spent] [money] NOT NULL,
  [email] [nvarchar](255) NULL,
  [last_order_id] [bigint] NULL,
  [tags] [nvarchar](max) NULL,
  [city] [nvarchar](255) NULL,
  [province] [nvarchar](255) NULL,
  [country] [nvarchar](255) NULL,
  [zip] [nvarchar](255) NULL,
  CONSTRAINT [PK_Customers_id] PRIMARY KEY CLUSTERED ([id])
)
ON [PRIMARY]
TEXTIMAGE_ON [PRIMARY]
GO

--
-- Create table [Adjustments]
--
PRINT (N'Create table [$(SchemaName)].[Adjustments]')
GO
IF OBJECT_ID(N'[$(SchemaName)].[Adjustments]', 'U') IS NULL
CREATE TABLE [$(SchemaName)].[Adjustments] (
  [id] [bigint] IDENTITY,
  [refund_id] [bigint] NOT NULL,
  [processed_at] [datetime] NOT NULL,
  [order_date] [datetime] NOT NULL,
  [order_id] [bigint] NOT NULL,
  [amount] [money] NOT NULL,
  [tax_amount] [money] NOT NULL,
  [kind] [nvarchar](255) NULL,
  [reason] [nvarchar](255) NULL,
  CONSTRAINT [PK_adj_id] PRIMARY KEY CLUSTERED ([id])
)
ON [PRIMARY]
GO
SET NOEXEC OFF
GO