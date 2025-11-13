#!/usr/bin/env python3
"""
Migration: Add credit tracking fields to Vendor table
Run this script to add: total_credit, outstanding_credit, cleared_credit, updated_at
"""

from app import app, db
from sqlalchemy import text

def add_vendor_credit_fields():
    with app.app_context():
        try:
            # Check if columns already exist
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('vendor')]
            
            # Add total_credit if not exists
            if 'total_credit' not in columns:
                db.session.execute(text("ALTER TABLE vendor ADD COLUMN total_credit NUMERIC(10, 2) DEFAULT 0.0"))
                print("✅ Added total_credit column")
            
            # Add outstanding_credit if not exists
            if 'outstanding_credit' not in columns:
                db.session.execute(text("ALTER TABLE vendor ADD COLUMN outstanding_credit NUMERIC(10, 2) DEFAULT 0.0"))
                print("✅ Added outstanding_credit column")
            
            # Add cleared_credit if not exists
            if 'cleared_credit' not in columns:
                db.session.execute(text("ALTER TABLE vendor ADD COLUMN cleared_credit NUMERIC(10, 2) DEFAULT 0.0"))
                print("✅ Added cleared_credit column")
            
            # Add updated_at if not exists
            if 'updated_at' not in columns:
                db.session.execute(text("ALTER TABLE vendor ADD COLUMN updated_at DATETIME"))
                print("✅ Added updated_at column")
            
            # Add vendor_name alias if not exists
            if 'vendor_name' not in columns:
                db.session.execute(text("ALTER TABLE vendor ADD COLUMN vendor_name VARCHAR(100)"))
                print("✅ Added vendor_name column")
            
            # Add vendor_type if not exists
            if 'vendor_type' not in columns:
                db.session.execute(text("ALTER TABLE vendor ADD COLUMN vendor_type VARCHAR(50)"))
                print("✅ Added vendor_type column")
            
            # Add contact_number alias if not exists
            if 'contact_number' not in columns:
                db.session.execute(text("ALTER TABLE vendor ADD COLUMN contact_number VARCHAR(20)"))
                print("✅ Added contact_number column")
            
            db.session.commit()
            print("\n✅ Migration completed successfully!")
            
            # Update existing vendors' credit totals
            from app import Vendor, CreditTransaction
            vendors = Vendor.query.all()
            print(f"\n🔄 Updating credit totals for {len(vendors)} vendors...")
            for vendor in vendors:
                vendor.update_credit_totals()
            db.session.commit()
            print("✅ Credit totals updated!")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    add_vendor_credit_fields()

