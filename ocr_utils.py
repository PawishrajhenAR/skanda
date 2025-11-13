"""
OCR Utilities for Bill Processing
Contains functions for parsing bill data from OCR extracted text
"""

import re
from datetime import datetime
from typing import Dict, Optional, Tuple

def parse_bill_number(text: str) -> Optional[str]:
    """
    Extract bill number from OCR text
    Looks for patterns like: Bill No:, Invoice No:, Bill #, etc.
    """
    patterns = [
        r'bill\s*(?:number|no|#|num)[\s:]*([A-Z0-9\-/]+)',
        r'invoice\s*(?:number|no|#|num)[\s:]*([A-Z0-9\-/]+)',
        r'bill[\s:]+([A-Z0-9\-/]+)',
        r'invoice[\s:]+([A-Z0-9\-/]+)',
        r'no[\.\s:]+([A-Z0-9\-/]+)',
    ]
    
    text_lower = text.lower()
    for pattern in patterns:
        match = re.search(pattern, text_lower, re.IGNORECASE)
        if match:
            return match.group(1).strip().upper()
    
    # Try to find standalone bill numbers (alphanumeric with dashes/slashes)
    standalone = re.search(r'\b([A-Z]{1,5}[-/]?\d{2,10})\b', text, re.IGNORECASE)
    if standalone:
        return standalone.group(1).strip().upper()
    
    return None

def parse_amount(text: str) -> Optional[float]:
    """
    Extract total amount from OCR text
    Looks for patterns like: Total, Amount, Grand Total, etc.
    """
    # Remove commas for parsing
    text_clean = text.replace(',', '')
    
    # Common patterns for total amount
    patterns = [
        r'(?:total|amount|grand\s*total|payable|amount\s*due)[\s:]*[₹rs\.]*\s*(\d+\.?\d*)',
        r'[₹rs\.]*\s*(\d+\.?\d*)\s*(?:total|amount|grand\s*total|payable)',
        r'final\s*amount[\s:]*[₹rs\.]*\s*(\d+\.?\d*)',
    ]
    
    text_lower = text_clean.lower()
    amounts_found = []
    
    for pattern in patterns:
        matches = re.finditer(pattern, text_lower, re.IGNORECASE)
        for match in matches:
            try:
                amount = float(match.group(1))
                amounts_found.append(amount)
            except ValueError:
                continue
    
    # Also look for currency symbols followed by numbers
    currency_pattern = r'[₹$]?\s*(\d{1,10}(?:\.\d{2})?)'
    currency_matches = re.findall(currency_pattern, text_clean)
    for match in currency_matches:
        try:
            amount = float(match)
            if amount > 0:  # Only consider positive amounts
                amounts_found.append(amount)
        except ValueError:
            continue
    
    # Return the largest amount found (likely the total)
    if amounts_found:
        return max(amounts_found)
    
    return None

def parse_date(text: str) -> Optional[datetime.date]:
    """
    Extract date from OCR text
    Handles various date formats: DD/MM/YYYY, DD-MM-YYYY, YYYY-MM-DD, etc.
    """
    date_patterns = [
        r'(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})',  # DD/MM/YYYY or DD-MM-YYYY
        r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})',  # YYYY-MM-DD
        r'date[\s:]*(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})',
        r'(\d{1,2})\s+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\s+(\d{2,4})',  # DD Month YYYY
    ]
    
    month_names = {
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
        'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
    }
    
    for pattern in date_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            try:
                groups = match.groups()
                
                # Handle DD/MM/YYYY or DD-MM-YYYY
                if len(groups) == 3:
                    d, m, y = groups
                    day, month, year = int(d), int(m), int(y)
                    
                    # Adjust 2-digit years (assuming 2000-2099)
                    if year < 100:
                        year += 2000
                    
                    return datetime(year, month, day).date()
                    
            except (ValueError, TypeError) as e:
                continue
    
    return None

def parse_vendor_name(text: str, existing_vendors=None) -> Optional[str]:
    """
    Extract vendor name from OCR text
    Looks for company names, business names in the header/first lines
    """
    lines = text.split('\n')
    
    # First few lines usually contain vendor name
    for i, line in enumerate(lines[:10]):  # Check first 10 lines
        line_clean = line.strip()
        
        # Skip common headers
        if any(skip in line_clean.lower() for skip in ['bill', 'invoice', 'tax', 'gst', 'date', 'amount']):
            continue
        
        # Look for company indicators
        if any(indicator in line_clean for indicator in ['Ltd', 'Limited', 'Pvt', 'Pvt.', 'Corp', 'Corporation', 'Inc']):
            return line_clean
        
        # If line is substantial (more than 5 chars) and looks like a name
        if len(line_clean) > 5 and not re.match(r'^\d+', line_clean):
            # Check against existing vendors if provided
            if existing_vendors:
                for vendor in existing_vendors:
                    if vendor.name.lower() in line_clean.lower():
                        return vendor.name
            
            # Return first substantial line that looks like a name
            if re.match(r'^[A-Za-z\s&]+$', line_clean[:50]):
                return line_clean[:100]  # Limit to 100 chars
    
    return None

def parse_bill_data(text: str, existing_vendors=None) -> Dict:
    """
    Parse all bill data from OCR text
    Returns a dictionary with extracted fields
    """
    return {
        'bill_number': parse_bill_number(text),
        'amount': parse_amount(text),
        'date': parse_date(text),
        'vendor_name': parse_vendor_name(text, existing_vendors)
    }

def compare_bill_data(stored_data: Dict, ocr_data: Dict) -> Dict:
    """
    Compare stored bill data with re-extracted OCR data
    Returns comparison results with discrepancies
    """
    discrepancies = []
    
    # Compare bill number
    if stored_data.get('bill_number') and ocr_data.get('bill_number'):
        if stored_data['bill_number'] != ocr_data['bill_number']:
            discrepancies.append({
                'field': 'bill_number',
                'stored': stored_data['bill_number'],
                'ocr': ocr_data['bill_number']
            })
    
    # Compare amount (allow small differences due to rounding)
    if stored_data.get('amount') and ocr_data.get('amount'):
        diff = abs(stored_data['amount'] - ocr_data['amount'])
        if diff > 0.01:  # More than 1 paisa difference
            discrepancies.append({
                'field': 'amount',
                'stored': stored_data['amount'],
                'ocr': ocr_data['amount'],
                'difference': diff
            })
    
    # Compare date
    if stored_data.get('date') and ocr_data.get('date'):
        if stored_data['date'] != ocr_data['date']:
            discrepancies.append({
                'field': 'date',
                'stored': str(stored_data['date']),
                'ocr': str(ocr_data['date'])
            })
    
    return {
        'has_discrepancy': len(discrepancies) > 0,
        'discrepancies': discrepancies
    }

