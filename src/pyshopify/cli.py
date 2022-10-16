""" Command Line Runner."""
import sys
import click
from pyshopify.runner import ShopifyApp
from pyshopify.sql import DBFactory


@click.command()
@click.option('--all', 'all_', is_flag=True, help='Run all tasks.')
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
def cli_runner(all_, orders, products, customers,
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

    if all_:
        if csv_out:
            app.write_all_to_csv()
            click.echo('CSV Export Complete')
        if sql_out:
            app.write_all_to_sql()
            click.echo("All data written to DB")
    elif customers:
        app.customers_writer(write_csv=csv_out, write_sql=sql_out)
        click.echo('Customers data written')
    elif orders:
        app.orders_writer(write_csv=csv_out, write_sql=sql_out)
        click.echo('Orders data written')
    elif products:
        app.products_inventory_writer(write_csv=csv_out, write_sql=sql_out)
        click.echo('Products data written')


@click.command()
@click.option('--db-tables/--tables-only', default=True,
              help='Specify whether to build  database or tables only')
@click.option('-c', '--connector', type=str, required=True,
              help="Connector + driver ex: mysql+pymysql")
@click.option('-s', '--server', 'server', type=str, required=True,
              help="SQL Server name or IP address")
@click.option('-p', '--port', 'port', type=int,
              help="SQL Server port")
@click.option('-U', '--sa-user', 'sa_user', type=str, required=True,
              help="SQL Server SA user")
@click.option('-W', '--sa-pass', 'sa_pass', type=str, required=True,
              help="SQL Server SA password")
@click.option('-d', '--db-name', 'db_name', type=str, required=True,
              help="DB to create or existing db to use")
@click.option('--schema', 'schema', type=str,
              help="MSSQL schema to create or existing schema to use")
@click.option('--db-user', 'db_user', type=str,
              help="DB user to create")
@click.option('--db-pass', 'db_pass', type=str,
              help="Created DB user password")
@click.option('--query', 'query', type=str,
              help="Connection string Query, use comma separated list with key:value")
@click.option('--date-start', 'date_start', type=str,
              help="Create DateDim table from starting date YYYY-MM-DD")
def build_database(connector, db_tables, server, port, sa_user, sa_pass,
                   db_name, schema, db_user, db_pass, query, date_start):
    """pyshopify database builder.

    Build on existing database with --tables-only
    New user can be created with --db-user and --db-pass
    For MSSQL, --schema will be created if it does not exist

    specifying date_start will build a date dimension table starting at date_start.

    """
    if (not db_user or not db_pass) and (db_user.strip() == '' or db_pass.strip() == ''):
        db_user = None
        db_pass = None
    if connector.split('+')[0] == 'mssql':
        if not query:
            query = None
        db = DBFactory(connector=connector,
                       server=server,
                       port=port,
                       db_name=db_name,
                       sa_user=sa_user,
                       sa_pass=sa_pass,
                       schema=schema,
                       connection_query=query)
    elif connector.split('+')[0] in ['mysql', 'mariadb']:
        db = DBFactory(connector=connector,
                       server=server,
                       port=port,
                       db_name=db_name,
                       sa_user=sa_user,
                       sa_pass=sa_pass)

    if db_tables:
        click.echo('Creating pyshopify database and tables')
        db.create_db()
        click.echo(f'Database {db_name} created')
    else:
        click.echo("Creating pyshopify tables only")
    if db_pass is not None and db_user is not None:
        db.create_user(db_user, db_pass)
        click.echo(f'User {db_user} created')
    db.create_tables()
    click.echo(f'Tables created in {db_name}')
    if date_start:
        db.create_date_dimension(date_start)
        click.echo("Date Dimension created")


if __name__ == "__main__":
    cli_runner()
