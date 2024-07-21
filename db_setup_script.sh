#!/bin/bash

# Variables
DB_NAME="rul_db"
DB_USER="rul_user"
DB_PASSWORD="yourpassword"

# Create the database
psql -U postgres -c "CREATE DATABASE $DB_NAME;"

# Create the user and grant privileges
psql -U postgres -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"

# Import the schema
psql -U $DB_USER -d $DB_NAME -f schema.sql

# Import the sample data
psql -U $DB_USER -d $DB_NAME -f sample_data.sql