db_spec = True
try:
    import sqlalchemy.types as sqlt
except:
    db_spec = False

return_keys = [
    'id',
    'created_at',
    'number',
    'total_price',
    'subtotal_price',
    'total_weight',
    'total_tax',
    'total_discounts',
    'total_line_items_price',
    'name',
    'total_price_usd',
    'order_number',
    'processing_method',
    'source_name',
    'fulfillment_status',
    'payment_gateway_names',
    'customer',
    'line_items',
    'refunds',

]

keys_list = [
    'id',
    'created_at',
    'number',
    'total_price',
    'subtotal_price',
    'total_weight',
    'total_tax',
    'total_discounts',
    'total_line_items_price',
    'name',
    'total_price_usd',
    'order_number',
    'processing_method',
    'source_name',
    'fulfillment_status',
    'payment_gateway_names'

]


def DBSpec():
    if db_spec is True:
        order_types = {
            'id': sqlt.BigInteger,
            'order_date': sqlt.DateTime,
            'number': sqlt.BigInteger,
            'total_price': sqlt.Float,
            'subtotal_price': sqlt.Float,
            'total_weight': sqlt.Float,
            'total_tax': sqlt.Float,
            'total_discounts': sqlt.Float,
            'total_line_items_price': sqlt.Float,
            'name': sqlt.String,
            'total_price_usd': sqlt.Float,
            'order_number': sqlt.BigInteger,
            'processing_method': sqlt.String,
            'source_name': sqlt.String,
            'fulfillment_status': sqlt.String,
            'payment_gateway_names': sqlt.String
        }
        ref_types = {
            'id': sqlt.BigInteger,
            'refund_date': sqlt.DateTime,
            'order_id': sqlt.BigInteger
        }
        refli_types = {
            'id': sqlt.BigInteger,
            'refund_id': sqlt.BigInteger,
            'order_id': sqlt.BigInteger,
            'line_item_id': sqlt.BigInteger,
            'quantity': sqlt.Integer,
            'variant_id': sqlt.BigInteger,
            'subtotal': sqlt.Float,
            'total_tax': sqlt.Float
        }
        adj_types = {
            'id': sqlt.BigInteger,
            'refund_id': sqlt.BigInteger,
            'order_id': sqlt.BigInteger,
            'amount': sqlt.Float,
            'tax_amount': sqlt.Float,
            'kind': sqlt.String,
            'reason': sqlt.String
        }
        item_types = {
            'id': sqlt.BigInteger,
            'order_id': sqlt.BigInteger,
            'order_date': sqlt.DateTime,
            'variant_id': sqlt.BigInteger,
            'quantity': sqlt.Integer,
            'price': sqlt.Float
        }
        trans_types = {
            'id': sqlt.BigInteger,
            'source_order_id': sqlt.BigInteger,
            'type': sqlt.String,
            'fee': sqlt.Float,
            'amount': sqlt.Float
        }
        cust_types = {
            'order_id': sqlt.BigInteger,
            'order_date': sqlt.DateTime,
            'customer_id': sqlt.BigInteger,
            'orders_count': sqlt.Integer,
            'email': sqlt.String,
            'created_at': sqlt.DateTime,
            'total_spent': sqlt.Float
        }
    else:
        order_types = {}
        ref_types = {}
        refli_types = {}
        adj_types = {}
        item_types = {}
        trans_types = {}
        cust_types = {}

    return {
        'Refunds': ref_types,
        'Orders': order_types,
        'LineItems': item_types,
        'RefundLineItem': refli_types,
        'Adjustments': adj_types,
        'Transactions': trans_types,
        'Customers': cust_types
        }


order_dtypes = {
    'id': 'string',
    'number': 'int64',
    'total_price': 'float64',
    'subtotal_price': 'float64',
    'total_weight': 'float64',
    'total_tax': 'float64',
    'total_discounts': 'float64',
    'total_line_items_price': 'float64',
    'name': 'string',
    'total_price_usd': 'float64',
    'order_number': 'int64',
    'processing_method': 'string',
    'source_name': 'string',
    'fulfillment_status': 'string',
    'payment_gateway_names': 'string'
}

ref_keys = [
    'created_at',
    'id',
    'order_id'
]

ref_dtypes = {
    'id': 'int64',
    'order_id': 'int64'
}


refli_keys = [
    'id',
    'refund_id',
    'order_id',
    'line_item_id',
    'quantity',
    'variant_id',
    'subtotal',
    'total_tax'
]

refli_dtypes = {
    'id': 'int64',
    'refund_id': 'int64',
    'order_id': 'int64',
    'line_item_id': 'int64',
    'quantity': 'int64',
    'variant_id': 'int64',
    'subtotal': 'float64',
    'total_tax': 'float64'
}



adj_keys = [
    'id',
    'refund_id',
    'order_id',
    'amount',
    'tax_amount',
    'kind',
    'reason'
]

adj_dtypes = {
    'id': 'int64',
    'refund_id': 'int64',
    'order_id': 'int64',
    'amount': 'float64',
    'tax_amount': 'float64',
    'kind': 'string',
    'reason': 'string'
}

item_keys = [
    'id',
    'order_id',
    'variant_id',
    'quantity',
    'price',
    'order_date'
]

item_dtypes = {
    'id': 'int64',
    'order_id': 'int64',
    'variant_id': 'int64',
    'quantity': 'float64',
    'price': 'float64'
}

trans_keys = [
    'id',
    'source_order_id',
    'type',
    'fee',
    'amount',
    'processed_at'
]

trans_dtypes = {
    'id': 'int64',
    'source_order_id': 'int64',
    'type': 'string',
    'fee': 'float64',
    'amount': 'float64'
}




cust_dtypes = {
    'order_id': 'int64',
    'customer_id': 'int64',
    'orders_count': 'int64',
    'email': 'string',
    'total_spent': 'float64'
}


cust_keys = [
    'id',
    'order_date',
    'customer_id',
    'orders_count',
    'email',
    'created_at',
    'total_spent'
]

cust_cols = [
    'id',
    'created_at',
    'customer_id',
    'customer_orders_count',
    'customer_email',
    'customer_created_at',
    'customer_total_spent'
]
cust_map = {
    'id': 'order_id',
    'created_at': 'order_date',
    'customer_id': 'customer_id',
    'customer_orders_count': 'orders_count',
    'customer_email': 'email',
    'customer_created_at': 'created_at',
    'customer_total_spent': 'total_spent'
}



proc_dict = {
    'Orders': 'orders_update',
    'Refunds': 'refunds_update',
    'LineItems': 'lineitems_update',
    'RefundLineItem': 'reflineitem_update',
    'Adjustments': 'adjustments_update',
    'Customers': 'cust_update'

}