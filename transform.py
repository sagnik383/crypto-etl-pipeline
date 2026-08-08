from datetime import datetime, timezone


def validate_row(row):
    """Raise if a coin's data doesn't look trustworthy."""
    assert row.get("id"), "missing coin id"
    price = row.get("current_price")
    assert isinstance(price, (int, float)) and price > 0, f"bad price for {row.get('id')}: {price}"
    return row


def transform_coin(row):
    """Turn one raw CoinGecko row into a clean dict ready for the DB."""
    validate_row(row)
    return {
        "coin_id": row["id"],
        "price_usd": round(float(row["current_price"]), 4),
        "market_cap": row.get("market_cap"),  # can be None, that's fine
        "change_24h": row.get("price_change_percentage_24h"),
        "fetched_at": datetime.now(timezone.utc),
    }


def transform_all(raw_data):
    """Transform every coin; skip and log any that fail validation instead of crashing the batch."""
    clean_rows = []
    for row in raw_data:
        try:
            clean_rows.append(transform_coin(row))
        except AssertionError as e:
            print(f"Skipping bad row: {e}")
    return clean_rows


if __name__ == "__main__":
    from extract import fetch_prices
    raw = fetch_prices()
    clean = transform_all(raw)
    print(f"Transformed {len(clean)} of {len(raw)} coins")
    for row in clean:
        print(row)
