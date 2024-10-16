#!/bin/sh

PG_HOST=${PG_HOST:-localhost}
PG_PORT=${PG_PORT:-5432}
MAX_RETRIES=30
RETRIES=0

while ! pg_isready -h $PG_HOST -p $PG_PORT > /dev/null 2>&1; do
  RETRIES=$((RETRIES+1))
  if [ $RETRIES -ge $MAX_RETRIES ]; then
    echo "Postgres is still not ready after $RETRIES seconds, exiting."
    exit 1
  fi
  echo "Waiting for Postgres on $PG_HOST:$PG_PORT... ($RETRIES/$MAX_RETRIES)"
  sleep 1
done

echo "Postgres is ready!"
pg_isready -h $PG_HOST -p $PG_PORT
