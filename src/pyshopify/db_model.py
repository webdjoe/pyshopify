"""pyshopify database model."""
from sqlalchemy import (BigInteger, Boolean, Column, Date, DateTime, Float,
                        Index, Integer, PrimaryKeyConstraint, Unicode)
from sqlalchemy.dialects.mssql import MONEY, TINYINT, NCHAR
from sqlalchemy.orm import declarative_base, DeclarativeMeta

Base: DeclarativeMeta = declarative_base()
DateBase: DeclarativeMeta = declarative_base()


class DBModel:
    """Instance that hold pyshopify database model & metadata."""
    def __init__(self):
        self.Adjustments = Adjustments()
        self.Customers = Customers()
        self.Discounts = DiscountApps()
        self.LineItems = LineItems()
        self.Orders = Orders()
        self.DiscountCodes = DiscountCodes()
        self.OrderAttr = OrderAttr()
        self.OrderPrices = OrderPrices()
        self.ProductOptions = ProductOptions()
        self.Products = Products()
        self.RefundLineItems = RefundLineItem()
        self.Refunds = Refunds()
        self.ShippingLines = ShipLines()
        self.Variants = Variants()
        self.InventoryLocations = InventoryLocations()
        self.InventoryLevels = InventoryLevels()
        self.model = Base
        self.DateDimension = DateDimension()
        self.date_model = DateBase

    @staticmethod
    def make_schema(schema_name: str, auth: str = 'dbo') -> str:
        """Returns the SQL string to create the schema passed."""
        return f'CREATE SCHEMA [{schema_name}] AUTHORIZATION [{auth}]'

    @staticmethod
    def make_db(db_name: str) -> str:
        """Returns the SQL string to create the database passed."""
        return f"""CREATE DATABASE {db_name}"""

    @staticmethod
    def check_schema(schema_name: str) -> str:
        """Returns the SQL string to check if the schema exists."""
        return f"""SELECT SCHEMA_ID('{schema_name}')"""

    @staticmethod
    def alter_db(db_name) -> str:
        """Returns the SQL string to alter the database created."""
        return f"""
        ALTER DATABASE {db_name}
        SET
        ANSI_NULL_DEFAULT OFF,
        ANSI_NULLS OFF,
        ANSI_PADDING OFF,
        ANSI_WARNINGS OFF,
        ARITHABORT OFF,
        AUTO_CLOSE OFF,
        AUTO_CREATE_STATISTICS ON,
        AUTO_SHRINK OFF,
        AUTO_UPDATE_STATISTICS ON,
        AUTO_UPDATE_STATISTICS_ASYNC OFF,
        COMPATIBILITY_LEVEL = 150,
        CONCAT_NULL_YIELDS_NULL OFF,
        CURSOR_CLOSE_ON_COMMIT OFF,
        CURSOR_DEFAULT GLOBAL,
        DATE_CORRELATION_OPTIMIZATION OFF,
        DB_CHAINING OFF,
        HONOR_BROKER_PRIORITY OFF,
        MULTI_USER,
        NESTED_TRIGGERS = ON,
        NUMERIC_ROUNDABORT OFF,
        PAGE_VERIFY CHECKSUM,
        PARAMETERIZATION SIMPLE,
        QUOTED_IDENTIFIER OFF,
        READ_COMMITTED_SNAPSHOT OFF,
        RECOVERY FULL,
        RECURSIVE_TRIGGERS OFF,
        TRANSFORM_NOISE_WORDS = OFF,
        TRUSTWORTHY OFF
        WITH ROLLBACK IMMEDIATE
    """


class Adjustments(Base):
    """Declarative model class to hold the Adjustments table."""
    __tablename__ = 'Adjustments'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='PK_adj_id'),
    )

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    refund_id = Column(BigInteger, nullable=False)
    processed_at = Column(DateTime, nullable=False)
    order_date = Column(DateTime, nullable=False)
    order_id = Column(BigInteger, nullable=False)
    amount = Column(MONEY, nullable=False)
    tax_amount = Column(MONEY, nullable=False)
    kind = Column(Unicode(255))
    reason = Column(Unicode(255))


class Customers(Base):
    """Declarative model class to hold the Customers table."""
    __tablename__ = 'Customers'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='PK_Customers_id'),
    )

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    updated_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)
    orders_count = Column(Integer, nullable=False)
    total_spent = Column(MONEY, nullable=False)
    email = Column(Unicode(255))
    last_order_id = Column(BigInteger)
    tags = Column(Unicode)
    city = Column(Unicode(255))
    province = Column(Unicode(255))
    country = Column(Unicode(255))
    zip = Column(Unicode(255))


class InventoryLevels(Base):
    """Declarative model class to hold the InventoryLevels table."""
    __tablename__ = 'InventoryLevels'
    __table_args__ = (
        PrimaryKeyConstraint('inventory_item_id', 'location_id',
                             name='PK_InventoryLevels_inventory_item_id'),
    )
    inventory_item_id = Column(BigInteger, autoincrement=False)
    location_id = Column(BigInteger, nullable=False)
    available = Column(Integer)
    updated_at = Column(DateTime, nullable=False)


class InventoryLocations(Base):
    """Declarative model class to hold the InventoryLocations table."""
    __tablename__ = 'InventoryLocations'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='PK_InventoryLocations_id'),
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


class DateDimension(DateBase):
    """Declarative model class to hold the DateDimension table."""
    __tablename__ = 'DateDimension'
    __table_args__ = (
        PrimaryKeyConstraint('TheDate', name='PK_DateDimension_TheDate'),
    )

    TheDate = Column(Date, primary_key=True, autoincrement=False)
    TheDay = Column(Integer, nullable=False)
    TheDaySuffix = Column(NCHAR(2), nullable=False)
    TheDayName = Column(Unicode(30), nullable=False)
    TheDayOfWeek = Column(Integer, nullable=False)
    TheDayOfWeekInMonth = Column(TINYINT, nullable=False)
    TheDayOfYear = Column(Integer, nullable=False)
    IsWeekend = Column(Integer, nullable=False)
    TheWeek = Column(Integer, nullable=False)
    TheISOWeek = Column(Integer, nullable=False)
    TheFirstOfWeek = Column(Date, nullable=False)
    TheLastOfWeek = Column(Date, nullable=False)
    TheWeekOfMonth = Column(TINYINT, nullable=False)
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
    MMYYYY = Column(NCHAR(6), nullable=False)
    Style101 = Column(NCHAR(10), nullable=False)
    Style103 = Column(NCHAR(10), nullable=False)
    Style112 = Column(NCHAR(8), nullable=False)
    Style120 = Column(NCHAR(10), nullable=False)


class DiscountApps(Base):
    """Declarative model class to hold the DiscountApps table."""
    __tablename__ = 'DiscountApps'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='PK_DiscountApps'),
        Index('IDX_DiscountApps_order_id', 'order_id')
    )

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    order_id = Column(BigInteger, nullable=False)
    processed_at = Column(DateTime, nullable=False)
    type = Column(Unicode(255), nullable=False)
    value = Column(MONEY, nullable=False)
    title = Column(Unicode(255))
    description = Column(Unicode(255))
    value_type = Column(Unicode(255))
    allocation_method = Column(Unicode(255))
    target_selection = Column(Unicode(255))
    target_type = Column(Unicode(255))
    code = Column(Unicode(255))


class DiscountCodes(Base):
    """Declarative model class to hold the DiscountCodes table."""
    __tablename__ = 'DiscountCodes'
    __table_args__ = (
        PrimaryKeyConstraint('order_id', 'code', name='PK_DiscountCodes'),
        Index('IDX_DiscountCodes_order_id', 'processed_at')
    )

    order_id = Column(BigInteger, nullable=False)
    processed_at = Column(DateTime, nullable=False)
    code = Column(Unicode(255), nullable=False)
    amount = Column(MONEY, nullable=False)
    type = Column(Unicode(255), nullable=False)


class LineItems(Base):
    """Declarative model class to hold the LineItems table."""
    __tablename__ = 'LineItems'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='PK_line_item_id'),
        Index('IDX_LineItems_processed_at', 'processed_at'),
        Index('IDX_LineItems_order_id', 'order_id')
    )

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    order_id = Column(BigInteger, nullable=False)
    processed_at = Column(DateTime, nullable=False)
    variant_id = Column(BigInteger, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(MONEY, nullable=False)
    product_id = Column(BigInteger, nullable=False)
    total_discount = Column(MONEY, nullable=False)
    name = Column(Unicode(255))
    sku = Column(Unicode(255))
    title = Column(Unicode(255))
    variant_title = Column(Unicode(255))
    fulfillment_status = Column(Unicode(255))


class OrderAttr(Base):
    """Declarative model class to hold the OrderAttr table."""
    __tablename__ = 'OrderAttr'
    __table_args__ = (
        PrimaryKeyConstraint('order_id', name='PK_OrderAttr_order_id'),
        Index('IDX_OrderAttr_processed_at', 'processed_at')
    )

    order_id = Column(BigInteger, primary_key=True, autoincrement=False)
    processed_at = Column(DateTime, nullable=False)
    landing_site = Column(Unicode)
    referring_site = Column(Unicode)
    source_name = Column(Unicode)
    source_identifier = Column(Unicode)
    source_url = Column(Unicode)


class OrderPrices(Base):
    """Declarative model class to hold the OrderPrices table."""
    __tablename__ = 'OrderPrices'
    __table_args__ = (
        PrimaryKeyConstraint('order_id', name='PK_OrderPrices_order_id'),
        Index('UK_OrderPrices', 'processed_at')
    )

    order_id = Column(BigInteger, primary_key=True, autoincrement=False)
    processed_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    current_total_discounts = Column(MONEY, nullable=False)
    current_total_price = Column(MONEY, nullable=False)
    current_subtotal_price = Column(MONEY, nullable=False)
    current_total_tax = Column(MONEY, nullable=False)
    subtotal_price = Column(MONEY, nullable=False)
    total_discounts = Column(MONEY, nullable=False)
    total_line_items_price = Column(MONEY, nullable=False)
    total_price = Column(MONEY, nullable=False)
    total_tax = Column(MONEY, nullable=False)
    total_shipping_price = Column(MONEY, nullable=False)
    taxes_included = Column(Boolean, nullable=False)


class Orders(Base):
    """Declarative model class to hold the Orders table."""
    __tablename__ = 'Orders'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='PK_OrderID'),
        Index('IDX_Orders_processed_at', 'processed_at'),
        Index('IDX_Orders_customer_id', 'customer_id')
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
    tags = Column(Unicode)


class ProductOptions(Base):
    """Declarative model class to hold the ProductOptions table."""
    __tablename__ = 'ProductOptions'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='PK_options'),
    )

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    product_id = Column(BigInteger, nullable=False)
    name = Column(Unicode(100))
    position = Column(Integer)
    values = Column(Unicode)


class Products(Base):
    """Declarative model class to hold the Products table."""
    __tablename__ = 'Products'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='PK_products'),
    )

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    title = Column(Unicode(255))
    body_html = Column(Unicode)
    vendor = Column(Unicode(255))
    product_type = Column(Unicode(255))
    handle = Column(Unicode(255))
    published_at = Column(DateTime)
    template_suffix = Column(Unicode(255))
    status = Column(Unicode(255))
    published_scope = Column(Unicode(255))
    tags = Column(Unicode)
    admin_graphql_api_id = Column(Unicode(255))
    image_src = Column(Unicode(255))


class RefundLineItem(Base):
    """Declarative model class to hold the RefundLineItem table."""
    __tablename__ = 'RefundLineItem'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='PK_refundlineitem_id'),
        Index('IDX_RefundLineItem_order_id', 'order_id'),
        Index('IDX_RefundLineItem_processed_at', 'processed_at')
    )

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    refund_id = Column(BigInteger, nullable=False)
    processed_at = Column(DateTime, nullable=False)
    order_date = Column(DateTime, nullable=False)
    order_id = Column(BigInteger, nullable=False)
    line_item_id = Column(BigInteger, nullable=False)
    variant_id = Column(BigInteger, nullable=False)
    quantity = Column(Integer, nullable=False)
    subtotal = Column(MONEY, nullable=False)
    total_tax = Column(MONEY, nullable=False)


class Refunds(Base):
    """Declarative model class to hold the Refunds table."""
    __tablename__ = 'Refunds'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='PK_refund_id'),
        Index('IDX_Refunds_created_at', 'created_at'),
        Index('IDX_Refunds_order_id', 'order_id')
    )

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    created_at = Column(DateTime, nullable=False)
    processed_at = Column(DateTime, nullable=False)
    order_date = Column(DateTime, nullable=False)
    order_id = Column(BigInteger, nullable=False)
    note = Column(Unicode)


class ShipLines(Base):
    """Declarative model class to hold the ShipLines table."""
    __tablename__ = 'ShipLines'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='PK_ShipLines'),
        Index('IDX_ShipLines', 'order_id', 'processed_at')
    )

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    processed_at = Column(DateTime, nullable=False)
    order_id = Column(BigInteger, nullable=False)
    discounted_price = Column(MONEY, nullable=False)
    price = Column(MONEY, nullable=False)
    carrier_identifier = Column(Unicode(255))
    code = Column(Unicode(255))
    delivery_category = Column(Unicode(255))
    phone = Column(Unicode(255))
    requested_fulfillment_service_id = Column(Unicode(255))
    source = Column(Unicode(255))
    title = Column(Unicode(255))


class Variants(Base):
    """Declarative model class to hold the Variants table."""
    __tablename__ = 'Variants'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='PK_Variants'),
    )

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    product_id = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    title = Column(Unicode(255))
    price = Column(MONEY)
    sku = Column(Unicode(255))
    position = Column(Integer)
    inventory_policy = Column(Unicode(255))
    compare_at_price = Column(MONEY)
    fulfillment_service = Column(Unicode(255))
    inventory_management = Column(Unicode(255))
    option1 = Column(Unicode(255))
    option2 = Column(Unicode(255))
    option3 = Column(Unicode(255))
    barcode = Column(BigInteger)
    grams = Column(Integer)
    image_id = Column(BigInteger)
    weight = Column(Float(53))
    weight_unit = Column(Unicode(50))
    inventory_item_id = Column(BigInteger)
    inventory_quantity = Column(Integer)
    old_inventory_quantity = Column(Integer)
    requires_shipping = Column(Boolean)
    admin_graphql_api_id = Column(Unicode(255))
