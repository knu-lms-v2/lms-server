import hashlib

def encrypt_token(token: str) -> bytes:
    return hashlib.sha256(token.encode()).digest()