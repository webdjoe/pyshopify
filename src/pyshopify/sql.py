"""Updated SQL Server Database."""
import json
import sys
from pandas import DataFrame
from configparser import SectionProxy
try:
    from sqlalchemy import create_engine, MetaData, Table, Column
    from sqlalchemy.engine import Engine
    from sqlalchemy.engine import URL
    from pyshopify.vars import merge_str, MergeDict
except ImportError as e:
    sys.stdout.write(f"Error importing SQLAlchemy: {e}")
    create_engine = None
    MetaData = None
    Engine = None
    Table = None
    merge_str = None  # type: ignore
    MergeDict = None  # type: ignore
    Column = None
    URL = None


def get_engine(sql_conf: SectionProxy) -> Engine:
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
    engine = create_engine(con_url)
    return engine


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
    log = sys.stdout.write
    schema = sql_config.get('schema')
    db = sql_config.get('database')
    for k, v in data.items():
        if k == 'Orders':
            min_date = v.order_date.min().strftime('%b %d-%Y')
            log(f"Writing orders run {j} from {min_date}\n")
        if v is None:
            log(f"No {k} data to merge")
            continue
        log(f"Writing Table {k} to SQL Server\n")
        merge_dict = MergeDict[k]
        with engine.begin() as conn:
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
