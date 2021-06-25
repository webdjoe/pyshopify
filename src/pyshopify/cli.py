""" Command Line Runner."""
import sys
import click
from pyshopify.runner import ShopifyApp


@click.command()
@click.option('-d', '--days', 'days', type=int, default=30, help='get days of history')
@click.option('-b', '--between', 'btw', nargs=2, type=str, help='get between 2 dates - yyyy-MM-dd, ex -b 2020-01-01 2020-01-02')
@click.option('--sql-out/--no-sql', default=False, help='write to database - Default False')
@click.option('--csv-out/--no-csv', default=True, help='Write results to csv files - Default true')
@click.option('--csv-location', default='csv_export', help='Relative location of csv export folder defaults to csv_export/')
@click.option('--config', default='config.ini', help='Relative location of config.ini - defaults to config.ini in currect directory')
def cli_runner(days, btw, sql_out, csv_out, csv_location, config):
    """Run Shopify App CLI."""
    log = sys.stdout.write
    app = ShopifyApp(config)
    shop_conf = app.configuration.shopify
    if not csv_out and not sql_out:
        log('Select CSV or SQL output with --csv or --sql')
        return
    if btw:
        if len(btw) != 2:
            log('Please enter only 2 dates with between option')
            return
        shop_conf['start'] = btw[0]
        shop_conf['end'] = btw[1]

    else:
        shop_conf['days'] = str(days)
        shop_conf['start'] = ''
        shop_conf['end'] = ''

    app.start_date, app.end_date = app.date_config()
    app.sql_enable = sql_out
    app.csv_enable = csv_out
    app.custom_enable = False
    if csv_location:
        app.csv_dir = csv_location
    app.app_runner()


if __name__ == "__main__":
    cli_runner()
