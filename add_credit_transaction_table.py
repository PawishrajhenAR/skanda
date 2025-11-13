#!/usr/bin/env python3
"""
Database migration script to add CreditTransaction table
Run this script to add the new credit_transaction table to your database
"""

from app import app, db, CreditTransaction
from sqlalchemy import text, inspect

def add_credit_transaction_table():
    """Add CreditTransaction table if it doesn't exist"""
    with app.app_context():
        try:
            # Check if credit_transaction table exists
            inspector = inspect(db.engine)
            existing_tables = inspector.get_table_names()
            
            if 'credit_transaction' not in existing_tables:
                print("Creating credit_transaction table...")
                
                # Create the table using SQLAlchemy
                db.create_all()
                
                print("✅ credit_transaction table created successfully!")
                print("\nTable structure:")
                print("  - id (Integer, PK)")
                print("  - bill_id (Integer, FK to bill.id)")
                print("  - bill_number (String)")
                print("  - vendor_id (Integer, FK to vendor.id)")
                print("  - salesman_id (Integer, FK to salesman.id)")
                print("  - credit_amount (Numeric)")
                print("  - due_date (Date)")
                print("  - status (String: Pending, Cleared, Overdue)")
                print("  - payment_method (String)")
                print("  - created_at (DateTime)")
                print("  - updated_at (DateTime)")
            else:
                print("✅ credit_transaction table already exists")
                
                # Check if all columns exist
                columns = [col['name'] for col in inspector.get_columns('credit_transaction')]
                required_columns = [
                    'id', 'bill_id', 'bill_number', 'vendor_id', 'salesman_id',
                    'credit_amount', 'due_date', 'status', 'payment_method',
                    'created_at', 'updated_at'
                ]
                
                missing_columns = [col for col in required_columns if col not in columns]
                
                if missing_columns:
                    print(f"⚠️  Missing columns: {missing_columns}")
                    print("Adding missing columns...")
                    
                    # Add missing columns
                    if 'bill_id' not in columns:
                        db.session.execute(text("ALTER TABLE credit_transaction ADD COLUMN bill_id INTEGER"))
                    if 'bill_number' not in columns:
                        db.session.execute(text("ALTER TABLE credit_transaction ADD COLUMN bill_number VARCHAR(50)"))
                    if 'vendor_id' not in columns:
                        db.session.execute(text("ALTER TABLE credit_transaction ADD COLUMN vendor_id INTEGER"))
                    if 'salesman_id' not in columns:
                        db.session.execute(text("ALTER TABLE credit_transaction ADD COLUMN salesman_id INTEGER"))
                    if 'credit_amount' not in columns:
                        db.session.execute(text("ALTER TABLE credit_transaction ADD COLUMN credit_amount NUMERIC(10,2)"))
                    if 'due_date' not in columns:
                        db.session.execute(text("ALTER TABLE credit_transaction ADD COLUMN due_date DATE"))
                    if 'status' not in columns:
                        db.session.execute(text("ALTER TABLE credit_transaction ADD COLUMN status VARCHAR(20) DEFAULT 'Pending'"))
                    if 'payment_method' not in columns:
                        db.session.execute(text("ALTER TABLE credit_transaction ADD COLUMN payment_method VARCHAR(50) DEFAULT 'Cash'"))
                    if 'created_at' not in columns:
                        db.session.execute(text("ALTER TABLE credit_transaction ADD COLUMN created_at DATETIME"))
                    if 'updated_at' not in columns:
                        db.session.execute(text("ALTER TABLE credit_transaction ADD COLUMN updated_at DATETIME"))
                    
                    db.session.commit()
                    print("✅ Missing columns added successfully!")
                else:
                    print("✅ All required columns exist")
            
            print("\n" + "=" * 50)
            print("Migration completed successfully!")
            print("=" * 50)
            
        except Exception as e:
            print(f"❌ Error updating database: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()

if __name__ == '__main__':
    print("=" * 50)
    print("Credit Transaction Table Migration")
    print("=" * 50)
    add_credit_transaction_table()

