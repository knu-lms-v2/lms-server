from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path('validate-token/', views.validate_token, name='validate_token'),  # 토큰 검증
    path('logout/', views.logout, name='logout'),  # 로그아웃
]