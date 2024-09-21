from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.get_profile, name='api_user_profile'),  # Updated path for profile
]