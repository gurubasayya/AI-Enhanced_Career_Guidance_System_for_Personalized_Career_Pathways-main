#!/usr/bin/env python3
"""
Installation script for resume parsing dependencies
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    """Install required packages for resume parsing"""
    print("Installing dependencies for resume parsing...")
    
    packages = [
        "pdfplumber==0.9.0",
        "python-docx==0.8.11", 
        "Pillow==10.0.1",
        "pytesseract==0.3.10",
        "Flask-WTF==1.1.1",
        "WTForms==3.0.1"
    ]
    
    failed_packages = []
    
    for package in packages:
        print(f"Installing {package}...")
        if install_package(package):
            print(f"✓ {package} installed successfully")
        else:
            print(f"✗ Failed to install {package}")
            failed_packages.append(package)
    
    if failed_packages:
        print(f"\nFailed to install: {', '.join(failed_packages)}")
        print("Please install them manually using: pip install <package_name>")
    else:
        print("\n✓ All dependencies installed successfully!")
        
    # Note about Tesseract OCR
    print("\nNote: For image processing (OCR), you also need to install Tesseract OCR:")
    print("- Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki")
    print("- macOS: brew install tesseract")
    print("- Linux: sudo apt-get install tesseract-ocr")

if __name__ == "__main__":
    main()