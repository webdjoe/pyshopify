"""Create folder with export in CSV files."""
from pathlib import Path
from configparser import SectionProxy


def csv_path(csv_dir: str) -> Path:
    """Build csv Path object & mkdir"""
    pwd = Path.cwd()
    base = pwd.joinpath(csv_dir)
    base.mkdir(exist_ok=True)
    return base


def csv_send(table_dict: dict, csv_config: SectionProxy) -> None:
    write_path = csv_path(csv_config.get('filepath'))
    for keys in table_dict.keys():
        file_path = write_path.joinpath(keys + ".csv")
        df = table_dict[keys]
        if file_path.is_file() is True:
            df.to_csv(file_path, mode='a', header=True,
                      index=False, encoding='utf-8-sig')
        else:
            df.to_csv(file_path, mode='w', header=True,
                      index=False, encoding='utf-8-sig')
    return
