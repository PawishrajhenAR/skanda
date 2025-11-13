#!/usr/bin/env python3
"""
Migration: Create OCRVendorLinkLog table
Run this script to create the table for tracking OCR vendor matches
"""

from app import app, db

def create_ocr_vendor_link_table():
    with app.app_context():
        try:
            # Check if table exists
            inspector = db.inspect(db.engine)
            table_names = inspector.get_table_names()
            
            if 'ocr_vendor_link_log' not in table_names:
                # Create table using SQLAlchemy
                from app import OCRVendorLinkLog
                db.create_all()
                print("✅ Created ocr_vendor_link_log table")
            else:
                print("ℹ️  ocr_vendor_link_log table already exists")
            
            print("\n✅ Migration completed successfully!")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    create_ocr_vendor_link_table()

