import time
import requests

COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets"
COINS = ["bitcoin", "ethereum", "solana", "cardano", "dogecoin"]


def fetch_prices(retries=3, backoff=2):
    params = {
        "vs_currency": "usd",
        "ids": ",".join(COINS),
        "order": "market_cap_desc",
        "price_change_percentage": "24h",
    }
    for attempt in range(retries):
        try:
            response = requests.get(COINGECKO_URL, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == retries - 1:
                raise
            time.sleep(backoff ** attempt)


if __name__ == "__main__":
    data = fetch_prices()
    print(f"Fetched {len(data)} coins")
    for coin in data:
        print(coin["id"], coin["current_price"])
