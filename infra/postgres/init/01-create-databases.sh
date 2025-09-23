#!/bin/bash
set -e

# Create auth database if it doesn't exist
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- Create auth database only when missing
    SELECT 'CREATE DATABASE it_auth OWNER ' || quote_ident('${POSTGRES_USER}') || ';'
    WHERE NOT EXISTS (
        SELECT FROM pg_database WHERE datname = 'it_auth'
    ) \gexec

    -- Ensure privileges are granted (safe to re-run)
    GRANT ALL PRIVILEGES ON DATABASE it_auth TO "${POSTGRES_USER}";

    -- Create additional databases for other services if needed
    -- (keeping it_graph as default database from environment)
    
EOSQL

echo "✅ Database initialization completed successfully"
echo "📊 Created databases: it_graph (default), it_auth"
