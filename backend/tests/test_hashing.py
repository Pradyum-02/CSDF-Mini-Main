import pytest
import hashlib
from app.hashing import calculate_hashes

def test_calculate_hashes():
    """Test hash calculation correctness"""
    test_data = b"Hello, World!"
    hashes = calculate_hashes(test_data)

    # Verify MD5
    expected_md5 = hashlib.md5(test_data).hexdigest().lower()
    assert hashes['md5'] == expected_md5

    # Verify SHA-1
    expected_sha1 = hashlib.sha1(test_data).hexdigest().lower()
    assert hashes['sha1'] == expected_sha1

    # Verify SHA-256
    expected_sha256 = hashlib.sha256(test_data).hexdigest().lower()
    assert hashes['sha256'] == expected_sha256

def test_calculate_hashes_empty():
    """Test hash calculation with empty data"""
    test_data = b""
    hashes = calculate_hashes(test_data)

    expected_md5 = hashlib.md5(test_data).hexdigest().lower()
    expected_sha1 = hashlib.sha1(test_data).hexdigest().lower()
    expected_sha256 = hashlib.sha256(test_data).hexdigest().lower()

    assert hashes['md5'] == expected_md5
    assert hashes['sha1'] == expected_sha1
    assert hashes['sha256'] == expected_sha256