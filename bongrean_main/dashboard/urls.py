from django.urls import path
from . import views

urlpatterns = [
    path('course-update/<int:course_id>/', views.update_course, name="update_course"),
    path('course-create/<int:user_id>/', views.create_course, name='course_create'), 
    path('course-delete/<int:course_id>/', views.course_delete, name='course_delete'),
    path('course-edit-detail/<int:course_id>/', views.course_edit_detail, name='course_edit_detail'),
    path('profile/content/<int:user_id>/', views.user_content, name='user_content'),
    path('update_lesson/<int:lesson_id>/', views.lesson_update, name="update_lesson"),

    # content
    path('upload-video/<int:course_id>/', views.create_upload_video, name='upload_video'),

]