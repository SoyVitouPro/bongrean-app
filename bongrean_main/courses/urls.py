from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='courses'),
    path('course-details/<int:course_id>/', views.course_details, name='course_details'),
]