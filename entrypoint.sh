#!/bin/sh

echo "⏳ Waiting for database at $DB_HOST:$DB_PORT..."
/wait-for-it.sh "$DB_HOST:$DB_PORT" --timeout=30 --strict -- echo "✅ DB is up"

echo "📦 Running Alembic migrations..."
alembic upgrade head

echo "🚀 Starting FastAPI app..."
exec python main.py