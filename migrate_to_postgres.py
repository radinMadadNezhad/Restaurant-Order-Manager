#!/usr/bin/env python
"""
This script migrates data from SQLite to PostgreSQL for the restaurant management system.
It uses Django's dumpdata and loaddata commands to export and import the data.
"""

import os
import subprocess
import sys
from dotenv import load_dotenv

def setup_postgres_environment():
    """Set up environment variables for PostgreSQL connection from .env file or defaults"""
    # Try to load from .env file first
    if os.path.exists('.env'):
        load_dotenv('.env')
        print("Loaded environment variables from .env file")
    else:
        print("No .env file found, using default values")
    
    # Set default values if not already in environment
    if 'USE_POSTGRES' not in os.environ:
        os.environ['USE_POSTGRES'] = 'True'
    
    # Check if database config is already set via DATABASE_URL
    if 'DATABASE_URL' not in os.environ:
        # Set individual PostgreSQL connection values if not using DATABASE_URL
        if 'POSTGRES_DB' not in os.environ:
            os.environ['POSTGRES_DB'] = 'restaurant_db'
        if 'POSTGRES_USER' not in os.environ:
            os.environ['POSTGRES_USER'] = 'postgres'
        if 'POSTGRES_PASSWORD' not in os.environ:
            os.environ['POSTGRES_PASSWORD'] = 'postgres'
        if 'POSTGRES_HOST' not in os.environ:
            os.environ['POSTGRES_HOST'] = 'localhost'
        if 'POSTGRES_PORT' not in os.environ:
            os.environ['POSTGRES_PORT'] = '5432'
    
    # Print the configuration
    if 'DATABASE_URL' in os.environ:
        # Mask password in the output for security
        db_url = os.environ['DATABASE_URL']
        masked_url = db_url.replace(db_url.split(':')[2].split('@')[0], '****')
        print(f"Using DATABASE_URL: {masked_url}")
    else:
        print(f"Using PostgreSQL configuration:")
        print(f"  Database: {os.environ['POSTGRES_DB']}")
        print(f"  User: {os.environ['POSTGRES_USER']}")
        print(f"  Host: {os.environ['POSTGRES_HOST']}:{os.environ['POSTGRES_PORT']}")

def run_command(command):
    """Run a shell command and display output"""
    print(f"Running: {' '.join(command)}")
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    if process.returncode != 0:
        print(f"Error: {process.stderr}")
        return False
    
    print(f"Success: {process.stdout}")
    return True

def main():
    """Main migration function"""
    # Ensure the script is run from the project root
    if not os.path.exists('manage.py'):
        print("Error: This script must be run from the Django project root directory")
        sys.exit(1)
    
    # Step 1: Dump data from SQLite
    print("\n=== Step 1: Dumping data from SQLite ===")
    if not run_command(['python', 'manage.py', 'dumpdata', '--exclude', 'contenttypes', '--exclude', 'auth.permission', '--output', 'data_dump.json']):
        sys.exit(1)
    
    # Step 2: Set up PostgreSQL environment
    print("\n=== Step 2: Setting up PostgreSQL environment ===")
    setup_postgres_environment()
    
    # Step 3: Create PostgreSQL database and tables
    print("\n=== Step 3: Creating PostgreSQL tables ===")
    if not run_command(['python', 'manage.py', 'migrate']):
        sys.exit(1)
    
    # Step 4: Load data into PostgreSQL
    print("\n=== Step 4: Loading data into PostgreSQL ===")
    if not run_command(['python', 'manage.py', 'loaddata', 'data_dump.json']):
        sys.exit(1)
    
    print("\n=== Migration completed successfully! ===")
    print("Your data has been migrated from SQLite to PostgreSQL.")
    print("Make sure to set USE_POSTGRES=True in your environment to use PostgreSQL.")

if __name__ == "__main__":
    main() 