"""Process Shopify Return."""
import pandas as pd
import json
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
                            cust_map
                            )


def pandas_work(json_list: json) -> Dict[str, pd.DataFrame]:
    """Parse orders API return data."""
    starttime = timeit.default_timer()
    table_dict = {}

    orders = pd.json_normalize(json_list, ['orders'])

    orders.drop(columns=orders.columns.difference(keys_list), inplace=True, axis='columns')

    orders.created_at = pd.to_datetime(orders.created_at)

    orders.fillna(0)

    orders = orders.astype(order_dtypes)

    orders['payment_gateway_names'] = orders['payment_gateway_names'].str.replace('[', '', regex=False)
    orders['payment_gateway_names'] = orders['payment_gateway_names'].str.replace(']', '', regex=False)
    orders['payment_gateway_names'] = orders['payment_gateway_names'].str.replace("'", '', regex=False)

    orders.rename(columns={'created_at': 'order_date'}, inplace=True)

    table_dict['Orders'] = orders

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

    lineitems = pd.json_normalize(json_list, ['orders', 'line_items'],
                                  meta=[['orders', 'id'], ['orders', 'created_at']], max_level=1)

    if len(lineitems.index) > 0:
        lineitems.rename(columns={'orders.id': 'order_id', 'orders.created_at': 'order_date'}, inplace=True)
        lineitems.drop(lineitems.columns.difference(item_keys), inplace=True, axis='columns')
        lineitems.order_date = pd.to_datetime(lineitems.order_date)
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
