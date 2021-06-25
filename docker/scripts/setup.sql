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
  SET ALLOW_SNAPSHOT_ISOLATION OFF
GO

ALTER DATABASE shop_rest
  SET FILESTREAM (NON_TRANSACTED_ACCESS = OFF)
GO

ALTER DATABASE shop_rest
  SET QUERY_STORE = OFF
GO

USE shop_rest
GO

ALTER DATABASE SCOPED CONFIGURATION SET MAXDOP = 0;
GO

ALTER DATABASE SCOPED CONFIGURATION FOR SECONDARY SET MAXDOP = PRIMARY;
GO

ALTER DATABASE SCOPED CONFIGURATION SET LEGACY_CARDINALITY_ESTIMATION = OFF;
GO

ALTER DATABASE SCOPED CONFIGURATION FOR SECONDARY SET LEGACY_CARDINALITY_ESTIMATION = PRIMARY;
GO

ALTER DATABASE SCOPED CONFIGURATION SET PARAMETER_SNIFFING = ON;
GO

ALTER DATABASE SCOPED CONFIGURATION FOR SECONDARY SET PARAMETER_SNIFFING = PRIMARY;
GO

ALTER DATABASE SCOPED CONFIGURATION SET QUERY_OPTIMIZER_HOTFIXES = OFF;
GO

ALTER DATABASE SCOPED CONFIGURATION FOR SECONDARY SET QUERY_OPTIMIZER_HOTFIXES = PRIMARY;
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


	INSERT INTO dbo.Orders 	(
	   id
	  ,order_date
      ,number
      ,total_price
      ,subtotal_price
      ,total_weight
      ,total_tax
      ,total_discounts
      ,total_line_items_price
      ,name
      ,total_price_usd
      ,order_number
      ,processing_method
      ,source_name
      ,fulfillment_status
      ,payment_gateway_names)
	  
	  SELECT tmp.id
      ,tmp.order_date
      ,tmp.number
      ,tmp.total_price
      ,tmp.subtotal_price
      ,tmp.total_weight
      ,tmp.total_tax
      ,tmp.total_discounts
      ,tmp.total_line_items_price
      ,tmp.name
      ,tmp.total_price_usd
      ,tmp.order_number
      ,tmp.processing_method
      ,tmp.source_name
      ,tmp.fulfillment_status
      ,tmp.payment_gateway_names

	  FROM tmp_tbl tmp
	  WHERE tmp.id NOT IN (SELECT id FROM dbo.Orders)
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

CREATE TABLE dbo.DateDimension (
  TheDate date NULL,
  TheDay int NULL,
  TheDaySuffix char(2) NULL,
  TheDayName nvarchar(30) NULL,
  TheDayOfWeek int NULL,
  TheDayOfWeekInMonth tinyint NULL,
  TheDayOfYear int NULL,
  IsWeekend int NOT NULL,
  TheWeek int NULL,
  TheISOweek int NULL,
  TheFirstOfWeek date NULL,
  TheLastOfWeek date NULL,
  TheWeekOfMonth tinyint NULL,
  TheMonth int NULL,
  TheMonthName nvarchar(30) NULL,
  TheFirstOfMonth date NULL,
  TheLastOfMonth date NULL,
  TheFirstOfNextMonth date NULL,
  TheLastOfNextMonth date NULL,
  TheQuarter int NULL,
  TheFirstOfQuarter date NULL,
  TheLastOfQuarter date NULL,
  TheYear int NULL,
  TheISOYear int NULL,
  TheFirstOfYear date NULL,
  TheLastOfYear date NULL,
  IsLeapYear bit NULL,
  Has53Weeks int NOT NULL,
  Has53ISOWeeks int NOT NULL,
  MMYYYY char(6) NULL,
  Style101 char(10) NULL,
  Style103 char(10) NULL,
  Style112 char(8) NULL,
  Style120 char(10) NULL
)
ON [PRIMARY]
GO

CREATE UNIQUE CLUSTERED INDEX PK_DateDimension
  ON dbo.DateDimension (TheDate)
  ON [PRIMARY]
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

CREATE TABLE dbo.LineItems (
  id bigint NOT NULL,
  order_id bigint NOT NULL,
  order_date datetime NOT NULL,
  variant_id bigint NOT NULL,
  quantity int NOT NULL,
  price float NOT NULL,
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
      ,[price])
	  
	  SELECT [id]
      ,tmp.[order_id]
      ,tmp.[order_date]
      ,tmp.[variant_id]
      ,tmp.[quantity]
      ,tmp.[price]

	  FROM tmp_tbl tmp
	  WHERE tmp.id NOT IN (SELECT id FROM dbo.LineItems)
	  DROP TABLE dbo.tmp_tbl
END
GO
SET NOEXEC OFF
GO
