from django.contrib import admin
from .models import UpcomingData

# Register your models here.
@admin.register(UpcomingData)
class UpcomingDataAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'type', 'course_name', 'week', 'due_date', 'created_at']
    search_fields = ['user_name', 'courese_name']