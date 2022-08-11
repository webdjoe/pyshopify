"""Process Shopify Return."""
import pandas as pd
from numpy import nan
from typing import Dict, List, Optional
from pyshopify.vars import PandasWorkVars as WorkVars


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


def products_parse(data: List[dict]) -> Optional[pd.DataFrame]:
    """Parse products into dataframe from API response."""
    products = pd.json_normalize(data, sep='_')
    if len(products.index) > 0:
        products.drop(columns=products.columns.difference(
            WorkVars.products_cols), inplace=True, axis='columns')
        products.astype(WorkVars.products_dtypes)
        products.created_at = pd.to_datetime(products.created_at)
        products.updated_at = pd.to_datetime(products.updated_at)
        products.published_at = pd.to_datetime(products.published_at)
        return products
    return None


def variants_parse(data: List[dict]) -> Optional[pd.DataFrame]:
    """Parse variants into dataframe from API response."""
    variants = pd.json_normalize(data, ['variants'])
    if len(variants.index) > 0:
        variants.drop(columns=variants.columns.difference(
            WorkVars.variants_cols), inplace=True, axis='columns')
        variants.created_at = pd.to_datetime(variants.created_at)
        variants.updated_at = pd.to_datetime(variants.updated_at)
        variants = variants.astype(WorkVars.variants_dtypes)
        return variants
    return None


def options_parse(data: List[dict]) -> Optional[pd.DataFrame]:
    """Parse Product Options Data."""
    options = pd.json_normalize(data, ['options'])
    if len(options.index) > 0:
        options.drop(columns=options.columns.difference(WorkVars.options_cols),
                     inplace=True, axis='columns')
        options = options.astype(WorkVars.options_dtypes)
        return options
    return None


def pandas_work(json_list: list) -> Dict[str, pd.DataFrame]:
    """Parse orders API return data."""
    table_dict = {}

    orders = orders_work(json_list)
    if orders is not None:
        table_dict['Orders'] = orders

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
        attr.drop(columns=attr.columns.difference(WorkVars.order_attr_cols),
                  inplace=True, axis='columns')
        attr.rename(columns=WorkVars.order_attr_map, inplace=True)
        attr.astype(WorkVars.order_attr_dtypes)
        return attr
    return None


def orders_work(data: list) -> Optional[pd.DataFrame]:
    """Parse order lines into dataframe from API response."""
    orders = pd.json_normalize(data, ['orders'], sep='_')
    if len(orders) > 0:
        orders.drop(columns=orders.columns.difference(WorkVars.order_cols),
                    inplace=True, axis='columns')
        orders.created_at = pd.to_datetime(orders.created_at)
        orders.updated_at = pd.to_datetime(orders.updated_at)
        orders.fillna(0)

        orders = orders.astype(WorkVars.order_dtypes)

        orders['payment_gateway_names'] = (orders['payment_gateway_names']
                                           .astype(str)
                                           .str.replace('[', '', regex=False))
        orders['payment_gateway_names'] = (orders['payment_gateway_names']
                                           .str.replace(']', '', regex=False))
        orders['payment_gateway_names'] = (orders['payment_gateway_names']
                                           .str.replace("'", '', regex=False))

        orders.rename(columns={'created_at': 'order_date'}, inplace=True)
        return orders
    return None


def ship_lines_work(data: List[dict]) -> Optional[pd.DataFrame]:
    """Parse shipping lines to dataframe from API response."""
    shiplines = pd.json_normalize(data, ['orders', 'shipping_lines'],
                                  meta=[['orders', 'id'],
                                        ['orders', 'created_at']])
    if len(shiplines.index) > 0:
        shiplines.drop(columns=shiplines.columns.difference(
            WorkVars.ship_li_cols),
            inplace=True, axis='columns')
        for col in WorkVars.ship_li_cols:
            if col not in shiplines.columns:
                shiplines[col] = ''
        collist = ['price', 'discounted_price']
        for column in collist:
            shiplines[column] = (shiplines[column]
                                 .replace(r'\s+', nan, regex=True))
            shiplines[column] = shiplines[column].fillna(0)
        shiplines.rename(columns=WorkVars.ship_li_map, inplace=True)
        shiplines.order_date = pd.to_datetime(shiplines.order_date)
        shiplines.astype(WorkVars.ship_li_dtypes)
        return shiplines
    return None


def refunds_work(data: List[dict]) -> Optional[pd.DataFrame]:
    """Parse refunds into dataframe from API Response."""
    refunds = pd.json_normalize(data, ['orders', 'refunds'])
    if len(refunds.index) > 0:
        refunds.drop(columns=refunds.columns.difference(WorkVars.refund_cols),
                     inplace=True, axis='columns')
        refunds.created_at = pd.to_datetime(refunds.created_at)
        refunds = refunds.fillna(0)
        refunds = refunds.astype(WorkVars.refund_dtypes)
        refunds.rename(columns={'created_at': 'refund_date'}, inplace=True)
        return refunds
    return None


def refund_line_items_work(data: List[dict]) -> Optional[pd.DataFrame]:
    """Parse refund line items from API response into dataframe."""
    refundli = pd.json_normalize(data,
                                 ['orders', 'refunds', 'refund_line_items'],
                                 meta=[['orders', 'refunds', 'id'],
                                       ['orders', 'id']])
    if len(refundli.index) > 0:
        refundli.rename(columns={
            'orders.refunds.id': 'refund_id',
            'orders.id': 'order_id',
            'line_item.variant_id': 'variant_id',
            'line_item.line_item_id': 'line_item_id'},
            inplace=True)
        refundli.drop(refundli.columns.difference(WorkVars.refund_li_cols),
                      inplace=True, axis='columns')
        return refundli
    return None


def adjustments_works(data: List[dict]) -> Optional[pd.DataFrame]:
    """Parse adjustments into dataframe from API response."""
    adjusts = pd.json_normalize(data,
                                ['orders', 'refunds', 'order_adjustments'])
    if len(adjusts.index) > 0:
        adjusts.drop(adjusts.columns.difference(WorkVars.adjustment_cols),
                     inplace=True, axis='columns')
        adjusts = adjusts.fillna(0)
        adjusts = adjusts.astype(WorkVars.adjustment_dtypes)
        return adjusts
    return None


def discount_app_work(data: List[dict]) -> Optional[pd.DataFrame]:
    """Parse discount application into dataframe."""
    discapp = pd.json_normalize(data, ['orders', 'discount_applications'],
                                meta=[['orders', 'id'],
                                      ['orders', 'created_at']],
                                sep='_')
    if len(discapp.index) > 0:
        discapp.rename(columns=WorkVars.discount_app_map, inplace=True)
        for col in WorkVars.discount_app_cols:
            if col not in discapp.columns:
                discapp[col] = nan
        discapp.order_date = pd.to_datetime(discapp.order_date)
        discapp[['value']] = discapp[['value']].fillna(0)
        discapp[['code']] = discapp[['code']].fillna('')
        discapp[['title']] = discapp[['title']].fillna('')
        discapp[['description']] = discapp[['description']].fillna('')
        discapp = discapp.astype(WorkVars.discount_app_dtypes)
        return discapp
    return None


def discount_code_work(data: List[dict]) -> Optional[pd.DataFrame]:
    """Parse discount code lines from API response into dataframe."""
    disccode = pd.json_normalize(data, ['orders', 'discount_codes'],
                                 meta=[['orders', 'id'],
                                       ['orders', 'created_at']],
                                 sep='_')
    if len(disccode.index) > 0:
        disccode.rename(columns=WorkVars.discount_code_map, inplace=True)
        disccode.order_date = pd.to_datetime(disccode.order_date)
        disccode = disccode.fillna(0)
        disccode = disccode.astype(WorkVars.discount_code_dtypes)
        return disccode
    return None


def line_item_work(data: List[dict]) -> Optional[pd.DataFrame]:
    """Parse order line items into dataframe from API response."""
    lineitems = pd.json_normalize(data, ['orders', 'line_items'],
                                  meta=[['orders', 'id'],
                                        ['orders', 'created_at']],
                                  max_level=1)

    if len(lineitems.index) > 0:
        lineitems.rename(columns={'orders.id': 'order_id',
                                  'orders.created_at': 'order_date'},
                         inplace=True)
        lineitems.drop(lineitems.columns.difference(WorkVars.line_item_cols),
                       inplace=True, axis='columns')
        lineitems.order_date = pd.to_datetime(lineitems.order_date)
        for col in WorkVars.line_item_cols:
            if col not in lineitems.columns:
                lineitems[col] = nan
        lineitems[['name']] = lineitems[['name']].fillna('')
        lineitems[['title']] = lineitems[['title']].fillna('')
        lineitems[['sku']] = lineitems[['sku']].fillna('')
        lineitems[['variant_title']] = lineitems[['variant_title']].fillna('')
        lineitems = lineitems.fillna(0)
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
        customers.created_at = pd.to_datetime(customers.created_at)
        customers.updated_at = pd.to_datetime(customers.updated_at)
        customers = customers.astype(WorkVars.customer_dtypes)
        return customers
    return None
