import hashlib

def calculate_hashes(file_data):
    """Calculate MD5, SHA-1, and SHA-256 hashes of file data"""
    hashes = {}

    # Calculate MD5
    md5_hash = hashlib.md5()
    md5_hash.update(file_data)
    hashes['md5'] = md5_hash.hexdigest().lower()

    # Calculate SHA-1
    sha1_hash = hashlib.sha1()
    sha1_hash.update(file_data)
    hashes['sha1'] = sha1_hash.hexdigest().lower()

    # Calculate SHA-256
    sha256_hash = hashlib.sha256()
    sha256_hash.update(file_data)
    hashes['sha256'] = sha256_hash.hexdigest().lower()

    return hashes