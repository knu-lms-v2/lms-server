from django.db import models

# Create your models here.
class UpcomingData(models.Model):
    user_name = models.CharField(max_length=100)
    type = models.CharField(max_length=20)
    course_name = models.CharField(max_length=200)
    week = models.CharField(max_length=50)
    remaining_days = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_name} - {self.course_name} - {self.week}"