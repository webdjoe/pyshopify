"""Updated SQL Server Database."""
import json
import re
import logging
import calendar
from typing import Union, Optional
from configparser import SectionProxy
from datetime import date
from datetime import timedelta as td
from dateutil import parser
from pandas import DataFrame

logger = logging.getLogger('pyshopify')
logger.setLevel(logging.DEBUG)
try:
    from sqlalchemy import create_engine, MetaData, Table, Column, schema, text
    from sqlalchemy.dialects.mysql import insert
    import sqlalchemy as sa
    from sqlalchemy.engine import Engine, URL
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

SUPPORTED_DIALECTS = ['mysql', 'mssql', 'mariadb']
MYSQL_SYNONYMS = ['mysql', 'mariadb']


class DBFactory:
    """
    Builds database, tables and create user.

    Parameters
    ----------
    connector: str,
        Connection string prefix for database, e.g. 'mssql+pyodbc' or 'mysql+pymysql'
    server : str,
        SQL Server name or IP address.
    port : str or int, optional
        SQL or MySQL Server port, uses default ports if not specified.
    db_name : str, required,
        Database name that can be built and is going to hold tables.
    sa_user : str, optional, default None,
        SQL Server admin username, optional only with windows_auth.
    sa_pass : str, optional, default None
        SQL Server admin password, optional only with windows_auth.
    windows_auth : bool, optional, default False
        Use Windows Authentication for MSSQL.
    schema : str, optional, default to None (dbo for MSSQL),
        Target schema (based on MSSQL construct), will be created if it does not exist.
    connection_query : dict, optional
        Connection string query parameters, if using SQL server the script will
        automatically find the available ODBC driver on the system.

    Attributes
    ----------

    self.master_engine : Engine
        DB Engine created with admin credentials for Master database.
    self.db_name : str
        Name of Database to optionally create and create tables.
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
    The connection query is optional for SQL Server and MySQL, the ODBC driver will
    automatically be found on the system.
    >>> db_factory = DBFactory(connector='mssql+pyodbc', server='localhost', port=1433,
    ...                  db_name='shop_rest', schema='Shop',
    ...                  sa_user='sa',
    ...                  sa_pass='password',
    ...                  connection_query={'driver': 'ODBC Driver 17 for SQL Server})

    Instantiate class with MySQL or MariaDB, pymysql or mysqldb can be used
    >>> db_factory = DBFactory(connector='mssql+pymysql', server='localhost', port=3306,
    ...                  db_name='shop_rest',
    ...                  sa_user='sa',
    ...                  sa_pass='password')

    Instantiate class with windows authentication
    >>> db_factory = DBFactory(connector='mssql+pyodbc', server='localhost',
    ...                  port=1433, db_name='shop_rest',
    ...                  windows_auth=True,
    ...                  connection_query={'driver': 'ODBC Driver 17 for SQL Server'})

    """
    def __init__(self, connector: str,
                 server: str,
                 db_name: str,
                 port: Union[str, int] = None,
                 sa_user: Optional[str] = None,
                 sa_pass: Optional[str] = None,
                 windows_auth: bool = False,
                 schema: Optional[str] = None,
                 connection_query: Union[str, dict, None] = None
                 ) -> None:
        self.connector = connector
        self.dialect = connector.split('+')[0]
        self.server = server
        self.port = port
        self.db_name = db_name
        self.sa_user = sa_user
        self.sa_pass = sa_pass
        self.schema = schema
        self.windows_auth = windows_auth
        self.connection_query = connection_query

        self.master_engine: Engine = self.get_db_engine()
        self.db_engine: Optional[Engine] = None
        self.db_user: Optional[str] = None
        self.db_pass: Optional[str] = None

    def get_db_engine(self, db: Optional[str] = None) -> Engine:
        """Get engine with admin credentials."""
        if db is None:
            if self.dialect == 'mssql':
                db = 'master'
            else:
                db = 'mysql'
        db_config = {
            'connector': self.connector,
            'server': self.server,
            'port': self.port,
            'database': db,
            'connection_query': self.connection_query,
        }
        if self.windows_auth is True:
            db_config['windows_auth'] = True
        elif self.sa_user is not None and self.sa_pass is not None:
            db_config['db_user'] = self.sa_user
            db_config['db_pass'] = self.sa_pass
        else:
            raise ValueError("Must provide SQL Server credentials.")
        return get_engine(db_config)

    def create_db(self) -> None:
        """Create database."""
        check_db = DBModel.check_db(self.db_name, self.dialect)
        make_db = DBModel.make_db(self.db_name, self.dialect)

        with self.master_engine.connect().execution_options(
                isolation_level='AUTOCOMMIT') as conn:
            if check_db is not None:
                stmt = conn.execute(text(check_db))
                if stmt.scalar() is not None:
                    logger.debug("Database %s already exists.", self.db_name)
                    return
            conn.execute(text(make_db))
        logger.debug("Database %s created.", self.db_name)

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

        if self.dialect == 'mssql':
            self._create_login()
        self.db_engine = self.get_db_engine(self.db_name)
        qry_str = DBModel.create_user(self.dialect, self.db_user,
                                      self.db_pass, self.db_name)
        with self.master_engine.connect().execution_options(
                isolation_level='AUTOCOMMIT') as conn:
            if self.dialect == 'mssql':
                stmt = conn.execute(text(qry_str['check_user']))
                if stmt.scalar() is not None:
                    logger.debug("%s already exists", db_user)
                    return False
                conn.execute(text(f'USE {self.db_name}'))
            conn.execute(text(qry_str['create_user']))
            conn.execute(text(qry_str['auth_user']))
        logger.debug("User %s created.", self.db_user)
        return True

    def _create_login(self) -> None:
        """Internal create login function"""
        if self.db_user is not None and self.db_pass is not None:
            check_login = DBModel.check_sql_login(self.db_user)
            make_login = DBModel.create_sql_login(self.db_user, self.db_pass)
        else:
            return
        with self.master_engine.connect().execution_options(
                isolation_level='AUTOCOMMIT') as conn:
            stmt = conn.execute(text(check_login))
            if stmt.scalar() is not None:
                logger.debug("%s login already exists", self.db_user)
                return
            conn.execute(text(make_login))

    def create_tables(self, schema: Optional[str] = None) -> None:
        """Create tables, schema is MSSQL based construct."""
        if self.db_engine is None:
            self.db_engine = self.get_db_engine(self.db_name)
        if self.dialect == 'mssql':
            if schema is not None:
                self.schema = schema
            if self.schema is None:
                self.schema = 'dbo'
            if self.schema != 'dbo' and self.schema is not None:
                self.__create_schema(self.schema)
            self.db_engine = self.db_engine.execution_options(
                schema_translate_map={None: self.schema})
        tbl_class = DBModel()
        tbl_class.model.metadata.create_all(self.db_engine)
        logger.debug("Tables created on %s.", self.db_name)

    def create_date_dimension(self, date_start: str,
                              schema: Optional[str] = None) -> None:
        """Create date dimension table and build out rows."""
        if self.db_engine is None:
            self.db_engine = self.get_db_engine(self.db_name)
        if self.dialect == 'mssql':
            if schema is not None:
                self.schema = schema
            if self.schema is not None and self.db_engine is not None:
                self.db_engine = self.db_engine.execution_options(
                    schema_translate_map={None: self.schema})
        tbl_class = DBModel()
        tbl_class.date_model.metadata.create_all(self.db_engine)
        tbl = tbl_class.date_model.metadata.tables['date_dimension']
        table_rows = date_row_builder(date_start)
        if len(table_rows) == 0:
            logger.error("No date rows to insert.")
            return
        with self.db_engine.connect().execution_options(
                isolation_level='AUTOCOMMIT') as conn:
            conn.execute(tbl.insert(), table_rows)
        logger.debug("Date dimension table created.")

    def __create_schema(self, schema_name: str) -> None:
        """Create schema."""
        if self.dialect != 'mssql':
            return
        if self.db_engine is None:
            self.db_engine = self.get_db_engine(self.db_name)
        with self.db_engine.connect().execution_options(
                isolation_level='AUTOCOMMIT') as conn:
            if schema_name not in sa.inspect(conn).get_schema_names():
                conn.execute(text(schema.CreateSchema(schema_name)))
        logger.debug("Schema %s created.", schema_name)


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
    ...     'connector': 'mssql+pyodbc',
    ...     'server': 'localhost',
    ...     'port': 1433,
    ...     'database': 'shop_db',
    ...     'driver': 'ODBC Driver 17 for SQL Server',
    ...     'db_user': 'sa',
    ...     'db_pass': 'password',
    ...     'windows_auth': False,
    ...     'connection_query': {'driver': 'ODBC Driver 17 for SQL Server'},
    ... }
    Connection_query is optional for MSSQL, the ODBC driver on the system will be used
    """
    if create_engine is None:
        raise ImportError("Error importing SQL Server dependencies")
    connector = sql_conf['connector']
    dialect = connector.split('+')[0]
    if dialect not in SUPPORTED_DIALECTS:
        raise Exception(f"{dialect} is not a supported dialect.")

    if isinstance(sql_conf, SectionProxy):
        windows_auth = sql_conf.getboolean('windows_auth', False)
        port = sql_conf.getint('port', None)
    elif isinstance(sql_conf, dict):
        windows_auth = sql_conf.get('windows_auth', False)
        port = sql_conf.get('port', None)

    raw_query = sql_conf.get('connection_query')
    if raw_query is not None and isinstance(raw_query, str):
        split_qry = raw_query.replace('\n', '').split(',')
        qry_dict = {x.split(':')[0].strip(): x.split(':')[1].strip() for x in split_qry}
    elif raw_query is not None and isinstance(raw_query, dict):
        qry_dict = raw_query
    else:
        qry_dict = {}

    conn_dict = {
        'connector': connector,
        'server': sql_conf['server'],
        'port': port,
        'database': sql_conf['database'],
        'user': sql_conf.get('db_user'),
        'password': sql_conf.get('db_pass'),
        'windows_auth': windows_auth,
        'query': qry_dict
    }
    if dialect == 'mssql':
        con_url = mssql_connection_string(conn_dict)
    elif dialect in MYSQL_SYNONYMS:
        con_url = mysql_connection_string(conn_dict)

    engine = create_engine(con_url, echo=True)
    return engine


def mysql_connection_string(sql_conf: dict) -> URL:
    """Generate Connection URL for MySQL & MariaDB."""
    if sql_conf.get('user') is None or sql_conf.get('password') is None:
        raise Exception("MySQL/MariaDB requires user and password.")
    return URL(
        drivername=sql_conf['connector'],
        host=sql_conf['server'],
        port=sql_conf['port'],
        database=sql_conf['database'],
        username=sql_conf['user'],
        password=sql_conf['password'],
        query=sql_conf['query']
    )


def mssql_connection_string(sql_conf: dict) -> URL:
    """Generate Connection URL for MS SQL SERVER"""
    if sql_conf.get('windows_auth') is False and \
        sql_conf.get('user') is None and \
            sql_conf.get('password') is None:
        raise Exception("user and password required if not using Windows Authentication")

    qry = sql_conf.get('query', {})
    driver = qry.get('driver')
    if driver is None:
        try:
            import pyodbc
            drivers = pyodbc.drivers()
            version = 0
            for odbc in drivers:
                matches = re.match(r"ODBC Driver (\d{2}) for SQL Server",
                                   odbc, re.IGNORECASE)
                if matches:
                    cur_version = int(matches.group(1))
                    if cur_version > version:
                        driver = odbc
                        qry['driver'] = driver
                    version = cur_version
        except ImportError:
            raise ImportError("Cannot use sql server without pyodbc")

    if qry.get('driver') is None:
        raise Exception("Cannot find ODBC Driver for SQL Server")
    matches = re.match(r"ODBC Driver (\d{2}) for SQL Server",
                       qry['driver'], re.IGNORECASE)
    if matches is not None:
        version = int(matches.group(1))
    else:
        version = 0
    if version == 18:
        qry['TrustedServerCertificate'] = qry.get('TrustedServerCertificate', 'yes')
        qry['encrypt'] = qry.get('encrypt', 'no')

    if sql_conf.get('port') is None:
        sql_conf['port'] = 1433

    if sql_conf.get('windows_auth') is True:
        qry['Trusted_Connection'] = 'yes'
        con_url = URL(
            sql_conf['connector'],
            host=sql_conf['server'],
            port=sql_conf['port'],
            database=sql_conf['database'],
            query=qry
        )
    else:
        con_url = URL(
            sql_conf['connector'],
            username=sql_conf['user'],
            password=sql_conf['password'],
            host=sql_conf['server'],
            port=sql_conf['port'],
            database=sql_conf['database'],
            query=qry
        )

    return con_url


class DBWriter:
    """Instance to store DB metadata and engine."""
    def __init__(self, sql_config: SectionProxy) -> None:
        self.engine: Engine = get_engine(sql_config)
        self.connector = sql_config['connector']
        self.dialect = self.connector.split('+')[0]
        self.sql_config = sql_config
        self.schema: str = sql_config.get('schema', 'dbo')
        if self.dialect == 'mssql':
            self.meta: MetaData = MetaData(schema=self.schema)
        elif self.dialect in MYSQL_SYNONYMS:
            self.meta = MetaData()
        self.tmp_meta: MetaData = MetaData()
        self.db: str = sql_config['database']

    @staticmethod
    def sql_arrange(df: DataFrame, col_list: list) -> list:
        """Arrange dataframe columns to match SQL columns."""
        df = df.reindex(columns=col_list)
        tbl_data = json.loads(df.to_json(
            orient='records', date_format='iso'))
        return tbl_data

    def sql_merge(self, data: dict, j: int = 0) -> bool:
        """Merge a dictionary of dataframes into an SQL table."""
        for k, v in data.items():
            if k == 'orders':
                min_date = v.processed_at.min().strftime('%b %d-%Y')
                logger.info("Writing %s orders run %i from %s\n",
                            len(v.index), j, min_date)
            if v is None:
                logger.warning("No %s data to merge", k)
                continue
            logger.info("Writing Table %s to SQL Server\n", k)
            merge_dict = MergeDict[k]
            if self.dialect == 'mssql':
                self.engine.execution_options(
                    schema_translate_map={None: self.schema})
            with self.engine.begin() as conn:
                tbl: Table = Table(k, self.meta, autoload_with=self.engine)
                tbl_data = self.sql_arrange(v, tbl.c.keys())
                if self.dialect == 'mssql':
                    tmp = self.temp_table(tbl.c)
                    tmp.create(conn)
                    conn.execute(tmp.insert(), tbl_data)
                    merge_qry = merge_str(self.db, self.schema, k,
                                          tmp.c.keys(), **merge_dict)  # type: ignore
                    conn.execute(text(merge_qry))
                    tmp.drop(conn)
                    self.tmp_meta.remove(tmp)
                elif self.dialect in MYSQL_SYNONYMS:
                    insert_qry = insert(tbl).values(tbl_data)
                    merge_qry = insert_qry.on_duplicate_key_update(insert_qry.inserted)
                    conn.execute(merge_qry)
        return True

    def temp_table(self, cols: sa.sql.expression.ColumnCollection) -> Table:
        """Create temporary table based on dialect"""
        new_cols = [Column(col.name, col.type) for col in cols]
        if self.dialect == 'mssql':
            tbl_name = "#tmp"
            return Table(tbl_name, self.tmp_meta, *new_cols)
        elif self.dialect in MYSQL_SYNONYMS:
            tbl_name = "tmp"
            return Table(tbl_name, self.tmp_meta, *new_cols, prefixes=['TEMPORARY'])


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
