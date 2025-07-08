from django.db import models

class EncryptedToken(models.Model):
    """SHA256 해시된 토큰 저장 모델"""
    token = models.BinaryField(unique=True)
    username = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    