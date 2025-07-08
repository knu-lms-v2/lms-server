from .models import EncryptedToken
from .utils import encrypt_token

def save_user_token(token, user_name):
    """토큰을 해시화하여 중복 없이 저장"""
    encrypted = encrypt_token(token)
    if not EncryptedToken.objects.filter(token=encrypted, username=user_name).exists():
        EncryptedToken.objects.create(token=encrypted, username=user_name)

def get_user_token(user_name):
    pass