import hashlib

def encrypt_token(token: str) -> bytes:
    """토큰을 SHA256 해시로 변환하여 반환"""
    return hashlib.sha256(token.encode()).digest()