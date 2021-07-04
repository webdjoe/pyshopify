# Shopify Orders Rest API Wrapper and Data Export

The purpose of this repository is to allow easier Shopify data analysis using any SQL or and BI tools that support sql. Shopify's rest API is not data analysis friendly, returning one large, denormalized dataset. This library yields a more normalized dataset that can be used to populate a database or perform a direct analysis.

This repository has two part - 
1) Python app - pulls data from shopify orders api into dataframes
2) [Docker container](docker/) - fully self contained database and app

This has the flexibility of exporting the data to a SQL Server ( along with other relational dbs), exporting to csv and returning a dictionary of dataframes.

The Structure of the SQL Database is described in depth in the [Docs](docs/) folder, an SQL script to build the database is in the scripts folder [setup.sql](docker/scripts/setup.sql).

A fully contained docker container with `docker-compose.yml` is included for simple deployment. Container contains Microsoft SQL Server 2019 with this library installed for easily running with a small amount of configuration.

## Table of Contents

1. [Configuration](#script-configuration-file)
2. [Base Installation](#installing-base-library)
3. [Installation with SQL Drivers](#library-with-sql-driver)
4. [Running the Application as a Module](#running-the-shopifyapp)
5. [Running as Command Line Applicaiton](#running-as-command-line-application)
6. [Database Structure](#database-structure)
    * [Tables](#tablesdocstablestablesmd)
    * [Stored Procedures](#stored-proceduresdocsproceduresproceduresmd)
    * [Full Documentation](docs/start.md)
7. [Database Script](#database-script)
8. [Docker Container](#docker-container)
9. [Useful Queries](#useful-queries)



## Script Configuration file
The python script is configured through an ini based file. Here is the template:
```ini
[shopify]
# Orders API Endpoint
url_base = https://**YOURSTORE**.myshopify.com
order_ep = /admin/api/2020-10/orders.json

# Shopify Access Token
access_token = ***ACCESS TOKEN FROM ADMIN***

# Earliest date
early_date = 20000101

# Items per Return - 250 Max
items_per_page = 250

# Uncomment to get data between two dates
# Overrides past days of history
# start = 20210610
# end = 20210617

# Get past days of history - 30 days is default
days = 30

[sql]
enable = False

# Driver for pyodbc to use
driver = ODBC Driver 17 for SQL Server

# Database server & port
server = ***DATABASE SERVER***
port = 1433
database = ***DATABASE***

# Database user & password
db_user = ***DB USER***
db_pass = ***DB PASSWORD***

[csv]
enable = True
# Relative filepath of csv folder output
filepath = csv_export

[custom]
#Output dictionary of dataframes
enable = False
```

The configuration file will default to `config.ini` in the current working directory. A custom path can be defined by passing to `ShopifyApp('rel/path/config.ini')` when instantiating or the `shopify_cli --config rel/path/config.ini`

## Installing Base Library

Install from PyPi through `pip install`. This will install all required dependencies for running to export to CSV and return a dictionary of dataframes. 
```shell script
$ python3 -m pip install pyshopify
```
## Library with SQL Driver
In order to use the sql output feature, the database driver and python library must be installed. 

On linux it takes several steps. pyodbc must be installed as root user.
```shell script
$ apt-get install -y unixodbc-dev msodbcsql17
$ sudo -H python3 -m pip install pyodbc
$ python3 -m pip install sqlalchemy 
```
Ensure MS ODBC driver is installed on Windows. Can be found [Microsoft SQL OBC Driver](https://docs.microsoft.com/en-us/sql/connect/odbc/windows/system-requirements-installation-and-driver-files?view=sql-server-ver15#installing-microsoft-odbc-driver-for-sql-server) 


## Running the ShopifyApp()

The primary class is `ShopifyApp()` which contains all of the necessary execution methods. 

Can be run two ways:

As a module, instantiating `ShopifyApp` and running `app_runner()`. If custom is disabled, it will return None. If custom is enabled, a dictionary of dataframes of the entire api call is returned. 
```python
from pyshopify.runner import ShopifyApp

# If no value is passed, the program will try to use a file in the working directory named config.ini
shop_instance = ShopifyApp('rel/dir/to/config.ini')

run = shop_instance.app_runner()
```

By enabling custom in the configuration, the entire API call is combined into a single dictionary. This can be a large amount of data, and want to apply logic in between each call.
In this case, use the app_iterator() method

```python
api_iterator = shop_instance.app_iterator()
for api_return in api_iterator:
    #Perform logic here, return dictionary is in same structure as the full dictionary from app_runner()
    print(api_iterator.get('Refunds'))
```

The configuration can be set after you've instantiated the class:
```python
shop_instance = ShopifyApp()
shop_instance.csv_enable = True # enables csv output
shop_instance.custom_enable = True # Enabled full output
```
Enabling SQL output is possible but slightly more involved.
```python
shop_instance = ShopifyApp()
shop_instance.sql_conf = {
    'enabled': True,
    'driver': 'ODBC Driver 17 for SQL Server',
    'server': 'localhost',
    'database': 'shop_rest',
    'db_user': 'sa',
    'db_password': 'StrongDBPassword'
}
shop_app.sql_alive = shop_app.sql_connect()
```
shop_app.sql_alive should return true if connected to database. An error will be raised if unable to connect


The return value of `app_runner()` and `app_iterator()` is a dictionary of dataframes in the structure below. This structure mirrors the structure of the database output.  

```python
from pyshopify.runner import ShopifyApp
shop_class = ShopifyApp()
run = ShopifyApp.app_runner()

# Order Details
# ['id' 'order_date' 'fulfillment_status' 'name' 'number' 'order_number', 'payment_gateway_names' 'processing_method' 'source_name', 'subtotal_price' 'total_discounts' 'total_line_items_price' 'total_price', 'total_price_usd' 'total_tax' 'total_weight', 'email', 'updated_at']
orders_dataframe = run.get("Orders")

# Refunds Dataframe with Date of Refund and Order ID
# Columns    ['refund_date', 'order_id']
refunds_dataframe = run.get("Refunds")

# Refund Line Items Showing Units returned
# ['id', 'line_item_id', 'quantity', 'subtotal', 'total_tax', 'variant_id', 'refund_id', 'order_id']
refund_lineitems = run.get("RefundLineItems")

# Line Items sold
# ['id', 'order_id', 'order_date', 'variant_id', 'quantity', 'price']
line_items = run.get("LineItems")

# Customer info for each order
# ['order_id', 'order_date', 'email', 'customer_id', 'orders_count', 'total_spent', 'created_at']
customer_orders = run.get("OrderCustomers")

# Order Shipping Prices
# [id, order_id, order_date, carrier_identifier, code, delivery_category, ship_discount_price, ship_price, phone, requested_fulfillment_id, source, title]
shipping_lines = run.get("ShipLines")

# Discount Applications
# ['order_id', 'order_date', 'type', 'code', 'title', 'description', 'value', 'value_type', 'allocation_method', 'target_selection', 'target_type']
discount_applications = run.get("DiscountApps")

# Discount Codes
# ['order_id', 'code', 'type', 'amount']
discount_codes = run.get('DiscountCodes')
 
```

## Running as Command Line Application
From command line:
```shell script
# There are different command options
$ shopify_cli --help
Usage: shopify_cli [OPTIONS]

  Run Shopify App CLI.

Options:
  -d, --days INTEGER     get days of history
  -b, --between TEXT...  get between 2 dates - yyyy-MM-dd, ex -b 2020-01-01
                         2020-01-02
  --sql-out / --no-sql   write to database - Default False
  --csv-out / --no-csv   Write results to csv files - Default true
  --csv-location TEXT    Relative location of csv export folder defaults to
                         csv_export/
  --config TEXT          Relative location of config.ini - defaults to
                         config.ini in currect directory
  --help                 Show this message and exit.

# Default arguments are:
$ shopify_cli -d 30 --csv-out --no-sql --config config.ini

$ shopify_cli -d 30 # get last 30 days of orders and export to CSV in CWD/csv_export
$ shopify_cli -b 2020-01-01 2020-01-02 # get orders between dates and export csv
$ shopify_cli -d 30 --sql-out # update SQL db
```

Enabling the custom section of `config.ini` will return a dictionary of order data parsed into separate key-value pairs that allow easier processing and analysis. Using the sql option will update an SQL Database with the data from the dictionary.

The structure of the custom return dictionary reflects the SQL database structure that it will update:
```python
from pyshopify import ShopifyApp

# Enable custom in config.ini
shop_app = ShopifyApp()

app_run = shop_app.app_runner()

app_run = {
      'Orders': OrdersDataframe,
      'Customers': CustomersDataframe,
      'LineItems': LineItemDataFrame
      'Refunds': RefundDataFrame,
      'RefundLineItem': RefLineItem.DataFrame,
      'Adjustments': RefundAdjustmentsDataFrame
}
```

Each dataframe in the return represents an SQL Table in the database. The dataframe column types match the database column types.

## Database Structure

Exporting SQL from API response is two step process:
1. Send DataFrame to temporary SQL Table
2. Run stored procedure to merge temp table with the appropriate table 

The full database documentation is located [here](docs/Start.md)

Click on each item for more details.

#### `shop_rest` is the default database name. Remember to change config.ini if using a different database name. 

### [Tables](docs/Tables/Tables.md)    

|Name|Description
|---|---
|[dbo.Adjustments](docs/Tables/dbo.Adjustments.md)|Order Refund Adjustments|
|[dbo.DateDimension](docs/Tables/dbo.DateDimension.md)|Date Dimension Table for Analysis|
|[dbo.DiscountApps](docs/Tables/dbo.DiscountApps.md)|Discount Applications for Each Order|
|[dbo.DiscountCodes](docs/Tables/dbo.DiscountCodes.md)|Discount Codes In Use for Each Order|
|[dbo.LineItems](docs/Tables/dbo.LineItems.md)|Line Items with Units Sold for Orders|
|[dbo.OrderCustomers](docs/Tables/dbo.OrderCustomers.md)|Customer Info based on Order ID|
|[dbo.Orders](docs/Tables/dbo.Orders.md)|Order Details|
|[dbo.RefundLineItem](docs/Tables/dbo.RefundLineItem.md)|Refunded Units|
|[dbo.Refunds](docs/Tables/dbo.Refunds.md)|Order Refunds |
|[dbo.ShipLines](docs/Tables/dbo.ShipLines.md)|Order shipping lines |

###  [Stored Procedures](docs/Procedures/Procedures.md)

|Name|Description
|---|---
|[dbo.adjustments_update](docs/Procedures/dbo.adjustments_update.md)|Update Adjustments|
|[dbo.cust_update](docs/Procedures/dbo.cust_update.md)|Update Customer Orders Table|
|[dbo.discapp_update](docs/Procedures/dbo.discapp_update.md)| Update discounts applied to each order|
|[dbo.disccode_update](docs/Procedures/dbo.disccode_update.md)| Update discount codes used for each order|
|[dbo.lineitems_update](docs/Procedures/dbo.lineitems_update.md)|Update Line Items|
|[dbo.orders_update](docs/Procedures/dbo.orders_update.md)|Merge Orders|
|[dbo.reflineitem_update](docs/Procedures/dbo.reflineitem_update.md)|Merge Refunded Line Items|
|[dbo.refunds_update](docs/Procedures/dbo.refunds_update.md)|Merge Refunds
|[dbo.shipline_update](docs/Procedures/dbo.shipline_update.md)|Update shipping lines table


A [DateDimension](docs/Tables/dbo.DateDimension.md) table is included for easier analysis

## Database script

To build the dataabse, run the [setup.sql](docker/scripts/setup.sql) script in the `docker/scripts` folder. This has only been tested on Microsoft SQL Server 2019 but can easily be adapted for other databases. It will set up all of the required tables and stored procedures.

The `DateDimension` table can be created from the [dates.sql](docker/scripts/dates.sql) script in the [docker/scripts](docker/scripts) fold. Credit goes to Aaron Bertrand for this amazing script - [Creating a date dimension or calendar table in SQL Server](https://www.mssqltips.com/sqlservertip/4054/creating-a-date-dimension-or-calendar-table-in-sql-server/)

Both are ran automatically when starting the docker container.

## Docker Container

There is a Dockerfile and docker-compose.yml in the [docker](docker) folder. This is based on the Microsoft SQL Server 2019 container running on Ubuntu. It installs all of the necessary applications to run pyshopify and a database instance to write to. 

NOTE: This is NOT production ready. Security is not hardened, container is run as root user.

Both containers automatically deploy [setup.sql](docker/scripts/setup.sql) and [dates.sql](docker/scripts/dates.sql) to build the required database structure.

Please make sure to set the password in the `docker-compose.yml` file.

Download entire docker folder or just clone repo  

```shell script
$ git clone https://github.com/webdjoe/pyshopify
$ cd docker
```
Use vim or nano to edit docker-compose.yml and config.ini in config folder
```shell script
$ vim docker-compose.yml
$ vim config/config.ini
```

Build & Run container. Use -d for detached
```shell script
$ docker-compose build
$ docker-compose run -d
```
Once started test if SQL server is running. A `0` return value indicates the server has started up.
```shell script
$ docker exec -it shopsql /opt/mssql-tools/bin/sqlcmd -h -1 -t 1 -U sa -P "$SA_PASSWORD" -Q "SET NOCOUNT ON; Select SUM(state) from sys.databases")
```
`shopify_cli` can be called in container to update the container's database.
```shell script
Get last 30 days of data and import into SQL Server running in container
$ docker exec -it shopsql shopify_cli -d 30 --no-csv --sql-out

Get data between dates and import into SQL Server running on container 
$ docker exec -it shopsql shopify_cli -b 20200101 20201231 --no-csv --sql-out
```

`shopify_cli` can also be run from container to get data in csv files in the csv_export folder
Assumes run from the same folder as the docker files. Container links csv_export folder to retreive export without having to copy from container.
```shell script
$ docker exec -it shopsql shopify_cli --csv-out
$ cd csv_export
```
 
 ## Useful Queries
 
 These scripts assume Shopify has been configured correctly from the start, meaning SKU's, product names and product titles remained consistent. If not, so data cleansing may be required. For example, if your product title has been properly configured you can update SKU's from the `variant_sku` column.
 
#### List all product names, titles, skus and variant SKU's to check for consistency.
 
Resulting table is ordered by quantity sold to check impact of product sku & naming consistency  
 
 ```tsql
SELECT [variant_id], [name], [product_id], [sku], [title], SUM([quantity]) quantity
FROM shop_rest.dbo.LineItems
GROUP BY [variant_id], [name], [product_id], [sku], [title]
ORDER BY SUM([quantity])
``` 
Or check if above a minimum threshold, 10 in this case:

```tsql
SELECT [variant_id], [name], [product_id], [sku], [title], SUM([quantity]) quantity
FROM shop_rest.dbo.LineItems
GROUP BY [variant_id], [name], [product_id], [sku], [title]
HAVING SUM([quantity]) > 10
ORDER BY SUM([quantity])
```

If there are inconsistencies, an easy way to clear up is to import the return table into excel and make a table of variant_id with the correct title and SKU. Import that table into SQL server and join with queries that return `variant_id`.

#### Quantities Sold

Return quantities sold, grouped by month. SKU and title are used as identifiers as identifiers.

```tsql
SELECT EOMONTH([order_date],0) OrderDate, [sku], [name], SUM([quantity]) Quantity
FROM shop_rest.dbo.LineItems
GROUP BY EOMONTH([order_date], 0), [sku], [name]
ORDER BY [order_date]
```

If there is inconsistency in product naming and SKU's, use a subquery to join table with the table created containing the variant_id with the corrected SKU's and product titles. The following logic can be applied to any other query containing `variant_id`

```tsql
SELECT te.OrderDate, te.sku, SUM(te.qty) Quantity FROM

(
    SELECT CAST(EOMONTH([order_date],0) as date) OrderDate
        ,vs.[sku]
        ,vs.[name]
        ,[sku]
        ,li.[quantity] qty
    FROM shop_rest.dbo.LineItems li
    INNER JOIN shop_rest.dbo.VariantSkus vs 
        ON li.variant_id = vs.variant_id
) te

GROUP BY te.OrderDate, te.sku
ORDER BY te.OrderDate
``` 

#### Number of returning customers per month

```tsql
SELECT COUNT(*) AS Customers, CAST(EOMONTH(order_date,0) AS date) AS OrderDate
    FROM dbo.OrderCustomers
WHERE [orders_count] > 1
GROUP BY CAST(EOMONTH(order_date) AS date)
```

#### Monthly Gross Sales with Discounts.

```tsql
SELECT CAST(EOMONTH([order_date],0) AS date) Month
      ,SUM([total_line_items_price]) GrossPrice
	  ,SUM([total_discounts]) TotalDiscount
      ,SUM([subtotal_price]) Subtotal
  FROM [shop_rest].[dbo].[Orders]  
  GROUP BY CAST(EOMONTH([order_date],0) AS DATE)
```

#### Monthly Sales, Discounts & Shipping Revenue
```tsql
SELECT 
     ord.[Month]
    ,ord.[GrossPrice]
    ,ord.[TotalDiscount]
    ,ord.[Subtotal]
    ,ship.[ShipPrice]
    ,(ord.[GrossPrice] - ord.[TotalDiscount] + ship.[ShipPrice]) TotalPrice
FROM (
    SELECT CAST(EOMONTH([order_date],0) AS date) Month
          ,SUM([total_line_items_price]) GrossPrice
          ,SUM([total_discounts]) TotalDiscount
          ,SUM([subtotal_price]) Subtotal
          ,SUM([total_tax]) TotalTax
          ,SUM([total_price]) TotalPrice
    FROM [shop_rest].[dbo].[Orders]  
    GROUP BY CAST(EOMONTH([order_date],0) AS DATE)
) ord 
INNER JOIN (
    SELECT SUM([ship_price]) ShipPrice, CAST(EOMONTH([order_date],0) AS date) Month
    FROM [shop_rest].[dbo].[ShipLines]
    GROUP BY CAST(EOMONTH([order_date],0) AS date)
) ship
ON ord.[Month] = ship.[Month]
  ORDER BY ord.[Month]
```