#!/usr/bin/env python
"""
This script runs the Django development server with PostgreSQL as the database.
It sets the necessary environment variables and starts the server.
"""

import os
import subprocess
import sys
from dotenv import load_dotenv

def setup_postgres_environment():
    """Set up environment variables for PostgreSQL connection"""
    # Try to load from .env file first
    if os.path.exists('.env'):
        load_dotenv('.env')
        print("Loaded environment variables from .env file")
    else:
        # Create a temporary .env file with default values
        with open('.env.temp', 'w') as f:
            f.write("USE_POSTGRES=True\n")
            f.write("POSTGRES_DB=restaurant_db\n")
            f.write("POSTGRES_USER=postgres\n")
            f.write("POSTGRES_PASSWORD=postgres\n")
            f.write("POSTGRES_HOST=localhost\n")
            f.write("POSTGRES_PORT=5432\n")
        
        # Load from the temporary file
        load_dotenv('.env.temp')
        print("Created and loaded temporary .env file with default values")
        print("Consider creating a permanent .env file with your configuration")
    
    # Make sure USE_POSTGRES is set
    os.environ['USE_POSTGRES'] = 'True'

def run_with_postgres():
    """Run the Django development server with PostgreSQL"""
    # Set up the environment
    setup_postgres_environment()
    
    # Check if PostgreSQL is available
    try:
        import psycopg2
    except ImportError:
        print("Error: psycopg2-binary package is not installed.")
        print("Install it with: pip install psycopg2-binary")
        sys.exit(1)
    
    # Start the server
    print("Starting Django development server with PostgreSQL...")
    cmd = [sys.executable, 'manage.py', 'runserver']
    
    # If arguments were passed to the script, add them to the command
    if len(sys.argv) > 1:
        cmd.extend(sys.argv[1:])
    
    # Run the server
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\nServer stopped.")

if __name__ == "__main__":
    run_with_postgres() 