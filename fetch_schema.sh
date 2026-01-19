#!/bin/bash

# Fetch the actual schema from the database
# This will show you the true structure of your tables

echo "=== Fetching position_configs table schema ==="
psql $DATABASE_URL -c "\d position_configs"

echo ""
echo "=== Fetching lp_positions table schema ==="
psql $DATABASE_URL -c "\d lp_positions"

echo ""
echo "=== Fetching user_api_keys table schema ==="
psql $DATABASE_URL -c "\d user_api_keys"
