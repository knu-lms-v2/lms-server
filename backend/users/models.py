from django.db import models

class EncryptedToken(models.Model):
    """SHA256 해시된 토큰 저장 모델"""
    token = models.CharField(max_length=512)
    username = models.CharField(max_length=150, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    