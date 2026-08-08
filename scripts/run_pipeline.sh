#!/bin/bash
cd "$(dirname "$0")/.."
source venv/bin/activate
source .env

python main.py >> logs/run.log 2>&1
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ] && [ -n "$HEALTHCHECK_URL" ]; then
    curl -fsS -m 10 --retry 3 "$HEALTHCHECK_URL" >> logs/run.log 2>&1
fi

exit $EXIT_CODE
