import os

from os import path
from typing import List

import pandas

from pynance import STATEMENTS_DIR
from pynance.parsing import PARSER_FUNCTIONS
from pynance.transformations import create_transaction_metadata_column, sort_by_key


def statement_file(file_name: str) -> str:
    return path.join(STATEMENTS_DIR, file_name)


def read_all_nationwide_statements() -> List[pandas.DataFrame]:
    statement_files = os.listdir(STATEMENTS_DIR)

    return [read_nationwide_statement(filename) for filename in statement_files]


def get_all_nationwide_statements() -> pandas.DataFrame:
    statements = read_all_nationwide_statements()
    return pandas.concat(statements, ignore_index=True)


def get_all_nationwide_statements_by_date(split_transaction_type=True) -> pandas.DataFrame:
    statements = get_all_nationwide_statements()
    sorted_statements = sort_by_key(statements, "Date")

    if split_transaction_type:
        create_transaction_metadata_column(sorted_statements)

    return sorted_statements


def read_nationwide_statement(
    file_name: str, from_statements_dir: bool = True
) -> pandas.DataFrame:
    """
    Loads the nationwide statement into memory as a DataFrame.

    :param file_name: Name of the file
    :param from_statements_dir: If True, assume file_name is in the statements directory. Else leave the path unchanged.
    """
    kwargs = {
        "header": 3,
        "parse_dates": [0],
        "infer_datetime_format": True,
        "converters": PARSER_FUNCTIONS,
    }

    if from_statements_dir:
        file_name = statement_file(file_name)

    try:
        return pandas.read_csv(file_name, **kwargs)
    except UnicodeDecodeError:
        clean_file(file_name)
        return pandas.read_csv(file_name, **kwargs)


def clean_file(file_name: str):
    """
    Attempts to convert a file in non-utf-8 format into a utf-8 file.

    If successful, re-writes file as utf-8.
    """
    with open(file_name, mode="rb") as the_file:
        contents = the_file.read().decode("latin1")

    with open(file_name, mode="w") as the_file:
        the_file.write(contents)
