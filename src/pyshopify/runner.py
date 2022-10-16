"""Shopify API Runner."""
import sys
import logging
from datetime import timedelta, datetime as dt
from typing import Tuple, List, Dict, Optional, Iterator, Callable, Union
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from configparser import SectionProxy
from dateutil import parser
from pandas import DataFrame
import pandas as pd
from pyshopify.api import api_call, header_link
from pyshopify.configure import Config
from pyshopify.csv_out import csv_send
from pyshopify.return_parse import (locations_parse, pandas_work,
                                    customers_work, products_work,
                                    inventory_levels_parse)
from pyshopify.sql import DBWriter
from pyshopify.vars import api_fields

logger = logging.getLogger('pyshopify')
logger.setLevel(logging.DEBUG)
log = sys.stdout.write
sql_works = False


class ShopifyApp:
    """Shopify API Runner Class."""
    def __init__(self, config_dir: Optional[str] = None,
                 config_dict: Optional[Dict[str, dict]] = None):
        """Initialize ShopifyApp.
        Arguments
        ----------
        config_dir (str): absolute or relative path of config file
        config_dict (Dict[str, dict]): configuration dictionary overrides
            config file

        Examples
        --------
        >>> config_dict = {'shopify':
        ...                   {'store_name': 'store_name_in_admin_url',
        ...                    'api_key': 'api_key',
        ...                    'time_zone': 'time_zone',
        ...                    'api_version': '2022-07'},
        ...                'csv': {'filepath': 'output_dir'},
        ...                'sql': {'connector': 'mssql+pyodbc',
        ...                        'database': 'database',
        ...                        'db_user': 'user',
        ...                        'db_pass': 'password',
        ...                        'server': 'server',
        ...                        'port': 1433,
        ...                        'schema': 'dbo'}
        ...                 }
        """
        self.retry_after: int = 0
        self.orders_dict: dict = {}
        if config_dir is not None:
            self.configuration = Config(config_dir)
        else:
            self.configuration = Config()
        if config_dict is not None:
            self.configuration.parser.read_dict(config_dict)
        self.csv_config: SectionProxy = self.configuration.csv_conf
        self.shop_config: SectionProxy = self.configuration.shopify
        self.sql_config: SectionProxy = self.configuration.sql_conf
        self.start_date, self.end_date = self.date_config()
        if not self.start_date or not self.end_date:
            raise ValueError("Error parsing dates")
        self.db_writer = DBWriter(self.sql_config)

    def update_config(self, config: Dict[str, Dict[str, str]]):
        """Pass configuration dictionary to update instance.

        Any date period included here will override existing configuration.

        Arguments
        ---------
        config: Dict[str, dict]
            dictionary with configuration sections:
            >>> config =
            ...   {
            ...      'shopify': {
            ...         'start': '20220101',
            ...         'end': '20220131'
            ...      },
            ...      'sql' {
            ...         'server': 'localhost'
            ...      },
            ...      'csv' : {
            ...         'filepath': 'csv_export'
            ...      }
            ... }
        """
        self.configuration.parser.read_dict(config)
        if config.get('shopify', {}).get('start', '') == '' \
                or config.get('shopify', {}).get('start', '') == '':
            self.configuration.parser.remove_option('shopify', 'start')
            self.configuration.parser.remove_option('shopify', 'end')
        self.start_date, self.end_date = self.date_config()

    @property
    def time_zone(self) -> ZoneInfo:
        """Get timezone from configuration."""
        try:
            return ZoneInfo(self.shop_config['time_zone'])
        except ZoneInfoNotFoundError:
            return ZoneInfo('UTC')

    def __url_builder(self, end_point) -> str:
        """Build URL for API call."""
        config = self.shop_config
        return (f"https://{config['store_name']}.myshopify.com/"
                f"{config['api_path']}{config['api_version']}/{end_point}")

    def date_config(self) -> Tuple[str, str]:
        """Get dates from configuration."""
        btw = []
        start_date = None
        end_date = None
        if self.shop_config.get('start', '') != '' \
                and self.shop_config.get('end', '') != '':
            btw = [parser.parse(self.shop_config.get('start')),
                   parser.parse(self.shop_config.get('end'))]
            start_date, end_date = self.__btw_config(btw)
            return start_date, end_date
        if self.shop_config.getint('days', 0) < 1:
            logger.error('Please enter days of history or dates to pull between')
            raise ValueError

        days = self.shop_config.getint('days', 30)
        start = dt.now() - timedelta(days=days)
        start_date = start.astimezone(self.time_zone).isoformat()
        end = dt.now()
        end_date = end.astimezone(self.time_zone).isoformat()
        return start_date, end_date

    def __btw_config(self, btw: List[dt]) -> Tuple[str, str]:
        """Parse between dates configuration."""
        t0 = btw[0]
        t1 = btw[1]
        if t0 < t1:
            start_date = dt.isoformat(t0.astimezone(self.time_zone))
            end_date = dt.isoformat(t1.astimezone(self.time_zone))
        else:
            start_date = dt.isoformat(t1.astimezone(self.time_zone))
            end_date = dt.isoformat(t0.astimezone(self.time_zone))
        return start_date, end_date

    def orders_iterator(self, shopify_config: Optional[dict] = None
                        ) -> Iterator[dict]:
        """Orders data return generator yields dict of order
            data in dataframes.

        Generator function that yields dictionary of dataframes
        for each paginated call to orders endpoint.

        Arguments
        ---------
        shopify_config (Optional[dict]): Pass configuration dictionary
            with shopify configuration:

        Yields
        ------
        dict: dictionary of dataframes for orders enpoint:
            >>> [('orders', DataFrame),
            ... ('refunds', DataFrame),
            ... ('line_items', DataFrame),
            ... ('refund_line_item', DataFrame),
            ... ('adjustments', DataFrame),
            ... ('discount_apps', DataFrame),
            ... ('discount_codes', DataFrame),
            ... ('ship_lines', DataFrame),
            ... ('order_attr', DataFrame),
            ... ('order_prices', DataFrame)]

        Examples
        --------
        Example `shopify_config`:
            >>> shopify_config = {'access_token': 'access_token',
            ...         'store_name': 'store-name-in-admin-url',
            ...         'api_version': '2022-07',
            ...         'days': 30}

        """
        if isinstance(shopify_config, dict):
            self.update_config({'shopify': shopify_config})
        for order_return in self.__orders_runner():
            yield order_return

    def get_orders_customers_df(self, shopify_config: Optional[dict] = None
                                ) -> Dict[str, DataFrame]:
        """Return full dataframe of orders and customers.

        Get all customers and orders data and return a dictionary of dataframes
        containing orders and customers data.

        Arguments
        ---------
        shopify_config (Optional[dict]): Pass configuration dictionary
            with shopify configuration:
            >>> shopify_config = {'access_token': 'access_token',
            ...                   'store_name': 'store-name-in-admin-url',
            ...                   'api_version': '2022-07',
            ...                   'days': 30}

        Returns
        -------
        Dict[str, DataFrame]: dict of dataframes for orders and customers:
        >>>  {'customers': Customers DataFrame,
        ...   'orders': Order DataFrame,
        ...   'refunds': Refund DataFrame,
        ...   'line_items': line_items DataFrame,
        ...   'refund_lineItem': refund_line_item DataFrame,
        ...   'adjustments': Adjustment DataFrame,
        ...   'customers': Customers DataFrame,
        ...   'discount_apps': discount_apps DataFrame,
        ...   'discount_codes': DiscCode DataFrame,
        ...   'ship_lines': Ship DataFrame,
        ...   'order_attr': order_attr DataFrame},
        ...   'order_prices': order_prices DataFrame},
        """
        if isinstance(shopify_config, dict):
            self.update_config({'shopify': shopify_config})
        return {
            **self.get_full_customers_df(),
            **self.get_full_orders_df()
        }

    def customers_iterator(self, shopify_config: Optional[dict] = None
                           ) -> Iterator[dict]:
        """Customers data return generator yields dict of customer data
            in dataframes.

        Generator function that yields dictionary of dataframes for each
            paginated call to orders endpoint.

        Arguments
        ---------
        shopify_config (Optional[dict]): Pass configuration dictionary
            with shopify configuration:
            >>> shopify_config = {'access_token': 'access_token',
            ...                'store_name': 'store-name-in-admin-url',
            ...                'api_version': '2022-07',
            ...                'days': 30}

        Yields
        ------
        Iterator[dict]: dictionary of dataframes for customers enpoint
            >>> [('customers', <pandas.DataFrame>)]
        """
        if isinstance(shopify_config, dict):
            self.update_config({'shopify': shopify_config})
        for customer_return in self.__customers_runner():
            yield customer_return

    def get_full_orders_df(self, shopify_config: Optional[dict] = None
                           ) -> Dict[str, DataFrame]:
        """Return full dataframe of orders data.

        Call Shopify runner with configuration if passed to get all
        pages of orders api for the configured date and return a
        dictionary of dataframes. Not recommended for large data pulls.

        Arguments
        ---------
        shopify_config (dict[str,str], optional): Dictionary with Shopify
            configuration section, defaults to None

        Returns
        -------
        Dict[str, DataFrame]: Dictionary of dataframes with all orders
            data from configuration data

        Examples
        --------
        Using a configuration dictionary::
        >>> shopify_config = {'access_token': 'access_token',
        ...                   'store_name': 'store-name-in-admin-url',
        ...                   'api_version': '2022-07',
        ...                   'days': 30}
        Instead of days you can use start and end keys with dates in
            'YYYY-MM-DD' format
        >>> shopify_config = {'start': '2020-01-01',
        ...                   'end': '2020-01-31'}
        >>> app = ShopifyApp()
        >>> orders_dict = app.orders_full_df(shopify_config=shopify_config)
        >>> orders_dict.items()
        ...    [('orders', DataFrame),
        ...    ('refunds', DataFrame),
        ...    ('line_items', DataFrame),
        ...    ('refund_line_item', DataFrame),
        ...    ('adjustments', DataFrame),
        ...    ('discount_apps', DataFrame),
        ...    ('discount_codes', DataFrame),
        ...    ('ship_lines', DataFrame),
        ...    ('order_attr', DataFrame),
        ...    ('order_prices', DataFrame)]
        """
        if isinstance(shopify_config, dict):
            self.update_config({'shopify': shopify_config})
        orders_df: Dict[str, DataFrame] = {}
        for table_dict in self.__orders_runner():
            orders_df = combine_dicts(orders_df, table_dict)
        return orders_df

    def get_full_customers_df(self, shopify_config: Optional[dict] = None
                              ) -> Dict[str, DataFrame]:
        """Return full dataframe of customers data.

        Call Shopify customers runner with configuration if passed to get all
        pages of orders api for the configured date and return a
        dictionary of dataframes.

        Parameters
        ----------
        shopify_config: Dict[str, str], optional
            Shopify configuration dictionary. Defaults to None.

        Returns
        -------
        Dict[str, DataFrame]
            Dictionary of dataframes with all
            customers data from configuration data

        Examples
        --------
        Using a configuration dictionary
        >>> shopify_config = {'access_token': 'access_token',
        ...                   'store_name': 'store-name-in-admin-url',
        ...                   'api_version': '2022-07',
        ...                   'days': 30}
        Instead of days you can use start and end keys with dates in
            'YYYY-MM-DD' format
        >>> shopify_config = {'start': '2020-01-01',
        ...                   'end': '2020-01-31'}
        >>> app = ShopifyApp()
        >>> customers_dict = app.customers_full_df(
        ... shopify_config=shopify_config)
        >>> customers_dict.items()
        ... [('customers', <pandas.DataFrame>)]
        """
        if isinstance(shopify_config, dict):
            self.update_config({'shopify': shopify_config})
        customers_df: Dict[str, DataFrame] = {}
        for table_dict in self.__customers_runner():
            customers_df = combine_dicts(customers_df, table_dict)
        return customers_df

    def __data_writer(self, gen_func: Callable[..., Iterator[dict]],
                      write_csv: bool = False,
                      write_sql: bool = False,
                      csv_operation: Optional[str] = None,
                      config: Optional[Dict[str, dict]] = None) -> None:
        """Internal data writer that take data generator
            and performs desired writes"""
        if isinstance(config, dict):
            self.update_config(config)
        i = 0
        for table_dict in gen_func():
            i += 1
            if len(table_dict.keys()) == 0:
                return
            if write_sql is True:
                self.__sql_writer(table_dict, i)
            if write_csv is True:
                self.__csv_writer(table_dict, csv_operation)

    def orders_customers_writer(self, write_sql: bool = False,
                                write_csv: bool = False,
                                config: Optional[dict] = None):
        """Write orders & customer data to csv and SQL server.

        Parameters
        ----------
        write_sql : bool, optional
            Write data to SQL server, by default False
        write_csv : bool, optional
            write data to CSV files, by default False
        config : dict, optional
            full configuration dictionary, by default {}

        See Also
        --------
        See ShopifyApp docstring for full configuration dictionary syntax
        """
        self.orders_writer(write_sql=write_sql, write_csv=write_csv,
                           config=config)
        self.customers_writer(write_sql=write_sql, write_csv=write_csv,
                              config=config)

    def orders_writer(self, write_csv: bool = False, write_sql: bool = False,
                      config: Optional[dict] = None) -> None:
        """Write orders data to CSV or SQL output based on configuration.

        Pass configuration as a dictionary of config sections to configure
        output.

       Arguments
       ----------
        write_csv : bool
            Write data to csv
        write_sql : bool
            Write data to sql
        config : Dict[str, Dict[str, str]]
            Pass configuration dictionary with config sections:
            >>> config ={
            ...     'shopify': {
            ...         'access_token': 'access_token',
            ...         'store_name': 'store-name-in-admin-url',
            ...         'api_version': '2022-07',
            ...         'days': 30
            ...      },
            ...     'sql': {
            ...         'database': 'shop_rest',
            ...         'db_user': 'db_user',
            ...         'db_password': 'db_password',
            ...         'server': 'localhost',
            ...     },
            ...     'csv': {
            ...         'filepath': 'output_dir'
            ...     }
            ... }

        Returns
        -------
        None
        """
        self.__data_writer(self.__orders_runner, write_csv=write_csv,
                           write_sql=write_sql, config=config)

    def customers_writer(self, write_csv: bool = False,
                         write_sql: bool = False,
                         config: Optional[dict] = None) -> None:
        """Write customer data to CSV or SQL output based on configuration.
        Pass configuration as a dictionary of config sections to configure
        output.

        Arguments
        ----------
        write_csv : bool
            Write data to csv
        write_sql : bool
            Write data to sql
        config : Dict[str, Dict[str, str]]
            Configuration dictionary with sections. For example:
            >>> config ={
            ...     'shopify': {
            ...         'access_token': 'access_token',
            ...         'store_name': 'store-name-in-admin-url',
            ...         'api_version': '2022-07',
            ...         'days': 30
            ...      },
            ...     'sql': {
            ...         'database': 'shop_rest',
            ...         'db_user': 'db_user',
            ...         'db_password': 'db_password',
            ...         'server': 'localhost',
            ...     },
            ...     'csv': {
            ...         'filepath': 'output_dir'
            ...     }
            ... }
        """
        self.__data_writer(gen_func=self.__customers_runner, write_csv=write_csv,
                           write_sql=write_sql, config=config)

    def write_all_to_sql(self, config: Optional[dict] = None) -> None:
        """Write products, inventory orders and customers to SQL
        output based on configuration. Pass configurations as a
        dictionary to configure output.

        Arguments
        ---------
        config : Dict[str, Dict[str, str]]
            Configuration dictionary with shopify and csv sections. For example:
            >>> config = {
            ...     'shopify': {
            ...         'access_token': 'access_token',
            ...         'store_name': 'store-name-in-admin-url',
            ...         'api_version': '2022-07',
            ...         'days': 30
            ...     },
            ...     'sql': {
            ...         'database': 'shop_rest',
            ...         'db_user': 'db_user',
            ...         'db_password': 'db_password',
            ...         'server': 'localhost',
            ...     }
            ... }
        """
        self.products_writer(write_csv=False, write_sql=True, config=config)
        self.inventory_locations_writer(write_csv=False, write_sql=True, config=config)
        self.inventory_levels_writer(write_csv=False, write_sql=True, config=config)
        self.customers_writer(write_csv=False, write_sql=True, config=config)
        self.orders_writer(write_csv=False, write_sql=True, config=config)

    def write_all_to_csv(self, config: Optional[dict] = None) -> None:
        """Write Products, Inventory, Orders and Customers data to CSV files
        based on configuration. Pass configuration as a dictionary

        Arguments
        ---------
        config (Dict[str, Dict[str, str]]): Configuration dictionary with
            shopify and csv sections. For example:
            >>> config = {
            ...     'shopify': {
            ...         'access_token': 'access_token',
            ...         'store_name': 'store-name-in-admin-url',
            ...         'api_version': '2022-07',
            ...         'days': 30
            ...     },
            ...     'csv': {
            ...         'filepath': 'output_dir'
            ...      }
            ...  }
        """
        self.products_writer(write_csv=True, write_sql=False, config=config)
        self.inventory_locations_writer(write_csv=True, write_sql=False, config=config)
        self.inventory_levels_writer(write_csv=True, write_sql=False)
        self.orders_writer(write_csv=True, write_sql=False, config=config)
        self.customers_writer(write_csv=True, write_sql=False, config=config)

    def products_writer(self, write_sql=False, write_csv=False,
                        config: Optional[dict] = None) -> None:
        """Write Products and Inventory Tables to SQL Server or csv.
        Arguments
        ---------
        write_sql : bool
            Write data to sql
        write_csv : bool
            Write data to csv
        config : Dict[str, Dict[str, str]]
            Full config dictionary

        Returns
        -------
        None

        See Also
        --------
        ShopifyApp.__init__ for full config dictionary example
        """
        if write_sql is False and write_csv is False:
            logger.error("No output enabled")
            return
        self.__data_writer(gen_func=self.__products_runner, write_sql=write_sql,
                           write_csv=write_csv, csv_operation='w',
                           config=config)

    def products_inventory_writer(self, write_sql: bool = False,
                                  write_csv: bool = False,
                                  config: Optional[dict] = None) -> None:
        """Write products and inventory data

        Arguments
        ---------
        write_sql: bool, optional
            Write data to sql
        write_csv: bool, optional
            Write data to csv
        config_dict : Optional[dict], optional
            Full config dict, optional

        Returns
        -------
        None

        See Also
        --------
        ShopifyApp : ShopifyApp class showing full configuration example
        """
        self.inventory_locations_writer(write_csv=write_csv, write_sql=write_sql,
                                        config=config)
        self.inventory_levels_writer(write_csv=write_csv, write_sql=write_sql,
                                     config=config)
        self.products_writer(write_sql=write_sql, write_csv=write_csv,
                             config=config)

    def get_products_inventory(self) -> Dict[str, DataFrame]:
        """Get products, options, variants, inventory locations and
            inventory levels.

        Returns
        -------
        Dict[str, DataFrame]

        Examples
        ---------
        Return value is a dictionary of DataFrames for each table:
        >>> products_inventory = app.get_products_inventory()
        >>> products_inventory = {
        ...     'products': products_df,
        ...     'options': options_df,
        ...     'variants': variants_df,
        ...     'inventory_locations': inventory_locations_df,
        ...     'inventory_levels': inventory_levels_df
        ... }

        See Also
        --------
        DataFrames are described in the get_products()
        and get_inventory() methods

        """
        products = self.get_products()
        inventory_locations = self.get_inventory_locations()
        inventory_df = inventory_locations.get('inventory_locations')
        if isinstance(inventory_df, DataFrame):
            locations = list(inventory_df.id)
        else:
            locations = []
        inventory_levels = self.get_inventory_levels(locations)
        return {
            **inventory_levels,
            **inventory_locations,
            **products
        }

    def get_products(self) -> Dict[str, Optional[DataFrame]]:
        """Get Product, Variant & Product Options Data to Dictionary of DataFrames.

        Returns
        -------
        Dict[str, DataFrame]
            Dictionary of product, variant & options DataFrames

        Examples
        --------
        >>> app.get_products() = {
        ...     'products': DataFrame,
        ...     'variants': DataFrame,
        ...     'product_options': DataFrame
        ... }
        """
        products: Dict[str, DataFrame] = {}
        for products_data in self.__products_runner():
            if len(products_data) == 0:
                return {'products': None}
            products = combine_dicts(products, products_data)
        return products

    def get_inventory_locations(self) -> Dict[str, Optional[DataFrame]]:
        """Get Inventory Locations DataFrame"""
        location_url = self.__url_builder('locations.json')
        locations = []
        for response in self.__request_runner(location_url):
            location = response.get('locations')
            locations.extend(location)
        if len(locations) == 0:
            return {"inventory_locations": None}
        loc_df = locations_parse(locations)
        return {"inventory_locations": loc_df}

    def inventory_locations_writer(self, write_csv: bool = False,
                                   write_sql: bool = False,
                                   config: Optional[dict] = None) -> None:
        """Write locations to SQL Server or CSV file.

        Retrieves and writes inventory locations associated with
        inventory items to SQL Server or CSV file.

        Parameters
        ----------
        write_csv : bool, optional
            Set to True to write data to CSV, by default False
        write_sql : bool, optional
            Set to True to write data to CSV, by default False
        config_dict : dict, optional
            Configuration dictionary, by default {}

        Returns
        -------
        None
        """
        if write_csv is False and write_sql is False:
            logger.error("No output enabled")
        if config is not None:
            self.update_config(config)

        locations = self.get_inventory_locations()
        if locations.get('inventory_locations') is None:
            logger.debug("No locations found")
            return
        # if self.sql_merge is not None:
        #     self.sql_merge(locations, 0, self.engine, self.sql_config)
        if self.db_writer is not None:
            self.db_writer.sql_merge(locations)
        return

    def inventory_levels_writer(self, write_csv: bool = False,
                                write_sql: bool = False,
                                config: Optional[dict] = None) -> None:
        """ Write Inventory levels to SQL Server or CSV file.

        Arguments
        ----------
        write_csv : (bool, optional)
            Set to true to output inventory levels to a csv file. Defaults to False.
        write_sql : (bool, optional)
            Set to true to write inventory level data to SQL server. Defaults to False.
        config : (dict, optional)
            Set configuration. Defaults to {}.

        See Also
        --------
        ShopifyApp.__init__ for full config dictionary example
        """
        if config is not None:
            self.update_config(config)
        inv = self.get_inventory_levels()
        if inv.get('inventory_levels') is None:
            logger.debug("No inventory levels found")
            return
        if write_sql is True:
            self.__sql_writer(inv, 0)
        if write_csv is True:
            self.__csv_writer(inv, 'w')

    def get_inventory_levels(self, locations: Optional[Union[list, str]] = None
                             ) -> Dict[str, Optional[DataFrame]]:
        """Get level and location inventory.

        Get inventory levels for all products and locations.
        If locations are not specified, all locations will be returned.

        Arguments
        ---------
        locations: Union[list, str], optional
            Specify locations to get inventory levels for. Defaults to all locations.

        Returns
        -------
        Dict[str, DataFrame]
            DataFrame of all inventory levels
            {'inventory_levels': DataFrame}
        """

        if self.db_writer is None:
            raise Exception("Unable to initialize DBWriter")
        url = self.__url_builder('inventory_levels.json')
        item_list = []
        if locations is None or len(locations) == 0:
            locations_df = self.get_inventory_locations().get('inventory_locations')
            if locations_df is None:
                logger.error("No inventory locations found")
                return {'inventory_levels': None}
            locations = list(locations_df['id'])
        if isinstance(locations, str):
            locations_str = locations
            locations_list = locations_str.split(',')
        elif isinstance(locations, list):
            locations_list = locations
            locations_str = ','.join([str(x) for x in locations])
        if len(locations_str) > 50:
            loc_lens = {i: len(str(j)) + 1 for i, j in enumerate(locations_list)}
            char_count = 0
            start = 0
            end = 0
            loc_lists = []
            for idx, cnt in loc_lens.items():
                char_count += (cnt + 1)
                if char_count > 50:
                    end = idx - 1
                    loc_lists.append(locations[start:end])
                    start = end + 1
                    char_count = cnt
            for locs in loc_lists:
                locs_str = ','.join([str(x) for x in locs])
                for items in self.__request_runner(url,
                                                   params={'location_ids': locs_str}):
                    inventory_levels = items.get('inventory_levels')
                    if len(inventory_levels) == 0:
                        break
                    item_list.extend(items.get('inventory_levels'))
        else:
            for items in self.__request_runner(url,
                                               params={'location_ids': locations_str}):
                inventory_levels = items.get('inventory_levels')
                if len(inventory_levels) == 0:
                    break
                item_list.extend(inventory_levels)
        if len(item_list) == 0:
            return {"inventory_levels": None}
        parsed_levels = inventory_levels_parse(item_list)
        return {"inventory_levels": parsed_levels}

    def inventory_table(self, product_ids: Optional[List[int]] = None,
                        location_ids: Optional[List[int]] = None,
                        variant_ids: Optional[List[int]] = None) -> Optional[DataFrame]:
        """Return a DataFrame of inventory levels by location
        with variant and product titles.

        Arguments
        ---------
        product_ids: list, optional
            List of products ID's to get inventory levels for. Defaults to all products.
        location_ids: list, optional
            List of location ID's to get inventory levels for. Defaults to all locations.
        variant_ids: list, optional
            List of variant ID's to get inventory levels for. Defaults to all variants.
        """
        prod_dict = self.get_products()
        products: DataFrame = prod_dict.get('products')
        variants = prod_dict.get('variants')
        if products is None:
            logger.error("No products found")
            return None
        if variants is None:
            logger.error("No variants found")
            return None
        products = products.loc[products['status'] == 'active']
        if product_ids is not None and len(product_ids) > 0 and products is not None:
            products = products.loc[products['id'].isin(product_ids)]
        if variant_ids is not None and len(variant_ids) > 0 and products is not None:
            variants = variants.loc[variants['id'].isin(variant_ids)]
        products = products.merge(variants, left_on='id', right_on='product_id',
                                  suffixes=('_prod', '_var'), how='inner')
        if location_ids is not None and len(location_ids) > 0:
            inv_levels = self.get_inventory_levels(
                locations=location_ids).get('inventory_levels')
        else:
            inv_levels = self.get_inventory_levels().get('inventory_levels')
        if inv_levels is None:
            return None
        inv_levels = inv_levels.loc[inv_levels['inventory_item_id'].isin(
            products['inventory_item_id'])]
        inv_levels = inv_levels.merge(products, how='inner', on='inventory_item_id')
        inv_levels.rename(columns={'id_var': 'variant_id',
                                   'title_var': 'variant_title',
                                   'title_prod': 'product_title'},
                          inplace=True)
        columns = ['variant_id', 'product_id', 'sku', 'variant_title',
                   'product_title', 'available', 'location_id']
        inv_levels = inv_levels[columns]
        return inv_levels

    def __sql_writer(self, data: Dict[str, DataFrame], j: int = 0) -> bool:
        """Internal SQL Checks and writer."""
        return self.db_writer.sql_merge(data, j)
        # return self.sql_merge(data, j, self.engine, self.sql_config)

    def __csv_writer(self, data: Dict[str, DataFrame],
                     csv_operation: Optional[str] = None) -> bool:
        """Write CSV data to file"""
        if self.csv_config.get('filepath') is None:
            logger.error("Please configure csv output directory")
            return False
        csv_send(data, self.csv_config, csv_operation)
        return True

    def __products_runner(self, extra_params: Optional[dict] = None
                          ) -> Iterator[Dict[str, DataFrame]]:
        """Pulls product data but yields a full set of data.

        Arguments
        ---------
        extra_params : (dict, optional)
            Extra parameters to pass to the request. Defaults to {}.

        Yields
        ------
        Iterator[Dict[str, DataFrame]]
        """
        url = self.__url_builder('products.json')
        init_params = {
            "limit": 250,
        }
        if extra_params is not None:
            init_params.update(extra_params)
        products_data = self.__request_runner(url, init_params)
        prod_list: Dict[str, DataFrame] = {}
        while True:
            try:
                resp_data = next(products_data)
            except StopIteration:
                break
            table_dict = products_work(resp_data.get('products'))
            prod_list = combine_dicts(prod_list, table_dict)
        yield table_dict

    def __customers_runner(self) -> Iterator[Dict[str, DataFrame]]:
        """Iterate customers API Return."""
        url = self.__url_builder('customers.json')
        init_params = {
            "updated_at_min": self.start_date,
            "updated_at_max": self.end_date,
            "limit": self.shop_config.get('items_per_page'),
        }
        customer_data = self.__request_runner(url, init_params)
        i = 1
        while True:
            try:
                resp_data = next(customer_data)

            except StopIteration:
                break
            table_dict = {
                'customers': customers_work(resp_data)
            }
            if table_dict.get('customers') is None:
                break
            yield table_dict
            i += 1

    def __orders_runner(self) -> Iterator[Dict[str, DataFrame]]:
        """Call API method and run SQL, CSV and data exports."""
        col_list = [str(key) for key in api_fields]
        col_str = ",".join(col_list)
        url = self.__url_builder('orders.json')
        init_params = {
            "status": "any",
            "created_at_min": self.start_date,
            "created_at_max": self.end_date,
            "limit": self.shop_config.get('items_per_page'),
            "fields": col_str
        }
        order_dict = self.__request_runner(url, init_params)
        i = 1
        while True:
            try:
                resp_data = next(order_dict)

            except StopIteration:
                break
            table_dict = pandas_work(resp_data)

            yield table_dict
            if table_dict is None:
                break

            i += 1

    def __request_runner(self, initial_url: str, params: Optional[dict] = None):
        """shopify API data iterator."""
        j = 1
        url: Optional[str] = initial_url
        while True:
            if url is None:
                break
            if j == 1:
                page = False
            else:
                page = True
            j += 1
            resp = api_call(url, self.shop_config,
                            init_params=params, page=page)
            if resp is None:
                break
            url, self.retry_after = header_link(resp.headers)

            yield resp.json()


def combine_dicts(dict1: Dict[str, DataFrame], dict2: Dict[str, DataFrame]
                  ) -> Dict[str, DataFrame]:
    """Combine two dictionaries."""
    for k, v in dict2.items():
        if dict1.get(k) is None:
            dict1[k] = v.copy()
        else:
            dict1[k] = pd.concat([dict1[k], v], axis=0, ignore_index=True)
    return dict1
