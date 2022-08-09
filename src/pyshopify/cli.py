""" Command Line Runner."""
import sys
import click
from pyshopify.runner import ShopifyApp


@click.command()
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
def cli_runner(days, btw, sql_out, csv_out, csv_location, config):
    """Run Shopify App CLI."""
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

    app.data_writer(customers=True, orders=True,
                    write_csv=csv_out, write_sql=sql_out)


if __name__ == "__main__":
    cli_runner()
