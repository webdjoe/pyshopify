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
    'orders': {
        "match_on": ["updated_at"],
        "merge_cols": ["id"],
        "update": True
    },
    'customers': {
        "match_on": ["updated_at"],
        "merge_cols": ["id"],
        "update": True
    },
    "refunds": {
        "merge_cols": ["id"],
        "update": False
    },
    "line_items": {
        "merge_cols": ["id"],
        "update": False
    },
    "refund_line_item": {
        "merge_cols": ["id"],
        "update": False
    },
    "ship_lines": {
        "merge_cols": ["id"],
        "update": False
    },
    "discount_codes": {
        "merge_cols": ["order_id", "code"],
        "update": False
    },
    "discount_apps": {
        "merge_cols": ["order_id", "code"],
        "update": False
    },
    "order_attr": {
        "merge_cols": ["order_id"],
        "update": False
    },
    "adjustments": {
        "merge_cols": ["id"],
        "update": False
    },
    "products": {
        "merge_cols": ["id"],
        "match_on": ["updated_at"],
        "update": True
    },
    "variants": {
        "merge_cols": ["id"],
        "match_on": ["updated_at"],
        "update": True
    },
    "product_options": {
        "merge_cols": ["id"],
        "update": True
    },
    "order_prices": {
        "merge_cols": ["order_id"],
        "update": True
    },
    "inventory_locations": {
        "merge_cols": ["id"],
        "update": True
    },
    "inventory_levels": {
        "merge_cols": ["location_id", "inventory_item_id"],
        "update": True
    }
}
