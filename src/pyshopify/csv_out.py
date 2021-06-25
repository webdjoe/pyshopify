"""Create folder with export in CSV files."""
from pathlib import Path


def csv_path(csv_dir: str) -> Path:
    """Build csv Path object & mkdir"""
    pwd = Path.cwd()
    base = pwd.joinpath(csv_dir)
    base.mkdir(exist_ok=True)
    return base


def csv_writer(table_dict: dict, j: int, csv_dir: str) -> None:
    write_path = csv_path(csv_dir)
    for keys in table_dict.keys():
        file_path = write_path.joinpath(keys + ".csv")
        csv_file = str(file_path)
        df = table_dict[keys]
        if j > 2:
            df.to_csv(csv_file, mode='a', header=True, index=False, encoding='utf-8-sig')
        else:
            df.to_csv(csv_file, mode='w', header=True, index=False, encoding='utf-8-sig')
    return
