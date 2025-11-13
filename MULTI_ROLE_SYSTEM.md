# Multi-Role Business Management & Billing System

## 🎭 User Roles & Access

### 1. **Admin** (Superuser)
- **Full Access**: All system features
- **Capabilities**:
  - Manage users, vendors, salesmen, customers
  - Create/edit invoices, bills, delivery orders
  - Approve/reject transactions
  - View all analytics, reports, activity logs
  - Access OCR verification
- **Dashboard**: Complete system overview with all KPIs
- **Login**: `admin` / `admin123`

### 2. **Delivery Man**
- **Restricted Access**: Only assigned deliveries
- **Capabilities**:
  - View assigned delivery orders
  - Update delivery status (Pending/In Transit/Delivered/Cancelled)
  - Upload delivery receipts via OCR
  - Add delivery remarks
- **Dashboard**: Personal delivery stats, today's assignments
- **Login**: `delivery1` / `delivery123`

### 3. **Salesman**
- **Sales & Billing Focus**
- **Capabilities**:
  - Create bills (Handbill/Normal Bill)
  - Manual entry or OCR upload for bill processing
  - Manage customers and vendors
  - View own sales and credit data
  - Track daily sales summary
- **Dashboard**: Today's sales, bill creation, vendor/customer lists
- **Login**: `salesman1` / `salesman123`

### 4. **Computer Organiser** (Back Office)
- **Records & OCR Verification**
- **Capabilities**:
  - Verify OCR-extracted bill data
  - Correct OCR errors
  - Manage bill verification queue
  - Export reports (Excel/PDF)
  - Maintain data integrity
- **Dashboard**: OCR verification queue, pending bills, verified count
- **Login**: `organiser1` / `organiser123`

## 📊 System Modules

### Invoice Management
- Create invoices with OCR image processing
- Track credits and outstanding balances
- View, edit, delete (Admin only)
- Payment tracking with multiple payment methods

### Bill Management
- **Handbill**: Quick informal receipts
- **Normal Bill**: Formal billing documents
- OCR text extraction from bill images
- Verification queue for Computer Organiser
- Vendor and customer linking

### Delivery Management
- Create delivery orders (Admin)
- Assign to delivery men
- Track status in real-time
- OCR receipt confirmation
- Delivery remarks and signatures

### Vendor Management
- Add/edit vendor profiles
- GST number tracking
- Category classification
- Contact information management

### Customer Management
- Customer profiles with credit limits
- GST number tracking
- Company information
- Credit management per customer

### Credit Management
- Record payments/credits
- Multiple payment methods
- Auto-calculation of outstanding balance
- Payment history tracking

### Reports & Analytics
- Collection rate dashboard
- Sales performance metrics
- Delivery completion rates
- Financial summaries
- Export to Excel/PDF

## 🔐 Security Features

- Role-based authentication
- Session management
- Password hashing (Werkzeug)
- Activity logging
- IP tracking for audit trails
- Role-based route guards

## 📁 Database Models

### User
- Role-based access control
- Active/inactive status
- Profile information

### Vendor
- Contact information
- GST numbers
- Categories

### Bill
- Handbill/Normal bill types
- OCR extraction with confidence scores
- Verification status
- Created by tracking

### DeliveryOrder
- Status tracking
- Delivery man assignment
- OCR receipt uploads
- Delivery remarks

### Invoice
- Customer and salesman linking
- Credit tracking
- OCR image processing

### Credit
- Payment recording
- Multiple payment methods
- Payment notes

### ActivityLog
- User action tracking
- Timestamp and IP recording
- Old/new value changes

## 🚀 Quick Start

1. **Start the application**:
   ```bash
   start.bat
   # or
   run.bat
   # or
   venv\Scripts\python.exe app.py
   ```

2. **Access**: http://localhost:5000

3. **Login with any role**:
   - Admin: admin / admin123
   - Delivery: delivery1 / delivery123
   - Salesman: salesman1 / salesman123
   - Organiser: organiser1 / organiser123

4. **Reset Database** (if needed):
   ```bash
   venv\Scripts\python.exe reset_database.py
   ```

## 🎯 Workflow Examples

### Salesman Creating a Bill
1. Login as salesman
2. Dashboard → New Bill
3. Select bill type (Handbill/Normal)
4. Choose vendor, enter amount
5. Upload bill image for OCR
6. Submit for verification

### Delivery Man Updating Status
1. Login as delivery man
2. View assigned deliveries
3. Click on delivery order
4. Update status: In Transit → Delivered
5. Upload delivery receipt (OCR)
6. Add delivery remarks

### Computer Organiser Verifying Bills
1. Login as computer organiser
2. View OCR verification queue
3. Review extracted text
4. Correct any errors
5. Approve/verify bill
6. Bill status updated to verified

### Admin Creating Delivery Order
1. Login as admin
2. Deliveries → New Delivery Order
3. Select delivery man
4. Enter delivery address and contact
5. Assign to delivery date
6. Delivery man receives notification

## 📝 Key Features

- ✅ Multi-role access control
- ✅ OCR bill processing with confidence scoring
- ✅ Delivery order tracking
- ✅ Real-time status updates
- ✅ Payment method variety (Cash, UPI, Bank, etc.)
- ✅ Activity logging and audit trail
- ✅ Export capabilities (Excel/PDF)
- ✅ Mobile-responsive design
- ✅ Beautiful modern UI with Bootstrap 5
- ✅ Role-specific dashboards
- ✅ Credit management with auto-calculation

## 🔧 Technical Stack

- **Backend**: Python Flask
- **Database**: SQLite with SQLAlchemy ORM
- **OCR**: Tesseract (pytesseract)
- **Image Processing**: Pillow
- **Report Generation**: ReportLab
- **Excel Export**: openpyxl
- **Frontend**: Bootstrap 5, Font Awesome 6
- **Deployment**: Vercel ready

## 📞 Support

For issues or questions:
- Check the logs in application console
- Review activity logs in admin dashboard
- Contact system administrator

---

**Version**: 2.0.0 (Multi-Role Enhanced)  
**Last Updated**: January 2025

