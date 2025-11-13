"""
Vendor OCR Matching Utilities
Uses RapidFuzz for fuzzy matching vendor names from OCR-extracted text
"""

try:
    from rapidfuzz import fuzz, process
    RAPIDFUZZ_AVAILABLE = True
except ImportError:
    RAPIDFUZZ_AVAILABLE = False

def match_vendor_from_ocr(extracted_text, vendors_list, threshold=80):
    """
    Match vendor name from OCR-extracted text using fuzzy matching
    
    Args:
        extracted_text: Text extracted from OCR
        vendors_list: List of Vendor objects or dicts with 'name' key
        threshold: Minimum similarity score (0-100)
    
    Returns:
        tuple: (matched_vendor, score, match_type) or (None, 0, 'no_match')
        match_type: 'exact', 'fuzzy', 'partial', 'no_match'
    """
    if not RAPIDFUZZ_AVAILABLE:
        # Fallback to simple string matching
        return simple_vendor_match(extracted_text, vendors_list, threshold)
    
    if not extracted_text or not vendors_list:
        return None, 0, 'no_match'
    
    # Extract vendor names
    vendor_names = []
    vendor_dict = {}
    
    for vendor in vendors_list:
        name = getattr(vendor, 'name', vendor.get('name', '')) if hasattr(vendor, 'name') else vendor.get('name', '')
        if name:
            vendor_names.append(name)
            vendor_dict[name] = vendor
    
    if not vendor_names:
        return None, 0, 'no_match'
    
    # Clean extracted text
    text_upper = extracted_text.upper()
    
    # Try to find vendor name in text
    # Look for common patterns: "Vendor:", "Supplier:", "From:", "To:"
    vendor_keywords = ['VENDOR', 'SUPPLIER', 'FROM', 'TO', 'COMPANY', 'STORE', 'SHOP']
    possible_vendor_texts = []
    
    lines = extracted_text.split('\n')
    for line in lines:
        line_upper = line.upper().strip()
        if not line_upper:
            continue
        
        # Check if line contains vendor keywords
        for keyword in vendor_keywords:
            if keyword in line_upper:
                # Extract text after keyword
                parts = line_upper.split(keyword, 1)
                if len(parts) > 1:
                    possible_text = parts[1].strip(' :\n\t').strip()
                    if possible_text:
                        possible_vendor_texts.append(possible_text)
        
        # Also check if line looks like a vendor name (not too long, has letters)
        if len(line.strip()) < 100 and len(line.strip()) > 2:
            if any(c.isalpha() for c in line):
                possible_vendor_texts.append(line.strip())
    
    # If no keywords found, use first few lines as possible vendor names
    if not possible_vendor_texts:
        for line in lines[:5]:  # Check first 5 lines
            line_clean = line.strip()
            if line_clean and len(line_clean) < 100 and len(line_clean) > 2:
                if any(c.isalpha() for c in line_clean):
                    possible_vendor_texts.append(line_clean)
    
    if not possible_vendor_texts:
        return None, 0, 'no_match'
    
    # Try fuzzy matching for each possible vendor text
    best_match = None
    best_score = 0
    best_text = None
    
    for possible_text in possible_vendor_texts:
        # Try exact match first
        if possible_text in vendor_names:
            matched_vendor = vendor_dict[possible_text]
            return matched_vendor, 100, 'exact'
        
        # Try fuzzy match
        try:
            result = process.extractOne(
                possible_text,
                vendor_names,
                scorer=fuzz.token_sort_ratio
            )
            
            if result:
                matched_name, score, _ = result
                if score > best_score:
                    best_score = score
                    best_match = vendor_dict[matched_name]
                    best_text = possible_text
        except Exception as e:
            print(f"Error in fuzzy matching: {e}")
            continue
    
    # Check if best match meets threshold
    if best_match and best_score >= threshold:
        match_type = 'fuzzy' if best_score < 100 else 'exact'
        return best_match, best_score, match_type
    
    # Try partial matching
    for possible_text in possible_vendor_texts:
        for vendor_name in vendor_names:
            if possible_text.lower() in vendor_name.lower() or vendor_name.lower() in possible_text.lower():
                score = fuzz.partial_ratio(possible_text, vendor_name)
                if score > best_score:
                    best_score = score
                    best_match = vendor_dict[vendor_name]
                    best_text = possible_text
    
    if best_match and best_score >= threshold:
        return best_match, best_score, 'partial'
    
    return None, best_score, 'no_match'


def simple_vendor_match(extracted_text, vendors_list, threshold=80):
    """Fallback simple string matching when RapidFuzz is not available"""
    if not extracted_text or not vendors_list:
        return None, 0, 'no_match'
    
    text_upper = extracted_text.upper()
    
    for vendor in vendors_list:
        name = getattr(vendor, 'name', vendor.get('name', '')) if hasattr(vendor, 'name') else vendor.get('name', '')
        if not name:
            continue
        
        name_upper = name.upper()
        
        # Exact match
        if name_upper in text_upper or text_upper in name_upper:
            return vendor, 100, 'exact'
        
        # Check if vendor name appears in text
        if name_upper in text_upper:
            return vendor, 90, 'partial'
    
    return None, 0, 'no_match'


def extract_vendor_name_from_text(text):
    """Extract vendor name from OCR text using patterns"""
    if not text:
        return None
    
    lines = text.split('\n')
    vendor_keywords = ['vendor', 'supplier', 'from', 'company', 'store', 'shop']
    
    for line in lines:
        line_lower = line.lower().strip()
        for keyword in vendor_keywords:
            if keyword in line_lower:
                # Extract text after keyword
                parts = line.split(keyword, 1)
                if len(parts) > 1:
                    vendor_name = parts[1].strip(' :\n\t').strip()
                    if vendor_name and len(vendor_name) > 2:
                        return vendor_name
    
    # Return first meaningful line
    for line in lines[:3]:
        line_clean = line.strip()
        if line_clean and len(line_clean) < 100 and len(line_clean) > 2:
            if any(c.isalpha() for c in line_clean):
                return line_clean
    
    return None

