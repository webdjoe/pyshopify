# Shopify Orders Rest API Wrapper and Data Export

The purpose of this repository is to allow easier Shopify data analysis using any SQL or and BI tools that support sql. Shopify's rest API is not data analysis friendly, returning one large, denormalized dataset. This library yields a "more normalized" dataset that can be used to perform analytics.

This repository has two part -

1) Python app - pulls data from shopify orders api into dataframes and export to csv files or sql database with a predefined structure.
2) Docker container - [Dockerfile](Dockerfile) and [Docker Compose](docker-compose.yml) - fully self-contained database and python application. Easiest method if docker is available- [Run as Docker Container](#docker-container)

This has the flexibility of exporting the data to a SQL Server ( along with other relational dbs), exporting to csv and returning a dictionary of dataframes.

The Structure of the SQL Database is described in depth in the [Docs](docs) folder, an SQL script to build the database is in the scripts folder [setup.sql](scripts/setup.sql), along with a command line function.

This requires the creation of a private app in the Shopify Admin center -> Setting -> Apps and Sales Channels -> Develop Apps.

## Table of Contents

- [Shopify Orders Rest API Wrapper and Data Export](#shopify-orders-rest-api-wrapper-and-data-export)
  - [Table of Contents](#table-of-contents)
  - [Data Returned](#data-returned)
    - [Orders Data](#orders-data)
    - [Customers Data](#customers-data)
    - [Product Data](#product-data)
  - [Configuration](#configuration)
    - [Default Configuration](#default-configuration)
    - [Environment Variables](#environment-variables)
    - [Example `config.ini` Configuration](#example-configini-configuration)
    - [Configuration Dictionary](#configuration-dictionary)
  - [Installation](#installation)
    - [Base Library](#base-library)
    - [Library with SQL Driver](#library-with-sql-driver)
    - [Installing ODBC Driver](#installing-odbc-driver)
    - [Installing Python SQL Dependencies](#installing-python-sql-dependencies)
  - [Running in a Python Script](#running-in-a-python-script)
    - [Instantiating Class](#instantiating-class)
    - [Updating Configuration](#updating-configuration)
      - [Full Configuration Dictionary](#full-configuration-dictionary)
      - [Shopify Configuration Dictionary](#shopify-configuration-dictionary)
    - [Product and Inventory Data](#product-and-inventory-data)
      - [Methods that Return Products and Inventory Data](#methods-that-return-products-and-inventory-data)
      - [Methods that Write Inventory and Product Data](#methods-that-write-inventory-and-product-data)
    - [Orders and Customers Data](#orders-and-customers-data)
      - [Returning Customers & Orders Data](#returning-customers--orders-data)
      - [Iterating through Orders and Customers Data](#iterating-through-orders-and-customers-data)
      - [Writing Orders and Customers Data to CSV and SQL Server](#writing-orders-and-customers-data-to-csv-and-sql-server)
      - [Writing data to desired output](#writing-data-to-desired-output)
  - [Running as Command Line Application](#running-as-command-line-application)
  - [Data Structure](#data-structure)
  - [Database Structure](#database-structure)
  - [Creating the Database and Tables](#creating-the-database-and-tables)
    - [CLI Command](#cli-command)
    - [Programatically via Python](#programatically-via-python)
    - [Using SQLCMD Script](#using-sqlcmd-script)
  - [Docker Container](#docker-container)
    - [Docker Compose](#docker-compose)
    - [Creating a Container](#creating-a-container)
    - [Running pyshopify in the container](#running-pyshopify-in-the-container)
    - [Setting up a cron job](#setting-up-a-cron-job)

## Data Returned

The following is a brief summary of the data being returned. The keys of the return dictionary match the table names of the database structure. The DataFrame columns match the columns of each table. For a detailed view of the structure of each DataFrame, see the database documentation.

### Orders Data

| Key/Table                                           | Description                                                                               |
|-----------------------------------------------------|-------------------------------------------------------------------------------------------|
| [Orders](docs/Tables/dbo.Orders.md)                 | Order ID's, date, pricing details, fulfilment status, financial status                    |
| [OrderAttr](docs/Tables/dbo.OrderAttr.md)           | Attribution details of each order - landing page, source url, referral url, campaign      |
| [OrderPrices](docs/Tables/dbo.OrderPrices.md)           | Prices, discounts and charges for each order.      |
| [LineItems](docs/Tables/dbo.LineItems.md)           | Order line items with order ID, date, quantity, product/variant ID's, sku, title, pricing |
| [Adjustments](docs/Tables/dbo.Adjustments.md)       | Order Refund Adjustments                                                                  |
| [DiscountApps](docs/Tables/dbo.DiscountApps.md)     | Discount Applications for Each Order                                                      |
| [DiscountCodes](docs/Tables/dbo.DiscountCodes.md)   | Discount Codes In Use for Each Order                                                      |
| [RefundLineItem](docs/Tables/dbo.RefundLineItem.md) | Refunded Units                                                                            |
| [Refunds](docs/Tables/dbo.Refunds.md)               | Order Refunds                                                                             |
| [ShipLines](docs/Tables/dbo.ShipLines.md)           | Order ID, shipping pricing, carrier, code, source, title                                  |

### Customers Data

| Key/Table                                           | Description                                                        |
|-----------------------------------------------------|--------------------------------------------------------------------|
| [Customers](docs/Tables/dbo.Customers.md)           | Customer purchase totals, numbers of orders, last order, geography |

### Product Data

| Name                                               | Description                                     |
|----------------------------------------------------|-------------------------------------------------|
| [dbo.Products](Tables/dbo.Products.md)           | Product & Listing Data                                |
| [dbo.Variants](Tables/dbo.Variants.md)           | Product Variant details & Inventory                                |
| [dbo.ProductOptions](Tables/dbo.ProductOptions.md)           | Product & variant options configurations                          |
|[dbo.InventoryLevels](Tables/dbo.InventoryLevels.md)|Inventory Levels for items at each inventory location|
|[dbo.InventoryLocations](Tables/dbo.InventoryLocations.md)|Inventory locations |

## Configuration

The application can be configured three ways, starting with the lowest priority:

1. Default configuration - loaded automatically
2. Reading Environment Variables. When using the included docker container, these environment variables are automatically set from docker compose.
3. File named `config.ini` in current working directory or with relative or absolute file path passed in as an argument `app = pyshopify.ShopifyApp(config_dir='/home/user/app/config.ini')`.
4. Configuration dictionary with 'shopify', 'sql' and/or 'csv' keys as the ini file is structured.

### Default Configuration

This is the default configuration automatically passed to `ShopifyApp` instance.

```python
default_configuration = {
    'shopify': {
        'items_per_page': 250,
        'days': 7,
        'admin_ep': '/admin/api/',
        'customers_ep': 'customers.json',
        'orders_ep': 'orders.json',
        'version': '2022-07',
        'time_zone': 'America/New_York',
    },
    'sql': {
        'windows_auth': False,
        'db': 'shop_rest',
        'schema': 'dbo',
        'server': 'localhost',
        'port': 1433,
        'user': 'shop_user',
    },
    'csv': {
        'filepath': 'csv_export',
    },
}
```

### Environment Variables

```bash
# Shopify Environment Variables
$ export SHOPIFY_ACCESS_TOKEN=<your access token>
$ export SHOPIFY_STORE_NAME=<your store name>
$ export SHOPIFY_API_VERSION=<Shopify api version> # ex. 2022-07
# SQL Server Environment Variables
$ export SHOPIFY_DB_USER=<your shopify db user>
$ export SHOPIFY_DB_PASSWORD=<your shopify db password>
$ export SHOPIFY_DB_NAME=<your shopify db name>
$ export SHOPIFY_DB_SERVER=<your db server>
$ export SHOPIFY_DB_SCHEMA=<your schema name>
```

### Example `config.ini` Configuration

The python script is configured through an ini based file using `configparser`. This is a template with all possible options:

```ini
[shopify]
# Optional Configuration
orders_ep = orders.json
customers_ep = customers.json
api_version = 2022-07
api_path = /admin/api/
items_per_page = 250

# Required Configuration
store_name = ***STORE-NAME-IN-ADMIN-URL***
# Shopify Access Token
access_token = ***ACCESS TOKEN FROM ADMIN***

# Uncomment to get data between two dates
# Overrides past days of history - Can be in 'YYYYMMDD' or 'MM-DD-YYYY' format
# start = 20210610
# end = 20210617

# Get past days of history - 7 days is default
days = 30

[sql]
# Driver for pyodbc to use
driver = ODBC Driver 18 for SQL Server

# Database server & port
server = ***DATABASE SERVER***
port = 1433
database = ***DATABASE***
schema = dbo
# Database user & password
db_user = ***DB USER***
db_pass = ***DB PASSWORD***

windows_auth = False

[csv]
# Relative filepath of csv folder output
filepath = csv_export
```

### Configuration Dictionary

```python
from pyshopify.runner import ShopifyApp
configuration = {
    "shopify": {
        "access_token": "<your api key>",
        "store_name": "<your store name>",
        "api_version": "2022-07",
        "days": 7,
    },
    "sql": {
        "db": "shop_rest",
        "server": "localhost",
        "port": 1433,
        "db_user": "shop_user",
        "db_pass": "StrongerPassword1!",
        "schema": "dbo",
    },
    "csv": {
        "filepath": "csv_export",
    }
}

app = ShopifyApp(config_dict=configuration)

```

___

## Installation

### Base Library

Install from PyPi through `pip install`. This will install all required dependencies for running to export to CSV and return a dictionary of dataframes.

```shell script
python3 -m pip install pyshopify
```

### Library with SQL Driver

In order to use the sql output feature, the Microsoft ODBC driver, ODBC headers and SQL python packages need to be installed. \

### Installing ODBC Driver

On linux, msodbc18 needs to be installed first, then unixodbc headers. This is an example on Ubuntu (only compatible with 18.04, 20.04 & 21.04):

```shell script
$ sudo su
# Install curl and gnupg2 if needed
$ apt update && apt install curl gnupg2 lsb_release
# Add Microsoft's Repository
$ curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
$ curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list > /etc/apt/sources.list.d/mssql-release.list
# Install ODBC Driver and unixodbc-dev headers
$ apt update && apt install -y msodbcsql18 unixodbc-dev
```

The Windows ODBC driver can be found here [Microsoft SQL OBC Driver](https://docs.microsoft.com/en-us/sql/connect/odbc/windows/system-requirements-installation-and-driver-files?view=sql-server-ver15#installing-microsoft-odbc-driver-for-sql-server)

### Installing Python SQL Dependencies

On Ubuntu or WSL:

```shell script
# Install python & venv if needed
$ apt install python3.9 python3.9-dev python3-pip python3-venv git
$ exit # exit sudo
$ cd ~
$ python3.9 -m venv ~/venv 
$ git clone https://github.com/webdjoe/pyshopify.git
$ source ~/venv/bin/activate && pip install -r ./pyshopify/requirements.txt
```

___

## Running in a Python Script

The primary class is `ShopifyApp()` which contains the necessary execution methods.

Can be run two ways:

### Instantiating Class

Instantiating `ShopifyApp()` from the `pyshopify.runner` module. To get a dictionary of dataframes:

```python
from pyshopify.runner import ShopifyApp

# Instantiate ShopifyApp() with a configuration dictionary or absolute or relative location of config.ini file
shop_instance = ShopifyApp(config_dir='rel/dir/to/config.ini')

# Use configuration dictionary above to instantiate ShopifyApp()
shop_instance = ShopifyApp(config_dict=configuration)
```

### Updating Configuration

The configuration can be updated at any point with the `update_config()` method. This can update the dates or time period of the export.

#### Full Configuration Dictionary

A full configuration dictionary can be passed to `update_config()` and all methods that output to csv or sql server. A full configuration dictionary can hav sql, csv & shopify keys.

```python
app = ShopifyApp()
updated_config = {
    "shopify": {
        "start": "20220110",
        "end": "20220217",
    },
    "sql": {
        "db": "shop_rest"
    }
}
app.update_config(updated_config)

# Methods that write to csv or sql, accept the full configuration dictionary
full_config = {
    "shopify": {
        "days": 30
    },
    "sql": {
        "server": "localhost"
    }
}
app.write_sql(config=full_config)
```

#### Shopify Configuration Dictionary

Methods that return or yield data, such as `orders/customers_full_df()`, `orders/customers_iterator()` and `get_full_df()` accept a shopify configuration dictionary. This is the `shopify` key from the full configuration dictionary. The date values passed here override the dates in the configuration file.

```python
# Methods that return or yield datasets accept only the shopify configuration section
shopify_config = {
    "days": 30
}
app.get_full_sales_df(shopify_config=shopify_config)

```

### Product and Inventory Data

Products and variant data can be pulled into a dictionary of DataFrames or written to SQL Server or a CSV file.

#### Methods that Return Products and Inventory Data

These methods retrieve inventory locations, inventory levels and product details into a dictionary of DataFrames. The dictionary keys are the respective table names with the same columns.

```python
from pyshopify.runner import ShopifyApp()
app = ShopifyApp()

# Get DataFrame of inventory levels
# Specify product_ids, variant_ids or location_ids to filter the data
inventory_levels = app.inventory_table(product_ids=[],
                                       variant_ids=[],
                                       location_ids=[])
# Returns DataFrame of inventory items with product & variant id & title
# Returns:
# DataFrame(columns=[
# 'product_id', 'variant_id', 'sku', 'product_title', 'variant_title',
# 'available', 'location_id'])



# Get inventory levels, locations, product, variant and options details in a dictionary of dataframes
# DataFrames have same columns and types as the associated Table
product_details = app.get_products()
product_details.items() 
# Returns: 
#  [(Products DataFrame)
#  (Variants, DataFrame),
#  (ProductOptions, DataFrame),
#  (InventoryLocations, DataFrame),
#  (InventoryLevels, DataFrame)]


# Get product, variant and options details in a dictionary of dataframes
# DataFrames have same columns and types as the associated Table
product_details = app.get_products()
product_details.items()
# Returns:
#  [(Products DataFrame)
#  (Variants, DataFrame),
#  (ProductOptions, DataFrame)]

# Get inventory levels at specific or all locations
# Locations can be passed as a list or comma separated string of location ID's
# Get location ID's from the get_inventory_locations() method
inventory_levels = app.get_inventory_levels(locations=[])
inventory_levels.items()
# Returns: 
#  [(InventoryLocations, DataFrame),
#  (InventoryLevels, DataFrame)]

# Get Dictionary with DataFrame of locations inventory is being held
inv_locations = app.get_inventory_locations()
inv_locations
# Returns:
# {"InventoryLocations": DataFrame(
# columns=['id', 'name', 'address1', 'address2',
#          'city', 'province', 'country', 'zip',
#          'phone', 'active', 'updated_at'])}

```

#### Methods that Write Inventory and Product Data

The following functions output the inventory and products data to a CSV file or SQL Server. The CSV file will be written to the directory specified in the configuration.

```python
# Write Products and All Inventory Data to CSV or SQL Server
app.products_inventory_writer(write_sql=True, write_csv=Tru, config_dict=None)

# Write products, variants & options to CSV or SQL Server
app.products_writer(config_dict=None)

# Write inventory levels to CSV or SQL
app.inventory_levels_writer(write_csv=True, write_sql=True, config_dict=None)

# Write inventory locations to CSV or SQL
app.inventory_locations_writer(write_csv=True, write_sql=True, config_dict=None)
```

### Orders and Customers Data

The following methods return the order details, pricing information and customers data. The methods return or yield a dictionary of DataFrames. The dictionary keys are the respective table names with the same columns. See the database documention for full column types and descriptions.

#### Returning Customers & Orders Data

A full customers and orders dataset can be returned with the entire date range in one dictionary of dataframes. This should only be used with smaller date ranges to avoid memory issues.

The shopify configuration can optionally be passed to these methods as a single dictionary with just the Shopify configuration.

```python
from pyshopify.runner import ShopifyApp
app = ShopifyApp()

shopify_config = {
    "access_token": "<your api key>",
    "store_name": "<your store name>",
    "api_version": "2022-07",
    "days": 7
}

# Return full orders dataset
orders = app.get_full_orders_df(shopify_config=shopify_config)
orders.items()
# Returns:
#   [('Orders', <pandas.DataFrame>),
#       ('Refunds', <pandas.DataFrame>),
#       ('LineItems', <pandas.DataFrame>),
#       ('RefundLineItem', <pandas.DataFrame>),
#       ('Adjustments', <pandas.DataFrame>),
#       ('DiscountApps', <pandas.DataFrame>),
#       ('DiscountCodes', <pandas.DataFrame>),
#       ('ShipLines', <pandas.DataFrame>),
#       ('OrderAttr', <pandas.DataFrame>)]

# Return full customers dataset
customers = app.get_full_customers_df()
customers.items()
# Returns:
#   [('Customers', <pandas.DataFrame>)]

# Return full orders and customers dataset
all_data = app.get_orders_customers_df(shopify_config=shopify_config)
all_data.items()
# Returns:
#   [('Orders', <pandas.DataFrame>),
#       ('Refunds', <pandas.DataFrame>),
#       ('LineItems', <pandas.DataFrame>),
#       ('RefundLineItem', <pandas.DataFrame>),
#       ('Adjustments', <pandas.DataFrame>),
#       ('DiscountApps', <pandas.DataFrame>),
#       ('DiscountCodes', <pandas.DataFrame>),
#       ('ShipLines', <pandas.DataFrame>),
#       ('OrderAttr', <pandas.DataFrame>),
#       ('Customers', <pandas.DataFrame>)]
```

#### Iterating through Orders and Customers Data

For larger datasets, it is recommended to use the generator methods to iterate through the paginated data. The methods yield the same structure as the `get_full_orders_df()` and `get_full_customers_df()` methods.

A [shopify configuration dictionary](#shopify-configuration-dictionary) can be passed to these methods.

```python
from pyshopify.runner import ShopifyApp
app = ShopifyApp()

# A shopify configuration dictionary can be passed to all the generator methods
for order_dict in app.orders_iterator(shopify_config=shopify_config):
    order_dict.items()
    # Returns:
    #   [('Orders', <pandas.DataFrame>),
    #       ('Refunds', <pandas.DataFrame>),
    #       ('LineItems', <pandas.DataFrame>),
    #       ('RefundLineItem', <pandas.DataFrame>),
    #       ('Adjustments', <pandas.DataFrame>),
    #       ('DiscountApps', <pandas.DataFrame>),
    #       ('DiscountCodes', <pandas.DataFrame>),
    #       ('ShipLines', <pandas.DataFrame>),
    #       ('OrderAttr', <pandas.DataFrame>)]
    #       ('OrderPrices', <pandas.DataFrame>)]

# Iterate through customers data
for customers_dict in app.customers_iterator():
    customers_dict.items()
    # Returns:
    #   [('Customers', <pandas.DataFrame>)]
```

#### Writing Orders and Customers Data to CSV and SQL Server

There are several convenience methods that can be used to write the orders and customers data to CSV and SQL Server. The sql configuration can be passed directly to these methods, as the `engine` is only created during the first SQL method and stored as an instance variable `app.engine`

#### Writing data to desired output

```python
from pyshopify.runner import ShopifyApp

# No arguments defaults to attempt to read to a config.ini file in CWD
app = ShopifyApp()

# Main method that can write order & customer data to csv/sql and set configuration. A full configuration dictionary can be passed to this method.
app.orders_customers_writer(write_csv=True, write_sql=True, config=full_config)

# Write only orders data to CSV and/or SQL
app.orders_writer(write_sql=True, write_csv=True, config=full_config)

# Write only customers data to CsV and/or SQL
app.customers_writer(write_sql=True, write_csv=True, config=full_config)

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

## Data Structure

The structure of the custom return dictionary reflects the SQL database structure that it will update. See the [database docs](docs/tables.md) for full details on each table/DataFrame.

```python
from pyshopify import ShopifyApp

# Enable custom in config.ini
shop_app = ShopifyApp()

orders_dict = shop_app.orders_full_df()

orders_dict = {
    'Orders': DataFrame,
    'Refunds': DataFrame,
    'LineItems': DataFrame,
    'RefundLineItem': DataFrame,
    'Adjustments': DataFrame,
    'DiscountApps': DataFrame,
    'DiscountCodes': DataFrame,
    'ShipLines': DataFrame,
    'OrderAttr': DataFrame
}

customers_dict = shop_app.customers_full_df()

customers_dict = {
    "Customers": DataFrame
}

```

## Database Structure

Exporting SQL from API response is two-step process:

1. Send DataFrame to temporary SQL Table
2. Run merge statement to update database tables

The full database documentation is located [here](docs/tables.md)

**`shop_rest`** is the default database name.

## Creating the Database and Tables

There are three ways to create the database and table structure - CLI command, via Python script or an SQLCMD script. All have the ability to create a new database or use an existing one. A new user can also be created with exclusive access to that database. It is recommended to create a new user instead of using the admin user. A new schema can be created or the default `dbo` schema can be used.

### CLI Command

Use the `shopify_db` command to create the database and tables.

```bash
shopify_db --help

Usage: shopify_db [OPTIONS]

  pyshopify database builder.

  Build on existing database with --tables-only New user can be created with
  --db-user and --db-pass A new schema will be built if the --schema is
  specified

  date_start will build a date dimension table starting at date_start.

Options:
  --db-tables / --tables-only  Specify whether to build  database or tables
                               only
  -s, --server TEXT            SQL Server name or IP address
  -p, --port INTEGER           SQL Server port
  --sa-user TEXT               SQL Server SA user
  --sa-pass TEXT               SQL Server SA password
  --db-name TEXT               DB to create or existing db
  --schema TEXT                Schema to create or existing schema
  --db-user TEXT               DB user to create
  --db-pass TEXT               Created DB user password
  --driver TEXT                SQL Server ODBC driver
  --date-start TEXT            Create DateDim table from starting date YYYY-
                               MM-DD
  --help                       Show this message and exit.

```

Build a new database, user and schema with the following command:

```shell
shopify_db --db-tables -s 192.168.1.202 -p 14333 \
    --sa-user sa --sa-pass TheStrongestpassword1! \
    --db-name test_shop --db-user test_shop_user --db-pass TestShopPass1! \
    --date-start 2015-01-01
```

Build tables into existing database, no new user or schema:

```shell
shopify_db --tables-only -s 192.168.1.202 -p 14333 \
    --sa-user sa --sa-pass TheStrongestpassword1! \
    --db-name test_shop --date-start 2015-01-01
```

### Programatically via Python

The `DBBuilder` class in `pyshopify.sql` can be used to create the database and tables, as well as user and/or schema.

```python
from pyshopify.sql import DBBuilder

db_builder = DBBuilder(server=localhost,
                       port=1433,
                       db_name='shop_rest',
                       sa_user='sa',
                       sa_pass='password',
                       schema='Shopify',
                       driver='ODBC Driver 17 for SQL Server',
                       windows_auth=False)
# Create database
db_builder.create_db()

# Optional but recommended, create a new login and user with appropriate permissions
db_builder.create_user('shopify_user', 'password')

# Build tables and the new schema if specified
db_builder.create_tables()

# Optional, Build DateDimension table
db_builder.create_date_dimension('2015-01-01')
```

### Using SQLCMD Script

To build the dataabse, run the [shopify.sql](scripts/shopify.sql) script in the `scripts` folder. The script should be run through `SQLCMD` with the following variables set. The database is built automatically with a new user that only has access to that database.

- **DBName** - Name of database to create for data, default `shop_rest`
- **DBUser** - Login & user to create for the shopify database, default `shop_user`
- **DBPassword** - Database user password, default `Strongerpassword1!`
- **DBSchema** - DB Schema - default `dbo`

```shell
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P "SA_User_Password" \
-v DBName="shop_rest" -v SchemaName="dbo" -v DBUser="shop_user" \
-v DBPassword="Strongerpassword1!" \
-i /usr/scripts/shopify.sql
```

If you do not want to add a new user, use `-v DBUser= "sa"` and `-v DBPassword="NotNeeded"`.

An existing database can be used by setting the `-v DBName` to the existing database name.

Pass dbo as the SchemaName to use the default db schema.

The DateDimension table is located in a separate script [scripts/`date_table.sql`](scripts/date_table.sql). It can be run with the following variables:

```shell
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P "SA_User_Password" \
-v DBName="shop_rest" -v SchemaName="dbo" -v DBUser="shop_user" \
-i date_table.sql
```

## Docker Container

The `Dockerfile` and `docker-compose.yml` files are based on the Microsoft SQL Server 2019 container running on Ubuntu 20.04. It hosts the database with the structure prebuilt and can run pyshopify from the commandline.

Both containers automatically deploy [shopify.sql](scripts/shopify.sql) to build the required database structure and create a user with access to that database.

Set environment variables and SA password to configure the database in `docker-compose.yml`. Configure a volume for CSV export if needed

The `config.ini` should be mapped to the `/root` user directory inside the container. A csv folder can also be mapped to a local folder. This should match the relative csv filepath in the configuration file. The working directory is the root user's home directory.

### Docker Compose

The docker compose file configures the db administrator and the shopify database user. The date dimension table is built based on the `STARTING_DATE` environment variable.

The default location of the `config.ini` file is in the root user dir, the container's working directory. The data directory volume is the db data folder and the csv_export folder can also be mapped to a local directory.

```yaml
version: "3.9"

services:
    sqlserver:
        build: .
        container_name: shop_sql
        hostname: shop_sql
        ports:
            - "1433:1433"
        environment:
            ACCEPT_EULA: "Y"
            SA_PASSWORD: "TheStrongestpassword1!"
            MSSQL_SA_PASSWORD: "TheStrongestpassword1!"
            SHOPIFY_DB_USER: "shop_user"
            SHOPIFY_DB_PASSWORD: "Strongerpassword1!"
            SHOPIFY_DB_NAME: "shop_rest"
            SHOPIFY_DB_SCHEMA: "dbo"
            STARTING_DATE: "2019-01-01"
            CONFIG_FILE: "/root/config.ini"
        volumes:
            - "./csv_export:/root/csv_export"
            - "./data:/var/opt/mssql"
            - "./config.ini:/root/config.ini"

```

### Creating a Container

To create a container:

```shell script
git clone https://github.com/webdjoe/pyshopify
# edit the docker compose env var with vim or nano
vim docker-compose.yml

# edit config.ini file
vim config.ini

# Build and run container
sudo docker compose build
sudo docker compose up
```

Once started test if SQL server is running. A `0` return value indicates the server has started up and is ready for connections. The shopify.sql script should have already run to build the necessary database.

```shell script
 sudo docker exec -it shop_sql bash -c '/opt/mssql-tools/bin/sqlcmd -h -1 -t 1 -U sa\
 -P "$MSSQL_SA_PASSWORD" -Q "SET NOCOUNT ON; Select SUM(state) from sys.databases"'
```

### Running pyshopify in the container

`shopify_cli` can be called in container to pull data and send to database or csv files.

```shell script
# Get last 30 days of data and import into SQL Server running in container
sudo docker exec -it shop_sql shopify_cli -d 30 --sql-out

# Get data between dates and import into SQL Server
sudo docker exec -it shop_sql shopify_cli -b 2020-01-01 2020-12-31 --sql-out

# Pull 30 days of data into csv files
sudo docker exec -it shop_sql shopify_cli --csv-out --csv-location csv_export
```

### Setting up a cron job

A script is included to automatically set up a cron job to run `shopify_cli` to pull the last 5 days of data, every day at 4AM.

```shell
sudo docker exec -it shop_sql bash /usr/scripts/add-cron.sh
```
