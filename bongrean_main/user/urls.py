from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/dashboard/', views.user_profile, name='user_profile'),
    
    path('profile/courses-admin/', views.courses_admin, name='courses_admin'),
]
