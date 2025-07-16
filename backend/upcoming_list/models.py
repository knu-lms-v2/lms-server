from django.db import models

# Create your models here.
class UpcomingData(models.Model):
    user_name = models.CharField(max_length=100) # 이름
    type = models.CharField(max_length=20) # 타입
    course_name = models.CharField(max_length=200) # 강의명
    week = models.CharField(max_length=50, null=True, blank=True) # 주차
    due_date = models.DateTimeField(null=True, blank=True) # 마감일
    created_at = models.DateTimeField(auto_now_add=True) # 등록일

    def __str__(self):
        return f"{self.user_name} - {self.course_name} - {self.week}"