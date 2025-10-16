#!/usr/bin/env python3
"""
Database Viewer Script
Shows all data stored in the Credit Management System
"""

import sqlite3
import os

def view_database():
    db_path = 'credit_management.db'
    
    if not os.path.exists(db_path):
        print("❌ Database file not found!")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("=" * 60)
    print("CREDIT MANAGEMENT SYSTEM - DATABASE VIEWER")
    print("=" * 60)
    
    # Show all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    for table in tables:
        table_name = table[0]
        print(f"\n📋 TABLE: {table_name.upper()}")
        print("-" * 40)
        
        # Get table structure
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        
        # Get all data
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()
        
        if rows:
            # Print column headers
            headers = [col[1] for col in columns]
            print(" | ".join(headers))
            print("-" * (len(" | ".join(headers))))
            
            # Print data rows
            for row in rows:
                print(" | ".join(str(cell) for cell in row))
        else:
            print("(No data)")
    
    conn.close()
    print("\n" + "=" * 60)
    print("Database viewing complete!")

if __name__ == "__main__":
    view_database()
