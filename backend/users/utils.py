import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv() # .env 파일에서 환경변수 읽기

def get_fernet():
    key = os.environ['FERNET_KEY']
    return Fernet(key)

def encrypt_token(token: str) -> bytes:
    f = get_fernet()
    return f.encrypt(token.encode())

def decrypt_token(token_encrypted: bytes) -> str:
    f = get_fernet()
    return f.decrypt(token_encrypted).decode()
