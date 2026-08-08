import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from transform import transform_coin, transform_all, validate_row

SAMPLE_GOOD = {
    "id": "bitcoin",
    "current_price": 65000.1234,
    "market_cap": 1200000000000,
    "price_change_percentage_24h": 1.23,
}

SAMPLE_NO_MARKET_CAP = {
    "id": "some-small-coin",
    "current_price": 0.05,
    "market_cap": None,
    "price_change_percentage_24h": -2.1,
}

SAMPLE_BAD_PRICE = {
    "id": "broken-coin",
    "current_price": -5,
    "market_cap": None,
    "price_change_percentage_24h": None,
}

SAMPLE_NO_ID = {
    "id": None,
    "current_price": 100,
}


def test_transform_coin_happy_path():
    row = transform_coin(SAMPLE_GOOD)
    assert row["coin_id"] == "bitcoin"
    assert row["market_cap"] == 1200000000000
    assert row["fetched_at"].tzinfo is not None


def test_transform_coin_rounds_price():
    row = transform_coin(SAMPLE_GOOD)
    assert row["price_usd"] == round(65000.1234, 4)


def test_missing_market_cap_is_allowed():
    row = transform_coin(SAMPLE_NO_MARKET_CAP)
    assert row["market_cap"] is None


def test_bad_price_raises():
    with pytest.raises(AssertionError):
        validate_row(SAMPLE_BAD_PRICE)


def test_missing_id_raises():
    with pytest.raises(AssertionError):
        validate_row(SAMPLE_NO_ID)


def test_transform_all_skips_bad_rows():
    raw = [SAMPLE_GOOD, SAMPLE_BAD_PRICE, SAMPLE_NO_ID]
    result = transform_all(raw)
    assert len(result) == 1
    assert result[0]["coin_id"] == "bitcoin"
