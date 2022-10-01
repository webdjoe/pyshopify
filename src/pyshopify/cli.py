""" Command Line Runner."""
import sys
import click
from pyshopify.runner import ShopifyApp
from pyshopify.sql import DBFactory

@click.command()
@click.option('--orders', is_flag=True, help='Get orders data')
@click.option('--customers', is_flag=True, help='Get customers data')
@click.option('--products', is_flag=True, help='Get products data')
@click.option('-d', '--days', 'days', type=int, default=7,
              help='get days of history, default 7')
@click.option('-b', '--between', 'btw', nargs=2, type=str,
              help=('get between 2 dates - yyyy-MM-dd,'
                    'ex -b 2020-01-01 2020-01-02'))
@click.option('--sql-out/--no-sql', default=False,
              help='write to database - Default False')
@click.option('--csv-out/--no-csv', default=False,
              help='Write results to csv files - Default true')
@click.option('--csv-location',
              help=('Relative folder of csv export folder'
                    'defaults to csv_export/'))
@click.option('--config',
              help=('Relative location of config.ini - defaults'
                    'to config.ini in currect directory'))
def cli_runner(orders, products, customers,
               days, btw, sql_out, csv_out, csv_location, config):
    """Run Shopify App CLI.

    Use -d or --days to get days of history, default 7
    Use -b or --between to get data between 2 dates - yyyy-MM-dd yyyy-MM-dd,

    --config is the relative or absolute location of config.ini
    """
    log = sys.stdout.write
    if csv_out is False and sql_out is False:
        log('Select CSV or SQL output with --csv or --sql')
        return
    config_dict = {
        'shopify': {},
        'csv': {},
        'sql': {},
    }
    if csv_location:
        config_dict['csv']['filepath'] = csv_location
    if btw:
        if len(btw) != 2:
            log('Please enter only 2 dates with between option')
            return
        config_dict['shopify']['start'] = btw[0]
        config_dict['shopify']['end'] = btw[1]
        config_dict.get('shopify', {}).pop('days', None)
    else:
        config_dict['shopify']['days'] = str(days)
        config_dict.get('shopify', {}).pop('start', None)
        config_dict.get('shopify', {}).pop('end', None)

    if config is not None:
        app = ShopifyApp(config_dir=config)
    else:
        app = ShopifyApp()
    app.update_config(config_dict)

    if csv_location:
        app.configuration.parser.set('csv', 'filepath', csv_location)

    if customers:
        app.customers_writer(write_csv=csv_out, write_sql=sql_out)
    if orders:
        app.orders_writer(write_csv=csv_out, write_sql=sql_out)
    if products:
        app.products__inventory_writer(write_csv=csv_out, write_sql=sql_out)


@click.command()
@click.option('--db-tables/--tables-only', default=True,
              help='Specify whether to build  database or tables only')
@click.option('-s', '--server', 'server', type=str,
              help="SQL Server name or IP address")
@click.option('-p', '--port', 'port', type=int,
              help="SQL Server port")
@click.option('--sa-user', 'sa_user', type=str,
              help="SQL Server SA user")
@click.option('--sa-pass', 'sa_pass', type=str,
              help="SQL Server SA password")
@click.option('--db-name', 'db_name', type=str,
              help="DB to create or existing db")
@click.option('--schema', 'schema', type=str, default='dbo',
              help="Schema to create or existing schema")
@click.option('--db-user', 'db_user', type=str,
              help="DB user to create")
@click.option('--db-pass', 'db_pass', type=str,
              help="Created DB user password")
@click.option('--driver', 'driver', type=str,
              help="SQL Server ODBC driver")
@click.option('--date-start', 'date_start', type=str,
              help="Create DateDim table from starting date YYYY-MM-DD")
def build_database(db_tables, server, port, sa_user, sa_pass,
                   db_name, schema, db_user, db_pass, driver, date_start):
    """pyshopify database builder.

    Build on existing database with --tables-only
    New user can be created with --db-user and --db-pass
    A new schema will be built if the --schema is specified

    date_start will build a date dimension table starting at date_start.

    """
    if not driver:
        driver = 'ODBC Driver 17 for SQL Server'
    db = DBFactory(server=server,
                   port=port,
                   db_name=db_name,
                   sa_user=sa_user,
                   sa_pass=sa_pass,
                   schema=schema,
                   driver=driver)
    click.echo(str(db_tables))
    click.echo(f"Creating database {db_name} on {server}")
    click.echo(f"sa user: {sa_user}")
    click.echo(f"sa pass: {sa_pass}")
    click.echo(f"db user: {db_user}")
    if db_tables:
        db.create_db()
    if db_user and db_pass:
        db.create_user(db_user, db_pass)
    db.create_tables()
    if date_start:
        db.create_date_dimension(date_start)


if __name__ == "__main__":
    cli_runner()
