"""pyshopify data types and columns."""
from typing import Optional, List, Dict, Union

api_fields: List[str] = [
    'id',
    'created_at',
    'processed_at',
    'number',
    'current_total_discounts',
    'current_total_price',
    'current_subtotal_price',
    'current_total_tax',
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
    'source_url',
    'total_shipping_price_set',
    'taxes_included'
]


class PandasWorkVars:
    """Table columns and types for DataFrames."""
    order_cols: List[str] = [
        'id',
        'created_at',
        'updated_at',
        'processed_at',
        'number',
        'total_weight',
        'name',
        'order_number',
        'processing_method',
        'source_name',
        'fulfillment_status',
        'payment_gateway_names',
        'email',
        'financial_status',
        'customer_id',
        'tags',
    ]

    order_dtypes: Dict[str, str] = {
        'number': 'int64',
        'total_weight': 'float64',
        'name': 'string',
        'order_number': 'int64',
        'processing_method': 'string',
        'source_name': 'string',
        'fulfillment_status': 'string',
        'email': 'string',
        'customer_id': 'Int64',
        'tags': 'string',
    }
    refund_cols: List[str] = [
        'id',
        'created_at',
        'processed_at',
        'order_date',
        'order_id',
        'note'
    ]

    refund_dtypes: Dict[str, str] = {
        'id': 'int64',
        'order_id': 'int64',
        'note': 'string'
    }

    refund_li_cols: List[str] = [
        'id',
        'order_date',
        'processed_at',
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
        'processed_at',
        'order_date',
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
        'kind': 'string',
        'reason': 'string'
    }

    line_item_cols: List[str] = [
        'id',
        'processed_at',
        'order_id',
        'variant_id',
        'quantity',
        'price',
        'name',
        'product_id',
        'sku',
        'title',
        'total_discount',
        'variant_title',
        'fulfillment_status'
    ]

    line_item_dtypes: Dict[str, str] = {
        'id': 'int64',
        'order_id': 'int64',
        'variant_id': 'int64',
        'quantity': 'int32',
        'price': 'float64',
        'name': 'string',
        'product_id': 'int64',
        'sku': 'string',
        'title': 'string',
        'total_discount': 'float64',
        'variant_title': 'string',
        'fulfillment_status': 'string'
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
        'type': 'string',
        'fee': 'float64',
        'amount': 'float64'
    }

    customer_dtypes: Dict[str, str] = {
        'id': "Int64",
        'last_order_id': "Int64",
        'tags': "string",
        'country': "string",
        'zip': "string",
        'province': "string",
        'city': "string",
        'orders_count': "Int32",
        'email': "string",
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
        'processed_at',
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
        'id': 'str',
        'order_id': 'int64',
        'type': 'string',
        'title': 'string',
        'value': 'float64',
        'value_type': 'string',
        'allocation_method': 'string',
        'target_selection': 'string',
        'target_type': 'string',
        'code': 'string'
    }

    discount_code_cols: List[str] = [
        'order_id',
        'processed_at',
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

    ship_li_cols: List[str] = [
        'id',
        'order_id',
        'processed_at',
        'carrier_identifier',
        'code',
        'delivery_category',
        'discounted_price',
        'phone',
        'price',
        'requested_fulfillment_service_id',
        'source',
        'title',
    ]

    ship_li_dtypes: Dict[str, str] = {
        'id': 'string',
        'carrier_identifier': 'string',
        'code': 'string',
        'delivery_category': 'string',
        'discounted_price': 'float64',
        'phone': 'string',
        'price': 'float64',
        'requested_fulfillment_service_id': 'string',
        'source': 'string',
        'title': 'string',
        'order_id': 'int64',
    }

    order_attr_cols: List[str] = [
            'order_id',
            'processed_at',
            'landing_site',
            'referring_site',
            'source_name',
            'source_identifier',
            'source_url'
        ]
    order_attr_dtypes: Dict[str, str] = {
        'order_id': 'int64',
        'landing_site': 'string',
        'referring_site': 'string',
        'source_name': 'string',
        'source_identifier': 'string',
        'source_url': 'string',
    }

    order_prices_cols: List[str] = [
        'order_id',
        'processed_at',
        'updated_at',
        'current_total_discounts',
        'current_subtotal_price',
        'current_total_price',
        'current_total_tax',
        'subtotal_price',
        'total_discounts',
        'total_line_items_price',
        'total_price',
        'total_tax',
        'total_shipping_price',
        'taxes_included'
    ]

    order_prices_dtypes: Dict[str, str] = {
        'order_id': 'int64',
        'current_total_discounts': 'float64',
        'current_subtotal_price': 'float64',
        'current_total_price': 'float64',
        'current_total_tax': 'float64',
        'subtotal_price': 'float64',
        'total_discounts': 'float64',
        'total_line_items_price': 'float64',
        'total_price': 'float64',
        'total_tax': 'float64',
        'total_shipping_price': 'float64',
        'taxes_included': 'boolean'
    }

    products_cols: List[str] = [
        'id',
        'title',
        'body_html',
        'vendor',
        'product_type',
        'created_at',
        'handle',
        'updated_at',
        'published_at',
        'template_suffix',
        'status',
        'published_scope',
        'tags',
        'admin_graphql_api_id',
        'image_src'
    ]
    products_dtypes: Dict[str, str] = {
        'id': 'Int64',
        'title': 'string',
        'body_html': 'string',
        'vendor': 'string',
        'product_type': 'string',
        'handle': 'string',
        'template_suffix': 'string',
        'status': 'string',
        'published_scope': 'string',
        'tags': 'string',
        'admin_graphql_api_id': 'string',
        'image_src': 'string'
    }
    variants_cols: List[str] = [
        'product_id',
        'id',
        'title',
        'price',
        'sku',
        'position',
        'inventory_policy',
        'compare_at_price',
        'fulfillment_service',
        'inventory_management',
        'option1',
        'option2',
        'option3',
        'created_at',
        'updated_at',
        'barcode',
        'grams',
        'image_id',
        'weight',
        'weight_unit',
        'inventory_item_id',
        'inventory_quantity',
        'old_inventory_quantity',
        'requires_shipping',
        'admin_graphql_api_id'
        ]

    variants_dtypes: Dict[str, str] = {
        'product_id': 'Int64',
        'id': 'Int64',
        'title': 'string',
        'price': 'float64',
        'sku': 'string',
        'position': 'Int64',
        'inventory_policy': 'string',
        'compare_at_price': 'float64',
        'fulfillment_service': 'string',
        'inventory_management': 'string',
        'option1': 'string',
        'option2': 'string',
        'option3': 'string',
        'barcode': 'string',
        'grams': 'Int64',
        'image_id': 'Int64',
        'weight': 'float64',
        'weight_unit': 'string',
        'inventory_item_id': 'Int64',
        'inventory_quantity': 'Int64',
        'old_inventory_quantity': 'Int64',
        'requires_shipping': 'bool',
        'admin_graphql_api_id': 'string'
    }

    options_cols: List[str] = [
        'product_id',
        'id',
        'name',
        'position',
        'values'
        ]
    options_dtypes: Dict[str, str] = {
        'product_id': 'int64',
        'id': 'int64',
        'name': 'string',
        'position': 'int64',
        'values': 'string'
    }

    locations_cols: List[str] = [
        "id",
        "name",
        "updated_at",
        "address1",
        "address2",
        "city",
        "province_code",
        "country_code",
        "zip",
        "active",
    ]

    locations_dtypes: Dict[str, str] = {
        "id": "int64",
        "name": "string",
        "address1": "string",
        "address2": "string",
        "city": "string",
        "province_code": "string",
        "country_code": "string",
        "zip": "string",
        "active": "bool",
    }

    levels_cols: List[str] = [
        'inventory_item_id',
        'location_id',
        'available',
        'updated_at',
        'admin_graphql_api_id'
    ]

    levels_dtypes: Dict[str, str] = {
        'inventory_item_id': 'int64',
        'location_id': 'int64',
        'available': 'Int64',
        'admin_graphql_api_id': 'string'
    }


def merge_str(db: str, schema: str, tbl_name: str, col_names: List[str],
              merge_cols: List[str], match_on: Optional[list] = None,
              update: bool = True) -> str:
    insert_list = ",".join(f"[{col}]" for col in col_names)
    source_list = ",".join(f"SOURCE.[{col}]" for col in col_names)
    merge_on = " AND ".join(f"TARGET.[{col}] = SOURCE.[{col}]"
                            for col in merge_cols)
    if update is True:
        match = ""
        if match_on is not None:
            match = " AND " + " AND".join(f"TARGET.[{col}] <> SOURCE.[{col}]"
                                          for col in match_on)
        update_cols = [col for col in col_names if col not in merge_cols]
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
    },
    "Products": {
        "merge_cols": ["id"],
        "match_on": ["updated_at"],
        "update": True
    },
    "Variants": {
        "merge_cols": ["id"],
        "match_on": ["updated_at"],
        "update": True
    },
    "ProductOptions": {
        "merge_cols": ["id"],
        "update": True
    },
    "OrderPrices": {
        "merge_cols": ["order_id"],
        "update": True
    },
    "InventoryLocations": {
        "merge_cols": ["id"],
        "update": True
    },
    "InventoryLevels": {
        "merge_cols": ["location_id", "inventory_item_id"],
        "update": True
    }
}
