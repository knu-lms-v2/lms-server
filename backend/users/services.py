from .models import EncryptedToken
from .utils import encrypt_token

def save_user_token(token):
    encrypted = encrypt_token(token)
    if not EncryptedToken.objects.filter(token=encrypted).exists():
        EncryptedToken.objects.create(token=encrypted)