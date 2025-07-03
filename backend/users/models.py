from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class EncryptedToken(models.Model):
    token = models.BinaryField()
    created_at = models.DateTimeField(auto_now_add=True)
    