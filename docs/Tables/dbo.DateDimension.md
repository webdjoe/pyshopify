[Start](../start.md)>[Tables](./Tables.md)>dbo.DateDimension

# ![logo](../Images/table.svg) dbo.DateDimension

## <a name="#Description"></a>Description
> Date Dimension Table for Time Series Analysis
## <a name="#Columns"></a>Columns _`34`_
|Key|Name|Data Type|Length|Precision|Scale|Not Null|Description
|---|---|---|---|---|---|---|---
|[![Cluster Key PK_DateDimension](../Images/Cluster.svg)](#Indexes)|TheDate|date|3|10|0|False||
| |TheDay|int|4|10|0|False||
| |TheDaySuffix|char|2|0|0|False||
| |TheDayName|nvarchar|30|0|0|False||
| |TheDayOfWeek|int|4|10|0|False||
| |TheDayOfWeekInMonth|tinyint|1|3|0|False||
| |TheDayOfYear|int|4|10|0|False||
| |IsWeekend|int|4|10|0|True||
| |TheWeek|int|4|10|0|False||
| |TheISOweek|int|4|10|0|False||
| |TheFirstOfWeek|date|3|10|0|False||
| |TheLastOfWeek|date|3|10|0|False||
| |TheWeekOfMonth|tinyint|1|3|0|False||
| |TheMonth|int|4|10|0|False||
| |TheMonthName|nvarchar|30|0|0|False||
| |TheFirstOfMonth|date|3|10|0|False||
| |TheLastOfMonth|date|3|10|0|False||
| |TheFirstOfNextMonth|date|3|10|0|False||
| |TheLastOfNextMonth|date|3|10|0|False||
| |TheQuarter|int|4|10|0|False||
| |TheFirstOfQuarter|date|3|10|0|False||
| |TheLastOfQuarter|date|3|10|0|False||
| |TheYear|int|4|10|0|False||
| |TheISOYear|int|4|10|0|False||
| |TheFirstOfYear|date|3|10|0|False||
| |TheLastOfYear|date|3|10|0|False||
| |IsLeapYear|bit|1|1|0|False||
| |Has53Weeks|int|4|10|0|True||
| |Has53ISOWeeks|int|4|10|0|True||
| |MMYYYY|char|6|0|0|False||
| |Style101|char|10|0|0|False||
| |Style103|char|10|0|0|False||
| |Style112|char|8|0|0|False||
| |Style120|char|10|0|0|False||

## <a name="#Indexes"></a>Indexes _`1`_
|Key|Name|Columns|Unique|Type|Description
|---|---|---|---|---|---
|[![Cluster Key PK_DateDimension](../Images/Cluster.svg)](#Indexes)|PK_DateDimension|TheDate|True|||

Credit goes to Aaron Bertrand for this amazing script - [Creating a date dimension or calendar table in SQL Server](https://www.mssqltips.com/sqlservertip/4054/creating-a-date-dimension-or-calendar-table-in-sql-server/)

## <a name="#SqlScript"></a>SQL Script
```SQL
USE shop_rest
GO

DECLARE @StartDate  date = '20100101';

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
    TheDaySuffix        = CONVERT(char(2), CASE WHEN TheDay / 10 = 1 THEN 'th' ELSE
                            CASE RIGHT(TheDay, 1) WHEN '1' THEN 'st' WHEN '2' THEN 'nd'
                            WHEN '3' THEN 'rd' ELSE 'th' END END),
    TheDayName,
    TheDayOfWeek,
    TheDayOfWeekInMonth = CONVERT(tinyint, ROW_NUMBER() OVER
                            (PARTITION BY TheFirstOfMonth, TheDayOfWeek ORDER BY TheDate)),
    TheDayOfYear,
    IsWeekend           = CASE WHEN TheDayOfWeek IN (CASE @@DATEFIRST WHEN 1 THEN 6 WHEN 7 THEN 1 END,7)
                            THEN 1 ELSE 0 END,
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
    IsLeapYear          = CONVERT(bit, CASE WHEN (TheYear % 400 = 0)
                            OR (TheYear % 4 = 0 AND TheYear % 100 <> 0)
                            THEN 1 ELSE 0 END),
    Has53Weeks          = CASE WHEN DATEPART(WEEK,     TheLastOfYear) = 53 THEN 1 ELSE 0 END,
    Has53ISOWeeks       = CASE WHEN DATEPART(ISO_WEEK, TheLastOfYear) = 53 THEN 1 ELSE 0 END,
    MMYYYY              = CONVERT(char(2), CONVERT(char(8), TheDate, 101))
                          + CONVERT(char(4), TheYear),
    Style101            = CONVERT(char(10), TheDate, 101),
    Style103            = CONVERT(char(10), TheDate, 103),
    Style112            = CONVERT(char(8),  TheDate, 112),
    Style120            = CONVERT(char(10), TheDate, 120)
  FROM src
)
SELECT * INTO dbo.DateDimension FROM dim
  ORDER BY TheDate
  OPTION (MAXRECURSION 0);
GO

CREATE UNIQUE CLUSTERED INDEX PK_DateDimension ON dbo.DateDimension(TheDate);
GO

```

___
