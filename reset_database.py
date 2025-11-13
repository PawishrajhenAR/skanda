#!/usr/bin/env python3
"""
Reset Database Script
This script deletes the existing database and recreates it with new schema
"""

import os
import sys

def reset_database():
    """Delete and recreate database"""
    
    # Database paths
    db_path = 'instance/credit_management.db'
    
    print("Resetting database...")
    print("=" * 50)
    
    # Delete existing database
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"✅ Deleted: {db_path}")
    else:
        print(f"ℹ️  Database file not found: {db_path}")
    
    # Import app and create tables
    from app import app, db, create_tables
    
    with app.app_context():
        create_tables()
        print("\n✅ Database recreated successfully!")
        print("=" * 50)
        print("\nDefault credentials:")
        print("  Admin: admin / admin123")
        print("  Delivery Man: delivery1 / delivery123")
        print("  Salesman: salesman1 / salesman123")
        print("  Computer Organiser: organiser1 / organiser123")

if __name__ == "__main__":
    reset_database()

