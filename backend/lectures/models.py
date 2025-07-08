from django.db import models

# Create your models here.
class LectureVideo(models.Model):
    title = models.CharField(max_length=100)
    course = models.CharField(max_length=30)
    due_at = models.DateTimeField()