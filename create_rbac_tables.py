#!/usr/bin/env python3
"""
Migration: Create RBAC tables (Role, Permission, role_permission, AuditLog)
"""

from app import app, db

def create_rbac_tables():
    with app.app_context():
        try:
            print("Creating RBAC and Audit Log tables...")
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
    create_rbac_tables()

