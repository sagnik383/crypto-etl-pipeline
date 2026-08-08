import sys
from datetime import datetime, timezone

from extract import fetch_prices
from transform import transform_all
from load import load_rows


def run():
    start = datetime.now(timezone.utc)
    print(f"[{start.isoformat()}] Pipeline run started")

    try:
        print("Stage: extract")
        raw = fetch_prices()
        print(f"  fetched {len(raw)} coins")

        print("Stage: transform")
        clean = transform_all(raw)
        print(f"  transformed {len(clean)} of {len(raw)} coins")

        print("Stage: load")
        count = load_rows(clean)
        print(f"  loaded {count} rows")

        end = datetime.now(timezone.utc)
        duration = (end - start).total_seconds()
        print(f"[{end.isoformat()}] Pipeline run succeeded in {duration:.2f}s")
        return 0

    except Exception as e:
        print(f"Pipeline run FAILED: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(run())
