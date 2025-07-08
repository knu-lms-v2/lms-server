from .models import EncryptedToken
from .utils import encrypt_token

def save_user_token(token):
    """토큰을 해시화하여 중복 없이 저장"""
    encrypted = encrypt_token(token)
    if not EncryptedToken.objects.filter(token=encrypted).exists():
        EncryptedToken.objects.create(token=encrypted)

def get_user_token():
    pass