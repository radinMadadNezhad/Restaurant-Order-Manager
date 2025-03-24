# PostgreSQL Setup for Restaurant Management System

This guide will help you set up PostgreSQL for your project and migrate your data from SQLite.

## Prerequisites

1. Install PostgreSQL from the [official website](https://www.postgresql.org/download/)
2. Install required Python packages:
   ```
   pip install psycopg2-binary dj-database-url
   ```

## PostgreSQL Setup

### 1. Create a Database

After installing PostgreSQL:

```bash
# Connect to PostgreSQL
psql -U postgres

# Create a database for the project
CREATE DATABASE restaurant_db;

# Create a user (optional, you can use the default postgres user)
CREATE USER restaurant_user WITH PASSWORD 'your_password';

# Grant privileges to the user
GRANT ALL PRIVILEGES ON DATABASE restaurant_db TO restaurant_user;

# Exit PostgreSQL
\q
```

### 2. Configure Environment Variables

Set the following environment variables to connect to your PostgreSQL database:

```bash
# Windows CMD
set USE_POSTGRES=True
set POSTGRES_DB=restaurant_db
set POSTGRES_USER=postgres  # or your custom user
set POSTGRES_PASSWORD=your_password
set POSTGRES_HOST=localhost
set POSTGRES_PORT=5432

# Windows PowerShell
$env:USE_POSTGRES = "True"
$env:POSTGRES_DB = "restaurant_db"
$env:POSTGRES_USER = "postgres"  # or your custom user
$env:POSTGRES_PASSWORD = "your_password"
$env:POSTGRES_HOST = "localhost"
$env:POSTGRES_PORT = "5432"

# Linux/Mac
export USE_POSTGRES=True
export POSTGRES_DB=restaurant_db
export POSTGRES_USER=postgres  # or your custom user
export POSTGRES_PASSWORD=your_password
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
```

Alternatively, you can set a single `DATABASE_URL` environment variable:

```bash
# Windows CMD
set DATABASE_URL=postgres://postgres:your_password@localhost:5432/restaurant_db

# Windows PowerShell
$env:DATABASE_URL = "postgres://postgres:your_password@localhost:5432/restaurant_db"

# Linux/Mac
export DATABASE_URL=postgres://postgres:your_password@localhost:5432/restaurant_db
```

## Data Migration

### Option 1: Using the Migration Script

Run the migration script to automatically transfer your data from SQLite to PostgreSQL:

```bash
python migrate_to_postgres.py
```

### Option 2: Manual Migration

1. Dump data from SQLite:
   ```bash
   python manage.py dumpdata --exclude contenttypes --exclude auth.permission --output data_dump.json
   ```

2. Set environment variables for PostgreSQL (see above)

3. Create tables in PostgreSQL:
   ```bash
   python manage.py migrate
   ```

4. Load data into PostgreSQL:
   ```bash
   python manage.py loaddata data_dump.json
   ```

## Verifying the Migration

To verify that the migration was successful:

1. Set the PostgreSQL environment variables
2. Run the development server:
   ```bash
   python manage.py runserver
   ```
3. Log in to your application and check that all data is present

## Production Deployment

For production deployment, use the `DATABASE_URL` environment variable with your production database credentials. This approach allows flexible deployment to various hosting platforms including:

- Heroku
- Railway
- Render
- AWS
- DigitalOcean
- Azure

Example production settings:

```bash
DATABASE_URL=postgresql://postgres:xkUxjYqDUndsizDgfSdxYdzROVcW@postgres.railway.internal:5432/railway
```

## Troubleshooting

- **Permission issues**: Make sure your PostgreSQL user has the necessary permissions
- **Connection issues**: Verify your PostgreSQL host and port settings
- **Migration errors**: Check that your PostgreSQL version is compatible with Django 