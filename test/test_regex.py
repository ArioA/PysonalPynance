import pytest

from pynance import parsing


@pytest.mark.parametrize("input, expected_counterparty, expected_metadata", [
    ("VILLAGE  Google ****2050", "VILLAGE", "Google ****2050"),
    ("DIGITALOCEAN.COM  6.00U.S. DOLLA at 1.31578947", "DIGITALOCEAN.COM", "6.00U.S. DOLLA at 1.31578947"),
    ("VILLAGE GROCER LTD  Contactless", "VILLAGE GROCER LTD", "Contactless"),
    ("YUKKA GARDEN", "YUKKA GARDEN", "Card Payment")
])
def test_regex_match(input, expected_counterparty, expected_metadata):
    counterparty, metadata = parsing.split_transaction(input)

    assert counterparty == expected_counterparty
    assert metadata == expected_metadata
