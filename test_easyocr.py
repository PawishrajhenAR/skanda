#!/usr/bin/env python3
"""
Quick test script to verify EasyOCR is working
Run this to test OCR without uploading through the web interface
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, extract_text_from_image

def test_ocr():
    """Test OCR with a sample image if available"""
    print("=" * 60)
    print("EasyOCR Test")
    print("=" * 60)
    
    # Check if any test images exist
    upload_dir = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    test_images = []
    
    if os.path.exists(upload_dir):
        for root, dirs, files in os.walk(upload_dir):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                    test_images.append(os.path.join(root, file))
                    break
            if test_images:
                break
    
    if not test_images:
        print("\n❌ No test images found in upload directory.")
        print("Upload a bill image first, then run this test.")
        print(f"Expected location: {upload_dir}")
        return
    
    test_image = test_images[0]
    print(f"\n📸 Testing with image: {os.path.basename(test_image)}")
    print("Processing... (this may take 1-3 minutes on first run)\n")
    
    try:
        text, confidence, error = extract_text_from_image(test_image)
        
        if error:
            print(f"❌ Error: {error}")
        elif text:
            print(f"✅ OCR Success!")
            print(f"📊 Confidence: {confidence:.1f}%")
            print(f"📝 Extracted Text ({len(text)} characters):")
            print("-" * 60)
            print(text[:500])  # Show first 500 chars
            if len(text) > 500:
                print("... (truncated)")
            print("-" * 60)
        else:
            print("⚠️ No text extracted (image may be blank or unclear)")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    with app.app_context():
        test_ocr()

