from .models import EncryptedToken
from .utils import encrypt_token, decrypt_token

def save_user_token(user, token):
    encrypted = encrypt_token(token)
    EncryptedToken.objects.update_or_create(user=user, defaults={'token': encrypted})

def get_user_token(user):
    encrypted = EncryptedToken.objects.get(user=user).token
    return decrypt_token(encrypted)