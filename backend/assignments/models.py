from django.db import models

# Create your models here.
class Assignment(models.Model):
    title = models.CharField(max_length=100)
    course = models.CharField(max_length=30)
    dueAt = models.DateTimeField()