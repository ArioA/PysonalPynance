import pandas

from pynance.parsing import split_transaction


def create_transaction_metadata_column(df: pandas.DataFrame):
    new_transactions = []
    payment_types = []

    for transaction in df["Transactions"]:
        new_transaction, payment_type = split_transaction(transaction)
        new_transactions.append(new_transaction)
        payment_types.append(payment_type)

    df["Transactions"] = new_transactions
    df["PaymentType"] = payment_types


def sort_by_key(statements, col):
    return statements.sort_values(col).reset_index(drop=True)
