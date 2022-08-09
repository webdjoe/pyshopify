"""Shopify API Runner."""
import sys
from datetime import timedelta, datetime as dt
from typing import Tuple, List, Dict, Optional, Iterator, Any, Callable
from dateutil import parser
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from pandas import DataFrame
import pandas as pd
from configparser import SectionProxy
from pyshopify.api import api_call, header_link
from pyshopify.configure import Config
from pyshopify.csv_out import csv_send
from pyshopify.return_parse import pandas_work, customers_work
from pyshopify.vars import api_fields

log = sys.stdout.write
sql_works = False


class ShopifyApp:
    """Shopify API Runner Class."""
    def __init__(self, config_dir: Optional[str] = None,
                 config_dict: Optional[Dict[str, dict]] = None):
        """Initialize ShopifyApp.
        Args:
            config_dir (str): absolute or relative path of config file
            config_dict (Dict[str, dict]): configuration dictionary overrides
                config file
        Examples:
                >>> config_dict = {'shopify': {'store_name': 'store_name',
                            'api_key': 'api_key',
                            'time_zone': 'time_zone',
                            'api_version': '2022-07'},
                'csv': {'filepath': 'output_dir'},
                'sql': {'database': 'database',
                        'db_user': 'user',
                        'db_pass': 'password',
                        'server': 'server',
                        'port': 1433,
                        'schema': 'dbo'}}
                }
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

        self.engine: Any = None
        self.sql_merge: Optional[Callable] = None
        self.start_date, self.end_date = self.date_config()
        if not self.start_date or not self.end_date:
            raise ValueError("Error parsing dates")

    def update_config(self, config: Dict[str, Dict[str, str]]):
        """Pass configuration dictionary to update instance.
        Arguments
        ---------
        config: Dict[str, dict]
            dictionary with configuration sections:
            {
                'shopify': {
                    'start': '20220101',
                    'end': '20220131'
                },
                'sql' {
                    'server': 'localhost'
                },
                'csv' : {
                    'filepath': 'csv_export'
                }
            }
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

    def __init_engine(self) -> bool:
        """Initialize engine in instance."""
        try:
            from pyshopify.sql import sql_merge
            from pyshopify.sql import get_engine
            self.engine = get_engine(self.sql_config)
            self.sql_merge = sql_merge
            return True
        except ImportError:
            raise ImportError("No SQL Python Modules installed")

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
        else:
            if self.shop_config.getint('days', 0) < 1:
                log('Please enter days of history or dates to pull between')
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

        Args:
            shopify_config (Optional[dict]): Pass configuration dictionary
                with shopify configuration:

        Yields:
            dict: dictionary of dataframes for orders enpoint:
                >>> [('Orders', DataFrame),
                    ('Refunds', DataFrame),
                    ('LineItems', DataFrame),
                    ('RefundLineItem', DataFrame),
                    ('Adjustments', DataFrame),
                    ('DiscountApps', DataFrame),
                    ('DiscountCodes', DataFrame),
                    ('ShipLines', DataFrame),
                    ('OrderAttr', DataFrame)]

        Examples:
            Example `shopify_config`:
                >>> shopify_config = {'access_token': 'access_token',
                            'store_name': 'store-name-in-admin-url',
                            'api_version': '2022-07',
                            'days': 30}

        """
        if isinstance(shopify_config, dict):
            self.update_config({'shopify': shopify_config})
        for order_return in self.__orders_runner():
            yield order_return

    def get_full_df(self, shopify_config: Optional[dict]
                    ) -> Dict[str, DataFrame]:
        """Return full dataframe of orders and customers.

        Get all customers and orders data and return a dictionary of dataframes
        containing the data.

        Args:
            shopify_config (Optional[dict]): Pass configuration dictionary
                with shopify configuration:
                >>> shopify_config = {'access_token': 'access_token',
                              'store_name': 'store-name-in-admin-url',
                              'api_version': '2022-07',
                              'days': 30}

        Returns:
            Dict[str, DataFrame]: dict of dataframes for orders and customers:
            >>>  {'customers': DataFrame,
                    'Orders': OrderStr,
                    'Refunds': RefundStr,
                    'LineItems': LineItemsStr,
                    'RefundLineItem': RefundLineItemStr,
                    'Adjustments': AdjustmentStr,
                    'Customers': CustomersStr,
                    'DiscountApps': DiscountAppStr,
                    'DiscountCodes': DiscCodeStr,
                    'ShipLines': ShipStr,
                    'OrderAttr': OrderAttrStr,
            """
        if isinstance(shopify_config, dict):
            self.update_config({'shopify': shopify_config})
        return {
            **self.customers_full_df(),
            **self.orders_full_df()
        }

    def customers_iterator(self, shopify_config: Optional[dict] = None
                           ) -> Iterator[dict]:
        """Customers data return generator yields dict of customer data
            in dataframes.

        Generator function that yields dictionary of dataframes for each
            paginated call to orders endpoint.

        Args:
            shopify_config (Optional[dict]): Pass configuration dictionary
                with shopify configuration:
                >>> shopify_config = {'access_token': 'access_token',
                              'store_name': 'store-name-in-admin-url',
                              'api_version': '2022-07',
                              'days': 30}
        Yields:
            Iterator[dict]: dictionary of dataframes for customers enpoint

        >>> [('Customers', <pandas.DataFrame>)]
        """
        if isinstance(shopify_config, dict):
            self.update_config({'shopify': shopify_config})
        for customer_return in self.__customers_runner():
            yield customer_return

    def orders_full_df(self, shopify_config: Optional[dict] = None
                       ) -> Dict[str, DataFrame]:
        """Return full dataframe of orders data.

        Call Shopify runner with configuration if passed to get all
        pages of orders api for the configured date and return a
        dictionary of dataframes.

        Args:
            shopify_config (dict[str,str], optional): Dictionary with Shopify
                configuration section, defaults to None

        Returns:
            Dict[str, DataFrame]: Dictionary of dataframes with all orders
                data from configuration data

        Examples:

            Using a configuration dictionary::
            >>> shopify_config = {'access_token': 'access_token',
                                'store_name': 'store-name-in-admin-url',
                                'api_version': '2022-07',
                                'days': 30}
            Instead of days you can use start and end keys with dates in
                'YYYY-MM-DD' format
            >>> shopify_config = {'start': '2020-01-01',
                                'end': '2020-01-31'}
            >>> app = ShopifyApp()
            >>> orders_dict = app.orders_full_df(shopify_config=shopify_config)
            >>> orders_dict.items()
            [('Orders', DataFrame),
                ('Refunds', DataFrame),
                ('LineItems', DataFrame),
                ('RefundLineItem', DataFrame),
                ('Adjustments', DataFrame),
                ('DiscountApps', DataFrame),
                ('DiscountCodes', DataFrame),
                ('ShipLines', DataFrame),
                ('OrderAttr', DataFrame)]
        """
        if isinstance(shopify_config, dict):
            self.update_config({'shopify': shopify_config})
        orders_df: Dict[str, DataFrame] = {}
        for table_dict in self.__orders_runner():
            for keys in table_dict:
                if orders_df.get(keys) is None:
                    orders_df[keys] = table_dict[keys].copy()
                else:
                    orders_df[keys] = pd.concat([table_dict.get(keys),
                                                 orders_df.get(keys)])
        return orders_df

    def customers_full_df(self, shopify_config: Optional[dict] = None
                          ) -> Dict[str, DataFrame]:
        """Return full dataframe of customers data.

        Call Shopify customers runner with configuration if passed to get all
        pages of orders api for the configured date and return a
        dictionary of dataframes.

        Args:
            shopify_config (Dict[str, str], optional): Shopify configuration
            dictionary. Defaults to None.

        Returns:
            Dict[str, DataFrame]: Dictionary of dataframes with all customers
            data from configuration data

        Examples:
            Using a configuration dictionary
            >>> shopify_config = {'access_token': 'access_token',
                                'store_name': 'store-name-in-admin-url',
                                'api_version': '2022-07',
                                'days': 30}
            Instead of days you can use start and end keys with dates in
                'YYYY-MM-DD' format
            >>> shopify_config = {'start': '2020-01-01',
                                  'end': '2020-01-31'}
            >>> app = ShopifyApp()
            >>> customers_dict = app.customers_full_df(
                shopify_config=shopify_config)
            >>> customers_dict.items()
            [('Customers', <pandas.DataFrame>)]
        """
        if isinstance(shopify_config, dict):
            self.update_config({'shopify': shopify_config})
        customers_df: Dict[str, DataFrame] = {}
        for table_dict in self.__customers_runner():
            for keys in table_dict:
                if customers_df.get(keys) is None:
                    customers_df[keys] = table_dict[keys].copy()
                else:
                    customers_df[keys] = pd.concat([table_dict.get(keys),
                                                    customers_df.get(keys)])
        return customers_df

    def data_writer(self, customers: bool = False, orders: bool = False,
                    write_csv: bool = False, write_sql: bool = False,
                    config: Optional[Dict[str, Dict[str, str]]] = None
                    ) -> None:
        """Write data to csv and/or sql.

        Set orders and/or customers arguments to True to write data.
        Set write_sql and/or write_csv to True to write to csv and/or sql.
        Pass configuration as a dictionary of config sections to configure
        output.

        Args:
            customers (bool): Get data from customer endpoint
            orders (bool: Get data from orders endpoint
            write_csv (bool): Write data to csv
            write_sql (bool): Write data to sql
            config: (Dict[str, Dict[str, str]]): Pass configuration dictionary
                with config sections

        Returns:
            None

        Examples:

        Example `config_dict`::
            >>> config = {
                'shopify': {
                    'access_token': 'access_token',
                    'store_name': 'store-name-in-admin-url',
                    'api_version': '2022-07',
                    'days': 30
                },
                'sql': {
                    'database': 'shop_rest',
                    'db_user': 'db_user',
                    'db_password': 'db_password',
                    'server': 'localhost',
                },
                'csv': {
                    'filepath': 'output_dir'
                }
            }
        """
        if write_sql is False and write_csv is False:
            log("No output enabled")
            return
        if customers is False and orders is False:
            log("Please enable customers or orders output")
            return
        if config is not None:
            self.update_config(config)
        if write_sql is True:
            if self.engine is None:
                self.__init_engine()
            if self.engine is None or self.sql_merge is None:
                raise Exception("Unable to initialize SQL Engine")
        if write_csv is True:
            if self.csv_config.get('filepath') is None:
                log("Please configure csv output directory")
                return
        if orders is True:
            i = 1
            for order_dict in self.__orders_runner():
                if len(order_dict) == 0:
                    log("No order data, stopping loop")
                    break
                if write_sql is True and self.sql_merge is not None:
                    self.sql_merge(order_dict, i, self.engine,
                                   self.sql_config)
                if write_csv is True:
                    csv_send(order_dict, self.csv_config)

        if customers is True:
            i = 1
            for customer_dict in self.__customers_runner():
                if len(customer_dict.values()) == 0:
                    log("No customer data, stopping loop")
                    break
                if write_sql is True and self.sql_merge is not None:
                    self.sql_merge(customer_dict, i, self.engine,
                                   self.sql_config)
                if write_csv is True:
                    csv_send(customer_dict, self.csv_config)

    def orders_writer(self, write_csv: bool = False, write_sql: bool = False,
                      config: Optional[dict] = None) -> None:
        """Write orders data to CSV or SQL output based on configuration.

        Pass configuration as a dictionary of config sections to configure
        output.

       Args:
            write_csv (bool): Write data to csv
            write_sql (bool): Write data to sql
            config (Dict[str, Dict[str, str]]): Pass configuration dictionary
                with config sections:
                >>> config ={
                    'shopify': {
                        'access_token': 'access_token',
                        'store_name': 'store-name-in-admin-url',
                        'api_version': '2022-07',
                        'days': 30
                    },
                    'sql': {
                        'database': 'shop_rest',
                        'db_user': 'db_user',
                        'db_password': 'db_password',
                        'server': 'localhost',
                    },
                    'csv': {
                        'filepath': 'output_dir'
                    }
                }
        Returns:
            None
        """
        self.data_writer(customers=False, orders=True,
                         write_csv=write_csv, write_sql=write_sql,
                         config=config)

    def customers_writer(self, write_csv: bool = False,
                         write_sql: bool = False,
                         config: Optional[dict] = None) -> None:
        """Write customer data to CSV or SQL output based on configuration.
        Pass configuration as a dictionary of config sections to configure
        output.

        Args:
            write_csv (bool): Write data to csv
            write_sql (bool): Write data to sql
            config (Dict[str, Dict[str, str]]): Configuration dictionary with
                sections. For example:
                >>> config = {
                    'shopify': {
                        'access_token': 'access_token',
                        'store_name': 'store-name-in-admin-url',
                        'api_version': '2022-07',
                        'days': 30
                    },
                    'sql': {
                        'database': 'shop_rest',
                        'db_user': 'db_user',
                        'db_password': 'db_password',
                        'server': 'localhost',
                    },
                    'csv': {
                        'filepath': 'output_dir'
                    }
                }
        """
        self.data_writer(customers=True, orders=False,
                         write_csv=write_csv, write_sql=write_sql,
                         config=config)

    def sql_writer(self, config: Optional[dict] = None) -> None:
        """Write orders and customers to SQL output based on configuration.
        Pass configurations as a dictionary to configure output.

        Args:
            config (Dict[str, Dict[str, str]]): Configuration dictionary with
                shopify and csv sections. For example:
                >>> config = {
                    'shopify': {
                        'access_token': 'access_token',
                        'store_name': 'store-name-in-admin-url',
                        'api_version': '2022-07',
                        'days': 30
                    },
                    'sql': {
                        'database': 'shop_rest',
                        'db_user': 'db_user',
                        'db_password': 'db_password',
                        'server': 'localhost',
                    }
                }
        """
        self.data_writer(customers=True, orders=True,
                         write_sql=True, write_csv=False,
                         config=config)

    def csv_writer(self, config=None) -> None:
        """Write Orders and Customers data to CSV files based on configuration
        Pass configuration as a dictionary:

        Args:
            config (Dict[str, Dict[str, str]]): Configuration dictionary with
                shopify and csv sections. For example:
                >>> config = {
                    'shopify': {
                        'access_token': 'access_token',
                        'store_name': 'store-name-in-admin-url',
                        'api_version': '2022-07',
                        'days': 30
                    },
                    'csv': {
                        'filepath': 'output_dir'
                        }
                    }
        """
        self.data_writer(customers=True, orders=True,
                         write_csv=True, write_sql=False,
                         config=config)

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
                'Customers': customers_work(resp_data)
            }
            yield table_dict
            if table_dict is None:
                break

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

    def __request_runner(self, initial_url: str, params: dict):
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
