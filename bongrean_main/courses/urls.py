from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    # used
    path('courses/', views.home, name='courses'),  # Changed name to 'home' for clarity
    path('course-details/<int:course_id>/', views.course_details, name='course_details'),
    path('course-list-all/', views.course_list_all, name='course_list_all'), 

    path('create-comment/<int:lesson_id>/', views.create_comment, name='create_comment'),
    
]