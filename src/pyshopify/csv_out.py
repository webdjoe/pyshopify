"""Create folder with export in CSV files."""
from pathlib import Path
from typing import Optional
from configparser import SectionProxy


def csv_path(csv_dir: str) -> Path:
    """Build csv Path object & mkdir"""
    pwd = Path.cwd()
    base = pwd.joinpath(csv_dir)
    base.mkdir(exist_ok=True)
    return base


def csv_send(table_dict: dict, csv_config: SectionProxy,
             file_operation: Optional[str] = None) -> None:
    """Write CSV with data from table_dict

    Arguments
    ----------
    table_dict: Dict[str, pd.DataFrame]
        Dictionary of table names and dataframes
    csv_config: configparser.SectionProxy
        csv configuration section
    file_operation: Optional[str], defaults to None
        If None, write or append based on file existence,
        other options are 'a' for append, 'w' for overwrite

    """
    write_path = csv_path(csv_config.get('filepath'))
    for keys in table_dict.keys():
        file_path = write_path.joinpath(keys + ".csv")
        df = table_dict[keys]
        if file_operation is None:
            if file_path.is_file() is True:
                df.to_csv(file_path, mode='a', header=True,
                          index=False, encoding='utf-8-sig')
            else:
                df.to_csv(file_path, mode='w', header=True,
                          index=False, encoding='utf-8-sig')
        elif file_operation in ['a', 'w']:
            df.to_csv(file_path, mode=file_operation, header=True,
                      index=False, encoding='utf-8-sig')
