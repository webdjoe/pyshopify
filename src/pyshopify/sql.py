"""Updated SQL Server Database."""
import json
import logging
import sys
import calendar
from typing import Union, Optional
from configparser import SectionProxy
from datetime import date
from datetime import timedelta as td
from dateutil import parser
from pandas import DataFrame

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
try:
    from sqlalchemy import create_engine, MetaData, Table, Column, select
    from sqlalchemy.engine import Engine, URL
    from sqlalchemy.exc import SQLAlchemyError
    from pyshopify.vars import merge_str, MergeDict
    from pyshopify.db_model import DBModel
except ImportError as e:
    logger.debug("Error importing SQLAlchemy: %", e)
    create_engine = None
    MetaData = None
    Engine = None
    Table = None
    merge_str = None  # type: ignore
    MergeDict = None  # type: ignore
    Column = None
    URL = None


class DBFactory:
    """
    Builds database, tables and create user.

    Parameters
    ----------
    server : str,
        SQL Server name or IP address.
    port : str or int,
        SQL Server port.
    db_name : str, required,
        Database name that can be built and is going to hold tables.
    schema : str, optional, default to None (dbo),
        Target schema, will be created if it does not exist.
    sa_user : str, optional, default None,
        SQL Server admin username, optional only with windows_auth.
    sa_pass : str, optional, default None
        SQL Server admin password, optional only with windows_auth.
    windows_auth : bool, optional, default False
        Use Windows Authentication.
    driver : str, optional
        SQL Server driver, defaults to ODBC Driver 17 for SQL Server.

    Attributes
    ----------

    self.master_engine : Engine
        DB Engine created with admin credentials for Master database.
    self.db_engine : Engine
        DB Engine created with admin credentials to the target database.
    self.db_user : str
        Database user created after database is built.
    self.db_pass : str
        Database password created after database is built.
    self.schema : str
        Database target schema, can be created.

    Methods
    -------

    create_db()
        Create database using self.master_engine and self.db_name.

    create_user(db_user: str, db_pass: str)
        Create database user for the target database.

    create_tables(schema: str = None)
        Create schema and tables in target database.

    create_date_table(starting_date: str)
        Create date dimension table and fill rows in target database.

    Examples
    --------
    Instantiate class with SQL admin user & password on non-default port to a new schema.
    >>> db_factory = DBFactory(server='localhost', port=1433,
    ...                        db_name='shop_rest', schema='Shop',
    ...                        sa_user='sa',
    ...                        sa_pass='password',
    ...                        diver='ODBC Driver 17 for SQL Server')

    Instantiate class with windows authentication
    >>> db_factory = DBFactory(server='localhost',
    ...                        port=1433, db_name='shop_rest',
    ...                        windows_auth=True,
    ...                        diver='ODBC Driver 17 for SQL Server')

    """
    def __init__(self, server: str,
                 port: Union[str, int],
                 db_name: str,
                 schema: Optional[str] = None,
                 sa_user: Optional[str] = None,
                 sa_pass: Optional[str] = None,
                 windows_auth: bool = False,
                 driver: Optional[str] = None
                 ) -> None:
        self.server = server
        self.port = port
        self.db_name = db_name
        self.sa_user = sa_user
        self.sa_pass = sa_pass
        self.schema = schema
        self.windows_auth = windows_auth
        if driver is not None:
            self.driver = driver
        else:
            self.driver = 'ODBC Driver 17 for SQL Server'
        self.master_engine = self.get_db_engine()
        self.db_engine: Optional[Engine] = None
        self.db_user: Optional[str] = None
        self.db_pass: Optional[str] = None

    def get_db_engine(self, db: str = 'master') -> Engine:
        """Get engine with admin credentials."""
        db_config = {
            'server': self.server,
            'port': self.port,
            'database': db,
            'driver': self.driver,
        }
        if self.windows_auth is True:
            db_config['windows_auth'] = True
        elif self.sa_user is not None and self.sa_pass is not None:
            db_config['db_user'] = self.sa_user
            db_config['db_pass'] = self.sa_pass
        else:
            raise ValueError("Must provide SQL Server credentials.")
        return get_engine(db_config)

    def get_shop_engine(self) -> None:
        """Get the database tables are being built into."""
        if self.db_engine is None:
            self.db_engine = self.get_db_engine(db=self.db_name)

    def create_db(self) -> None:
        """Create database."""
        with self.master_engine.connect().execution_options(
                isolation_level='AUTOCOMMIT') as conn:
            conn.execute(DBModel.make_db(self.db_name))
            conn.execute(DBModel.alter_db(self.db_name))

    def create_user(self, db_user: str = None, db_pass: str = None) -> bool:
        """Create login and user for database."""
        if db_user is None:
            if self.db_user is None:
                logger.error("Must provide a username.")
                return False
        else:
            self.db_user = db_user
        if db_pass is None:
            if self.db_pass is None:
                logger.error("Must provide a password.")
                return False
        else:
            self.db_pass = db_pass

        with self.master_engine.connect().execution_options(
                isolation_level='AUTOCOMMIT') as conn:
            stmt = conn.execute(
                f"SELECT * FROM [master].[sys].[server_principals]\
                    WHERE [name] = N'{self.db_user}'")
            if stmt.scalar() is not None:
                logger.debug("$ login already exists", self.db_user)
                return False
            conn.execute("CREATE LOGIN % WITH PASSWORD = '%'",
                         self.db_user, self.db_pass)
        if self.db_engine is None:
            self.get_shop_engine()
        if self.db_engine is not None:
            with self.db_engine.connect().execution_options(
                    isolation_level='AUTOCOMMIT') as conn:
                try:
                    stmt = conn.execute(
                        f"SELECT * FROM sys.database_principals \
                                        WHERE name = N'{db_user}'")
                    if stmt.scalar() is not None:
                        logger.debug("% already exists", db_user)
                        return False
                    conn.execute(
                        f"CREATE USER [{db_user}] FOR LOGIN [{db_user}]")
                    conn.execute(
                        f"EXEC sp_addrolemember N'db_owner', N'{db_user}'")
                except SQLAlchemyError as e:
                    logger.error("Cannot create user - %", e)
                    return False
        return True

    def create_tables(self, schema: Optional[str] = None) -> None:
        """Create tables."""
        if self.db_engine is None:
            self.get_shop_engine()
        if schema is not None:
            self.schema = schema
        if self.schema is not None and self.schema != 'dbo' and \
                self.db_engine is not None:
            self.__create_schema(self.schema)
            self.db_engine = self.db_engine.execution_options(
                schema_translate_map={None: schema})
        tbl_class = DBModel()
        tbl_class.model.metadata.create_all(self.db_engine)

    def create_date_dimension(self, date_start: str,
                              schema: Optional[str] = None) -> None:
        """Create date dimension table and build out rows."""
        if schema is not None:
            self.schema = schema
        if self.db_engine is None:
            self.get_shop_engine()
        if self.schema is not None and self.db_engine is not None:
            self.db_engine = self.db_engine.execution_options(
                schema_translate_map={None: self.schema})
        tbl_class = DBModel()
        tbl_class.date_model.metadata.create_all(self.db_engine)
        tbl = tbl_class.date_model.metadata.tables['DateDimension']
        table_rows = date_row_builder(date_start)
        if len(table_rows) == 0:
            logger.error("No date rows to insert.")
            return
        with self.db_engine.connect().execution_options(
                isolation_level='AUTOCOMMIT') as conn:
            conn.execute(tbl.insert(), table_rows)

    def __create_schema(self, schema: str) -> None:
        """Create schema."""
        if self.db_engine is not None:
            with self.db_engine.connect().execution_options(
                    isolation_level='AUTOCOMMIT') as conn:
                stmt = conn.execute(DBModel.check_schema(schema))
                if stmt.scalar() is None:
                    conn.execute(DBModel.make_schema(schema))
                    logger.debug('Created schema %', schema)
                else:
                    logger.debug('Schema % already exists', schema)


def get_engine(sql_conf: Union[SectionProxy, dict]) -> Engine:
    """
    Get engine from config Sections/Dict.

    Arguments
    ----------
    sql_conf: Union[SectionProxy, dict]
        Configuration dictionary or SectionProxy object.

    Returns
    -------
    Engine

    Examples
    --------
    >>> sql_conf = {
    ...     'server': 'localhost',
    ...     'port': 1433,
    ...     'database': 'shop_db',
    ...     'driver': 'ODBC Driver 17 for SQL Server',
    ...     'db_user': 'sa',
    ...     'db_pass': 'password',
    ...     'windows_auth': False
    ... }
    """
    if create_engine is None:
        raise ImportError("Error importing SQL Server dependencies")
    server = sql_conf.get('server')
    database = sql_conf.get('database')
    driver = sql_conf.get('driver')
    user = sql_conf.get('db_user')
    port = sql_conf.get('port', "1433")
    password = sql_conf.get('db_pass')
    if sql_conf.get('windows_auth') is True:
        con_url = URL(
            "mssql+pyodbc",
            host=server,
            port=port,
            database=database,
            query={
                "driver": driver,
                "Trusted_Connection": "yes",
                "TrustedServerCertificate": "yes",
                "encrypt": "no"
            }
        )
    elif user is not None and password is not None:
        con_url = URL(
            "mssql+pyodbc",
            username=user,
            password=password,
            host=server,
            port=port,
            database=database,
            query={
                "driver": driver,
                "TrustedServerCertificate": "yes",
                "encrypt": "no"
            }
        )
    else:
        raise Exception('Error connecting to database,'
                        'check user password and authentication method')
    engine = create_engine(con_url, echo=True)
    return engine


def get_distinct_locations(engine: Engine, schema: str = 'dbo') -> list:
    """Get list of inventory locations from database."""
    model = DBModel()
    tbl = model.model.metadata.tables['InventoryLocations']
    engine = engine.execution_options(schema_translate_map={None: schema})
    location_ids = engine.execute(select(tbl.c.id)).scalars()
    if location_ids is None:
        return []
    return location_ids.all()


def sql_arrange(df: DataFrame, col_list: list) -> list:
    """Arrange dataframe columns to match SQL columns."""
    df = df.reindex(columns=col_list)
    tbl_data = json.loads(df.to_json(
        orient='records', date_format='iso'))
    return tbl_data


def sql_merge(data: dict,
              j: int,
              engine: Engine,
              sql_config: SectionProxy) -> bool:
    """Merge a dictionary of dataframes into an SQL table."""
    log = sys.stdout.write
    schema = sql_config.get('schema', 'dbo')
    db = sql_config.get('database')
    for k, v in data.items():
        if k == 'Orders':
            min_date = v.processed_at.min().strftime('%b %d-%Y')
            log(f"Writing {len(v.index)} orders run {j} from {min_date}\n")
        if v is None:
            log(f"No {k} data to merge")
            continue
        log(f"Writing Table {k} to SQL Server\n")
        merge_dict = MergeDict[k]
        if schema != 'dbo' and schema is not None:
            engine.execution_options(schema_translate_map={None: schema})
        with engine.begin() as conn:
            if schema is not None and schema != 'dbo':
                meta = MetaData(schema=schema)
            else:
                meta = MetaData()
            tbl = Table(k, meta, autoload_with=engine)
            columns = []
            col_names = []
            for column in tbl.c:
                col_names.append(column.name)
                columns.append(Column(column.name, column.type))
            tmp = Table('#tmp', meta, *columns)
            tmp.create(conn)
            tbl_data = sql_arrange(v, col_names)
            conn.execute(tmp.insert(), tbl_data)
            merge_qry = merge_str(db, schema, k,
                                  col_names, **merge_dict)  # type: ignore
            conn.execute(merge_qry)
            conn.execute("DROP TABLE IF EXISTS #tmp")
    return True


def date_row_builder(start_str) -> list:
    """Build rows for DateDimension table."""
    try:
        start_date = parser.isoparse(start_str).date()
    except parser.ParserError:
        logger.debug("Error parsing start date, defaulting to 1/1/2019")
        start_date = date(2019, 1, 1)
    end_date = start_date + td(days=(30*365))
    row_array = []
    current_date = start_date
    while current_date <= end_date:
        TheDate = current_date
        TheDay = current_date.day
        TheDaySuffix = 'tsnrhtdd'[TheDay % 5 * (
            TheDay % 100 ^ 15 > 4 > TheDay % 10)::4]
        TheDayName = TheDate.strftime('%A')
        TheDayOfWeek = int(TheDate.strftime('%w')) + 1
        TheDayOfWeekInMonth = (TheDay - 1) // 7 + 1
        TheDayOfYear = current_date.timetuple().tm_yday
        IsWeekend = 1 if TheDayOfWeek in [1, 7] else 0
        TheWeek = int(TheDate.strftime('%U')) + 1
        TheISOWeek = TheDate.isocalendar().week
        TheFirstOfWeek = TheDate - td(days=TheDate.isoweekday() % 7)
        TheLastOfWeek = TheFirstOfWeek + td(days=6)
        TheWeekOfMonth = get_week_of_month(TheDate)
        TheMonth = int(TheDate.month)
        TheMonthName = TheDate.strftime('%B')
        TheFirstOfMonth = TheDate.replace(day=1)
        TheLastOfMonth = TheDate.replace(day=calendar.monthrange(
            TheDate.year, TheDate.month)[1])
        TheFirstOfNextMonth = TheLastOfMonth + td(days=1)
        TheLastOfNextMonth = TheFirstOfNextMonth.replace(
            day=calendar.monthrange(TheFirstOfNextMonth.year,
                                    TheFirstOfNextMonth.month)[1])
        TheQuarter = (TheMonth - 1) // 3 + 1
        TheFirstOfQuarter = date(TheDate.year, 3 * (
            (TheDate.month - 1) // 3) + 1, 1)
        TheLastOfQuarter = date(
                TheDate.year + 3 * TheQuarter // 12,
                3 * TheQuarter % 12 + 1, 1) \
            + td(days=-1)
        TheYear = TheDate.year
        TheISOYear = TheDate.isocalendar().year
        TheFirstOfYear = TheDate.replace(month=1, day=1)
        TheLastOfYear = TheDate.replace(month=12, day=31)
        IsLeapYear = ((TheYear % 400 == 0) or (TheYear % 100 != 0)
                      and (TheYear % 4 == 0))
        Has53Weeks = (int(TheLastOfYear.strftime('%U')) + 1) == 53
        Has53ISOWeeks = TheLastOfYear.isocalendar().week == 53
        MMYYYY = TheDate.strftime('%m%Y')
        Style101 = TheDate.strftime('%m/%d/%Y')
        Style103 = TheDate.strftime('%d/%m/%Y')
        Style112 = TheDate.strftime('%Y%m%d')
        Style120 = TheDate.strftime('%Y-%m-%d')
        row_array.append(
            {
                'TheDate': TheDate,
                'TheDay': TheDay,
                'TheDaySuffix': TheDaySuffix,
                'TheDayName': TheDayName,
                'TheDayOfWeek': TheDayOfWeek,
                'TheDayOfWeekInMonth': TheDayOfWeekInMonth,
                'TheDayOfYear': TheDayOfYear,
                'IsWeekend': IsWeekend,
                'TheWeek': TheWeek,
                'TheISOWeek': TheISOWeek,
                'TheFirstOfWeek': TheFirstOfWeek,
                'TheLastOfWeek': TheLastOfWeek,
                'TheWeekOfMonth': TheWeekOfMonth,
                'TheMonth': TheMonth,
                'TheMonthName': TheMonthName,
                'TheFirstOfMonth': TheFirstOfMonth,
                'TheLastOfMonth': TheLastOfMonth,
                'TheFirstOfNextMonth': TheFirstOfNextMonth,
                'TheLastOfNextMonth': TheLastOfNextMonth,
                'TheQuarter': TheQuarter,
                'TheFirstOfQuarter': TheFirstOfQuarter,
                'TheLastOfQuarter': TheLastOfQuarter,
                'TheYear': TheYear,
                'TheISOYear': TheISOYear,
                'TheFirstOfYear': TheFirstOfYear,
                'TheLastOfYear': TheLastOfYear,
                'IsLeapYear': IsLeapYear,
                'Has53Weeks': Has53Weeks,
                'Has53ISOWeeks': Has53ISOWeeks,
                'MMYYYY': MMYYYY,
                'Style101': Style101,
                'Style103': Style103,
                'Style112': Style112,
                'Style120': Style120
            }
        )
        current_date = current_date + td(days=1)
    return row_array


def get_week_of_month(cal_date) -> int:
    """Get the week of the month starting sunday."""
    cal = calendar.Calendar(6)
    weeks = cal.monthdayscalendar(cal_date.year, cal_date.month)
    for x in range(len(weeks)):
        if cal_date.day in weeks[x]:
            return x + 1
    return 0
