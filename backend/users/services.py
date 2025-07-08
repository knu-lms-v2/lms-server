from .models import EncryptedToken
from .utils import encrypt_token

def save_user_token(token, user_name):
    """토큰을 해시화하여 중복 없이 저장"""
    encrypted = encrypt_token(token)
    if not EncryptedToken.objects.filter(token=encrypted, username=user_name).exists():
        EncryptedToken.objects.create(token=encrypted, username=user_name)

def get_token_by_username(user_name):
    """user_name으로 토큰을 조회"""
    token_obj = EncryptedToken.objects.filter(username=user_name).order_by('-id').first()
    if token_obj:
        return token_obj.token
    return None