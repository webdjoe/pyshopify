"""Process Shopify Return."""
import pandas as pd
import json
from numpy import nan, sum
from typing import Dict
import timeit
from pyshopify.vars import (keys_list,
                            order_dtypes,
                            cust_dtypes,
                            ref_dtypes,
                            ref_keys,
                            refli_keys,
                            adj_dtypes,
                            adj_keys,
                            item_dtypes,
                            item_keys,
                            cust_cols,
                            cust_map,
                            discapp_map,
                            discapp_dtypes,
                            disccode_dtypes,
                            disccode_map,
                            discapp_keys,
                            shipline_keys,
                            shipline_map,
                            shipline_dtypes
                            )


def pandas_work(json_list: json) -> Dict[str, pd.DataFrame]:
    """Parse orders API return data."""
    starttime = timeit.default_timer()
    table_dict = {}

    orders = pd.json_normalize(json_list, ['orders'])

    orders.drop(columns=orders.columns.difference(keys_list), inplace=True, axis='columns')

    orders.created_at = pd.to_datetime(orders.created_at)
    orders.updated_at = pd.to_datetime(orders.updated_at)
    orders.fillna(0)

    orders = orders.astype(order_dtypes)

    orders['payment_gateway_names'] = orders['payment_gateway_names'].astype(str).str.replace('[', '', regex=False)
    orders['payment_gateway_names'] = orders['payment_gateway_names'].str.replace(']', '', regex=False)
    orders['payment_gateway_names'] = orders['payment_gateway_names'].str.replace("'", '', regex=False)

    orders.rename(columns={'created_at': 'order_date'}, inplace=True)

    table_dict['Orders'] = orders

    shiplines = pd.json_normalize(json_list, ['orders', 'shipping_lines'],
                                  meta=[['orders', 'id'], ['orders', 'created_at']])
    if len(shiplines.index) > 0:
        shiplines.drop(columns=shiplines.columns.difference(shipline_keys), inplace=True, axis='columns')
        for col in shipline_keys:
            if col not in shiplines.columns:
                shiplines[col] = ''
        collist = ['price', 'discounted_price']
        for column in collist:
            shiplines[column] = shiplines[column].replace(r'\s+', nan, regex=True)
            shiplines[column] = shiplines[column].fillna(0)
        shiplines.rename(columns=shipline_map, inplace=True)
        shiplines.order_date = pd.to_datetime(shiplines.order_date)
        shiplines.astype(shipline_dtypes)
        table_dict['ShipLines'] = shiplines



    refunds = pd.json_normalize(json_list, ['orders', 'refunds'])
    if len(refunds.index) > 0:
        refunds.drop(columns=refunds.columns.difference(ref_keys), inplace=True, axis='columns')
        refunds.created_at = pd.to_datetime(refunds.created_at)
        refunds = refunds.fillna(0)
        refunds = refunds.astype(ref_dtypes)
        refunds.rename(columns={'created_at': 'refund_date'}, inplace=True)
        table_dict['Refunds'] = refunds
        refundli = pd.json_normalize(json_list, ['orders', 'refunds', 'refund_line_items'],
                                     meta=[['orders', 'refunds', 'id'], ['orders', 'id']])

        if len(refundli.index) > 0:
            refundli.rename(columns={
                'orders.refunds.id': 'refund_id',
                'orders.id': 'order_id',
                'line_item.variant_id': 'variant_id',
                'line_item.line_item_id': 'line_item_id'},
                inplace=True)
            refundli.drop(refundli.columns.difference(refli_keys), inplace=True, axis='columns')
            table_dict['RefundLineItem'] = refundli

        adjusts = pd.json_normalize(json_list, ['orders', 'refunds', 'order_adjustments'])
        if len(adjusts.index) > 0:
            adjusts.drop(adjusts.columns.difference(adj_keys), inplace=True, axis='columns')
            adjusts = adjusts.fillna(0)
            adjusts = adjusts.astype(adj_dtypes)
            table_dict['Adjustments'] = adjusts

    discapp = pd.json_normalize(json_list, ['orders', 'discount_applications'],
                                meta=[['orders', 'id'], ['orders', 'created_at']], sep='_')
    if len(discapp.index) > 0:
        discapp.rename(columns=discapp_map, inplace=True)
        for col in discapp_keys:
            if col not in discapp.columns:
                discapp[col] = nan
        discapp.order_date = pd.to_datetime(discapp.order_date)
        discapp[['value']] = discapp[['value']].fillna(0)
        discapp[['code']] = discapp[['code']].fillna('')
        discapp[['title']] = discapp[['title']].fillna('')
        discapp[['description']] = discapp[['description']].fillna('')
        discapp = discapp.astype(discapp_dtypes)
        table_dict['DiscountApps'] = discapp

    disccode = pd.json_normalize(json_list, ['orders', 'discount_codes'],
                                 meta=[['orders', 'id'], ['orders', 'created_at']], sep='_')
    if len(disccode.index) > 0:
        disccode.rename(columns=disccode_map, inplace=True)
        disccode.order_date = pd.to_datetime(disccode.order_date)
        disccode = disccode.fillna(0)
        disccode = disccode.astype(disccode_dtypes)
        table_dict['DiscountCodes'] = disccode

    lineitems = pd.json_normalize(json_list, ['orders', 'line_items'],
                                  meta=[['orders', 'id'], ['orders', 'created_at']], max_level=1)

    if len(lineitems.index) > 0:
        lineitems.rename(columns={'orders.id': 'order_id', 'orders.created_at': 'order_date'}, inplace=True)
        lineitems.drop(lineitems.columns.difference(item_keys), inplace=True, axis='columns')
        lineitems.order_date = pd.to_datetime(lineitems.order_date)
        for col in item_keys:
            if col not in lineitems.columns:
                lineitems[col] = nan
        lineitems[['name']] = lineitems[['name']].fillna('')
        lineitems[['title']] = lineitems[['title']].fillna('')
        lineitems[['sku']] = lineitems[['sku']].fillna('')
        lineitems[['variant_title']] = lineitems[['variant_title']].fillna('')
        lineitems = lineitems.fillna(0)
        lineitems = lineitems.astype(item_dtypes)
        table_dict['LineItems'] = lineitems

    customers = pd.json_normalize(json_list, ['orders'], max_level=2, sep='_')
    customers.drop(columns=customers.columns.difference(cust_cols), inplace=True, axis='columns')
    customers.rename(columns=cust_map, inplace=True)
    customers.created_at = pd.to_datetime(customers.created_at)
    customers.order_date = pd.to_datetime(customers.order_date)
    customers.dropna(inplace=True)
    customers = customers.astype(cust_dtypes)

    table_dict['Customers'] = customers
    return table_dict
