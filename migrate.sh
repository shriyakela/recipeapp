#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Setting the FLASK_APP environment variable
export FLASK_APP=main.py

# Check if migrations directory already exists
if [ ! -d "migrations" ]; then
    # Initializing the database migration environment only if the directory does not exist
    flask db init
fi

# Generating a migration script
flask db migrate -m "Added new columns"

# Applying the migrations
flask db upgrade
