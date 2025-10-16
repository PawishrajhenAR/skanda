#!/usr/bin/env python3
"""
Database update script to add image fields to Invoice table
"""

from app import app, db, Invoice
import os

def update_database_schema():
    """Update database schema to add image fields"""
    with app.app_context():
        try:
            # Check if image_filename column exists
            from sqlalchemy import text
            result = db.session.execute(text("PRAGMA table_info(invoice)"))
            columns = [row[1] for row in result]
            
            if 'image_filename' not in columns:
                print("Adding image fields to Invoice table...")
                
                # Add new columns
                db.session.execute(text("ALTER TABLE invoice ADD COLUMN image_filename VARCHAR(255)"))
                db.session.execute(text("ALTER TABLE invoice ADD COLUMN extracted_text TEXT"))
                db.session.execute(text("ALTER TABLE invoice ADD COLUMN ocr_confidence FLOAT"))
                db.session.commit()
                
                print("✅ Image fields added successfully!")
            else:
                print("✅ Image fields already exist in Invoice table")
                
            # Create upload directory
            upload_dir = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
            os.makedirs(upload_dir, exist_ok=True)
            print(f"✅ Upload directory created: {upload_dir}")
            
        except Exception as e:
            print(f"❌ Error updating database: {e}")
            db.session.rollback()

if __name__ == '__main__':
    update_database_schema()
