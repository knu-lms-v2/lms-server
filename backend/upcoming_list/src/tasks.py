from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from ..models import UpcomingData
from .update_upcoming_list import update_user_upcoming_list

@shared_task
def update_recent_users_data():
    seven_days_ago = timezone.now() - timedelta(days=7)
    recent_users = UpcomingData.objects.filter(last_accessed__gte=seven_days_ago).values_list('user_name', flat=True).distinct()
    for user_name in recent_users:
        update_user_upcoming_list(user_name)