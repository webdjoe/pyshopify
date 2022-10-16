# Shopify Orders Rest API Wrapper and Data Export

pyShopify is a python wrapper for Shopify's REST API that pulls and inserts store data into a relational database and exports to a CSV file. This library is compatible with Microsoft SQL Server, MariaDB, and MySQL.

This has the flexibility of exporting the data to MS SQL Server or MySQL (and MariaDB), exporting to csv and yielding or returning a dictionary of dataframes.

The Structure of the Database is described in depth in the [Docs](docs) folder. The database can be built through the `shopify_db` CLI command or programmatically.

This requires the creation of a private app in the Shopify Admin center -> Setting -> Apps and Sales Channels -> Develop Apps.

## Table of Contents

- [Shopify Orders Rest API Wrapper and Data Export](#shopify-orders-rest-api-wrapper-and-data-export)
  - [Table of Contents](#table-of-contents)
  - [Data Returned](#data-returned)
    - [Orders Data](#orders-data)
    - [customers Data](#customers-data)
    - [Product Data](#product-data)
  - [Configuration](#configuration)
    - [Default Configuration](#default-configuration)
    - [Environment Variables](#environment-variables)
    - [Example `config.ini` Configuration](#example-configini-configuration)
      - [`config.ini` Sections](#configini-sections)
      - [MS SQL `config.ini` Section](#ms-sql-configini-section)
    - [Configuration Dictionary](#configuration-dictionary)
  - [Installation](#installation)
    - [SQL Driver Requirements](#sql-driver-requirements)
      - [Installing MySQLdb (MySQLClient) Driver](#installing-mysqldb-mysqlclient-driver)
      - [Installing pyMySQL Driver](#installing-pymysql-driver)
    - [Installing MS SQL ODBC Driver](#installing-ms-sql-odbc-driver)
    - [Installing Python and Virtual Environment](#installing-python-and-virtual-environment)
  - [Creating the Database and Tables](#creating-the-database-and-tables)
    - [CLI Command](#cli-command)
    - [Programatically via Python](#programatically-via-python)
  - [Using the Python Interface](#using-the-python-interface)
    - [Instantiating the `ShopifyApp` Class](#instantiating-the-shopifyapp-class)
    - [Updating Configuration](#updating-configuration)
    - [Product and Inventory Data](#product-and-inventory-data)
      - [Methods that Return products and Inventory Data](#methods-that-return-products-and-inventory-data)
        - [Get All Product, Variant and Product Option DataFrames](#get-all-product-variant-and-product-option-dataframes)
        - [Get Inventory Levels and Locations Details](#get-inventory-levels-and-locations-details)
      - [Methods that Write Inventory and Product Data](#methods-that-write-inventory-and-product-data)
    - [Orders and customers Data](#orders-and-customers-data)
      - [Returning/Yielding customers & Orders Data](#returningyielding-customers--orders-data)
      - [Writing Orders and Customers Data](#writing-orders-and-customers-data)
      - [Writing Data to Desired Output](#writing-data-to-desired-output)
    - [Writing All Data to DB or CSV](#writing-all-data-to-db-or-csv)
  - [Running as Command Line Application](#running-as-command-line-application)
  - [Data Structure](#data-structure)
  - [Docker Container](#docker-container)
    - [Docker Compose](#docker-compose)
      - [MS SQL Docker Container](#ms-sql-docker-container)
      - [MySQL Docker Container](#mysql-docker-container)
    - [Creating a Container](#creating-a-container)
    - [Running pyshopify in the container](#running-pyshopify-in-the-container)

## Data Returned

The following is a brief summary of the data being returned. The keys of the return dictionary match the table names of the database structure. The DataFrame columns match the columns of each table. For a detailed view of the structure of each DataFrame, see the database documentation.

### Orders Data

| Key/Table                                           | Description                                                                               |
|-----------------------------------------------------|-------------------------------------------------------------------------------------------|
| [orders](docs/Tables/orders.md)                 | Order ID's, date, pricing details, fulfilment status, financial status                    |
| [order_attr](docs/Tables/order_attr.md)           | Attribution details of each order - landing page, source url, referral url, campaign      |
| [order_prices](docs/Tables/order_prices.md)           | Prices, discounts and charges for each order.      |
| [line_items](docs/Tables/line_items.md)           | Order line items with order ID, date, quantity, product/variant ID's, sku, title, pricing |
| [adjustments](docs/Tables/adjustments.md)       | Order Refund adjustments                                                                  |
| [discount_apps](docs/Tables/discount_apps.md)     | Discount Applications for Each Order                                                      |
| [discount_codes](docs/Tables/discount_codes.md)   | Discount Codes In Use for Each Order                                                      |
| [refund_line_item](docs/Tables/refund_line_item.md) | Refunded Units                                                                            |
| [refunds](docs/Tables/refunds.md)               | Order refunds                                                                             |
| [ship_lines](docs/Tables/ship_lines.md)           | Order ID, shipping pricing, carrier, code, source, title                                  |

### customers Data

| Key/Table                                           | Description                                                        |
|-----------------------------------------------------|--------------------------------------------------------------------|
| [customers](docs/Tables/customers.md)           | Customer purchase totals, numbers of orders, last order, geography |

### Product Data

| Name                                               | Description                                     |
|----------------------------------------------------|-------------------------------------------------|
| [products](docs/Tables/products.md)           | Product & Listing Data                                |
| [variants](docs/Tables/variants.md)           | Product Variant details & Inventory                                |
| [product_options](docs/Tables/product_options.md)           | Product & variant options configurations                          |
|[inventory_levels](docs/Tables/inventory_levels.md)|Inventory Levels for items at each inventory location|
|[inventory_locations](docs/Tables/inventory_locations.md)|Inventory locations |

## Configuration

The application can be configured three ways, starting with the lowest priority:

1. Default configuration - loaded automatically
2. Reading Environment Variables. When using the included docker container, these environment variables are automatically set from docker compose.
3. File named `config.ini` in current working directory or with relative or absolute file path passed in as an argument `app = pyshopify.ShopifyApp(config_dir='/home/user/app/config.ini')`.
4. Configuration dictionary with 'shopify', 'sql' and/or 'csv' keys as the ini file is structured.

### Default Configuration

**Note** Schema is based on the MS SQL Server construct, not MySQL. MySQL does not have schemas in the same sense as MSSQL, therefore it will have no impact if defined for a MySQL database.

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
        'connector': 'mssql+pyodbc',
        'windows_auth': False,
        'db': 'shop_rest'
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

The python script is configured through an ini based file using `configparser`.

#### `config.ini` Sections

This is the structure of the `config.ini` file. The sections are `shopify`, `sql` and `csv`. The `shopify` and `sql` sections are required, the and `csv` section is optional.

The date range to pull the data can be set to the last number of days using `days` or a specific date range using `start` and `end`. If both are set, `start_end` and `end_date` will take precedence.

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

[csv]
# Relative directory for CSV exports
filepath = csv_export

[sql]
# Configuration for Database - See sections below
```

#### MS SQL `config.ini` Section

The following is an example of `config.ini` section for Microsoft SQL Server. The connector is `mssql+pyodbc`. To use windows authentication, set `windows_auth` to True, it defaults to False. The `db` is the database of tables. If no schema is set, `dbo` will be used.

`port` is optional, if not set, the default port for the connector will be used.

```ini
[shopify]
...
...

[sql]
# DB dialect & driver - first part of connection string -eg mssql-pyodbc, mysql-pymysql
connector = mssql+pyodbc
; connector = mysql+mysqldb
# Database server & port - localhost for docker container
server = ***SERVER_ADDRESS***
port = 1433
database = shop_rest
# Schema is optional, based on MSSQL construct (no impact for MySQL)
schema = dbo
# Database user & password
db_user = ***DB_USER***
db_pass = ***DATABASE_PW***
# Authenticate with Windows User
windows_auth = False
# Query to add to connection string - This is optional, the available ODBC Driver for SQL Server will automatically be detected
# Ensure to indent any subsequent lines
; connect_query = driver:ODBC Driver 17 for SQL Server
;     TrustedServerCertificate:yes
;     encrypt:no
```

**MySQL Configuration**
Both `mysql+pymysql` and `mysql+mysqldb` are supported. This is the new version of mysqldb - [MySQLClient](https://github.com/PyMySQL/mysqlclient). Other drivers have not been tested.

```ini

[shopify]
...
...

[csv]
...

[sql]
# DB dialect & driver - first part of connection string -eg mssql-pyodbc, mysql-pymysql
connector = mssql+pyodbc
; connector = mysql+mysqldb
# Database server & port - localhost for docker container
server = ***SERVER_ADDRESS***
port = 1433
database = shop_rest
# Database user & password
db_user = ***DB_USER***
db_pass = ***DATABASE_PW***
# Authenticate with Windows User
windows_auth = False

```

### Configuration Dictionary

The configuration dictionary overrides the `config.ini` file. It follows the same structure of the `config.ini` file.

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
        "connector": "mssql+pyodbc",
        "db": "**DB_NAME**",
        "server": "**SERVER_ADDRESS**",
        "port": 1433,
        "db_user": "**DB_USER**",
        "db_pass": "**DB_PASS**",
        "schema": "dbo",
        "connect_query": {
            "driver": "ODBC Driver 17 for SQL Server",
            "TrustedServerCertificate": "yes",
            "encrypt": "no"
        }
    },
    "csv": {
        "filepath": "csv_export",
    }
}

app = ShopifyApp(config_dict=configuration)

```

___

## Installation

### SQL Driver Requirements

Before pyShopify can be installed, the appropriate requirements for the SQL driver must be installed. The following drivers are supported:

- [pyodbc](https://github.com/mkleehammer/pyodbc/wiki/Install) - SQL Server Driver, requires additional installation steps.
- [pymysql](https://github.com/PyMySQL/PyMySQL) - Pure python MySQL driver, the easiest to install, no prerequisites needed.
- [mysqldb](https://github.com/PyMySQL/mysqlclient) - New fork of C-based MySQLdb driver. Faster than pymysql but requires additional installation steps.

#### Installing MySQLdb (MySQLClient) Driver

The MySQLdb driver (MySQLClient) requires MySQL C libraries if building from source. On Windows, the [MariaDB C Connecter](https://mariadb.com/downloads/connectors/) may be required.

On Ubuntu, the following packages should be first installed:

```bash
apt install -y build-essential libssl-dev python3-dev libmysqlclient-dev
```

Then install the python package:

```bash
python3 -m pip install mysqlclient
```

The python package can also be installed with the pyshopify package: `pip install pyshopify[mysqldb]`

#### Installing pyMySQL Driver

It's pure python, so it's as simple as:

```bash
pip install pymysql
```

Note: you can also use the pip extras to install the python package `pip install pyshopify[pymysql]`

### Installing MS SQL ODBC Driver

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

### Installing Python and Virtual Environment

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

## Creating the Database and Tables

The database and table structure can be created one of two ways - CLI command or via Python script. All have the ability to create a new database or use an existing one. A new user can also be created with exclusive access to that database. It is recommended to create a new user instead of using the admin user when running the script. A new schema can also be created in MSSQL or the default `dbo` schema can be used.

### CLI Command

Use the `shopify_db` command to create the database and tables.

```bash
shopify_db --help

Usage: shopify_db [OPTIONS]

  pyshopify database builder.

  Build on existing database with --tables-only
  New user can be created with --db-user and --db-pass
  For MSSQL, --schema will be created if it does not exist

  specifying date_start will build a date dimension table starting at date_start.

Options:
  --db-tables / --tables-only  Specify whether to build  database or tables
                               only
  -c, connector TEXT           Database connector - mysql+mysqldb, mysql+pymysql, mssql+pyodbc
  -s, --server TEXT            SQL Server name or IP address
  -p, --port INTEGER           SQL Server port
  -U, --sa-user TEXT           SQL Server SA user
  -W, --sa-pass TEXT           SQL Server SA password
  -d, --db-name TEXT           DB to create or existing db
  --schema TEXT                Schema to create or existing schema
  --db-user TEXT               DB user to create
  --db-pass TEXT               Created DB user password
  --driver TEXT                SQL Server ODBC driver
  --date-start TEXT            Create DateDim table from starting date YYYY-
                               MM-DD
  --help                       Show this message and exit.

```

Build a new MSSQL database, user and schema with the following command:

```shell
shopify_db -c mssql+pyodbc -s localhost -p 1433 \
    -U sa -W TheStrongestpassword1! -d test_shop \
    --db-user test_shop_user --db-pass TestShopPass1! \
    --schema NewSchema --date-start 2015-01-01
```

Build tables into existing MSSQL database, no new user or schema:

```shell
shopify_db --tables-only -s localhost -p 1433 \
    -U sa -W TheStrongestpassword1! -d test_shop \
    --date-start 2015-01-01
```

Build a new MySQL database and user with the following command:

```shell
shopify_db -c mysql+pymysql -s localhost -p 3306 \
    -U sa -W TheStrongestpassword1! -d test_shop \
    --db-user test_shop_user --db-pass TestShopPass1! \
```

### Programatically via Python

The `DBBuilder` class in the `pyshopify.sql` module can be used to create the database and tables, as well as user and/or schema.

```python
from pyshopify.sql import DBBuilder

# port, schema, driver and connect_query are optional for MSSQL
# Schema and driver have no impact on MySQL
db_builder = DBBuilder(connector='mssql+pyodbc',
                       server=localhost,
                       port=1433,
                       db_name='shop_rest',
                       sa_user='sa',
                       sa_pass='password',
                       schema='Shopify',
                       driver='ODBC Driver 17 for SQL Server',
                       connect_query={'TrustedServerCertificate':'yes'},
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

___

## Using the Python Interface

The primary class is `pyshopify.runner.ShopifyApp()` which contains the necessary execution methods.

### Instantiating the `ShopifyApp` Class

Instantiate `ShopifyApp` from the `pyshopify.runner` module.

```python
from pyshopify.runner import ShopifyApp

# Instantiate ShopifyApp() with a configuration dictionary or absolute or relative location of config.ini file
shop_instance = ShopifyApp(config_dir='rel/dir/to/config.ini')

# Use configuration dictionary above to instantiate ShopifyApp()
shop_instance = ShopifyApp(config_dict=configuration)
```

### Updating Configuration

The configuration can be updated at any point with the `update_config()` method. This can update the dates or time period of the export. Any date periods specified will override the current configuration, regardless of precedence.

```python
# A full or partial configuration dictionary can be passed to update_config()
updated_config = {
    'shopify': {
      'start': '2020-01-01',
      'end': '2020-01-31'
    }
}

shop_instance.update_config(updated_config)
```

### Product and Inventory Data

Product and variant data can be pulled into a dictionary of DataFrames or written to SQL Server or a CSV file.

#### Methods that Return products and Inventory Data

These methods retrieve inventory locations, inventory levels and product details into a dictionary of DataFrames. The dictionary keys are the respective table names with the same columns.

**Get Inventory Levels at all locations**
The `inventory_table()` method returns a single dataframe with the product and variant id and title at all inventory locations. The method accepts lists or comma separated strings of product ids, variant ids and location_id. If no ids are specified, all products and variants will be returned.

```python
from pyshopify.runner import ShopifyApp()
app = ShopifyApp()

inventory_levels = app.inventory_table(product_ids=[],
                                       variant_ids=[],
                                       location_ids=[])
# Returns DataFrame of inventory items with product & variant id & title
# Returns:
# DataFrame(columns=[
# 'product_id', 'variant_id', 'sku', 'product_title', 'variant_title',
# 'available', 'location_id'])
```

**Get All Products and Inventory Detail DataFrames**
The `get_products_inventory()` method returns a dictionary of DataFrames with product, variant, product option, inventory locations & inventory levels. The dictionary keys are the respective table names with values containing a dataframe of the associated table structure.

```python
product_details = app.get_products_inventory()
product_details.items() 
# Returns: 
#  [(products DataFrame)
#  (variants, DataFrame),
#  (product_options, DataFrame),
#  (inventory_locations, DataFrame),
#  (inventory_levels, DataFrame)]
```

##### Get All Product, Variant and Product Option DataFrames

The `get_products()` method returns a dictionary of DataFrames containing the product, variant and product option data. The dictionary keys are the respective table names with values containing a dataframe of the associated table structure.

The variants table contains the quantity of product that is available accross all locations.

```python
product_details = app.get_products()
product_details.items()
# Returns:
#  [(products DataFrame)
#  (variants, DataFrame),
#  (product_options, DataFrame)]
```

##### Get Inventory Levels and Locations Details

The `get_inventory_levels()` method returns a dictionary of DataFrames containing the inventory levels and inventory locations data. The dictionary keys are the respective table names with values containing a dataframe of the associated table structure.

A list or comma separated string of location ids can be passed to filter the inventory levels to the specified locations.

```python
# Get inventory levels at specific or all locations
# Locations can be passed as a list or comma separated string of location ID's
# Get location ID's from the get_inventory_locations() method
inventory_levels = app.get_inventory_levels(locations=[])
inventory_levels.items()
# Returns: 
#  [(inventory_levels, DataFrame)]
```

The `get_inventory_locations()` method returns a dictionary containing a DataFrame of inventory locations.

```python
# Get Dictionary with DataFrame of locations inventory is being held
inv_locations = app.get_inventory_locations()
inv_locations
# Returns:
# {"inventory_locations": DataFrame(
# columns=['id', 'name', 'address1', 'address2',
#          'city', 'province', 'country', 'zip',
#          'phone', 'active', 'updated_at'])}
```

#### Methods that Write Inventory and Product Data

The following functions output the inventory and products data to a CSV file or SQL Server. The CSV file will be written to the directory specified in the configuration.

A configuration dictionary can be passed to each method to override the current configuration. The configuration dictionary can be a full or partial configuration dictionary.

```python
# Write All products and All Inventory Data to CSV or SQL Server
app.products_inventory_writer(write_sql=True, write_csv=Tru, config_dict=None)

# Write products, variants & options to CSV or SQL Server
app.products_writer(config_dict=None)

# Write inventory levels to CSV or SQL
app.inventory_levels_writer(write_csv=True, write_sql=True, config_dict=None)

# Write inventory locations to CSV or SQL
app.inventory_locations_writer(write_csv=True, write_sql=True, config_dict=None)
```

### Orders and customers Data

The following methods return the order details, pricing information and customers data. The methods return or yield a dictionary of DataFrames. The dictionary keys are the respective table names with the same columns. See the database documention for full column types and descriptions.

#### Returning/Yielding customers & Orders Data

The customers and orders data can be returned or yielded, in addition to written to the database or CSV file. A full or partial configuration dictionary can be passed to these methods to override the current configuration.

All of these methods can accept a configuration dictionary with just the shopify section.

**Shopify Configuration Dictionary**
The shopify configuration dictionary is the sql section of `config.ini`

```python
shop_config = {
  'start': '2020-06-01',
  'end': '2020-06-30'
}
```

**Get Full Customers and Orders DataFrames**
This method will return a full dataset of customers and orders DataFrames for the specified time period. The method returns a dictionary of DataFrames with the dictionary keys being the respective table names.

These methods are not recommended for large time periods due to memory constraints.

```python
from pyshopify.runner import ShopifyApp
app = ShopifyApp()

shopify_config = {
    "access_token": "<your api key>",
    "store_name": "<your store name>",
    "api_version": "2022-07",
    "days": 7
}

# Return full customers and orders dataset
orders = app.get_orders_customers_df(shopify_config=shopify_config)
orders.items()
# Returns:
#   [('customers', <pandas.DataFrame>),
#       ('Orders', <pandas.DataFrame>),
#       ('refunds', <pandas.DataFrame>),
#       ('line_items', <pandas.DataFrame>),
#       ('refund_line_item', <pandas.DataFrame>),
#       ('adjustments', <pandas.DataFrame>),
#       ('discount_apps', <pandas.DataFrame>),
#       ('discount_codes', <pandas.DataFrame>),
#       ('ship_lines', <pandas.DataFrame>),
#       ('order_prices', <pandas.DataFrame>),
#       ('order_attr', <pandas.DataFrame>)]

# Return full customers dataset
customers = app.get_full_customers_df()
customers.items()
# Returns:
#   [('customers', <pandas.DataFrame>)]

# Return full orders and customers dataset
all_data = app.get_full_orders_df(shopify_config=shopify_config)
all_data.items()
# Returns:
#   [('Orders', <pandas.DataFrame>),
#       ('refunds', <pandas.DataFrame>),
#       ('line_items', <pandas.DataFrame>),
#       ('refund_line_item', <pandas.DataFrame>),
#       ('adjustments', <pandas.DataFrame>),
#       ('discount_apps', <pandas.DataFrame>),
#       ('discount_codes', <pandas.DataFrame>),
#       ('ship_lines', <pandas.DataFrame>),
#       ('order_prices', <pandas.DataFrame>),
#       ('order_attr', <pandas.DataFrame>)]
```

**Iterating through Orders and customers Data**
For larger datasets, it is recommended to use the generator methods to iterate through the paginated data. The methods yield the same structure as the `get_full_orders_df()` and `get_full_customers_df()` methods.

A [shopify configuration dictionary](#returningyielding-customers--orders-data) can be passed to these methods as well.

```python
from pyshopify.runner import ShopifyApp
app = ShopifyApp()

# A shopify configuration dictionary can be passed to all the generator methods
for order_dict in app.orders_iterator(shopify_config=shopify_config):
    order_dict.items()
    # Returns:
    #   [('Orders', <pandas.DataFrame>),
    #       ('refunds', <pandas.DataFrame>),
    #       ('line_items', <pandas.DataFrame>),
    #       ('refund_line_item', <pandas.DataFrame>),
    #       ('adjustments', <pandas.DataFrame>),
    #       ('discount_apps', <pandas.DataFrame>),
    #       ('discount_codes', <pandas.DataFrame>),
    #       ('ship_lines', <pandas.DataFrame>),
    #       ('order_attr', <pandas.DataFrame>)]
    #       ('order_prices', <pandas.DataFrame>)]

# Iterate through customers data
for customers_dict in app.customers_iterator():
    customers_dict.items()
    # Returns:
    #   [('customers', <pandas.DataFrame>)]
```

#### Writing Orders and Customers Data

There are several convenience methods that can be used to write the orders and customers data to CSV and SQL Server. The sql configuration can be passed directly to these methods, as the `engine` is only created during the first SQL method and stored as an instance variable `app.engine`

#### Writing Data to Desired Output

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

### Writing All Data to DB or CSV

A convenience method can be used to write all data to the database or CSV. This accepts a full configuration dictionary.

```python
from pyshopify.runner import ShopifyApp

app = ShopifyApp()

# Write product, inventory, customers, and orders data to db
app.write_all_to_sql(config=full_config)

# Write product, inventory, customers, and orders data to csv
app.write_all_to_csv(config=full_config)
```

## Running as Command Line Application

The command line application `shopify_cli` can output the data to CSV or SQL Server. The command line application can be run with the following command:

From command line:

```bash
# There are different command options
$ shopify_cli --help
Usage: shopify_cli [OPTIONS]

  Run Shopify App CLI.

  Use -d or --days to get days of history, default 7 Use -b or --between to
  get data between 2 dates - yyyy-MM-dd yyyy-MM-dd,

  --config is the relative or absolute location of config.ini

Options:
  --all                  Get all product, order and customer data
  --orders               Get orders data
  --customers            Get customers data
  --products             Get products data
  -d, --days INTEGER     get days of history, default 7
  -b, --between TEXT...  get between 2 dates - yyyy-MM-dd,ex -b 2020-01-01
                         2020-01-02
  --sql-out / --no-sql   write to database - Default False
  --csv-out / --no-csv   Write results to csv files - Default true
  --csv-location TEXT    Relative folder of csv export folderdefaults to
                         csv_export/
  --config TEXT          Relative location of config.ini - defaultsto
                         config.ini in currect directory

# Write last 30 days of all data to DB
$ shopify_cli --all -d 30 --sql-out --config config.ini

# Write 30 days of only orders data to CSV
$ shopify_cli --orders -d 30 --csv-out --config config.ini

# Get customers created between 2 dates
$ shopify_cli --customers -b 2020-01-01 2020-01-02 --sql-out
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
    'refunds': DataFrame,
    'line_items': DataFrame,
    'refund_line_item': DataFrame,
    'adjustments': DataFrame,
    'discount_apps': DataFrame,
    'discount_codes': DataFrame,
    'ship_lines': DataFrame,
    'order_attr': DataFrame,
    'order_prices': DataFrame
}

customers_dict = shop_app.customers_full_df()

customers_dict = {
    "customers": DataFrame
}

```

## Docker Container

There are two docker containers that can be used to run the application - an MS SQL based container and a MySQL based container. They are located in the respective docker folders, [docker-mysql](docker-mysql) and [docker-mssql](docker-mssql). Set the environment variables in the docker-compose.yml file before running.

Both containers have the same structure and can be used interchangeably. The only difference is the database engine used.

Set environment variables and SA password to configure the database in `docker-compose.yml`. Configure a volume for CSV export if needed

The `config.ini` should be mapped to the `/root` user directory inside the container. A csv folder can also be mapped to a local folder. This should match the relative csv filepath in the configuration file. The working directory is the root user's home directory.

### Docker Compose

The docker compose file configures the db administrator and the shopify database user. The date dimension table is built based on the `STARTING_DATE` environment variable.

The default location of the `config.ini` file is in the root user dir, the container's working directory. The data directory volume is the db data folder and the csv_export folder can also be mapped to a local directory.

#### MS SQL Docker Container

The Microsoft SQL Server container is based on the Microsoft image with Ubuntu 20.04 and the pyshopify library installed alongside python 3.9. The container is configured to run the `shopify_cli` command line application.

On the initial run, the database structure is automatically built based on the environment variables in docker compose. The `config.ini` file is automatically populated with the database details based on the environment variables.

```yaml
services:
    sqlserver:
        build:
            context: ..
            dockerfile: docker-mssql/Dockerfile
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
            - "../csv_export:/root/csv_export"
            - "../data:/var/opt/mssql"
            - "../config.ini:/root/config.ini"
```

#### MySQL Docker Container

The MySQL container is based on the MySQL image with Debian-8 and the pyshopify library installed alongside python 3.9. The container is configured to run the `shopify_cli` command line application.

On the initial run, the database structure is automatically built based on the environment variables in docker compose. The `config.ini` file is automatically populated with the database details based on the environment variables.

```yml
services:
    mysql-db:
        build:
            context: ..
            dockerfile: docker-mysql/Dockerfile
        container_name: shop_mysql
        hostname: shop_mysql
        ports:
            - "3306:3306"
        environment:
            MYSQL_TCP_PORT: 3306
            MYSQL_ROOT_PASSWORD: StrongestPassword1
            DB_NAME: shop_sql
            DB_USER: shop_user
            DB_PASS: StrongerPassword1
            STARTING_DATE: "2019-01-01"
            CONFIG_FILE: "/root/config.ini"
        volumes:
            - "../csv_export:/root/csv_export"
            - "../data:/var/lib/mysql"
            - "../config.ini:/root/config.ini"
```

### Creating a Container

To create a container:

```shell script
git clone https://github.com/webdjoe/pyshopify

# Switch to the appropriate docker container folder
cd pyshopify/docker-mssql
cd pyshopify/docker-mysql

# edit the docker compose environment variables with vim or nano
vim docker-compose.yml

# Build and run container detached
sudo docker compose up --build -d

# edit config.ini file
vim config.ini
```

Once started test if SQL server is running. A `0` return value indicates the server has started up and is ready for connections.

```shell script
 sudo docker exec -it shop_sql bash -c '/opt/mssql-tools/bin/sqlcmd -h -1 -t 1 -U sa \
 -P "$MSSQL_SA_PASSWORD" -Q "SET NOCOUNT ON; Select SUM(state) from sys.databases"'
```

### Running pyshopify in the container

`shopify_cli` can be called in container to pull data and send to database or csv files. Check out the [`shopify_cli`](#running-as-command-line-application) section for more details.

```shell script
# Get last 30 days of data and import into SQL Server running in container
sudo docker exec -it shop_sql shopify_cli --all -d 30 --sql-out

# Get orders data between dates and import into SQL Server
sudo docker exec -it shop_sql shopify_cli --orders -b 2020-01-01 2020-12-31 --sql-out

# Pull 30 days of data into csv files
sudo docker exec -it shop_sql shopify_cli --csv-out --csv-location csv_export
```
