[Start](../start.md)>[Tables](./Tables.md)>dbo.LineItems

# ![logo](../Images/table.svg) dbo.DateDimension

## <a name="#Description"></a>Description
> Date Dimension Table for Analysis
## <a name="#Columns"></a>Columns _`34`_
|Key|Name|Data Type|Length|Precision|Scale|Not Null|Identity|Rule|Default|Computed|Persisted|Description
|---|---|---|---|---|---|---|---|---|---|---|---|---
|[![Cluster Key PK_DateDimension](../Images/Cluster.svg)](#Indexes)|TheDate|date|3|10|0|False||||False|False||
||TheDay|int|4|10|0|False||||False|False||
||TheDaySuffix|char|2|0|0|False||||False|False||
||TheDayName|nvarchar|30|0|0|False||||False|False||
||TheDayOfWeek|int|4|10|0|False||||False|False||
||TheDayOfWeekInMonth|tinyint|1|3|0|False||||False|False||
||TheDayOfYear|int|4|10|0|False||||False|False||
||IsWeekend|int|4|10|0|True||||False|False||
||TheWeek|int|4|10|0|False||||False|False||
||TheISOweek|int|4|10|0|False||||False|False||
||TheFirstOfWeek|date|3|10|0|False||||False|False||
||TheLastOfWeek|date|3|10|0|False||||False|False||
||TheWeekOfMonth|tinyint|1|3|0|False||||False|False||
||TheMonth|int|4|10|0|False||||False|False||
||TheMonthName|nvarchar|30|0|0|False||||False|False||
||TheFirstOfMonth|date|3|10|0|False||||False|False||
||TheLastOfMonth|date|3|10|0|False||||False|False||
||TheFirstOfNextMonth|date|3|10|0|False||||False|False||
||TheLastOfNextMonth|date|3|10|0|False||||False|False||
||TheQuarter|int|4|10|0|False||||False|False||
||TheFirstOfQuarter|date|3|10|0|False||||False|False||
||TheLastOfQuarter|date|3|10|0|False||||False|False||
||TheYear|int|4|10|0|False||||False|False||
||TheISOYear|int|4|10|0|False||||False|False||
||TheFirstOfYear|date|3|10|0|False||||False|False||
||TheLastOfYear|date|3|10|0|False||||False|False||
||IsLeapYear|bit|1|1|0|False||||False|False||
||Has53Weeks|int|4|10|0|True||||False|False||
||Has53ISOWeeks|int|4|10|0|True||||False|False||
||MMYYYY|char|6|0|0|False||||False|False||
||Style101|char|10|0|0|False||||False|False||
||Style103|char|10|0|0|False||||False|False||
||Style112|char|8|0|0|False||||False|False||
||Style120|char|10|0|0|False||||False|False||

## <a name="#Indexes"></a>Indexes _`1`_
|Key|Name|Columns|Unique|Type|Description
|---|---|---|---|---|---
|[![Cluster Key PK_DateDimension](../Images/Cluster.svg)](#Indexes)|PK_DateDimension|TheDate|True|||

## <a name="#SqlScript"></a>SQL Script
```SQL
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
```

___
