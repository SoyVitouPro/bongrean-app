from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from courses.models import Course, Category, Instructor, Lesson
from django.contrib.auth.decorators import login_required
from moviepy.editor import VideoFileClip
from django.core.files.storage import default_storage
import os
from datetime import timedelta  # Add this import


def user_content(request, user_id):
    course_by_user = Course.objects.filter(instructor__user_id=user_id).values('id', 'title', 'description', 'price', 'thumbnail') 
    print(course_by_user)
    return render(request, 'content.html', {'courses': course_by_user}) 

def create_upload_video(request, course_id):
    if request.method == 'POST':
        title = request.POST.get('title')
        video_file = request.FILES.get('video_file')  # Ensure this matches the form field name
        is_free = request.POST.get('is_free') == 'true'  # Convert string to boolean
        order = Lesson.objects.filter(course_id=course_id).count()
        if video_file:  # Check if video_file is provided
            # Save the uploaded video file to a temporary location
            video_path = default_storage.save(video_file.name, video_file)

            # Use a context manager to ensure the video file is properly closed
            with VideoFileClip(video_path) as video_clip:
                duration = video_clip.duration  # Get duration in seconds

                # Convert duration from seconds (float) to timedelta
                duration_timedelta = timedelta(seconds=duration)

                lesson = Lesson(course_id=course_id, title=title,order=order, video_file=video_file, duration=duration_timedelta, is_free=is_free)
                lesson.save()

            # Now it's safe to delete the temporary file
            os.remove(video_path)

            return JsonResponse({'success': True, 'message': 'Video uploaded successfully.'})
        
        return JsonResponse({'success': False, 'error': 'No video file provided.'}, status=400)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)



def course_edit_detail(request, course_id):
    categories = Category.objects.all()
    course = get_object_or_404(Course, id=course_id)  # Retrieve the course or return 404
    lessons = Lesson.objects.filter(course_id=course_id)  # Fetch lessons using course_id
    context = {
        'course': course,
        'categories': categories,
        'lessons': lessons  # Pass the lessons information to the template
    }
    return render(request, 'courses-edit-detail.html', context)

def course_delete(request, course_id):
    # Logic to delete a course
    course = get_object_or_404(Course, id=course_id)  # Retrieve the course or return 404
    if request.method == 'POST':
        course.delete()  # Delete the course
        return redirect('courses_admin')  # Redirect to the course list after deletion

@login_required
def create_course(request, user_id):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        level = request.POST.get('level')
        language = request.POST.get('language')
        certificate = request.POST.get('certificate') == 'true'  # Convert string to boolean
        thumbnail = request.FILES.get('thumbnail')
        category_id = request.POST.get('category')

        # Retrieve the instructor object by user_id
        instructor = Instructor.objects.filter(user_id=user_id).first()

        # Retrieve the category object by category_id
        category = Category.objects.filter(id=category_id).first()

        # Create the course object
        new_course = Course(
            title=title,
            description=description,
            instructor=instructor,
            price=price,
            certificate=certificate,
            level=level,
            language=language,
            thumbnail=thumbnail,
            category=category
        )
        new_course.save()
        return redirect('courses_admin')

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

# Create your views here.
@login_required
def update_course(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, id=course_id)
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        level = request.POST.get('level')
        language = request.POST.get('language')
        certificate = request.POST.get('certificate') == 'true'  # Convert string to boolean
        thumbnail = request.FILES.get('thumbnail')
        category_id = request.POST.get('category')

        # Update course fields
        course.title = title
        course.description = description
        course.price = price
        course.level = level
        course.language = language
        course.certificate = certificate
        if thumbnail:
            course.thumbnail = thumbnail
        if category_id:
            category = Category.objects.filter(id=category_id).first()
            course.category = category

        course.save()

        return JsonResponse({'success': True, 'message': 'Course updated successfully!'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)