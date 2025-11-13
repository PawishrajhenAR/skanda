#!/usr/bin/env python3
"""
Verify CreditTransaction table structure
"""

from app import app, db
from sqlalchemy import text, inspect

def verify_table():
    """Verify credit_transaction table has all required columns"""
    with app.app_context():
        try:
            inspector = inspect(db.engine)
            
            # Check if table exists
            if 'credit_transaction' not in inspector.get_table_names():
                print("❌ credit_transaction table does not exist!")
                return False
            
            # Get columns
            columns = {col['name']: col['type'] for col in inspector.get_columns('credit_transaction')}
            
            print("=" * 50)
            print("Credit Transaction Table Structure")
            print("=" * 50)
            
            required_columns = {
                'id': 'Integer (PK)',
                'bill_id': 'Integer (FK)',
                'bill_number': 'String',
                'vendor_id': 'Integer (FK)',
                'salesman_id': 'Integer (FK)',
                'credit_amount': 'Numeric',
                'due_date': 'Date',
                'status': 'String',
                'payment_method': 'String',
                'created_at': 'DateTime',
                'updated_at': 'DateTime'
            }
            
            all_present = True
            for col_name, col_type in required_columns.items():
                if col_name in columns:
                    print(f"✅ {col_name}: {columns[col_name]}")
                else:
                    print(f"❌ {col_name}: MISSING!")
                    all_present = False
            
            print("=" * 50)
            if all_present:
                print("✅ All required columns are present!")
                return True
            else:
                print("❌ Some columns are missing!")
                return False
                
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    verify_table()

