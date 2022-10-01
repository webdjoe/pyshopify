"""Process Shopify Return."""
import logging
from typing import Dict, List, Optional, Union, Tuple
import pandas as pd
from numpy import nan
from pyshopify.vars import PandasWorkVars as WorkVars

logger = logging.getLogger(__name__)


def products_work(json_list: list) -> Dict[str, pd.DataFrame]:
    """Parse Products data"""
    products_dict = {}

    prod_table = products_parse(json_list)
    if prod_table is not None:
        products_dict['Products'] = prod_table

    variants_table = variants_parse(json_list)
    if variants_table is not None:
        products_dict['Variants'] = variants_table

    options_table = options_parse(json_list)
    if options_table is not None:
        products_dict['ProductOptions'] = options_table
    return products_dict


def locations_parse(data: List[dict]) -> pd.DataFrame:
    """Parse inventory locations response."""
    loc_df = pd.DataFrame.from_records(data)
    loc_df.drop(columns=loc_df.columns.difference(
        WorkVars.locations_cols), axis='columns', inplace=True)
    loc_df.updated_at = pd.to_datetime(loc_df.updated_at, errors='coerce', utc=True)
    return loc_df


def inventory_levels_parse(data: List[dict]) -> pd.DataFrame:
    """Parse inventory levels response."""
    inv_df = pd.DataFrame.from_records(data)
    inv_df.drop(columns=inv_df.columns.difference(
        WorkVars.levels_cols), axis='columns', inplace=True)
    inv_df = inv_df.astype(WorkVars.levels_dtypes)
    inv_df.updated_at = pd.to_datetime(inv_df.updated_at, errors='coerce', utc=True)
    return inv_df


def products_parse(data: List[dict]) -> Optional[pd.DataFrame]:
    """Parse products into dataframe from API response."""
    products = pd.json_normalize(data, sep='_')
    if len(products.index) > 0:
        products.drop(columns=products.columns.difference(
            WorkVars.products_cols), inplace=True, axis='columns')
        products = products.astype(WorkVars.products_dtypes)
        products.created_at = pd.to_datetime(products.created_at,
                                             errors='coerce', utc=True)
        products.updated_at = pd.to_datetime(products.updated_at,
                                             errors='coerce', utc=True)
        products.published_at = pd.to_datetime(products.published_at,
                                               errors='coerce', utc=True)
        return products
    return None


def variants_parse(data: List[dict]) -> Optional[pd.DataFrame]:
    """Parse variants into dataframe from API response."""
    variants = pd.json_normalize(data, ['variants'])
    if len(variants.index) > 0:
        variants.drop(columns=variants.columns.difference(
            WorkVars.variants_cols), inplace=True, axis='columns')
        variants.created_at = pd.to_datetime(variants.created_at,
                                             errors="coerce", utc=True)
        variants.updated_at = pd.to_datetime(variants.updated_at,
                                             errors="coerce", utc=True)
        variants = variants.astype(WorkVars.variants_dtypes)
        return variants
    return None


def options_parse(data: List[dict]) -> Optional[pd.DataFrame]:
    """Parse Product Options Data."""
    options = pd.json_normalize(data, ['options'])
    if len(options.index) > 0:
        options.drop(columns=options.columns.difference(WorkVars.options_cols),
                     inplace=True, axis='columns')
        options['values'] = options['values'].apply(lambda x: ",".join(x))
        options = options.astype(WorkVars.options_dtypes)
        return options
    return None


def pandas_work(json_list: list) -> Dict[str, pd.DataFrame]:
    """Parse orders API return data."""
    table_dict = {}

    orders, prices = orders_work(json_list)
    if orders is not None:
        table_dict['Orders'] = orders
    if prices is not None:
        table_dict['OrderPrices'] = prices

    ship_lines = ship_lines_work(json_list)
    if ship_lines is not None:
        table_dict['ShipLines'] = ship_lines

    refunds = refunds_work(json_list)
    if refunds is not None:
        table_dict['Refunds'] = refunds

        refund_li = refund_line_items_work(json_list)
        if refund_li is not None:
            table_dict['RefundLineItem'] = refund_li

        adjustments = adjustments_works(json_list)
        if adjustments is not None:
            table_dict['Adjustments'] = adjustments

    discount_apps = discount_app_work(json_list)
    if discount_apps is not None:
        table_dict['DiscountApps'] = discount_apps

    discount_codes = discount_code_work(json_list)
    if discount_codes is not None:
        table_dict['DiscountCodes'] = discount_codes

    line_items = line_item_work(json_list)
    if line_items is not None:
        table_dict['LineItems'] = line_items

    order_attr = order_attr_work(json_list)
    if order_attr is not None:
        table_dict['OrderAttr'] = order_attr

    return table_dict


def order_attr_work(data: list) -> Optional[pd.DataFrame]:
    """Parse order attribution data."""
    attr = pd.json_normalize(data, ['orders'], max_level=1)
    if len(attr.index) > 0:
        attr.rename(columns={'id': 'order_id'}, inplace=True)
        attr.drop(columns=attr.columns.difference(WorkVars.order_attr_cols),
                  inplace=True, axis='columns')
        attr = attr.reindex(columns=WorkVars.order_attr_cols, fill_value='')
        attr.processed_at = pd.to_datetime(attr.processed_at, errors="coerce", utc=True)
        attr.astype(WorkVars.order_attr_dtypes)
        return attr
    return None


def orders_work(data: list
                ) -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame]]:
    """Parse order lines into dataframe from API response."""
    order_data = pd.json_normalize(data, ['orders'], sep='_')
    if len(order_data) > 0:
        order_data.created_at = pd.to_datetime(order_data.created_at,
                                               errors="coerce", utc=True)
        order_data.updated_at = pd.to_datetime(order_data.updated_at,
                                               errors="coerce", utc=True)
        order_data.processed_at = pd.to_datetime(order_data.processed_at,
                                                 errors="coerce", utc=True)
        orders = order_data.drop(columns=order_data.columns.difference(
            WorkVars.order_cols), axis='columns')
        orders.reindex(columns=WorkVars.order_cols, fill_value='')

        orders = orders.astype(WorkVars.order_dtypes)

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
        prices = prices.drop(columns=prices.columns.difference(
            WorkVars.order_prices_cols), axis='columns')
        prices = prices.astype(WorkVars.order_prices_dtypes)
        num_cols = ['current_total_discounts',
                    'current_subtotal_price',
                    'current_total_price',
                    'current_total_tax',
                    'subtotal_price',
                    'total_discounts',
                    'total_line_items_price',
                    'total_price',
                    'total_tax',
                    'total_shipping_price']
        prices = clean_num_cols(prices, num_cols)
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
        shiplines.drop(columns=shiplines.columns.difference(
            WorkVars.ship_li_cols),
            inplace=True, axis='columns')
        shiplines = shiplines.reindex(columns=WorkVars.ship_li_cols, fill_value='')
        collist = ['price', 'discounted_price']
        shiplines = clean_num_cols(shiplines, collist)
        shiplines.fillna('', inplace=True)
        shiplines.processed_at = pd.to_datetime(shiplines.processed_at,
                                                errors="coerce", utc=True)
        shiplines.astype(WorkVars.ship_li_dtypes)
        return shiplines
    return None


def refunds_work(data: List[dict]) -> Optional[pd.DataFrame]:
    """Parse refunds into dataframe from API Response."""
    refunds = pd.json_normalize(data, ['orders', 'refunds'],
                                meta=[['orders', 'processed_at']])
    if len(refunds.index) > 0:
        refunds.rename(columns={'orders.processed_at': 'order_date'},
                       inplace=True)
        refunds.drop(columns=refunds.columns.difference(WorkVars.refund_cols),
                     inplace=True, axis='columns')
        refunds = refunds.reindex(columns=WorkVars.refund_cols, fill_value='')
        date_cols = ['created_at', 'processed_at', 'order_date']
        for col in date_cols:
            refunds[col] = pd.to_datetime(refunds[col], errors="coerce", utc=True)
        refunds = refunds.fillna('')
        refunds = refunds.astype(WorkVars.refund_dtypes)
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
        refundli.drop(refundli.columns.difference(WorkVars.refund_li_cols),
                      inplace=True, axis='columns')
        refundli = refundli.reindex(columns=WorkVars.refund_li_cols,
                                    fill_value='')
        refundli = clean_num_cols(refundli,
                                  ['quantity', 'subtotal', 'total_tax'])
        refundli.fillna('', inplace=True)
        refundli.processed_at = pd.to_datetime(refundli.processed_at,
                                               errors="coerce", utc=True)
        refundli.order_date = pd.to_datetime(refundli.order_date,
                                             errors="coerce", utc=True)
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
        adjusts.drop(adjusts.columns.difference(WorkVars.adjustment_cols),
                     inplace=True, axis='columns')
        adjusts = adjusts.reindex(columns=WorkVars.adjustment_cols,
                                  fill_value='')
        adjusts = clean_num_cols(adjusts, ['tax_amount', 'amount'])
        adjusts.fillna('', inplace=True)
        adjusts = adjusts.astype(WorkVars.adjustment_dtypes)
        adjusts.processed_at = pd.to_datetime(adjusts.processed_at,
                                              errors="coerce", utc=True)
        adjusts.order_date = pd.to_datetime(adjusts.order_date,
                                            errors="coerce", utc=True)
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
        discapp = discapp.reindex(columns=WorkVars.discount_app_cols,
                                  fill_value='')
        discapp.processed_at = pd.to_datetime(discapp.processed_at,
                                              errors="coerce", utc=True)
        discapp = clean_num_cols(discapp, ['value'])
        discapp.fillna('', inplace=True)
        discapp['id_cnt'] = discapp.groupby('order_id').cumcount() + 1
        discapp['id'] = discapp['order_id'].astype(str) + discapp['id_cnt'].astype(str)
        discapp = discapp.astype(WorkVars.discount_app_dtypes)
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
        disccode = disccode.reindex(columns=WorkVars.discount_code_cols,
                                    fill_value='')
        disccode.processed_at = pd.to_datetime(disccode.processed_at,
                                               errors="coerce", utc=True)
        disccode = clean_num_cols(disccode, ['amount'])
        disccode = disccode.fillna('')
        disccode = disccode.astype(WorkVars.discount_code_dtypes)
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
        lineitems.drop(lineitems.columns.difference(WorkVars.line_item_cols),
                       inplace=True, axis='columns')
        lineitems = lineitems.reindex(columns=WorkVars.line_item_cols,
                                      fill_value='')
        lineitems = clean_num_cols(lineitems,
                                   ['quantity', 'price', 'total_discount'])
        lineitems.processed_at = pd.to_datetime(lineitems.processed_at,
                                                errors="coerce", utc=True)
        lineitems = lineitems.fillna('')
        lineitems = lineitems.astype(WorkVars.line_item_dtypes)
        return lineitems
    return None


def customers_work(data: List[dict]) -> Optional[pd.DataFrame]:
    """Parse order customers into dataframe from API response."""
    customers = pd.json_normalize(data, ['customers'], sep='_')
    if len(customers) > 0:
        customers.drop(columns=customers.columns.difference(
            WorkVars.customer_cols),
            inplace=True, axis='columns')
        customers.rename(columns=WorkVars.customer_map, inplace=True)
        customers.created_at = pd.to_datetime(customers.created_at,
                                              errors="coerce", utc=True)
        customers.updated_at = pd.to_datetime(customers.updated_at,
                                              errors="coerce", utc=True)
        customers = customers.astype(WorkVars.customer_dtypes)
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
