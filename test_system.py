#!/usr/bin/env python3
"""
Test script for Credit Management System
This script tests the basic functionality of the system
"""

import os
import sys
import sqlite3
from datetime import datetime, date

def test_database_creation():
    """Test if database can be created and tables exist"""
    print("Testing database creation...")
    
    try:
        # Import the app to create database
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from app import app, db, User, Salesman, Invoice, Credit, create_tables
        
        with app.app_context():
            create_tables()
            
            # Check if tables exist
            conn = sqlite3.connect('credit_management.db')
            cursor = conn.cursor()
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [table[0] for table in cursor.fetchall()]
            
            print(f"Found tables: {tables}")
            
            expected_tables = ['user', 'salesman', 'invoice', 'credit']
            # SQLite might use different casing, so let's check both
            tables_lower = [table.lower() for table in tables]
            missing_tables = [table for table in expected_tables if table not in tables_lower]
            
            if missing_tables:
                print(f"❌ Missing tables: {missing_tables}")
                return False
            else:
                print("✅ All tables created successfully")
                return True
                
    except Exception as e:
        print(f"❌ Database creation failed: {e}")
        return False

def test_default_admin():
    """Test if default admin user is created"""
    print("Testing default admin user...")
    
    try:
        from app import app, User
        
        with app.app_context():
            admin = User.query.filter_by(username='admin').first()
            
            if admin and admin.role == 'admin':
                print("✅ Default admin user created successfully")
                return True
            else:
                print("❌ Default admin user not found or incorrect role")
                return False
                
    except Exception as e:
        print(f"❌ Admin user test failed: {e}")
        return False

def test_sample_data():
    """Test creating sample data"""
    print("Testing sample data creation...")
    
    try:
        from app import app, db, User, Salesman, Invoice, Credit
        
        with app.app_context():
            # Create a test salesman
            salesman = Salesman(
                name="Test Salesman",
                contact="9876543210",
                email="test@example.com",
                address="Test Address"
            )
            db.session.add(salesman)
            db.session.commit()
            
            # Create a test invoice
            invoice = Invoice(
                invoice_number="TEST-001",
                salesman_id=salesman.id,
                delivery_date=date.today(),
                bill_amount=10000.00,
                created_by=1  # Assuming admin user has ID 1
            )
            db.session.add(invoice)
            db.session.commit()
            
            # Create a test credit
            credit = Credit(
                invoice_id=invoice.id,
                amount=5000.00,
                payment_date=date.today(),
                payment_method="Cash",
                notes="Test payment",
                created_by=1
            )
            db.session.add(credit)
            db.session.commit()
            
            # Verify data
            if invoice.outstanding_balance == 5000.00:
                print("✅ Sample data created and calculations working")
                return True
            else:
                print(f"❌ Calculation error: Expected 5000.00, got {invoice.outstanding_balance}")
                return False
                
    except Exception as e:
        print(f"❌ Sample data test failed: {e}")
        return False

def test_password_hashing():
    """Test password hashing functionality"""
    print("Testing password hashing...")
    
    try:
        from app import User
        
        user = User(username="test_user", email="test@test.com")
        user.set_password("test_password")
        
        if user.check_password("test_password") and not user.check_password("wrong_password"):
            print("✅ Password hashing working correctly")
            return True
        else:
            print("❌ Password hashing failed")
            return False
            
    except Exception as e:
        print(f"❌ Password hashing test failed: {e}")
        return False

def cleanup_test_data():
    """Clean up test data"""
    print("Cleaning up test data...")
    
    try:
        from app import app, db, Salesman, Invoice, Credit
        
        with app.app_context():
            # Delete test data
            Credit.query.filter(Credit.notes == "Test payment").delete()
            Invoice.query.filter(Invoice.invoice_number == "TEST-001").delete()
            Salesman.query.filter(Salesman.name == "Test Salesman").delete()
            db.session.commit()
            
            print("✅ Test data cleaned up")
            return True
            
    except Exception as e:
        print(f"❌ Cleanup failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("Credit Management System - Test Suite")
    print("=" * 50)
    
    tests = [
        test_database_creation,
        test_default_admin,
        test_password_hashing,
        test_sample_data,
        cleanup_test_data
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
        print()
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The system is ready to use.")
        print("\nTo start the application:")
        print("1. Run: python app.py")
        print("2. Open: http://localhost:5000")
        print("3. Login with: admin / admin123")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
