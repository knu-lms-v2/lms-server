from django.urls import path
from . import views

app_name = "deadline_list"

urlpatterns = [
    path('view-item/', views.view_item, name='view_item'),
]