from moviepy.editor import VideoFileClip
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from courses.models import Category, Course, Instructor, Lesson
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
def home(request):
    # Retrieve all courses from the database
    courses = Course.objects.all()
    
    return render(request, 'course.html', {'courses': courses})




def course_details(request, course_id):
    courses = Lesson.objects.filter(course_id = course_id)
    
    context = {
        'course': courses,
        'video_range': range(1, 7)  # Pass the range to the template
    }
    
    return render(request, 'course-details.html', context)


def course_list_all(request):
    # Logic to list all courses
    courses = Course.objects.all()  # Retrieve all courses from the database
    context = {'courses': courses}
    return render(request, 'course-list.html', context)


def course_list_by_id(request, course_id):
    # Logic to retrieve a course by its ID
    course = get_object_or_404(Course, id=course_id)  # Retrieve the course or return 404
    context = {'course': course}
    return render(request, 'course-detail.html', context)








