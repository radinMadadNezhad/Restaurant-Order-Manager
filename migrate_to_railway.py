#!/usr/bin/env python
"""
This script migrates your Django database schema and data to Railway PostgreSQL.
"""

import os
import subprocess
import sys
from dotenv import load_dotenv

def setup_railway_environment():
    """Load Railway environment variables"""
    # Load from .env file if it exists
    if os.path.exists('.env'):
        load_dotenv('.env')
        print("✅ Loaded environment variables from .env file")
    else:
        print("❌ No .env file found. Please create one with your Railway DATABASE_URL")
        sys.exit(1)
    
    # Check if DATABASE_URL is set
    if 'DATABASE_URL' not in os.environ:
        print("❌ DATABASE_URL not found in .env file")
        sys.exit(1)
    
    print(f"✅ Using database: {os.environ['DATABASE_URL'].split('@')[1].split('/')[0]}")

def run_command(command, description):
    """Run a shell command and display output"""
    print(f"\n📋 {description}...")
    print(f"Running: {' '.join(command)}")
    
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    if process.returncode != 0:
        print(f"❌ Error: {process.stderr}")
        return False
    
    print(f"✅ Success!")
    return True

def migrate_database():
    """Run migrations to create database schema on Railway"""
    return run_command(
        ['python', 'manage.py', 'migrate'], 
        "Creating database schema on Railway"
    )

def export_data_from_sqlite():
    """Export data from SQLite database"""
    return run_command(
        ['python', 'manage.py', 'dumpdata', '--exclude', 'contenttypes', 
         '--exclude', 'auth.permission', '--output', 'data_dump.json'],
        "Exporting data from SQLite database"
    )

def import_data_to_railway():
    """Import data to Railway PostgreSQL"""
    return run_command(
        ['python', 'manage.py', 'loaddata', 'data_dump.json'],
        "Importing data to Railway PostgreSQL"
    )

def main():
    """Main migration function"""
    print("🚂 Starting migration to Railway PostgreSQL...")
    
    # Set up environment
    setup_railway_environment()
    
    # Create database schema on Railway
    if not migrate_database():
        print("❌ Failed to create database schema on Railway")
        sys.exit(1)
    
    # Ask if user wants to migrate data
    migrate_data = input("\n❓ Do you want to migrate data from SQLite to Railway? (yes/no): ").lower()
    
    if migrate_data in ('yes', 'y'):
        # Export data from SQLite
        if not export_data_from_sqlite():
            print("❌ Failed to export data from SQLite")
            sys.exit(1)
        
        # Import data to Railway
        if not import_data_to_railway():
            print("❌ Failed to import data to Railway")
            sys.exit(1)
    
    print("\n🎉 Migration completed successfully!")
    print("Your database schema has been created on Railway.")
    if migrate_data in ('yes', 'y'):
        print("Your data has been migrated from SQLite to Railway PostgreSQL.")
    
    print("\n📝 Next steps:")
    print("1. Deploy your application to Railway")
    print("2. Set environment variables on Railway (SECRET_KEY, DEBUG=False, etc.)")
    print("3. Enjoy your deployed application!")

if __name__ == "__main__":
    main() 