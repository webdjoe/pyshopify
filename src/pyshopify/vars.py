from numpy import dtype

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
    'email',
    'discount_applications',
    'discount_codes',
    'updated_at',
    'shipping_lines'

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
    'payment_gateway_names',
    'email',
    'updated_at'

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
            'payment_gateway_names': sqlt.String,
            'email': sqlt.String,
            'updated_at': sqlt.DateTime
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
            'price': sqlt.Float,
            'name': sqlt.String,
            'product_id': sqlt.BigInteger,
            'sku': sqlt.String,
            'title': sqlt.String,
            'total_discount': sqlt.Float,
            'variant_title': sqlt.String
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
        discapp_types = {
            'order_id': sqlt.BigInteger,
            'order_date': sqlt.DateTime,
            'type': sqlt.String,
            'title': sqlt.String,
            'description': sqlt.String,
            'value': sqlt.NUMERIC,
            'value_type': sqlt.String,
            'allocation_method': sqlt.String,
            'target_selection': sqlt.String,
            'target_type': sqlt.String
        }
        disccodes_types = {
            'order_id': sqlt.BigInteger,
            'order_date': sqlt.DateTime,
            'code': sqlt.String,
            'amount': sqlt.DECIMAL,
            'type': sqlt.String,
        }
        shipline_types = {
            'id': sqlt.String,
            'carrier_identifier': sqlt.String,
            'code': sqlt.String,
            'delivery_category': sqlt.String,
            'ship_discount_price': sqlt.Float,
            'phone': sqlt.String,
            'ship_price': sqlt.Float,
            'requested_fulfillment_id': sqlt.String,
            'source': sqlt.String,
            'title': sqlt.String,
            'order_id': sqlt.BigInteger,
            'order_date': sqlt.DateTime,
        }
    else:
        order_types = {}
        ref_types = {}
        refli_types = {}
        adj_types = {}
        item_types = {}
        trans_types = {}
        cust_types = {}
        discapp_types = {}
        disccodes_types = {}
        shipline_types = {}

    return {
        'Refunds': ref_types,
        'Orders': order_types,
        'LineItems': item_types,
        'RefundLineItem': refli_types,
        'Adjustments': adj_types,
        'Transactions': trans_types,
        'Customers': cust_types,
        'DiscountApps': discapp_types,
        'DiscountCodes': disccodes_types,
        'ShipLines': shipline_types
        }


order_dtypes = {
    'number': dtype('int64'),
    'total_price': dtype('float64'),
    'subtotal_price': dtype('float64'),
    'total_weight': dtype('float64'),
    'total_tax': dtype('float64'),
    'total_discounts': dtype('float64'),
    'total_line_items_price': dtype('float64'),
    'name': dtype('O'),
    'total_price_usd': dtype('float64'),
    'order_number': dtype('int64'),
    'processing_method': dtype('O'),
    'source_name': dtype('O'),
    'fulfillment_status': dtype('O'),
    'email': dtype('O')
}

ref_keys = [
    'created_at',
    'id',
    'order_id'
]

ref_dtypes = {
    'id': dtype('int64'),
    'order_id': dtype('int64')
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
    'id': dtype('int64'),
    'refund_id': dtype('int64'),
    'order_id': dtype('int64'),
    'line_item_id': dtype('int64'),
    'quantity': dtype('int64'),
    'variant_id': dtype('int64'),
    'subtotal': dtype('float64'),
    'total_tax': dtype('float64')
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
    'id': dtype('int64'),
    'refund_id': dtype('int64'),
    'order_id': dtype('int64'),
    'amount': dtype('float64'),
    'tax_amount': dtype('float64'),
    'kind': dtype('O'),
    'reason': dtype('O')
}

item_keys = [
    'id',
    'order_id',
    'variant_id',
    'quantity',
    'price',
    'order_date',
    'name',
    'product_id',
    'sku',
    'title',
    'total_discount',
    'variant_title',

]

item_dtypes = {
    'id': dtype('int64'),
    'order_id': dtype('int64'),
    'variant_id': dtype('int64'),
    'quantity': dtype('float64'),
    'price': dtype('float64'),
    'name': dtype('O'),
    'product_id': dtype('int64'),
    'sku': dtype('O'),
    'title': dtype('O'),
    'total_discount': dtype('float64'),
    'variant_title': dtype('O')
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
    'id': dtype('int64'),
    'source_order_id': dtype('int64'),
    'type': dtype('O'),
    'fee': dtype('float64'),
    'amount': dtype('float64')
}




cust_dtypes = {
    'order_id': dtype('int64'),
    'customer_id': dtype('int64'),
    'orders_count': dtype('int64'),
    'email': dtype('O'),
    'total_spent': dtype('float64')
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

discapp_keys = [
    'order_id',
    'order_date',
    'type',
    'code',
    'title',
    'description',
    'value',
    'value_type',
    'allocation_method',
    'target_selection',
    'target_type'
]

discapp_dtypes = {
    'order_id': dtype('int64'),
    'type': dtype('O'),
    'title': dtype('O'),
    'value': dtype('float64'),
    'value_type': dtype('O'),
    'allocation_method': dtype('O'),
    'target_selection': dtype('O'),
    'target_type': dtype('O'),
    'code': dtype('O')
}

discapp_map = {
    'orders_id': 'order_id',
    'orders_created_at': 'order_date'
}

disccode_keys = [
    'order_id',
    'created_at',
    'code',
    'amount',
    'type'
]

disccode_dtypes = {
    'order_id': 'int64',
    'code': 'string',
    'type': 'string',
    'amount': 'float64'
}

disccode_map = {
    'orders_id': 'order_id',
    'orders_created_at': 'order_date'
}

shipline_keys = [
    'id',
    'carrier_identifier',
    'code',
    'delivery_category',
    'discounted_price',
    'phone',
    'price',
    'discounted_price',
    'requested_fulfillment_id',
    'source',
    'title',
    'orders.id',
    'orders.created_at'
]

shipline_dtypes = {
    'id': 'string',
    'carrier_identifier': 'string',
    'code': 'string',
    'delivery_category': 'string',
    'ship_discount_price': 'float64',
    'phone': 'string',
    'ship_price': 'float64',
    'requested_fulfillment_id': 'string',
    'source': 'string',
    'title': 'string',
    'order_id': 'int64',
}

shipline_map = {
    'orders.id': 'order_id',
    'orders.created_at': 'order_date',
    'price': 'ship_price',
    'discounted_price': 'ship_discount_price'
}

proc_dict = {
    'Orders': 'orders_update',
    'Refunds': 'refunds_update',
    'LineItems': 'lineitems_update',
    'RefundLineItem': 'reflineitem_update',
    'Adjustments': 'adjustments_update',
    'Customers': 'cust_update',
    'DiscountApps': 'discapp_update',
    'DiscountCodes': 'disccode_update',
    'ShipLines': 'shipline_update'

}