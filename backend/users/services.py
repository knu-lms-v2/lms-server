from .models import EncryptedToken
from .utils import decrypt_token, encrypt_token
from django.utils import timezone

def save_user_token(token, user_name) -> timezone:
    """토큰을 Fernet으로 암호화하여 중복 없이 저장"""
    now = timezone.now()
    encrypted = encrypt_token(token)
    EncryptedToken.objects.update_or_create(
        username=user_name,
        defaults={
            'token': encrypted,
            'last_login': now
        }
    )
    return now

def get_token_by_username(user_name):
    """user_name으로 토큰을 조회"""
    token_obj = EncryptedToken.objects.filter(username=user_name).order_by('-id').first()
    if token_obj:
        try:
            return decrypt_token(token_obj.token)
        except Exception as e:
            print(f"error: {e}")
            return None
