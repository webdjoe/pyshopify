USE master
GO

IF DB_NAME() <> N'master' SET NOEXEC ON

CREATE DATABASE $(DBName)
GO

ALTER DATABASE $(DBName)
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

ALTER DATABASE $(DBName)
  SET DISABLE_BROKER
GO



ALTER DATABASE $(DBName)
  SET QUERY_STORE = OFF
GO

CREATE LOGIN [$(DBUser)] WITH PASSWORD=N'$(DBPassword)'

USE $(DBName)
GO

IF DB_NAME() <> N'$(DBName)' SET NOEXEC ON
GO

IF NOT EXISTS (SELECT * FROM sys.database_principals WHERE name = N'$(DBUser)')
BEGIN
	CREATE USER [$(DBUser)] FOR LOGIN [$(DBUser)]
	EXEC sp_addrolemember N'db_owner', N'$(DBUser)'
END;
GO

DECLARE @StartDate  date = '$(StartDate)';

DECLARE @CutoffDate date = DATEADD(DAY, -1, DATEADD(YEAR, 30, @StartDate));

;WITH seq(n) AS
(
  SELECT 0 UNION ALL SELECT n + 1 FROM seq
  WHERE n < DATEDIFF(DAY, @StartDate, @CutoffDate)
),
d(d) AS
(
  SELECT DATEADD(DAY, n, @StartDate) FROM seq
),
src AS
(
  SELECT
    TheDate         = CONVERT(date, d),
    TheDay          = DATEPART(DAY,       d),
    TheDayName      = DATENAME(WEEKDAY,   d),
    TheWeek         = DATEPART(WEEK,      d),
    TheISOWeek      = DATEPART(ISO_WEEK,  d),
    TheDayOfWeek    = DATEPART(WEEKDAY,   d),
    TheMonth        = DATEPART(MONTH,     d),
    TheMonthName    = DATENAME(MONTH,     d),
    TheQuarter      = DATEPART(Quarter,   d),
    TheYear         = DATEPART(YEAR,      d),
    TheFirstOfMonth = DATEFROMPARTS(YEAR(d), MONTH(d), 1),
    TheLastOfYear   = DATEFROMPARTS(YEAR(d), 12, 31),
    TheDayOfYear    = DATEPART(DAYOFYEAR, d)
  FROM d
),
dim AS
(
  SELECT
    TheDate,
    TheDay,
    TheDaySuffix        = CONVERT(char(2), IIF(TheDay / 10 = 1, 'th', CASE RIGHT(TheDay, 1)
                                                                          WHEN '1' THEN 'st'
                                                                          WHEN '2' THEN 'nd'
                                                                          WHEN '3' THEN 'rd'
                                                                          ELSE 'th' END)),
    TheDayName,
    TheDayOfWeek,
    TheDayOfWeekInMonth = CONVERT(tinyint, ROW_NUMBER() OVER
                            (PARTITION BY TheFirstOfMonth, TheDayOfWeek ORDER BY TheDate)),
    TheDayOfYear,
    IsWeekend           = IIF(TheDayOfWeek IN (CASE @@DATEFIRST WHEN 1 THEN 6 WHEN 7 THEN 1 END, 7), 1, 0),
    TheWeek,
    TheISOweek,
    TheFirstOfWeek      = DATEADD(DAY, 1 - TheDayOfWeek, TheDate),
    TheLastOfWeek       = DATEADD(DAY, 6, DATEADD(DAY, 1 - TheDayOfWeek, TheDate)),
    TheWeekOfMonth      = CONVERT(tinyint, DENSE_RANK() OVER
                            (PARTITION BY TheYear, TheMonth ORDER BY TheWeek)),
    TheMonth,
    TheMonthName,
    TheFirstOfMonth,
    TheLastOfMonth      = MAX(TheDate) OVER (PARTITION BY TheYear, TheMonth),
    TheFirstOfNextMonth = DATEADD(MONTH, 1, TheFirstOfMonth),
    TheLastOfNextMonth  = DATEADD(DAY, -1, DATEADD(MONTH, 2, TheFirstOfMonth)),
    TheQuarter,
    TheFirstOfQuarter   = MIN(TheDate) OVER (PARTITION BY TheYear, TheQuarter),
    TheLastOfQuarter    = MAX(TheDate) OVER (PARTITION BY TheYear, TheQuarter),
    TheYear,
    TheISOYear          = TheYear - CASE WHEN TheMonth = 1 AND TheISOWeek > 51 THEN 1
                            WHEN TheMonth = 12 AND TheISOWeek = 1  THEN -1 ELSE 0 END,
    TheFirstOfYear      = DATEFROMPARTS(TheYear, 1,  1),
    TheLastOfYear,
    IsLeapYear          = CONVERT(bit, IIF((TheYear % 400 = 0)
                                               OR (TheYear % 4 = 0 AND TheYear % 100 <> 0), 1, 0)),
    Has53Weeks          = IIF(DATEPART(WEEK, TheLastOfYear) = 53, 1, 0),
    Has53ISOWeeks       = IIF(DATEPART(ISO_WEEK, TheLastOfYear) = 53, 1, 0),
    MMYYYY              = CONVERT(char(2), CONVERT(char(8), TheDate, 101))
                          + CONVERT(char(4), TheYear),
    Style101            = CONVERT(char(10), TheDate, 101),
    Style103            = CONVERT(char(10), TheDate, 103),
    Style112            = CONVERT(char(8),  TheDate, 112),
    Style120            = CONVERT(char(10), TheDate, 120)
  FROM src
)
SELECT * INTO $(SchemaName).DateDimension FROM dim
  ORDER BY TheDate
  OPTION (MAXRECURSION 0);
GO

CREATE UNIQUE CLUSTERED INDEX PK_DateDimension ON $(SchemaName).DateDimension(TheDate);
GO


SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE $(SchemaName).[Adjustments](
	[id] [bigint] NOT NULL,
	[refund_id] [bigint] NOT NULL,
	[order_id] [bigint] NOT NULL,
	[amount] [float] NOT NULL,
	[tax_amount] [float] NOT NULL,
	[kind] [nvarchar](255) NULL,
	[reason] [nvarchar](255) NULL,
 CONSTRAINT [PK_adj_id] PRIMARY KEY CLUSTERED
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE $(SchemaName).[Customers](
	[id] [bigint] NOT NULL,
	[updated_at] [datetime] NOT NULL,
	[created_at] [datetime] NOT NULL,
	[email] [nvarchar](255) NULL,
	[last_order_id] [bigint] NULL,
	[orders_count] [int] NOT NULL,
	[total_spent] [money] NOT NULL,
	[tags] [nvarchar](max) NULL,
	[city] [nvarchar](255) NULL,
	[province] [nvarchar](255) NULL,
	[country] [nvarchar](255) NULL,
	[zip] [nvarchar](255) NULL,
 CONSTRAINT [PK_Customers_id] PRIMARY KEY CLUSTERED
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO


SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE $(SchemaName).[DiscountApps](
	[order_id] [bigint] NOT NULL,
	[order_date] [datetime] NOT NULL,
	[type] [nvarchar](255) NULL,
	[title] [nvarchar](255) NULL,
	[description] [nvarchar](255) NULL,
	[value] [money] NULL,
	[value_type] [nvarchar](255) NULL,
	[allocation_method] [nvarchar](255) NULL,
	[target_selection] [nvarchar](255) NULL,
	[target_type] [nvarchar](255) NULL,
	[code] [nvarchar](255) NULL
) ON [PRIMARY]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE $(SchemaName).[DiscountCodes](
	[order_id] [bigint] NOT NULL,
	[order_date] [datetime] NOT NULL,
	[code] [nvarchar](255) NOT NULL,
	[amount] [money] NOT NULL,
	[type] [nvarchar](255) NOT NULL
) ON [PRIMARY]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE $(SchemaName).[LineItems](
	[id] [bigint] NOT NULL,
	[order_id] [bigint] NOT NULL,
	[order_date] [datetime] NOT NULL,
	[variant_id] [bigint] NOT NULL,
	[quantity] [int] NOT NULL,
	[price] [float] NOT NULL,
	[name] [nvarchar](255) NULL,
	[product_id] [bigint] NULL,
	[sku] [nvarchar](255) NULL,
	[title] [nvarchar](255) NULL,
	[total_discount] [money] NULL,
	[variant_title] [nvarchar](255) NULL,
 CONSTRAINT [PK_line_item_id] PRIMARY KEY CLUSTERED
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE $(SchemaName).[OrderAttr](
	[order_id] [bigint] NOT NULL,
	[order_date] [datetimeoffset] NOT NULL,
	[landing_site] [nvarchar](max) NULL,
	[referring_site] [nvarchar](max) NULL,
	[source_name] [nvarchar](max) NULL,
	[source_identifier] [nvarchar](max) NULL,
	[source_url] [nvarchar](max) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE $(SchemaName).[Orders](
	[id] [bigint] NOT NULL,
	[order_date] [datetime] NOT NULL,
	[number] [bigint] NOT NULL,
	[total_price] [float] NOT NULL,
	[subtotal_price] [float] NOT NULL,
	[total_weight] [float] NOT NULL,
	[total_tax] [float] NOT NULL,
	[total_discounts] [float] NULL,
	[total_line_items_price] [float] NULL,
	[name] [nvarchar](255) NOT NULL,
	[total_price_usd] [float] NOT NULL,
	[order_number] [bigint] NULL,
	[processing_method] [nvarchar](255) NULL,
	[source_name] [nvarchar](255) NULL,
	[fulfillment_status] [nvarchar](255) NULL,
	[payment_gateway_names] [nvarchar](max) NULL,
	[email] [nvarchar](255) NULL,
	[updated_at] [datetime] NULL,
	[financial_status] [nvarchar](255) NULL,
	[customer_id] [bigint] NULL,
	[tags] [nvarchar](max) NULL,
 CONSTRAINT [PK_OrderID] PRIMARY KEY CLUSTERED
(
	[id] ASC
)
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE $(SchemaName).[RefundLineItem](
	[id] [bigint] NOT NULL,
	[refund_id] [bigint] NOT NULL,
	[order_id] [bigint] NOT NULL,
	[line_item_id] [bigint] NOT NULL,
	[variant_id] [bigint] NOT NULL,
	[quantity] [int] NOT NULL,
	[subtotal] [float] NOT NULL,
	[total_tax] [float] NOT NULL,
 CONSTRAINT [PK_refundlineitem_id] PRIMARY KEY CLUSTERED
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE $(SchemaName).[Refunds](
	[id] [bigint] NOT NULL,
	[refund_date] [datetime] NOT NULL,
	[order_id] [bigint] NOT NULL,
 CONSTRAINT [PK_refund_id] PRIMARY KEY CLUSTERED
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE $(SchemaName).[ShipLines](
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
