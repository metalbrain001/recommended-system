#!/bin/sh
while ! nc -z db 5432; do
  echo "Waiting for Postgres..."
  sleep 1
done
echo "Postgres is ready!"
