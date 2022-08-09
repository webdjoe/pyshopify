from typing import Optional, List, Dict, Union

api_fields: List[str] = [
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
    'shipping_lines',
    'financial_status',
    'tags',
    'landing_site',
    'referring_site',
    'source_name',
    'source_identifier',
    'source_url'
]


class PandasWorkVars:
    order_cols: List[str] = [
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
        'updated_at',
        'financial_status',
        'customer_id',
        'tags',
    ]

    order_dtypes: Dict[str, str] = {
        'number': 'int64',
        'total_price': 'float64',
        'subtotal_price': 'float64',
        'total_weight': 'float64',
        'total_tax': 'float64',
        'total_discounts': 'float64',
        'total_line_items_price': 'float64',
        'name': 'object',
        'total_price_usd': 'float64',
        'order_number': 'int64',
        'processing_method': 'object',
        'source_name': 'object',
        'fulfillment_status': 'object',
        'email': 'object',
        'customer_id': 'Int64',
        'tags': 'object',
    }
    refund_cols: List[str] = [
        'created_at',
        'id',
        'order_id'
    ]

    refund_dtypes: Dict[str, str] = {
        'id': 'int64',
        'order_id': 'int64'
    }

    refund_li_cols: List[str] = [
        'id',
        'refund_id',
        'order_id',
        'line_item_id',
        'quantity',
        'variant_id',
        'subtotal',
        'total_tax'
    ]

    refund_li_dtypes: Dict[str, str] = {
        'id': 'int64',
        'refund_id': 'int64',
        'order_id': 'int64',
        'line_item_id': 'int64',
        'quantity': 'int64',
        'variant_id': 'int64',
        'subtotal': 'float64',
        'total_tax': 'float64'
    }

    adjustment_cols: List[str] = [
        'id',
        'refund_id',
        'order_id',
        'amount',
        'tax_amount',
        'kind',
        'reason'
    ]

    adjustment_dtypes: Dict[str, str] = {
        'id': 'int64',
        'refund_id': 'int64',
        'order_id': 'int64',
        'amount': 'float64',
        'tax_amount': 'float64',
        'kind': 'object',
        'reason': 'object'
    }

    line_item_cols: List[str] = [
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

    line_item_dtypes: Dict[str, str] = {
        'id': 'int64',
        'order_id': 'int64',
        'variant_id': 'int64',
        'quantity': 'int32',
        'price': 'float64',
        'name': 'object',
        'product_id': 'int64',
        'sku': 'object',
        'title': 'object',
        'total_discount': 'float64',
        'variant_title': 'object'
    }

    transaction_cols: List[str] = [
        'id',
        'source_order_id',
        'type',
        'fee',
        'amount',
        'processed_at'
    ]

    transaction_dtypes: Dict[str, str] = {
        'id': 'int64',
        'source_order_id': 'int64',
        'type': 'object',
        'fee': 'float64',
        'amount': 'float64'
    }

    customer_dtypes: Dict[str, str] = {
        'id': "Int64",
        'last_order_id': "Int64",
        'tags': "object",
        'country': "object",
        'zip': "object",
        'province': "object",
        'city': "object",
        'orders_count': "Int32",
        'email': "object",
        'total_spent': "float64",
    }

    customer_cols: List[str] = [
        'id',
        'created_at',
        'updated_at',
        'default_address_city',
        'email',
        'orders_count',
        'default_address_province',
        'default_address_country',
        'default_address_zip',
        'total_spent',
        'last_order_id',
        'tags'
    ]

    customer_map: Dict[str, str] = {
        'default_address_city': 'city',
        'default_address_province': 'province',
        'default_address_country': 'country',
        'default_address_zip': 'zip',
    }

    discount_app_cols: List[str] = [
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

    discount_app_dtypes: Dict[str, str] = {
        'order_id': 'int64',
        'type': 'object',
        'title': 'object',
        'value': 'float64',
        'value_type': 'object',
        'allocation_method': 'object',
        'target_selection': 'object',
        'target_type': 'object',
        'code': 'object'
    }

    discount_app_map: Dict[str, str] = {
        'orders_id': 'order_id',
        'orders_created_at': 'order_date'
    }

    discount_code_cols: List[str] = [
        'order_id',
        'created_at',
        'code',
        'amount',
        'type'
    ]

    discount_code_dtypes: Dict[str, str] = {
        'order_id': 'int64',
        'code': 'string',
        'type': 'string',
        'amount': 'float64'
    }

    discount_code_map: Dict[str, str] = {
        'orders_id': 'order_id',
        'orders_created_at': 'order_date'
    }

    ship_li_cols: List[str] = [
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

    ship_li_dtypes: Dict[str, str] = {
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

    ship_li_map: Dict[str, str] = {
        'orders.id': 'order_id',
        'orders.created_at': 'order_date',
        'price': 'ship_price',
        'discounted_price': 'ship_discount_price'
    }
    order_attr_cols: List[str] = [
            'id',
            'created_at',
            'landing_site',
            'referring_site',
            'source_name',
            'source_identifier',
            'source_url'
        ]
    order_attr_map: Dict[str, str] = {
        'id': 'order_id',
        'created_at': 'order_date'
    }
    order_attr_dtypes: Dict[str, str] = {
        'order_id': 'int64',
        'landing_site': 'object',
        'referring_site': 'object',
        'source_name': 'object',
        'source_identifier': 'object',
        'source_url': 'object',
    }


def merge_str(db: str, schema: str, tbl_name: str, col_names: List[str],
              merge_cols: List[str], match_on: Optional[list] = None,
              update: bool = True) -> str:
    insert_list = ",".join(f"[{col}]" for col in col_names)
    source_list = ",".join(f"SOURCE.[{col}]" for col in col_names)
    merge_on = " AND ".join(f"TARGET.[{col}] = SOURCE.[{col}]"
                            for col in merge_cols)
    if update is True:
        if match_on is not None:
            match = " AND " + " AND".join(f"TARGET.[{col}] <> SOURCE.[{col}]"
                                          for col in match_on)
        else:
            match = ""
        if isinstance(match_on, list):
            update_cols = [col for col in col_names if col not in set(
                    merge_cols + match_on)]
        update_list = ", ".join(f"TARGET.[{col}] = SOURCE.[{col}]"
                                for col in update_cols)
        return f"""
            MERGE {db}.{schema}.{tbl_name} TARGET
            USING #tmp SOURCE
            ON ({merge_on})
            WHEN MATCHED {match}
            THEN UPDATE SET {update_list}
            WHEN NOT MATCHED BY TARGET
            THEN INSERT ({insert_list})
            VALUES ({source_list});
        """
    return f"""
        MERGE {db}.{schema}.{tbl_name} TARGET
        USING #tmp SOURCE
        ON ({merge_on})
        WHEN NOT MATCHED BY TARGET
        THEN INSERT ({insert_list})
        VALUES ({source_list});
    """


MergeDict: Dict[str, Dict[str, Union[list, str, bool]]] = {
    'Orders': {
        "match_on": ["updated_at"],
        "merge_cols": ["id"],
        "update": True
    },
    'Customers': {
            "match_on": ["updated_at"],
            "merge_cols": ["id"],
            "update": True
    },
    "Refunds": {
        "merge_cols": ["id"],
        "update": False
    },
    "LineItems": {
        "merge_cols": ["id"],
        "update": False
    },
    "RefundLineItem": {
        "merge_cols": ["id"],
        "update": False
    },
    "ShipLines": {
        "merge_cols": ["id"],
        "update": False
    },
    "DiscountCodes": {
        "merge_cols": ["order_id", "code"],
        "update": False
    },
    "DiscountApps": {
        "merge_cols": ["order_id", "code"],
        "update": False
    },
    "OrderAttr": {
        "merge_cols": ["order_id"],
        "update": False
    },
    "Adjustments": {
        "merge_cols": ["id"],
        "update": False
    }
}
