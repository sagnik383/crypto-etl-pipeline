CREATE TABLE IF NOT EXISTS crypto_prices (
    id SERIAL PRIMARY KEY,
    coin_id TEXT NOT NULL,
    price_usd NUMERIC NOT NULL,
    market_cap NUMERIC,
    change_24h NUMERIC,
    fetched_at TIMESTAMPTZ NOT NULL
);
