# ![logo](../Images/table.svg) dbo.OrderAttr

[Start](../start.md)>dbo.OrderAttr

## [](#Description) Description

> Attribution details for each order, such as campaign, source, and landing page.

## [](#Columns) Columns _`7`_

| Key | Name              | Data Type | Length | Precision | Scale | Not Null | Description                    |
|:---:|-------------------|-----------|--------|-----------|-------|----------|--------------------------------|
|     | order_id          | bigint    | 8      | 19        | 0     | True     | Order ID of attribution data   |
|     | order_date        | datetime  | 8      | 23        | 3     | True     | Order Date of attribution data |
|     | landing_site      | nvarchar  |        | 0         | 0     | False    | Landing site URL               |
|     | referring_site    | nvarchar  |        | 0         | 0     | False    | Referring site URL             |
|     | source_name       | nvarchar  |        | 0         | 0     | False    | Order Source name              |
|     | source_identifier | nvarchar  |        | 0         | 0     | False    | Order Source identifier        |
|     | source_url        | nvarchar  |        | 0         | 0     | False    | Order Source URL               |


## [](#SqlScript) SQL Script

```SQL
CREATE TABLE dbo.OrderAttr (
  order_id bigint NOT NULL,
  order_date datetime NOT NULL,
  landing_site nvarchar(max) NULL,
  referring_site nvarchar(max) NULL,
  source_name nvarchar(max) NULL,
  source_identifier nvarchar(max) NULL,
  source_url nvarchar(max) NULL
)
ON [PRIMARY]
TEXTIMAGE_ON [PRIMARY]
GO
```

___
