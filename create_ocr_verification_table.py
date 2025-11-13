#!/usr/bin/env python3
"""
Migration: Create OCRVerificationLog table
"""

from app import app, db

def create_ocr_verification_table():
    with app.app_context():
        try:
            print("Creating OCR Verification Log table...")
            print("=" * 60)
            
            # Create all tables
            db.create_all()
            print("✅ All tables created/verified")
            
            print("\n✅ Migration completed successfully!")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    create_ocr_verification_table()

