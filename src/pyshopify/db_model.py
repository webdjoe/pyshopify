"""pyshopify database model."""
from typing import Optional
from sqlalchemy import (BigInteger, Boolean, Column, Date, DateTime, Float, Text,
                        Index, Integer, PrimaryKeyConstraint, Unicode, Numeric)
from sqlalchemy.dialects.mssql import MONEY, NVARCHAR
from sqlalchemy.orm import declarative_base, DeclarativeMeta
Base: DeclarativeMeta = declarative_base()
DateBase: DeclarativeMeta = declarative_base()

MONEY_VARIANT = Numeric(10, 4).with_variant(MONEY, 'mssql')
LARGE_UNICODE = Text().with_variant(NVARCHAR(None), 'mssql')


class DBModel:
    """Instance that hold pyshopify database model & metadata."""
    def __init__(self):
        self.adjustments = adjustments()
        self.customers = customers()
        self.discounts = discount_apps()
        self.line_items = line_items()
        self.orders = orders()
        self.discount_codes = discount_codes()
        self.order_attr = order_attr()
        self.order_prices = order_prices()
        self.product_options = product_options()
        self.products = products()
        self.refund_line_item = refund_line_item()
        self.refunds = refunds()
        self.shipping_lines = ship_lines()
        self.variants = variants()
        self.inventory_locations = inventory_locations()
        self.inventory_levels = inventory_levels()
        self.model = Base
        self.date_dimension = date_dimension()
        self.date_model = DateBase

    @staticmethod
    def check_db(db_name: str, dialect: str) -> Optional[str]:
        """Returns the SQL string to check if the database exists."""
        if dialect == 'mssql':
            return f"SELECT name FROM sys.databases WHERE name = '{db_name}'"
        elif dialect in ['mysql', 'mariadb']:
            return None
        raise Exception("Unsupported dialect.")

    @staticmethod
    def make_db(db_name: str, dialect: str) -> str:
        """Returns the SQL string to create the database passed."""
        if dialect == 'mssql':
            return f"""CREATE DATABASE {db_name}"""
        elif dialect in ['mysql', 'mariadb']:
            return f"""CREATE DATABASE IF NOT EXISTS `{db_name}`"""
        raise Exception("Unsupported dialect")

    @staticmethod
    def check_sql_login(login: str) -> str:
        """Returns the SQL string to check if the login exists."""
        return f"SELECT * FROM [master].[sys].[server_principals] \
            WHERE [name] = N'{login}'"

    @staticmethod
    def create_sql_login(login: str, password: str) -> str:
        """Returns the SQL string to create the login passed."""
        return f"CREATE LOGIN {login} WITH PASSWORD = '{password}'"

    @classmethod
    def create_user(cls, dialect: str, user: str, password: str,
                    db: Optional[str] = None) -> dict:
        """Strings to Create User."""
        string_dict = {}
        if dialect == 'mssql':
            string_dict['check_user'] = f"SELECT * FROM sys.database_principals \
                                            WHERE name = N'{user}'"
            string_dict['create_user'] = f"CREATE USER [{user}] FOR LOGIN [{user}]"
            string_dict['auth_user'] = f"EXEC sp_addrolemember N'db_owner', N'{user}'"
        if dialect == 'mysql':
            string_dict['create_user'] = f"CREATE USER IF NOT EXISTS '{user}' \
                IDENTIFIED BY '{password}'"
            string_dict['auth_user'] = f"GRANT ALL ON `{db}`.* TO '{user}'"

        return string_dict


class adjustments(Base):
    """Declarative model class to hold the adjustments table."""
    __tablename__ = 'adjustments'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='PK_adj_id'),
    )

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    refund_id = Column(BigInteger, nullable=False)
    processed_at = Column(DateTime, nullable=False)
    order_date = Column(DateTime, nullable=False)
    order_id = Column(BigInteger, nullable=False)
    amount = Column(MONEY_VARIANT, nullable=False)
    tax_amount = Column(MONEY_VARIANT, nullable=False)
    kind = Column(Unicode(255))
    reason = Column(Unicode(255))


class customers(Base):
    """Declarative model class to hold the customers table."""
    __tablename__ = 'customers'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='PK_customers_id'),
    )

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    updated_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)
    orders_count = Column(Integer, nullable=False)
    total_spent = Column(MONEY_VARIANT, nullable=False)
    email = Column(Unicode(255))
    last_order_id = Column(BigInteger)
    tags = Column(LARGE_UNICODE)
    city = Column(Unicode(255))
    province = Column(Unicode(255))
    country = Column(Unicode(255))
    zip = Column(Unicode(255))


class inventory_levels(Base):
    """Declarative model class to hold the inventory_levels table."""
    __tablename__ = 'inventory_levels'
    __table_args__ = (
        PrimaryKeyConstraint('inventory_item_id', 'location_id',
                             name='PK_inventory_levels_inventory_item_id'),
    )
    inventory_item_id = Column(BigInteger, autoincrement=False)
    location_id = Column(BigInteger, nullable=False)
    available = Column(Integer)
    updated_at = Column(DateTime, nullable=False)


class inventory_locations(Base):
    """Declarative model class to hold the inventory_locations table."""
    __tablename__ = 'inventory_locations'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='PK_inventory_locations_id'),
    )
    id = Column(BigInteger, primary_key=True, autoincrement=False)
    name = Column(Unicode(255), nullable=False)
    address1 = Column(Unicode(255))
    address2 = Column(Unicode(255))
    city = Column(Unicode(255))
    country_code = Column(Unicode(255))
    province_code = Column(Unicode(255))
    updated_at = Column(DateTime, nullable=False)
    zip = Column(Unicode(255))
    active = Column(Boolean, nullable=False)


class date_dimension(DateBase):
    """Declarative model class to hold the date_dimension table."""
    __tablename__ = 'date_dimension'
    __table_args__ = (
        PrimaryKeyConstraint('TheDate', name='PK_date_dimension_thedate'),
    )

    TheDate = Column(Date, primary_key=True, autoincrement=False)
    TheDay = Column(Integer, nullable=False)
    TheDaySuffix = Column(Unicode(2), nullable=False)
    TheDayName = Column(Unicode(30), nullable=False)
    TheDayOfWeek = Column(Integer, nullable=False)
    TheDayOfWeekInMonth = Column(Integer, nullable=False)
    TheDayOfYear = Column(Integer, nullable=False)
    IsWeekend = Column(Integer, nullable=False)
    TheWeek = Column(Integer, nullable=False)
    TheISOWeek = Column(Integer, nullable=False)
    TheFirstOfWeek = Column(Date, nullable=False)
    TheLastOfWeek = Column(Date, nullable=False)
    TheWeekOfMonth = Column(Integer, nullable=False)
    TheMonth = Column(Integer, nullable=False)
    TheMonthName = Column(Unicode(30), nullable=False)
    TheFirstOfMonth = Column(Date, nullable=False)
    TheLastOfMonth = Column(Date, nullable=False)
    TheFirstOfNextMonth = Column(Date, nullable=False)
    TheLastOfNextMonth = Column(Date, nullable=False)
    TheQuarter = Column(Integer, nullable=False)
    TheFirstOfQuarter = Column(Date, nullable=False)
    TheLastOfQuarter = Column(Date, nullable=False)
    TheYear = Column(Integer, nullable=False)
    TheISOYear = Column(Integer, nullable=False)
    TheFirstOfYear = Column(Date, nullable=False)
    TheLastOfYear = Column(Date, nullable=False)
    IsLeapYear = Column(Boolean, nullable=False)
    Has53Weeks = Column(Integer, nullable=False)
    Has53ISOWeeks = Column(Integer, nullable=False)
    MMYYYY = Column(Unicode(6), nullable=False)
    Style101 = Column(Unicode(10), nullable=False)
    Style103 = Column(Unicode(10), nullable=False)
    Style112 = Column(Unicode(8), nullable=False)
    Style120 = Column(Unicode(10), nullable=False)


class discount_apps(Base):
    """Declarative model class to hold the discount_apps table."""
    __tablename__ = 'discount_apps'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='PK_discount_apps'),
        Index('IDX_discount_apps_order_id', 'order_id')
    )

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    order_id = Column(BigInteger, nullable=False)
    processed_at = Column(DateTime, nullable=False)
    type = Column(Unicode(255), nullable=False)
    value = Column(MONEY_VARIANT, nullable=False)
    title = Column(Unicode(255))
    description = Column(Unicode(255))
    value_type = Column(Unicode(255))
    allocation_method = Column(Unicode(255))
    target_selection = Column(Unicode(255))
    target_type = Column(Unicode(255))
    code = Column(Unicode(255))


class discount_codes(Base):
    """Declarative model class to hold the discount_codes table."""
    __tablename__ = 'discount_codes'
    __table_args__ = (
        PrimaryKeyConstraint('order_id', 'code', name='PK_discount_codes'),
        Index('IDX_discount_codes_order_id', 'processed_at')
    )

    order_id = Column(BigInteger, nullable=False)
    processed_at = Column(DateTime, nullable=False)
    code = Column(Unicode(255), nullable=False)
    amount = Column(MONEY_VARIANT, nullable=False)
    type = Column(Unicode(255), nullable=False)


class line_items(Base):
    """Declarative model class to hold the line_items table."""
    __tablename__ = 'line_items'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='PK_line_item_id'),
        Index('IDX_line_items_processed_at', 'processed_at'),
        Index('IDX_line_items_order_id', 'order_id')
    )

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    order_id = Column(BigInteger, nullable=False)
    processed_at = Column(DateTime, nullable=False)
    variant_id = Column(BigInteger, nullable=True)
    quantity = Column(Integer, nullable=False)
    price = Column(MONEY_VARIANT, nullable=False)
    product_id = Column(BigInteger, nullable=True)
    total_discount = Column(MONEY_VARIANT, nullable=False)
    name = Column(Unicode(255))
    sku = Column(Unicode(255))
    title = Column(Unicode(255))
    variant_title = Column(Unicode(255))
    fulfillment_status = Column(Unicode(255))


class order_attr(Base):
    """Declarative model class to hold the order_attr table."""
    __tablename__ = 'order_attr'
    __table_args__ = (
        PrimaryKeyConstraint('order_id', name='PK_order_attr_order_id'),
        Index('IDX_order_attr_processed_at', 'processed_at')
    )

    order_id = Column(BigInteger, primary_key=True, autoincrement=False)
    processed_at = Column(DateTime, nullable=False)
    landing_site = Column(LARGE_UNICODE)
    referring_site = Column(LARGE_UNICODE)
    source_name = Column(LARGE_UNICODE)
    source_identifier = Column(LARGE_UNICODE)
    source_url = Column(LARGE_UNICODE)


class order_prices(Base):
    """Declarative model class to hold the order_prices table."""
    __tablename__ = 'order_prices'
    __table_args__ = (
        PrimaryKeyConstraint('order_id', name='PK_order_prices_order_id'),
        Index('UK_order_prices', 'processed_at')
    )

    order_id = Column(BigInteger, primary_key=True, autoincrement=False)
    processed_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    current_total_discounts = Column(MONEY_VARIANT, nullable=False)
    current_total_price = Column(MONEY_VARIANT, nullable=False)
    current_subtotal_price = Column(MONEY_VARIANT, nullable=False)
    current_total_tax = Column(MONEY_VARIANT, nullable=False)
    subtotal_price = Column(MONEY_VARIANT, nullable=False)
    total_discounts = Column(MONEY_VARIANT, nullable=False)
    total_line_items_price = Column(MONEY_VARIANT, nullable=False)
    total_price = Column(MONEY_VARIANT, nullable=False)
    total_tax = Column(MONEY_VARIANT, nullable=False)
    total_shipping_price = Column(MONEY_VARIANT, nullable=False)
    taxes_included = Column(Boolean, nullable=False)


class orders(Base):
    """Declarative model class to hold the orders table."""
    __tablename__ = 'orders'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='PK_OrderID'),
        Index('IDX_orders_processed_at', 'processed_at'),
        Index('IDX_orders_customer_id', 'customer_id')
    )

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    processed_at = Column(DateTime, nullable=False)
    number = Column(BigInteger, nullable=False)
    total_weight = Column(Float(53), nullable=False)
    name = Column(Unicode(50), nullable=False)
    order_number = Column(BigInteger, nullable=False)
    processing_method = Column(Unicode(255))
    source_name = Column(Unicode(50))
    fulfillment_status = Column(Unicode(50))
    payment_gateway_names = Column(Unicode(255))
    email = Column(Unicode(255))
    financial_status = Column(Unicode(50))
    customer_id = Column(BigInteger)
    tags = Column(LARGE_UNICODE)


class product_options(Base):
    """Declarative model class to hold the product_options table."""
    __tablename__ = 'product_options'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='PK_options'),
    )

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    product_id = Column(BigInteger, nullable=False)
    name = Column(Unicode(100))
    position = Column(Integer)
    values = Column(LARGE_UNICODE)


class products(Base):
    """Declarative model class to hold the products table."""
    __tablename__ = 'products'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='PK_products'),
    )

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    title = Column(Unicode(255))
    body_html = Column(LARGE_UNICODE)
    vendor = Column(Unicode(255))
    product_type = Column(Unicode(255))
    handle = Column(Unicode(255))
    published_at = Column(DateTime)
    template_suffix = Column(Unicode(255))
    status = Column(Unicode(255))
    published_scope = Column(Unicode(255))
    tags = Column(LARGE_UNICODE)
    admin_graphql_api_id = Column(Unicode(255))
    image_src = Column(Unicode(255))


class refund_line_item(Base):
    """Declarative model class to hold the refund_line_item table."""
    __tablename__ = 'refund_line_item'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='PK_refund_line_item_id'),
        Index('IDX_refund_line_item_order_id', 'order_id'),
        Index('IDX_refund_line_item_processed_at', 'processed_at')
    )

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    refund_id = Column(BigInteger, nullable=False)
    processed_at = Column(DateTime, nullable=False)
    order_date = Column(DateTime, nullable=False)
    order_id = Column(BigInteger, nullable=False)
    line_item_id = Column(BigInteger, nullable=False)
    variant_id = Column(BigInteger, nullable=False)
    quantity = Column(Integer, nullable=False)
    subtotal = Column(MONEY_VARIANT, nullable=False)
    total_tax = Column(MONEY_VARIANT, nullable=False)


class refunds(Base):
    """Declarative model class to hold the refunds table."""
    __tablename__ = 'refunds'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='PK_refund_id'),
        Index('IDX_refunds_created_at', 'created_at'),
        Index('IDX_refunds_order_id', 'order_id')
    )

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    created_at = Column(DateTime, nullable=False)
    processed_at = Column(DateTime, nullable=False)
    order_date = Column(DateTime, nullable=False)
    order_id = Column(BigInteger, nullable=False)
    note = Column(LARGE_UNICODE)


class ship_lines(Base):
    """Declarative model class to hold the ship_lines table."""
    __tablename__ = 'ship_lines'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='PK_ship_lines'),
        Index('IDX_ship_lines', 'order_id', 'processed_at')
    )

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    processed_at = Column(DateTime, nullable=False)
    order_id = Column(BigInteger, nullable=False)
    discounted_price = Column(MONEY_VARIANT, nullable=False)
    price = Column(MONEY_VARIANT, nullable=False)
    carrier_identifier = Column(Unicode(255))
    code = Column(Unicode(255))
    delivery_category = Column(Unicode(255))
    phone = Column(Unicode(255))
    requested_fulfillment_service_id = Column(Unicode(255))
    source = Column(Unicode(255))
    title = Column(Unicode(255))


class variants(Base):
    """Declarative model class to hold the variants table."""
    __tablename__ = 'variants'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='PK_variants'),
    )

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    product_id = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    title = Column(Unicode(255))
    price = Column(MONEY_VARIANT)
    sku = Column(Unicode(255))
    position = Column(Integer)
    inventory_policy = Column(Unicode(255))
    compare_at_price = Column(MONEY_VARIANT)
    fulfillment_service = Column(Unicode(255))
    inventory_management = Column(Unicode(255))
    option1 = Column(Unicode(255))
    option2 = Column(Unicode(255))
    option3 = Column(Unicode(255))
    barcode = Column(Unicode(255))
    grams = Column(Integer)
    image_id = Column(BigInteger)
    weight = Column(Float(53))
    weight_unit = Column(Unicode(50))
    inventory_item_id = Column(BigInteger)
    inventory_quantity = Column(Integer)
    old_inventory_quantity = Column(Integer)
    requires_shipping = Column(Boolean)
    admin_graphql_api_id = Column(Unicode(255))
