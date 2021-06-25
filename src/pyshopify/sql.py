"""Updated SQL Server Database."""
from typing import Tuple, Any
import sys
try:
    from sqlalchemy import create_engine
    from sqlalchemy.engine import URL, Connection as con
    from pyshopify.vars import proc_dict, DBSpec as sqalch_dict
except ImportError:
    create_engine = None
    URL = None
    con = None


def sql_connect(sql_conf) -> Tuple[Any, Any]:
    if create_engine is None or URL is None or con is None:
        return None, None
    connectionstring = "DRIVER={" + sql_conf.get('driver') \
                       + "};SERVER=" + sql_conf.get('server') \
                       + ";DATABASE=" + sql_conf.get('database') \
                       + ";Uid=" + sql_conf.get('db_user') \
                       + ";Pwd=" + sql_conf.get('db_pass')
    conlink = URL.create("mssql+pyodbc", query={"odbc_connect": connectionstring})
    eng = create_engine(conlink, isolation_level='AUTOCOMMIT')
    connection = eng.raw_connection()
    return connection, eng


def sql_send(table_dict: dict, j: int, connection: con, engine) -> bool:
    log = sys.stdout.write

    tmptbl = 'tmp_tbl'
    cursor = connection.cursor()
    cursor.fast_executemany = True
    ords = table_dict.get('Orders')
    if ords is not None:
        ord_date = ords.iloc[0].order_date.strftime('%b-%d-%Y')
        log(f"Run {j - 1} - First order date - {ord_date}")
        log('\n')
    for k, v in table_dict.items():

        if k != 'Customers':
            ilabel = v['id']
        else:
            ilabel = v['order_id']
        ddict = sqalch_dict()
        dtype_name = ddict[k]
        v.to_sql(tmptbl, con=engine, if_exists='replace', index=False, index_label=ilabel, dtype=dtype_name)
        cursor.execute(proc_dict[k])
        log(f"Run {j - 1} - {len(v.index)} {k} written")
        log('\n')
    cursor.close()
    return True
