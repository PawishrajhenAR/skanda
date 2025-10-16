"""
Credit Management System for Skanda Enterprises
Main Flask application file
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, make_response, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import os
import io
import uuid
from functools import wraps
from PIL import Image
import pytesseract
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'skanda-enterprises-credit-management-2024')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///credit_management.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

db = SQLAlchemy(app)

# OCR Functions
def extract_text_from_image(image_path):
    """Extract text from image using OCR"""
    try:
        # Open image
        image = Image.open(image_path)
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Extract text using pytesseract
        text = pytesseract.image_to_string(image, lang='eng')
        
        # Get confidence score
        data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
        confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        
        return text.strip(), avg_confidence
    except Exception as e:
        print(f"OCR Error: {e}")
        return "", 0

def allowed_file(filename):
    """Check if file extension is allowed"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='delivery')  # admin or delivery
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120))
    address = db.Column(db.Text)
    company_name = db.Column(db.String(100))
    gst_number = db.Column(db.String(20))
    credit_limit = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    invoices = db.relationship('Invoice', backref='customer', lazy=True)

class Salesman(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120))
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    invoices = db.relationship('Invoice', backref='salesman', lazy=True)

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(50), unique=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=True)
    salesman_id = db.Column(db.Integer, db.ForeignKey('salesman.id'), nullable=False)
    delivery_date = db.Column(db.Date, nullable=False)
    bill_amount = db.Column(db.Float, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Image fields for OCR
    image_filename = db.Column(db.String(255), nullable=True)
    extracted_text = db.Column(db.Text, nullable=True)
    ocr_confidence = db.Column(db.Float, nullable=True)
    
    # Relationship
    credits = db.relationship('Credit', backref='invoice', lazy=True, cascade='all, delete-orphan')
    
    @property
    def total_credits(self):
        return sum(credit.amount for credit in self.credits)
    
    @property
    def outstanding_balance(self):
        return self.bill_amount - self.total_credits
    
    @property
    def is_paid(self):
        return self.outstanding_balance <= 0

class Credit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    payment_method = db.Column(db.String(50), default='Cash')
    notes = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Authentication decorators
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        
        user = User.query.get(session['user_id'])
        if not user or user.role != 'admin':
            flash('Admin access required.', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Get statistics for dashboard
    total_invoices = Invoice.query.count()
    total_pending = Invoice.query.filter(Invoice.bill_amount > db.func.coalesce(
        db.select(db.func.sum(Credit.amount)).where(Credit.invoice_id == Invoice.id).scalar_subquery(), 0
    )).count()
    total_paid = total_invoices - total_pending
    
    # Calculate collection rate
    total_bill_amount = db.session.query(db.func.sum(Invoice.bill_amount)).scalar() or 0
    total_collected = db.session.query(db.func.sum(Credit.amount)).scalar() or 0
    collection_rate = (total_collected / total_bill_amount * 100) if total_bill_amount > 0 else 0
    
    # Calculate outstanding amount
    total_outstanding = total_bill_amount - total_collected
    
    recent_invoices = Invoice.query.order_by(Invoice.created_at.desc()).limit(5).all()
    
    return render_template('dashboard.html', 
                         total_invoices=total_invoices,
                         total_pending=total_pending,
                         total_paid=total_paid,
                         total_bill_amount=total_bill_amount,
                         total_collected=total_collected,
                         total_outstanding=total_outstanding,
                         collection_rate=collection_rate,
                         recent_invoices=recent_invoices)

@app.route('/invoices')
@login_required
def invoices():
    page = request.args.get('page', 1, type=int)
    salesman_filter = request.args.get('salesman', type=int)
    status_filter = request.args.get('status', 'all')
    
    query = Invoice.query
    
    if salesman_filter:
        query = query.filter(Invoice.salesman_id == salesman_filter)
    
    if status_filter == 'pending':
        query = query.filter(Invoice.bill_amount > db.func.coalesce(
            db.select(db.func.sum(Credit.amount)).where(Credit.invoice_id == Invoice.id).scalar_subquery(), 0
        ))
    elif status_filter == 'paid':
        query = query.filter(Invoice.bill_amount <= db.func.coalesce(
            db.select(db.func.sum(Credit.amount)).where(Credit.invoice_id == Invoice.id).scalar_subquery(), 0
        ))
    
    invoices = query.order_by(Invoice.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False)
    
    salesmen = Salesman.query.all()
    
    return render_template('invoices.html', invoices=invoices, salesmen=salesmen)

@app.route('/invoices/new', methods=['GET', 'POST'])
@login_required
def new_invoice():
    if request.method == 'POST':
        try:
            invoice_number = request.form['invoice_number']
            salesman_id = request.form['salesman_id']
            delivery_date = datetime.strptime(request.form['delivery_date'], '%Y-%m-%d').date()
            bill_amount = float(request.form['bill_amount'])
            
            # Check for duplicate invoice number
            existing_invoice = Invoice.query.filter_by(invoice_number=invoice_number).first()
            if existing_invoice:
                flash('Invoice number already exists!', 'error')
                return render_template('new_invoice.html', salesmen=Salesman.query.all())
            
            invoice = Invoice(
                invoice_number=invoice_number,
                salesman_id=salesman_id,
                delivery_date=delivery_date,
                bill_amount=bill_amount,
                created_by=session['user_id']
            )
            
            db.session.add(invoice)
            db.session.commit()
            
            flash('Invoice created successfully!', 'success')
            return redirect(url_for('invoices'))
        except Exception as e:
            flash(f'Error creating invoice: {str(e)}', 'error')
            return render_template('new_invoice.html', salesmen=Salesman.query.all())
    
    return render_template('new_invoice.html', salesmen=Salesman.query.all())

@app.route('/invoices/<int:invoice_id>')
@login_required
def view_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    return render_template('view_invoice.html', invoice=invoice)

@app.route('/invoices/<int:invoice_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    
    if request.method == 'POST':
        invoice.invoice_number = request.form['invoice_number']
        invoice.salesman_id = request.form['salesman_id']
        invoice.delivery_date = datetime.strptime(request.form['delivery_date'], '%Y-%m-%d').date()
        invoice.bill_amount = float(request.form['bill_amount'])
        
        db.session.commit()
        flash('Invoice updated successfully!', 'success')
        return redirect(url_for('view_invoice', invoice_id=invoice.id))
    
    return render_template('edit_invoice.html', invoice=invoice, salesmen=Salesman.query.all())

@app.route('/invoices/<int:invoice_id>/delete', methods=['POST'])
@admin_required
def delete_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    db.session.delete(invoice)
    db.session.commit()
    flash('Invoice deleted successfully!', 'success')
    return redirect(url_for('invoices'))

@app.route('/invoices/<int:invoice_id>/upload-image', methods=['GET', 'POST'])
@login_required
def upload_invoice_image(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No image file selected.', 'error')
            return redirect(request.url)
        
        file = request.files['image']
        if file.filename == '':
            flash('No image file selected.', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            try:
                # Create upload directory if it doesn't exist
                upload_dir = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
                os.makedirs(upload_dir, exist_ok=True)
                
                # Generate unique filename
                file_extension = file.filename.rsplit('.', 1)[1].lower()
                filename = f"invoice_{invoice_id}_{uuid.uuid4().hex}.{file_extension}"
                file_path = os.path.join(upload_dir, filename)
                
                # Save file
                file.save(file_path)
                
                # Extract text using OCR
                extracted_text, confidence = extract_text_from_image(file_path)
                
                # Update invoice with image info
                invoice.image_filename = filename
                invoice.extracted_text = extracted_text
                invoice.ocr_confidence = confidence
                
                db.session.commit()
                
                flash(f'Image uploaded successfully! OCR confidence: {confidence:.1f}%', 'success')
                return redirect(url_for('view_invoice', invoice_id=invoice_id))
            except Exception as e:
                flash(f'Image upload failed: {str(e)}. OCR feature may not be available in serverless environment.', 'error')
                return redirect(url_for('view_invoice', invoice_id=invoice_id))
        else:
            flash('Invalid file type. Please upload a valid image file.', 'error')
    
    return render_template('upload_image.html', invoice=invoice)

@app.route('/invoices/<int:invoice_id>/image')
@login_required
def view_invoice_image(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    
    if not invoice.image_filename:
        flash('No image available for this invoice.', 'error')
        return redirect(url_for('view_invoice', invoice_id=invoice_id))
    
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], invoice.image_filename)
    return send_file(image_path)

@app.route('/invoices/<int:invoice_id>/credits/new', methods=['GET', 'POST'])
@login_required
def new_credit(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    
    if request.method == 'POST':
        amount = float(request.form['amount'])
        payment_date = datetime.strptime(request.form['payment_date'], '%Y-%m-%d').date()
        payment_method = request.form['payment_method']
        notes = request.form.get('notes', '')
        
        credit = Credit(
            invoice_id=invoice_id,
            amount=amount,
            payment_date=payment_date,
            payment_method=payment_method,
            notes=notes,
            created_by=session['user_id']
        )
        
        db.session.add(credit)
        db.session.commit()
        
        flash('Credit recorded successfully!', 'success')
        return redirect(url_for('view_invoice', invoice_id=invoice_id))
    
    return render_template('new_credit.html', invoice=invoice)

@app.route('/salesmen')
@admin_required
def salesmen():
    salesmen = Salesman.query.all()
    return render_template('salesmen.html', salesmen=salesmen)

@app.route('/salesmen/new', methods=['GET', 'POST'])
@admin_required
def new_salesman():
    if request.method == 'POST':
        salesman = Salesman(
            name=request.form['name'],
            contact=request.form['contact'],
            email=request.form.get('email', ''),
            address=request.form.get('address', '')
        )
        
        db.session.add(salesman)
        db.session.commit()
        
        flash('Salesman added successfully!', 'success')
        return redirect(url_for('salesmen'))
    
    return render_template('new_salesman.html')

@app.route('/salesmen/<int:salesman_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_salesman(salesman_id):
    salesman = Salesman.query.get_or_404(salesman_id)
    
    if request.method == 'POST':
        salesman.name = request.form['name']
        salesman.contact = request.form['contact']
        salesman.email = request.form.get('email', '')
        salesman.address = request.form.get('address', '')
        
        db.session.commit()
        flash('Salesman updated successfully!', 'success')
        return redirect(url_for('salesmen'))
    
    return render_template('edit_salesman.html', salesman=salesman)

# Customer Management Routes
@app.route('/customers')
@admin_required
def customers():
    customers = Customer.query.all()
    return render_template('customers.html', customers=customers)

@app.route('/customers/new', methods=['GET', 'POST'])
@admin_required
def new_customer():
    if request.method == 'POST':
        customer = Customer(
            name=request.form['name'],
            contact=request.form['contact'],
            email=request.form.get('email', ''),
            address=request.form.get('address', ''),
            company_name=request.form.get('company_name', ''),
            gst_number=request.form.get('gst_number', ''),
            credit_limit=float(request.form.get('credit_limit', 0))
        )
        
        db.session.add(customer)
        db.session.commit()
        
        flash('Customer added successfully!', 'success')
        return redirect(url_for('customers'))
    
    return render_template('new_customer.html')

@app.route('/customers/<int:customer_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    
    if request.method == 'POST':
        customer.name = request.form['name']
        customer.contact = request.form['contact']
        customer.email = request.form.get('email', '')
        customer.address = request.form.get('address', '')
        customer.company_name = request.form.get('company_name', '')
        customer.gst_number = request.form.get('gst_number', '')
        customer.credit_limit = float(request.form.get('credit_limit', 0))
        
        db.session.commit()
        flash('Customer updated successfully!', 'success')
        return redirect(url_for('customers'))
    
    return render_template('edit_customer.html', customer=customer)

# User Management Routes
@app.route('/users')
@admin_required
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/new', methods=['GET', 'POST'])
@admin_required
def new_user():
    if request.method == 'POST':
        user = User(
            username=request.form['username'],
            email=request.form['email'],
            role=request.form['role']
        )
        user.set_password(request.form['password'])
        
        db.session.add(user)
        db.session.commit()
        
        flash('User added successfully!', 'success')
        return redirect(url_for('users'))
    
    return render_template('new_user.html')

# Export Routes
@app.route('/export/pdf')
@login_required
def export_pdf():
    salesman_filter = request.args.get('salesman', type=int)
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    
    query = Invoice.query
    
    if salesman_filter:
        query = query.filter(Invoice.salesman_id == salesman_filter)
    
    if date_from:
        query = query.filter(Invoice.delivery_date >= datetime.strptime(date_from, '%Y-%m-%d').date())
    
    if date_to:
        query = query.filter(Invoice.delivery_date <= datetime.strptime(date_to, '%Y-%m-%d').date())
    
    invoices = query.order_by(Invoice.delivery_date.desc()).all()
    
    # Create PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    title = Paragraph("Credit Management Report - Skanda Enterprises", title_style)
    
    # Report details
    report_date = datetime.now().strftime("%B %d, %Y")
    report_info = Paragraph(f"Generated on: {report_date}", styles['Normal'])
    
    # Summary statistics
    total_invoices = len(invoices)
    total_amount = sum(invoice.bill_amount for invoice in invoices)
    total_collected = sum(invoice.total_credits for invoice in invoices)
    collection_rate = (total_collected / total_amount * 100) if total_amount > 0 else 0
    
    summary_data = [
        ['Total Invoices', str(total_invoices)],
        ['Total Amount', f'₹{total_amount:,.2f}'],
        ['Total Collected', f'₹{total_collected:,.2f}'],
        ['Collection Rate', f'{collection_rate:.1f}%']
    ]
    
    summary_table = Table(summary_data, colWidths=[2*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    # Invoice details table
    if invoices:
        invoice_data = [['Invoice #', 'Customer', 'Salesman', 'Date', 'Amount', 'Collected', 'Outstanding', 'Status']]
        
        for invoice in invoices:
            customer_name = invoice.customer.name if invoice.customer else 'N/A'
            status = 'Paid' if invoice.is_paid else 'Pending'
            invoice_data.append([
                invoice.invoice_number,
                customer_name,
                invoice.salesman.name,
                invoice.delivery_date.strftime('%Y-%m-%d'),
                f'₹{invoice.bill_amount:,.2f}',
                f'₹{invoice.total_credits:,.2f}',
                f'₹{invoice.outstanding_balance:,.2f}',
                status
            ])
        
        invoice_table = Table(invoice_data, colWidths=[1*inch, 1.2*inch, 1*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.6*inch])
        invoice_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
    else:
        invoice_table = Paragraph("No invoices found for the selected criteria.", styles['Normal'])
    
    # Build PDF
    elements = [title, Spacer(1, 20), report_info, Spacer(1, 20), 
                Paragraph("Summary", styles['Heading2']), summary_table, Spacer(1, 20),
                Paragraph("Invoice Details", styles['Heading2']), invoice_table]
    
    doc.build(elements)
    
    buffer.seek(0)
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=credit_report_{datetime.now().strftime("%Y%m%d")}.pdf'
    
    return response

@app.route('/export/excel')
@login_required
def export_excel():
    salesman_filter = request.args.get('salesman', type=int)
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    
    query = Invoice.query
    
    if salesman_filter:
        query = query.filter(Invoice.salesman_id == salesman_filter)
    
    if date_from:
        query = query.filter(Invoice.delivery_date >= datetime.strptime(date_from, '%Y-%m-%d').date())
    
    if date_to:
        query = query.filter(Invoice.delivery_date <= datetime.strptime(date_to, '%Y-%m-%d').date())
    
    invoices = query.order_by(Invoice.delivery_date.desc()).all()
    
    # Create Excel file
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Credit Report"
    
    # Headers
    headers = ['Invoice #', 'Customer', 'Salesman', 'Date', 'Amount', 'Collected', 'Outstanding', 'Status']
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = Font(bold=True)
        cell.fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        cell.alignment = Alignment(horizontal="center")
    
    # Data
    for row, invoice in enumerate(invoices, 2):
        customer_name = invoice.customer.name if invoice.customer else 'N/A'
        status = 'Paid' if invoice.is_paid else 'Pending'
        
        ws.cell(row=row, column=1, value=invoice.invoice_number)
        ws.cell(row=row, column=2, value=customer_name)
        ws.cell(row=row, column=3, value=invoice.salesman.name)
        ws.cell(row=row, column=4, value=invoice.delivery_date.strftime('%Y-%m-%d'))
        ws.cell(row=row, column=5, value=invoice.bill_amount)
        ws.cell(row=row, column=6, value=invoice.total_credits)
        ws.cell(row=row, column=7, value=invoice.outstanding_balance)
        ws.cell(row=row, column=8, value=status)
    
    # Auto-adjust column widths
    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = min(max_length + 2, 20)
        ws.column_dimensions[column_letter].width = adjusted_width
    
    # Save to buffer
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response.headers['Content-Disposition'] = f'attachment; filename=credit_report_{datetime.now().strftime("%Y%m%d")}.xlsx'
    
    return response

@app.route('/reports')
@login_required
def reports():
    salesman_filter = request.args.get('salesman', type=int)
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    
    query = Invoice.query
    
    if salesman_filter:
        query = query.filter(Invoice.salesman_id == salesman_filter)
    
    if date_from:
        query = query.filter(Invoice.delivery_date >= datetime.strptime(date_from, '%Y-%m-%d').date())
    
    if date_to:
        query = query.filter(Invoice.delivery_date <= datetime.strptime(date_to, '%Y-%m-%d').date())
    
    invoices = query.order_by(Invoice.delivery_date.desc()).all()
    salesmen = Salesman.query.all()
    
    # Calculate collection rate for filtered data
    total_bill_amount = sum(invoice.bill_amount for invoice in invoices)
    total_collected = sum(invoice.total_credits for invoice in invoices)
    collection_rate = (total_collected / total_bill_amount * 100) if total_bill_amount > 0 else 0
    
    return render_template('reports.html', 
                         invoices=invoices, 
                         salesmen=salesmen,
                         total_bill_amount=total_bill_amount,
                         total_collected=total_collected,
                         collection_rate=collection_rate)

# Initialize database
def create_tables():
    db.create_all()
    
    # Create default admin user if none exists
    if not User.query.filter_by(role='admin').first():
        admin = User(username='admin', email='admin@skanda.com', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Default admin user created: username='admin', password='admin123'")

# Initialize database
def init_db():
    with app.app_context():
        create_tables()

# For Vercel deployment
if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5001)
else:
    # Initialize database when running on Vercel
    try:
        init_db()
    except Exception as e:
        print(f"Database initialization error: {e}")
        # Continue anyway, database might already exist
