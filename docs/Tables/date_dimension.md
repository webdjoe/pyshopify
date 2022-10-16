# ![logo](../Images/table.svg) date_dimension

[Start](../start.md)>date_dimension

## [](#Description) Description

> Date Dimension Table for Time Series Analysis

## [](#Columns) Columns _`34`_

|Key|Name|Data Type|Length|Precision|Scale|Not Null|Description
|---|---|---|---|---|---|---|---
|[![Cluster Key PK_DateDimension](../Images/cluster.svg)](#Indexes)|TheDate|date|3|10|0|False||
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

## [](#Indexes) Indexes _`1`_

|Key|Name|Columns|Unique|Type|Description
|---|---|---|---|---|---
|[![Cluster Key PK_DateDimension](../Images/cluster.svg)](#Indexes)|PK_DateDimension|TheDate|True|||

Credit goes to Aaron Bertrand for this amazing script - [Creating a date dimension or calendar table in SQL Server](https://www.mssqltips.com/sqlservertip/4054/creating-a-date-dimension-or-calendar-table-in-sql-server/)

___
