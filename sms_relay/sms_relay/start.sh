#!/bin/bash


MAX_RETRIES=5
RETRIES=0
# This shows heads, which is just a haack
# to wait for PostgreSQL to be available
until poetry run alembic heads; do
   RETRIES=`expr $RETRIES + 1`
   if [[ "$RETRIES" -eq "$MAX_RETRIES" ]]; then
       echo "Retry Limit Exceeded. Aborting..."
       exit 1
   fi
   sleep 2
done

echo "PostgreSQL is up - running migrations..."

# Apply migrations to the database
poetry run alembic upgrade head

# Finally, start the FastAPI server with hot-reloading enabled
echo "Starting FastAPI server..."
poetry run uvicorn sms_relay.main:app --host 0.0.0.0 --port 8000 --reload
