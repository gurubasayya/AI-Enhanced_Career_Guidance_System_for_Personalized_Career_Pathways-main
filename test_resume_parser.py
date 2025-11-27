#!/usr/bin/env python3
"""
Test script for resume parsing functionality
"""

import os
from app import extract_text_from_file, parse_resume_info

def test_resume_parsing():
    """Test resume parsing with sample files in uploads directory"""
    uploads_dir = "uploads"
    
    if not os.path.exists(uploads_dir):
        print("Uploads directory not found!")
        return
    
    # Get all files in uploads directory
    files = [f for f in os.listdir(uploads_dir) if f.lower().endswith(('.pdf', '.docx', '.doc', '.txt'))]
    
    if not files:
        print("No resume files found in uploads directory!")
        return
    
    print("Testing resume parsing functionality...\n")
    
    for filename in files[:3]:  # Test first 3 files
        file_path = os.path.join(uploads_dir, filename)
        print(f"Processing: {filename}")
        print("-" * 50)
        
        try:
            # Extract text
            text = extract_text_from_file(file_path)
            if text:
                print(f"Text extracted successfully ({len(text)} characters)")
                
                # Parse information
                info = parse_resume_info(text)
                
                print("Extracted Information:")
                for key, value in info.items():
                    if value:
                        print(f"  {key.title()}: {value}")
                
                print("\n" + "="*60 + "\n")
            else:
                print("No text extracted from file")
                
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
            print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    test_resume_parsing()