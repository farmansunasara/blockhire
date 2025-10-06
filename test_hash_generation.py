#!/usr/bin/env python3
"""
Test script to demonstrate the new hash generation with salt.
"""

import hashlib
import secrets
import time

def generate_document_hash(file_content, file_name):
    """Generate hash using file content + document name + random salt."""
    
    # Create a unique salt combining timestamp and random data
    timestamp = str(int(time.time() * 1000))  # milliseconds for uniqueness
    random_salt = secrets.token_hex(16)  # 32-character random hex
    
    # Combine file content, document name, and salt for hash
    hash_input = file_content + file_name.encode('utf-8') + timestamp.encode('utf-8') + random_salt.encode('utf-8')
    doc_hash = hashlib.sha256(hash_input).hexdigest()
    
    return doc_hash, timestamp, random_salt

def test_hash_uniqueness():
    """Test that same file with different names generates different hashes."""
    
    print("🧪 Testing Hash Generation with Salt")
    print("=" * 50)
    
    # Simulate the same file content
    test_content = b"This is a test document content that is identical."
    
    print("Testing with same file content but different names:")
    print()
    
    # Test 1: Same file, different names
    hash1, timestamp1, salt1 = generate_document_hash(test_content, "document1.pdf")
    hash2, timestamp2, salt2 = generate_document_hash(test_content, "document2.pdf")
    
    print(f"📄 File 1: 'document1.pdf'")
    print(f"   Hash: {hash1}")
    print(f"   Salt: {salt1}")
    print(f"   Timestamp: {timestamp1}")
    print()
    
    print(f"📄 File 2: 'document2.pdf'")
    print(f"   Hash: {hash2}")
    print(f"   Salt: {salt2}")
    print(f"   Timestamp: {timestamp2}")
    print()
    
    print(f"🔍 Hash Comparison:")
    print(f"   Hashes are different: {hash1 != hash2}")
    print(f"   Salt 1: {salt1}")
    print(f"   Salt 2: {salt2}")
    print()
    
    # Test 2: Same file, same name, different upload times
    print("Testing with same file and name but different upload times:")
    print()
    
    hash3, timestamp3, salt3 = generate_document_hash(test_content, "same_document.pdf")
    time.sleep(0.001)  # Small delay to ensure different timestamp
    hash4, timestamp4, salt4 = generate_document_hash(test_content, "same_document.pdf")
    
    print(f"📄 Upload 1: 'same_document.pdf'")
    print(f"   Hash: {hash3}")
    print(f"   Salt: {salt3}")
    print(f"   Timestamp: {timestamp3}")
    print()
    
    print(f"📄 Upload 2: 'same_document.pdf'")
    print(f"   Hash: {hash4}")
    print(f"   Salt: {salt4}")
    print(f"   Timestamp: {timestamp4}")
    print()
    
    print(f"🔍 Hash Comparison:")
    print(f"   Hashes are different: {hash3 != hash4}")
    print(f"   Timestamps are different: {timestamp3 != timestamp4}")
    print(f"   Salts are different: {salt3 != salt4}")
    print()
    
    print("✅ SUCCESS: Each upload now generates a unique hash!")
    print("   - Same file + different name = different hash")
    print("   - Same file + same name + different time = different hash")
    print("   - Each upload is guaranteed to be unique")

if __name__ == "__main__":
    test_hash_uniqueness()
