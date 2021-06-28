import configparser
import pathlib
import os
from datetime import datetime
from dateutil.parser import parse
from configparser import SectionProxy


class Config:
    def __init__(self, conf='config.ini'):
        default_conf = {
            'shopify': {
                'items_per_page': 250,
                'days': 30
            },
            'sql': {
                'enable': False,
            },
            'csv': {
                'enable': False,
                'filepath': 'csv_export'
            },
            'custom': {
                'enable': False
            }
        }

        self.config_file = pathlib.Path.cwd().joinpath(conf)
        if not os.path.exists(self.config_file):
            raise OSError(f"Config file not found - {self.config_file}")
        self.parser = configparser.ConfigParser()
        self.parser.read_dict(default_conf)
        self.parser.read(str(self.config_file))

    @property
    def shopify(self) -> SectionProxy:
        return self.parser['shopify']

    @property
    def shopify_early(self) -> datetime:
        return parse(self.shopify.get('early_date'))

    @property
    def sql_conf(self) -> SectionProxy:
        return self.parser['sql']

    @property
    def sql_enable(self) -> bool:
        return self.sql_conf.getboolean('enable')

    @sql_enable.setter
    def sql_enable(self, enable: bool) -> None:
        """Enable/Disable SQL Output """
        self.sql_conf['enable'] = str(enable)

    @property
    def csv_conf(self) -> SectionProxy:
        return self.parser['csv']

    @property
    def csv_enable(self) -> bool:
        """CSV Export Enabled/Disabled."""
        return self.csv_conf.getboolean('enable')

    @csv_enable.setter
    def csv_enable(self, enable: bool) -> None:
        """Enable/Disable CSV Output """
        self.csv_conf['enable'] = str(enable)

    @property
    def custom_enable(self) -> bool:
        """Custom return Enabled/Disabled - Calling app_runner returns full dataframe"""
        return self.parser['custom'].getboolean('enable')

    @custom_enable.setter
    def custom_enable(self, enable: bool) -> None:
        """Custom return Enabled/Disabled - Calling app_runner returns full dataframe"""
        self.parser['custom']['enable'] = str(enable)
