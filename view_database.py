#!/usr/bin/env python3
"""
Simple Database Viewer for Credit Management System
"""

import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User, Salesman, Invoice, Credit

def view_all_data():
    """View all data in the database"""
    with app.app_context():
        print("=" * 60)
        print("CREDIT MANAGEMENT SYSTEM - DATA VIEWER")
        print("=" * 60)
        
        # Users
        print("\n👥 USERS:")
        print("-" * 30)
        users = User.query.all()
        if users:
            for user in users:
                print(f"ID: {user.id} | Username: {user.username} | Role: {user.role} | Email: {user.email}")
        else:
            print("No users found")
        
        # Salesmen
        print("\n👨‍💼 SALESMEN:")
        print("-" * 30)
        salesmen = Salesman.query.all()
        if salesmen:
            for salesman in salesmen:
                print(f"ID: {salesman.id} | Name: {salesman.name} | Contact: {salesman.contact} | Email: {salesman.email}")
        else:
            print("No salesmen found")
        
        # Invoices
        print("\n📄 INVOICES:")
        print("-" * 30)
        invoices = Invoice.query.all()
        if invoices:
            for invoice in invoices:
                salesman_name = invoice.salesman.name if invoice.salesman else "Unknown"
                print(f"ID: {invoice.id} | Invoice #: {invoice.invoice_number} | Salesman: {salesman_name} | Amount: ₹{invoice.bill_amount} | Date: {invoice.delivery_date}")
        else:
            print("No invoices found")
        
        # Credits
        print("\n💳 CREDITS/PAYMENTS:")
        print("-" * 30)
        credits = Credit.query.all()
        if credits:
            for credit in credits:
                print(f"ID: {credit.id} | Invoice ID: {credit.invoice_id} | Amount: ₹{credit.amount} | Method: {credit.payment_method} | Date: {credit.payment_date}")
        else:
            print("No credits found")
        
        print("\n" + "=" * 60)
        print("Data viewing complete!")

if __name__ == "__main__":
    view_all_data()
