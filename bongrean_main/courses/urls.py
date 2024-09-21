from django.urls import path
from . import views

urlpatterns = [
    # used
    path('courses/', views.home, name='courses'),  # Changed name to 'home' for clarity
    path('course-details/<int:course_id>/', views.course_details, name='course_details'),
    path('course-update/<int:course_id>/', views.update_course, name="update_course"),
    path('course-create/<int:user_id>/', views.create_course, name='course_create'), 
    path('course-delete/<int:course_id>/', views.course_delete, name='course_delete'),
    path('course-edit-detail/<int:course_id>/', views.course_edit_detail, name='course_edit_detail'),
    path('profile/content/', views.user_content, name='user_content'),
    # not use yet
    path('course-list-all/', views.course_list_all, name='course_list_all'), 
    
    path('course-list-by-id/<int:course_id>/', views.course_list_by_id, name='course_list_by_id'),  # Changed name for consistency
    path('course-list-all-by-category/<str:category>/', views.course_list_all_by_category, name='course_list_all_by_category'),  # Changed type to str for consistency
    
]