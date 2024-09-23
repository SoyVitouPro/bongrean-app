
from django.conf import settings
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from courses.models import Category, Course, Instructor, Lesson
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from courses.models import Comment


# Create your views here.
def home(request):
    # Retrieve all courses from the database
    courses = Course.objects.all()
    
    return render(request, 'course.html', {'courses': courses})


# Create a new comment
def create_comment(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    
    if request.method == 'POST':
        # Extract the content from the POST request
        content = request.POST.get('content')
        
        if content:  # Basic validation to check if content is not empty
            # Create and save the comment
            comment = Comment.objects.create(
                lesson=lesson,
                user=request.user,
                content=content
            )
            # Redirect to course details page after comment is added
            return redirect('course_details', course_id=lesson.course.id)


# Update an existing comment
def update_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Check if the user is the author of the comment
    if comment.user != request.user:
        return HttpResponseForbidden('You are not allowed to edit this comment.')
    
    if request.method == 'POST':
        # Extract the updated content from the POST request
        content = request.POST.get('content')
        
        if content:  # Basic validation to check if content is not empty
            comment.content = content
            comment.save()
            return redirect('course_details', course_id=comment.lesson.course.id)


# Delete a comment
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Check if the user is the author of the comment
    if comment.user != request.user:
        return HttpResponseForbidden('You are not allowed to delete this comment.')
    
    if request.method == 'POST':
        comment.delete()
        return redirect('course_details', course_id=comment.lesson.course.id)



def course_details(request, course_id):
    course = Course.objects.get(id=course_id)  # Correct
    courses = Lesson.objects.filter(course=course).values('video_file', 'title', 'duration', 'views', 'created_at')  # Changed 'view' to 'views'
    instructor = Instructor.objects.filter(course=course).first()  # Get the first instructor for the course
    course_thumbnail = Course.objects.filter(instructor=instructor).values('thumbnail') if instructor else None  # Fetch course thumbnail with instructor id
    
    context = {
        'courses': courses,
        'MEDIA_URL': settings.MEDIA_URL,
        'instructor_image': instructor.profile_pic if instructor else None,  # Get profile_pic if instructor exists
        'instructor': instructor.bio if instructor else 'Unknown',  # Get instructor name if exists
        'course_thumbnail': course_thumbnail,  # Pass course thumbnail to the template
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








