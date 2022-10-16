"""Process Shopify Return."""
import logging
from typing import Dict, List, Optional, Union, Tuple
import pandas as pd
from numpy import nan
import sqlalchemy as sa
import sqlalchemy.dialects.mssql as mssql
import sqlalchemy.dialects.mysql as mysql
from pyshopify.db_model import DBModel
logger = logging.getLogger(__name__)


def products_work(json_list: list) -> Dict[str, pd.DataFrame]:
    """Parse Products data"""
    products_dict = {}

    prod_table = products_parse(json_list)
    if prod_table is not None:
        products_dict['products'] = prod_table

    variants_table = variants_parse(json_list)
    if variants_table is not None:
        products_dict['variants'] = variants_table

    options_table = options_parse(json_list)
    if options_table is not None:
        products_dict['product_options'] = options_table
    return products_dict


def locations_parse(data: List[dict]) -> pd.DataFrame:
    """Parse inventory locations response."""
    loc_df = pd.DataFrame.from_records(data)
    # loc_df.drop(columns=loc_df.columns.difference(
    #     WorkVars.locations_cols), axis='columns', inplace=True)
    # loc_df = fill_string_cols(loc_df)
    # loc_df.updated_at = pd.to_datetime(loc_df.updated_at, errors='coerce', utc=True)
    loc_df = DFWork.convert_df('inventory_locations', loc_df)
    return loc_df


def inventory_levels_parse(data: List[dict]) -> pd.DataFrame:
    """Parse inventory levels response."""
    inv_df = pd.DataFrame.from_records(data)
    # inv_df.drop(columns=inv_df.columns.difference(
    #     WorkVars.levels_cols), axis='columns', inplace=True)
    # inv_df = fill_string_cols(inv_df)
    # inv_df = inv_df.astype(WorkVars.levels_dtypes)
    # inv_df.updated_at = pd.to_datetime(inv_df.updated_at, errors='coerce', utc=True)
    inv_df = DFWork.convert_df('inventory_levels', inv_df)
    return inv_df


def products_parse(data: List[dict]) -> Optional[pd.DataFrame]:
    """Parse products into dataframe from API response."""
    products = pd.json_normalize(data, sep='_')
    if len(products.index) > 0:
        products = DFWork.convert_df('products', products)
        # products.drop(columns=products.columns.difference(
        #     WorkVars.products_cols), inplace=True, axis='columns')
        # products = products.astype(WorkVars.products_dtypes)
        # products.created_at = pd.to_datetime(products.created_at,
        #                                      errors='coerce', utc=True)
        # products.updated_at = pd.to_datetime(products.updated_at,
        #                                      errors='coerce', utc=True)
        # products.published_at = pd.to_datetime(products.published_at,
        #                                        errors='coerce', utc=True)
        # products = fill_string_cols(products)
        return products
    return None


def variants_parse(data: List[dict]) -> Optional[pd.DataFrame]:
    """Parse variants into dataframe from API response."""
    variants = pd.json_normalize(data, ['variants'])
    if len(variants.index) > 0:
        # variants.drop(columns=variants.columns.difference(
        #     WorkVars.variants_cols), inplace=True, axis='columns')
        # variants.created_at = pd.to_datetime(variants.created_at,
        #                                      errors="coerce", utc=True)
        # variants.updated_at = pd.to_datetime(variants.updated_at,
        #                                      errors="coerce", utc=True)
        # variants = fill_string_cols(variants)
        # variants = variants.astype(WorkVars.variants_dtypes)
        variants = DFWork.convert_df('variants', variants)
        return variants
    return None


def options_parse(data: List[dict]) -> Optional[pd.DataFrame]:
    """Parse Product Options Data."""
    options = pd.json_normalize(data, ['options'])
    if len(options.index) > 0:
        # options.drop(columns=options.columns.difference(WorkVars.options_cols),
        #              inplace=True, axis='columns')
        # options = fill_string_cols(options)
        # options = options.astype(WorkVars.options_dtypes)
        options['values'] = options['values'].apply(",".join)
        options = DFWork.convert_df('product_options', options)

        return options
    return None


def pandas_work(json_list: list) -> Dict[str, pd.DataFrame]:
    """Parse orders API return data."""
    table_dict = {}

    orders, prices = orders_work(json_list)
    if orders is not None:
        table_dict['orders'] = orders
    if prices is not None:
        table_dict['order_prices'] = prices

    ship_lines = ship_lines_work(json_list)
    if ship_lines is not None:
        table_dict['ship_lines'] = ship_lines

    refunds = refunds_work(json_list)
    if refunds is not None:
        table_dict['refunds'] = refunds

        refund_li = refund_line_items_work(json_list)
        if refund_li is not None:
            table_dict['refund_line_item'] = refund_li

        adjustments = adjustments_works(json_list)
        if adjustments is not None:
            table_dict['adjustments'] = adjustments

    discount_apps = discount_app_work(json_list)
    if discount_apps is not None:
        table_dict['discount_apps'] = discount_apps

    discount_codes = discount_code_work(json_list)
    if discount_codes is not None:
        table_dict['discount_codes'] = discount_codes

    line_items = line_item_work(json_list)
    if line_items is not None:
        table_dict['line_items'] = line_items

    order_attr = order_attr_work(json_list)
    if order_attr is not None:
        table_dict['order_attr'] = order_attr

    return table_dict


def order_attr_work(data: list) -> Optional[pd.DataFrame]:
    """Parse order attribution data."""
    attr = pd.json_normalize(data, ['orders'], max_level=1)
    if len(attr.index) > 0:
        attr.rename(columns={'id': 'order_id'}, inplace=True)
        # attr.drop(columns=attr.columns.difference(WorkVars.order_attr_cols),
        #           inplace=True, axis='columns')
        # attr = attr.reindex(columns=WorkVars.order_attr_cols, fill_value='')
        # attr.processed_at = pd.to_datetime(attr.processed_at, errors="coerce", utc=True)
        # attr = fill_string_cols(attr)
        # attr.astype(WorkVars.order_attr_dtypes)
        attr = DFWork.convert_df('order_attr', attr)
        return attr
    return None


def orders_work(data: list
                ) -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame]]:
    """Parse order lines into dataframe from API response."""
    order_data = pd.json_normalize(data, ['orders'], sep='_')
    if len(order_data) > 0:
        # order_data.created_at = pd.to_datetime(order_data.created_at,
        #                                        errors="coerce", utc=True)
        # order_data.updated_at = pd.to_datetime(order_data.updated_at,
        #                                        errors="coerce", utc=True)
        # order_data.processed_at = pd.to_datetime(order_data.processed_at,
        #                                          errors="coerce", utc=True)
        # orders = order_data.drop(columns=order_data.columns.difference(
        #     WorkVars.order_cols), axis='columns')
        # orders.reindex(columns=WorkVars.order_cols, fill_value='')

        # orders = orders.astype(WorkVars.order_dtypes)
        orders = DFWork.convert_df('orders', order_data.copy())

        orders['payment_gateway_names'] = (orders['payment_gateway_names']
                                           .astype(str)
                                           .str.replace('[', '', regex=False))
        orders['payment_gateway_names'] = (orders['payment_gateway_names']
                                           .str.replace(']', '', regex=False))
        orders['payment_gateway_names'] = (orders['payment_gateway_names']
                                           .str.replace("'", '', regex=False))

        prices = order_data.rename(columns={
            'total_shipping_price_set_shop_money_amount': 'total_shipping_price',
            'id': 'order_id'
        })
        prices = DFWork.convert_df('order_prices', prices)
        # prices = prices.drop(columns=prices.columns.difference(
        #     WorkVars.order_prices_cols), axis='columns')
        # prices = prices.astype(WorkVars.order_prices_dtypes)
        # num_cols = ['current_total_discounts',
        #             'current_subtotal_price',
        #             'current_total_price',
        #             'current_total_tax',
        #             'subtotal_price',
        #             'total_discounts',
        #             'total_line_items_price',
        #             'total_price',
        #             'total_tax',
        #             'total_shipping_price']
        # prices = clean_num_cols(prices, num_cols)
        return orders, prices
    return None, None


def ship_lines_work(data: List[dict]) -> Optional[pd.DataFrame]:
    """Parse shipping lines to dataframe from API response."""
    shiplines = pd.json_normalize(data, ['orders', 'shipping_lines'],
                                  meta=[['orders', 'id'],
                                        ['orders', 'processed_at']])
    if len(shiplines.index) > 0:
        shiplines.rename(columns={
            'orders.id': 'order_id',
            'orders.processed_at': 'processed_at'
            },
                         inplace=True)
        shiplines = DFWork.convert_df('ship_lines', shiplines)
        # shiplines.drop(columns=shiplines.columns.difference(
        #     WorkVars.ship_li_cols),
        #     inplace=True, axis='columns')
        # shiplines = shiplines.reindex(columns=WorkVars.ship_li_cols, fill_value='')
        # collist = ['price', 'discounted_price']
        # shiplines = clean_num_cols(shiplines, collist)
        # shiplines = fill_string_cols(shiplines)
        # shiplines.processed_at = pd.to_datetime(shiplines.processed_at,
        #                                         errors="coerce", utc=True)
        # shiplines.astype(WorkVars.ship_li_dtypes)
        return shiplines
    return None


def refunds_work(data: List[dict]) -> Optional[pd.DataFrame]:
    """Parse refunds into dataframe from API Response."""
    refunds = pd.json_normalize(data, ['orders', 'refunds'],
                                meta=[['orders', 'processed_at']])
    if len(refunds.index) > 0:
        refunds.rename(columns={'orders.processed_at': 'order_date'},
                       inplace=True)
        refunds = DFWork.convert_df('refunds', refunds)
        # refunds.drop(columns=refunds.columns.difference(WorkVars.refund_cols),
        #              inplace=True, axis='columns')
        # refunds = refunds.reindex(columns=WorkVars.refund_cols, fill_value='')
        # date_cols = ['created_at', 'processed_at', 'order_date']
        # for col in date_cols:
        #     refunds[col] = pd.to_datetime(refunds[col], errors="coerce", utc=True)
        # refunds = fill_string_cols(refunds)
        # refunds = refunds.astype(WorkVars.refund_dtypes)
        return refunds
    return None


def refund_line_items_work(data: List[dict]) -> Optional[pd.DataFrame]:
    """Parse refund line items from API response into dataframe."""
    refundli = pd.json_normalize(data,
                                 ['orders', 'refunds', 'refund_line_items'],
                                 meta=[['orders', 'refunds', 'id'],
                                       ['orders', 'id'],
                                       ['orders', 'refunds', 'processed_at'],
                                       ['orders', 'processed_at']])
    if len(refundli.index) > 0:
        refundli.rename(columns={
            'orders.refunds.id': 'refund_id',
            'orders.id': 'order_id',
            'orders.refunds.processed_at': 'processed_at',
            'orders.processed_at': 'order_date',
            'line_item.variant_id': 'variant_id',
            'line_item.line_item_id': 'line_item_id'},
            inplace=True)
        refundli = DFWork.convert_df('refund_line_item', refundli)
        # refundli.drop(refundli.columns.difference(WorkVars.refund_li_cols),
        #               inplace=True, axis='columns')
        # refundli = refundli.reindex(columns=WorkVars.refund_li_cols,
        #                             fill_value='')
        # refundli = clean_num_cols(refundli,
        #                           ['quantity', 'subtotal', 'total_tax'])
        # refundli = fill_string_cols(refundli)
        # refundli.processed_at = pd.to_datetime(refundli.processed_at,
        #                                        errors="coerce", utc=True)
        # refundli.order_date = pd.to_datetime(refundli.order_date,
        #                                      errors="coerce", utc=True)
        return refundli
    return None


def adjustments_works(data: List[dict]) -> Optional[pd.DataFrame]:
    """Parse adjustments into dataframe from API response."""
    adjusts = pd.json_normalize(data,
                                ['orders', 'refunds', 'order_adjustments'],
                                meta=[['orders', 'refunds', 'processed_at'],
                                      ['orders', 'processed_at']])
    if len(adjusts.index) > 0:
        adjusts.rename(columns={'orders.refunds.processed_at': 'processed_at',
                                'orders.processed_at': 'order_date'},
                       inplace=True)
        adjusts = DFWork.convert_df('adjustments', adjusts)
        # adjusts.drop(adjusts.columns.difference(WorkVars.adjustment_cols),
        #              inplace=True, axis='columns')
        # adjusts = adjusts.reindex(columns=WorkVars.adjustment_cols,
        #                           fill_value='')
        # adjusts = clean_num_cols(adjusts, ['tax_amount', 'amount'])
        # adjusts = fill_string_cols(adjusts)
        # adjusts = adjusts.astype(WorkVars.adjustment_dtypes)
        # adjusts.processed_at = pd.to_datetime(adjusts.processed_at,
        #                                       errors="coerce", utc=True)
        # adjusts.order_date = pd.to_datetime(adjusts.order_date,
        #                                     errors="coerce", utc=True)
        return adjusts
    return None


def discount_app_work(data: List[dict]) -> Optional[pd.DataFrame]:
    """Parse discount application into dataframe."""
    discapp = pd.json_normalize(data, ['orders', 'discount_applications'],
                                meta=[['orders', 'id'],
                                      ['orders', 'processed_at']],
                                sep='_')
    if len(discapp.index) > 0:
        discapp.rename(columns={
            'orders_id': 'order_id',
            'orders_processed_at': 'processed_at'
            }, inplace=True)
        # discapp = discapp.reindex(columns=WorkVars.discount_app_cols,
        #                           fill_value='')
        # discapp.processed_at = pd.to_datetime(discapp.processed_at,
        #                                       errors="coerce", utc=True)
        # discapp = clean_num_cols(discapp, ['value'])
        # discapp = fill_string_cols(discapp)
        discapp['id_cnt'] = discapp.groupby('order_id').cumcount() + 1
        discapp['id'] = discapp['order_id'].astype(str) + discapp['id_cnt'].astype(str)
        # discapp = discapp.astype(WorkVars.discount_app_dtypes)
        discapp = DFWork.convert_df('discount_apps', discapp)
        return discapp
    return None


def discount_code_work(data: List[dict]) -> Optional[pd.DataFrame]:
    """Parse discount code lines from API response into dataframe."""
    disccode = pd.json_normalize(data, ['orders', 'discount_codes'],
                                 meta=[['orders', 'id'],
                                       ['orders', 'processed_at']],
                                 sep='_')
    if len(disccode.index) > 0:
        disccode.rename(columns={
            'orders_id': 'order_id',
            'orders_processed_at': 'processed_at'
        }, inplace=True)
        # disccode = disccode.reindex(columns=WorkVars.discount_code_cols,
        #                             fill_value='')
        # disccode.processed_at = pd.to_datetime(disccode.processed_at,
        #                                        errors="coerce", utc=True)
        # disccode = clean_num_cols(disccode, ['amount'])
        # disccode = fill_string_cols(disccode)
        # disccode = disccode.astype(WorkVars.discount_code_dtypes)
        disccode = DFWork.convert_df('discount_codes', disccode)
        return disccode
    return None


def line_item_work(data: List[dict]) -> Optional[pd.DataFrame]:
    """Parse order line items into dataframe from API response."""
    lineitems = pd.json_normalize(data, ['orders', 'line_items'],
                                  meta=[['orders', 'id'],
                                        ['orders', 'processed_at']],
                                  max_level=1)

    if len(lineitems.index) > 0:
        lineitems.rename(columns={'orders.id': 'order_id',
                                  'orders.processed_at': 'processed_at'},
                         inplace=True)
        # lineitems.drop(lineitems.columns.difference(WorkVars.line_item_cols),
        #                inplace=True, axis='columns')
        # lineitems = lineitems.reindex(columns=WorkVars.line_item_cols,
        #                               fill_value='')
        # lineitems = clean_num_cols(lineitems,
        #                            ['quantity', 'price', 'total_discount'])
        # lineitems.processed_at = pd.to_datetime(lineitems.processed_at,
        #                                         errors="coerce", utc=True)
        # lineitems = fill_string_cols(lineitems)
        # lineitems = lineitems.astype(WorkVars.line_item_dtypes)
        lineitems = DFWork.convert_df('line_items', lineitems)
        return lineitems
    return None


def customers_work(data: List[dict]) -> Optional[pd.DataFrame]:
    """Parse order customers into dataframe from API response."""
    customers = pd.json_normalize(data, ['customers'], sep='_')
    if len(customers) > 0:
        # customers.drop(columns=customers.columns.difference(
        #     WorkVars.customer_cols),
        #     inplace=True, axis='columns')
        customers.rename(columns={
                'default_address_city': 'city',
                'default_address_province': 'province',
                'default_address_country': 'country',
                'default_address_zip': 'zip'
                }, inplace=True)
        # customers.created_at = pd.to_datetime(customers.created_at,
        #                                       errors="coerce", utc=True)
        # customers.updated_at = pd.to_datetime(customers.updated_at,
        #                                       errors="coerce", utc=True)
        # customers = customers.astype(WorkVars.customer_dtypes)
        customers = DFWork.convert_df('customers', customers)
        return customers
    return None


def clean_num_cols(df: pd.DataFrame,
                   col_list: Union[List[str], str]) -> pd.DataFrame:
    """Clean columns in dataframe."""
    if isinstance(col_list, str):
        col_list = [col_list]
    for col in col_list:
        if col not in df.columns:
            logger.debug("Column % not in dataframe", col)
            continue
        df[col] = (df[col].replace(r'^\s*$', nan, regex=True))
        df[col] = df[col].fillna(0)
    return df


def fill_string_cols(df: pd.DataFrame,
                     exclude_list: Optional[list] = None) -> pd.DataFrame:
    """Fill string columns with empty string."""
    for col in df:
        if exclude_list is not None and col in exclude_list:
            continue
        if df[col].dtype == 'object':
            df[col] = df[col].fillna('')
    return df


class DFWork:
    dtypes = {
        'int64': [sa.BIGINT, sa.BigInteger],
        'int32': [sa.INTEGER, sa.Integer],
        'str': [sa.String, sa.VARCHAR, sa.NVARCHAR, sa.NCHAR,
                sa.Text, sa.Unicode, sa.CHAR, sa.UnicodeText, sa.TEXT,
                mssql.NTEXT, mysql.TEXT, mysql.NCHAR, mysql.NVARCHAR,
                mysql.VARCHAR, mysql.CHAR],
        'int16': [sa.SMALLINT, sa.SmallInteger],
        'bool': [sa.BOOLEAN, sa.Boolean, mssql.BIT],
        'float': [sa.Float, sa.FLOAT, sa.Numeric, sa.NUMERIC, sa.DECIMAL,
                  sa.REAL, mssql.MONEY, mssql.SMALLMONEY, mysql.NUMERIC,
                  mysql.DECIMAL, mysql.FLOAT, mysql.REAL],
    }
    date_types = [sa.DateTime, sa.Date, sa.DATETIME, sa.TIMESTAMP, sa.DATE,
                  mssql.DATETIMEOFFSET]

    @classmethod
    def convert_df(cls, tbl_name: str, df: pd.DataFrame):
        """Convert DataFrame Types Based on SQL Table."""
        model = DBModel().model
        meta = model.metadata
        table = meta.tables[tbl_name]
        df = cls._get_columns(df, table)
        df = cls._fill_null(df, table)
        df_types = cls._get_types(table)
        if df_types:
            df = df.astype(df_types)
        df = cls._convert_dates(df, table)
        return df

    @classmethod
    def _fill_null(cls, df: pd.DataFrame, table: sa.Table) -> pd.DataFrame:
        for col in table.columns:
            if type(col.type) in [
                    *cls.dtypes['int64'], *cls.dtypes['int16'],
                    *cls.dtypes['int32'], *cls.dtypes['float']]:
                df[col.name].replace(r'^\s*$', nan, regex=True, inplace=True)
            if col.nullable is False and type(col.type) in [
                    *cls.dtypes['int64'], *cls.dtypes['int16'],
                    *cls.dtypes['int32'], *cls.dtypes['float']]:
                df[col.name].fillna(0, inplace=True)
            elif type(col.type) in cls.dtypes['str']:
                df[col.name].fillna('', inplace=True)
        return df

    @classmethod
    def _get_columns(cls, df: pd.DataFrame, table: sa.Table) -> pd.DataFrame:
        """Get columns from table."""
        df.drop(df.columns.difference(table.c.keys()),
                inplace=True, axis='columns')
        df = df.reindex(columns=table.c.keys())
        return df

    @classmethod
    def _get_types(cls, tbl: sa.Table) -> dict:
        type_dict = {}
        for col in tbl.c:
            for str_type, sa_types in cls.dtypes.items():
                if type(col.type) in sa_types:
                    type_dict[col.name] = str_type
                    if col.nullable and str_type in ['int64', 'int32', 'int16']:
                        type_dict[col.name] = str_type.replace('i', 'I')
        return type_dict

    @classmethod
    def _convert_dates(cls, df: pd.DataFrame, tbl: sa.Table) -> pd.DataFrame:
        for col in tbl.c:
            if type(col.type) in cls.date_types:
                df[col.name] = pd.to_datetime(df[col.name], errors='coerce', utc=True)
                df[col.name] = df[col.name].dt.tz_convert(None)
        return df
