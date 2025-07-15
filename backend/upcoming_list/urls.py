from django.urls import path
from . import views

app_name = "deadline_list"

# localhost:8000/api/upcoming-list/
urlpatterns = [
    path('upcoming-events/', views.set_upcoming_data, name='set_upcoming_data'),
    path('upcoming-data/', views.get_upcoming_data, name='get_upcoming_data')
]