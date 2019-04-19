import enum
import os
import re

from os import path
from typing import Optional, Tuple, List

import pandas

from pynance import STATEMENTS_DIR


def parse_price(price_str: Optional[str]) -> float:
    if not price_str:
        price_num = 0.0
    else:
        price_num = float(price_str[1:])

    return price_num


PARSER_FUNCTIONS = {"Paid in": parse_price, "Paid out": parse_price}


class TransactionRegex(enum.Enum):
    GOOGLE_PAY_REGEX = re.compile(r"  Google \*{4}\d{4}")
    CONTACTLESS_REGEX = re.compile(r"  Contactless")
    FX_REGEX = re.compile(r"  \d+[.]\d+.* at \d+[.]\d+")


def match_transaction_metadata(transaction: str) -> Optional[re.Match]:
    match = None

    for regex in TransactionRegex:
        match = regex.value.search(transaction)
        if match is not None:
            return match
    return match


def split_transaction(transaction: str) -> Tuple[str, str]:
    match = match_transaction_metadata(transaction)

    if match is None:
        counterparty = transaction
        payment_type = "Card Payment"
    else:
        counterparty = transaction[: match.start()]
        payment_type = match.group().strip()

    return counterparty, payment_type


def create_transaction_metadata_column(df: pandas.DataFrame):
    new_transactions = []
    payment_types = []

    for transaction in df["Transactions"]:
        new_transaction, payment_type = split_transaction(transaction)
        new_transactions.append(new_transaction)
        payment_types.append(payment_type)

    df["Transactions"] = new_transactions
    df["PaymentType"] = payment_types


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
    sorted_statements = statements.sort_values("Date").reset_index(drop=True)

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
