#!/usr/bin/env python3
"""
Database migration script to add new fields to Bill table
Adds payment_method, ocr_text, verification_status, and parsed OCR fields
"""

from app import app, db, Bill
from sqlalchemy import text, inspect

def update_bill_schema():
    """Add new fields to Bill table if they don't exist"""
    with app.app_context():
        try:
            inspector = inspect(db.engine)
            
            # Check if bill table exists
            if 'bill' not in inspector.get_table_names():
                print("❌ Bill table does not exist! Run db.create_all() first.")
                return False
            
            columns = [col['name'] for col in inspector.get_columns('bill')]
            
            print("=" * 50)
            print("Bill Table Schema Update")
            print("=" * 50)
            
            new_fields = {
                'payment_method': ('VARCHAR(50) DEFAULT "Cash"', 'Payment method field'),
                'ocr_text': ('TEXT', 'OCR extracted text (alias)'),
                'verification_status': ('VARCHAR(20) DEFAULT "unverified"', 'Verification status'),
                'ocr_bill_number': ('VARCHAR(50)', 'Parsed OCR bill number'),
                'ocr_amount': ('FLOAT', 'Parsed OCR amount'),
                'ocr_date': ('DATE', 'Parsed OCR date'),
                'ocr_vendor_name': ('VARCHAR(200)', 'Parsed OCR vendor name')
            }
            
            added_count = 0
            for field_name, (field_type, description) in new_fields.items():
                if field_name not in columns:
                    print(f"Adding {field_name}...")
                    try:
                        db.session.execute(text(f"ALTER TABLE bill ADD COLUMN {field_name} {field_type}"))
                        added_count += 1
                        print(f"  ✅ {field_name} added ({description})")
                    except Exception as e:
                        print(f"  ❌ Error adding {field_name}: {e}")
                else:
                    print(f"  ✓ {field_name} already exists")
            
            if added_count > 0:
                db.session.commit()
                print(f"\n✅ Successfully added {added_count} new field(s)!")
            else:
                print("\n✅ All fields already exist. No changes needed.")
            
            print("=" * 50)
            return True
            
        except Exception as e:
            print(f"❌ Error updating database: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False

if __name__ == '__main__':
    update_bill_schema()

