import configparser
import pathlib
import os
from typing import Mapping
from configparser import SectionProxy

SHOP_ENV_MAP = {
    "STORE_NAME": "store_name",
    "SHOPIFY_API_KEY": "access_token",
    "SHOPIFY_API_VERSION": "version",
}

SQL_ENV_MAP = {
    "SHOPIFY_DB_NAME": "database",
    "SHOPIFY_DB_USER": "db_user",
    "SHOPIFY_DB_PASSWORD": "db_password",
    "SHOPIFY_DB_SHCHEMA": "schema",
    "SHOPIFY_DB_PORT": "port",
    "SHOPIFY_DB_SERVER": "server",
    "SHOPIFY_WINDOWS_AUTH": "windows_auth"
}


class Config:
    """Configuration Class for pyshopify using configparser.

    The parser is initialized with a default configuration and
    then loads a configuration file if it exists, followed by a
    configuration dictionary if supplied.

    The parser object is available as self.parser.
    """
    def __init__(self, conf: str = ''):
        default_conf: Mapping[str, Mapping] = {
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
                'server': 'localhost'
            },
            'csv': {
                'filepath': 'csv_export',
            },
        }

        if conf == '':
            conf = os.getenv('CONFIG_FILE', 'config.ini')
        path_obj = pathlib.Path(conf)
        if path_obj.is_absolute():
            self.config_file = path_obj
        else:
            self.config_file = pathlib.Path.cwd().joinpath(conf)

        self.parser = configparser.ConfigParser()
        self.parser.read_dict(default_conf)
        self.configure_env()
        if self.config_file.exists():
            self.parser.read(str(self.config_file))

    def configure_env(self) -> None:
        """Configure from environment variables."""
        for k, v in SHOP_ENV_MAP.items():
            if k in os.environ:
                self.parser.set('shopify', v, os.environ[k])
        for k, v in SQL_ENV_MAP.items():
            if k in os.environ:
                self.parser.set('sql', v, os.environ[k])

    @property
    def shopify(self) -> SectionProxy:
        """Shopify Configuration Section."""
        return self.parser['shopify']

    @property
    def time_zone(self) -> str:
        """Time zone from Shopify configuration."""
        return self.shopify['timezone']

    @property
    def sql_conf(self) -> SectionProxy:
        """SQL Configuration Section."""
        return self.parser['sql']

    @property
    def csv_conf(self) -> SectionProxy:
        """CSV Configuration Section."""
        return self.parser['csv']
