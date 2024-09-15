from django.urls import path
from . import views
from .views import user_profile

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', user_profile, name='user_profile'),
]
