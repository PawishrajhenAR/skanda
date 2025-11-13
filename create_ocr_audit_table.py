#!/usr/bin/env python3
"""
Database migration script to create OCR Audit Log table
"""

from app import app, db, OCRAuditLog
from sqlalchemy import inspect

def create_ocr_audit_table():
    """Create OCR Audit Log table if it doesn't exist"""
    with app.app_context():
        try:
            inspector = inspect(db.engine)
            existing_tables = inspector.get_table_names()
            
            if 'ocr_audit_log' not in existing_tables:
                print("Creating ocr_audit_log table...")
                db.create_all()
                print("✅ ocr_audit_log table created successfully!")
            else:
                print("✅ ocr_audit_log table already exists")
            
            print("=" * 50)
            print("Migration completed successfully!")
            print("=" * 50)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    create_ocr_audit_table()

