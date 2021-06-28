"""Shopify API Runner."""
import sys
import timeit
from datetime import timedelta, datetime as dt
from typing import Tuple, List, Dict, Union

from dateutil import parser
from pandas import DataFrame

from pyshopify.api import api_call, header_link
from pyshopify.configure import Config
from pyshopify.csv_out import csv_writer
from pyshopify.return_parse import pandas_work
from pyshopify.vars import return_keys

log = sys.stdout.write

try:
    from pyodbc import ProgrammingError
    from pyshopify.sql import sql_send, sql_connect
except:
    log("SQL Python Modules not installed - pyodbc & sqlalchemy required")
    ProgrammingError = None
    sql_connect = None
    sql_send = None


class ShopifyApp:
    """Shopify API Runner Class."""
    def __init__(self, config_dir: str = None):
        self.starttime = timeit.default_timer()
        if config_dir is not None:
            self.configuration = Config(config_dir)
        else:
            self.configuration = Config()
        self.config_parser = self.configuration.parser
        self.retry_after = 0
        self.custom_dict = {}
        self.custom_enable = self.configuration.custom_enable
        self.connection = None

        self.engine = None
        if ProgrammingError is None or sql_send is None or sql_connect is None:
            self.sql_enable = False
        else:
            self.sql_enable = self.configuration.sql_enable
        self.csv_enable = self.configuration.csv_enable
        self.shop_config = self.configuration.shopify
        self.csv_config = self.configuration.csv_conf
        self.sql_conf = self.configuration.sql_conf
        self.order_url = self.shop_config.get('url_base') + self.shop_config.get('order_ep')
        self.csv_dir = self.csv_config.get('filepath')

        self.start_date = None
        self.end_date = None
        if self.sql_enable:
            self.sql_alive = self.sql_connect()
            if not self.connection or not self.engine:
                raise ProgrammingError("Unable to log in to database")
        else:
            self.sql_alive = False
        self.start_date, self.end_date = self.date_config()
        if not self.start_date or not self.end_date:
            raise ValueError

    def sql_connect(self) -> bool:
        if ProgrammingError is not None and \
                sql_send is not None and \
                sql_connect is not None:
            self.connection, self.engine = sql_connect(self.sql_conf)
            if not self.connection or not self.engine:
                raise ProgrammingError("Unable to log in to database")
            return True
        return False

    def date_config(self) -> Tuple[str, str]:
        """Get dates from configuration."""
        btw = []
        start_date = None
        end_date = None
        if self.shop_config.get('start') and self.shop_config.get('end'):
            btw = [parser.parse(self.shop_config.get('start')),
                   parser.parse(self.shop_config.get('end'))]
            start_date, end_date = self.btw_config(btw)
            return start_date, end_date
        else:
            if not self.shop_config.getint('days') or self.shop_config.getint('days') < 1:
                log('Please enter days of history or dates to pull between')
                raise ValueError

        if not btw and self.shop_config.getint('days') > 0:
            days = self.shop_config.getint('days')
            start = dt.now() - timedelta(days=days)
            start_date = start.strftime("%Y-%m-%dT%H:%M") + "-5:00"
            end = dt.now()
            end_date = end.strftime("%Y-%m-%dT%H:%M") + "-5:00"
        return start_date, end_date

    def btw_config(self, btw: List[dt]) -> Tuple[str, str]:
        """Parse between dates configuration."""
        if btw[0] < self.configuration.shopify_early or btw[1] < self.configuration.shopify_early:
            log("Make sure dates provided are after earliest date set in confg.py")
            raise ValueError
        if btw[0] < btw[1]:
            start_date = dt.isoformat(btw[0]) + "-05:00"
            end_date = dt.isoformat(btw[1]) + "-05:00"
        else:
            start_date = dt.isoformat(btw[1]) + "-05:00"
            end_date = dt.isoformat(btw[0]) + "-05:00"
        return start_date, end_date

    def app_iterator(self):
        """Iterate through API returns for large datasets.
            Perform tasks after each call.
        """
        table_dict = self.shopify_runner()
        for shop_return in table_dict:
            yield shop_return

    def app_runner(self) -> Union[Dict[str, DataFrame], None]:
        """Call API method and run SQL, CSV and data exports."""
        i = 1
        table_dict = self.shopify_runner()
        while True:
            try:
                table_data = next(table_dict)
            except StopIteration:
                break

            i += 1

            if self.sql_alive:
                sql_return = sql_send(table_data, i, self.connection, self.engine)
                if not sql_return:
                    break
            if self.csv_enable:
                csv_writer(table_data, i, self.csv_dir)
        if self.sql_alive:
            self.connection.close()
        if self.custom_enable:
            return self.custom_dict
        return None

    def shopify_runner(self):
        """shopify API data iterator."""
        col_list = [str(key) for key in return_keys]
        col_str = ",".join(col_list)
        init_params = {
            "status": "any",
            "created_at_min": self.start_date,
            "created_at_max": self.end_date,
            "limit": self.shop_config.get('items_per_page'),
            "fields": col_str
        }

        j = 1

        while self.order_url is not None:
            if j == 1:
                page = False
            else:
                page = True
            j += 1
            resp = api_call(self.order_url, self.shop_config, init_params=init_params, page=page)
            self.order_url, self.retry_after = header_link(resp.headers)
            table_dict = pandas_work(resp.json())
            if table_dict is None:
                break

            if self.custom_enable:
                for keys in table_dict:
                    if j == 2:
                        self.custom_dict[keys] = table_dict.get(keys).copy()
                    else:
                        self.custom_dict[keys].append(table_dict.get(keys))
            yield table_dict
