from .models import EncryptedToken
from .utils import encrypt_token, decrypt_token

def save_user_token(token):
    encrypted = encrypt_token(token)
    EncryptedToken.objects.create(token=encrypted)

def get_user_token(user):
    encrypted = EncryptedToken.objects.latest('created_at').token
    return decrypt_token(encrypted)