# Credit Management System for Skanda Enterprises

A comprehensive web-based credit management system built with Flask, featuring role-based authentication, invoice management, credit tracking, and detailed reporting capabilities.

## Features

### 🔐 Authentication & Roles
- **Admin**: Full access to all features including invoice editing, deletion, and salesman management
- **Delivery Person**: Can add invoices and record credits, but cannot delete invoices or view admin-only reports
- Secure password storage using Werkzeug's password hashing

### 📄 Invoice Management
- Create invoices with unique invoice numbers
- Salesman details (name, contact)
- Delivery date tracking
- Bill amount management
- Edit and view invoices (admin only)
- Delete invoices (admin only)
- **📸 OCR Image Processing**: Upload invoice images with automatic text extraction
- View extracted text and OCR confidence scores
- Image storage and retrieval for admin review

### 💳 Credit Management
- Add credits/payments to invoices
- Auto-calculate outstanding balance = Bill Amount – Sum of Credits
- Track payment methods (Cash, Bank Transfer, Cheque, UPI, Credit Card, Other)
- Payment history with notes
- Show pending credits

### 👥 Salesman Management
- Add, edit, and view salesmen (admin only)
- Contact information management
- Invoice tracking per salesman

### 📊 Reports & Analytics
- View all invoices with filtering options
- Filter by salesman, date range, and payment status
- Payment progress visualization
- Salesman performance metrics
- Export capabilities (Excel/CSV)
- Real-time statistics dashboard

### 📱 Responsive Design
- Mobile-first approach
- Desktop, tablet, and mobile optimized
- Bootstrap 5 framework
- Modern UI with Font Awesome icons

## Tech Stack

- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **OCR**: Tesseract (pytesseract) for text extraction from images
- **Image Processing**: Pillow (PIL) for image handling
- **UI Framework**: Bootstrap 5
- **Icons**: Font Awesome 6
- **Security**: Werkzeug password hashing

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Step 1: Clone/Download the Project
```bash
# If you have git
git clone <repository-url>
cd Skanda

# Or download and extract the project files
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5001`

### Step 4: Access the System
1. Open your web browser
2. Navigate to `http://localhost:5001`
3. Login with default admin credentials:
   - **Username**: `admin`
   - **Password**: `admin123`

## Default Login Credentials

| Role | Username | Password | Access Level |
|------|----------|----------|--------------|
| Admin | admin | admin123 | Full access |

## Project Structure

```
Skanda/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── login.html        # Login page
│   ├── dashboard.html    # Dashboard
│   ├── invoices.html     # Invoice list
│   ├── new_invoice.html  # Create invoice
│   ├── view_invoice.html # View invoice details
│   ├── edit_invoice.html # Edit invoice
│   ├── new_credit.html   # Add credit/payment
│   ├── salesmen.html     # Salesman list
│   ├── new_salesman.html # Add salesman
│   ├── edit_salesman.html# Edit salesman
│   └── reports.html      # Reports & analytics
├── static/               # Static assets
│   ├── css/
│   │   └── style.css     # Custom styles
│   └── js/
│       └── main.js       # JavaScript functionality
└── credit_management.db # SQLite database (created automatically)
```

## Usage Guide

### 1. Getting Started
- Login with admin credentials
- Change the default password immediately
- Add your first salesman
- Create your first invoice

### 2. Managing Salesmen (Admin Only)
- Navigate to "Salesmen" in the menu
- Click "Add Salesman" to create new salesmen
- Edit existing salesmen information
- View invoice statistics per salesman

### 3. Creating Invoices
- Go to "Invoices" → "New Invoice"
- Fill in invoice details:
  - Invoice Number (auto-generated if left empty)
  - Select Salesman
  - Delivery Date
  - Bill Amount
- Click "Create Invoice"

### 4. Recording Payments
- View any invoice
- Click "Add Credit" button
- Enter payment details:
  - Payment Amount
  - Payment Date
  - Payment Method
  - Optional notes
- Click "Record Payment"

### 5. Viewing Reports
- Navigate to "Reports"
- Use filters to narrow down data:
  - By Salesman
  - By Date Range
- View payment progress and statistics
- Export data to Excel/CSV

## Key Features Explained

### Data Integrity
- **Unique Invoice Numbers**: System prevents duplicate invoice numbers
- **Proper Linking**: Credits are properly linked to invoices
- **Auto-calculations**: Outstanding balances are automatically calculated

### Security Features
- Password hashing using Werkzeug
- Session management
- Role-based access control
- CSRF protection

### Responsive Design
- Mobile-first approach
- Touch-friendly interface
- Optimized for all screen sizes
- Print-friendly layouts

## Customization

### Adding New Payment Methods
Edit the `new_credit.html` template and add new options to the payment method select:

```html
<option value="New Method">New Method</option>
```

### Modifying User Roles
In `app.py`, you can add new roles by modifying the User model and adding role checks in the decorators.

### Database Modifications
To add new fields to existing models:
1. Modify the model in `app.py`
2. Create a database migration (or delete the existing database file)
3. Restart the application

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Change port in app.py
   app.run(debug=True, host='0.0.0.0', port=5001)
   ```

2. **Database Errors**
   ```bash
   # Delete the database file and restart
   rm credit_management.db
   python app.py
   ```

3. **Permission Errors**
   ```bash
   # Make sure you have write permissions in the project directory
   chmod 755 /path/to/Skanda
   ```

### Browser Compatibility
- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## Future Enhancements

### Planned Features
- Customer management system
- Advanced reporting with charts
- PDF invoice generation
- Email notifications
- Multi-language support
- API endpoints for mobile apps
- Backup and restore functionality
- Audit trail logging

### Integration Possibilities
- Accounting software integration
- Payment gateway integration
- SMS notifications
- Cloud storage integration

## Support

For technical support or feature requests, please contact the development team.

## License

This project is proprietary software developed for Skanda Enterprises.

---

**Version**: 1.0.0  
**Last Updated**: December 2024  
**Developed for**: Skanda Enterprises
