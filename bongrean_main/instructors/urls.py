from django.urls import path
from . import views

urlpatterns = [
    path('instructors/', views.instructors, name='instructors'),
]