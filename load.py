import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

INSERT_SQL = """
    INSERT INTO crypto_prices (coin_id, price_usd, market_cap, change_24h, fetched_at)
    VALUES (%s, %s, %s, %s, %s)
"""


def load_rows(rows):
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    try:
        with conn.cursor() as cur:
            for row in rows:
                cur.execute(INSERT_SQL, (
                    row["coin_id"],
                    row["price_usd"],
                    row["market_cap"],
                    row["change_24h"],
                    row["fetched_at"],
                ))
        conn.commit()
    finally:
        conn.close()
    return len(rows)


if __name__ == "__main__":
    from extract import fetch_prices
    from transform import transform_all

    raw = fetch_prices()
    clean = transform_all(raw)
    count = load_rows(clean)
    print(f"Loaded {count} rows into crypto_prices")
