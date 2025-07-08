from cryptography.fernet import Fernet
import os

FERNET_KEY = os.environ.get("FERNET_KEY")
cipher_suite = Fernet(FERNET_KEY)

if not FERNET_KEY:
    raise Exception("환경변수 FERNET_KEY가 설정되어 있지 않습니다.")

def encrypt_token(token: str) -> str:
    """토큰을 Fernet으로 암호화하여 문자열로 반환"""
    encrypted = cipher_suite.encrypt(token.encode())
    return encrypted.decode()

def decrypt_token(encrypted_token: str) -> str:
    """암호화된 토큰을 복호화해서 원본 토큰 반환"""
    decrypted = cipher_suite.decrypt(encrypt_token.encode())
    return decrypted.decode()