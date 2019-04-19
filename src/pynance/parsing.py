import enum
import re
from typing import Optional, Tuple


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
