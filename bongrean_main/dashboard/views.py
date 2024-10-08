import subprocess
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from courses.models import Course, Category, Instructor, Lesson
from django.contrib.auth.decorators import login_required
from moviepy.editor import VideoFileClip # type: ignore
from django.core.files.storage import default_storage
import os
from datetime import timedelta  # Add this import


def user_content(request, user_id):
    course_by_user = Course.objects.filter(instructor__user_id=user_id).values('id', 'title', 'description', 'price', 'thumbnail') 
    print(course_by_user)
    return render(request, 'content.html', {'courses': course_by_user}) 


def lesson_delete(request, lesson_id):
    # Retrieve the lesson or return 404
    lesson = get_object_or_404(Lesson, id=lesson_id)
    
    if request.method == 'POST':
        # Get the course ID from the lesson's foreign key relationship
        course_id = lesson.course.id  # Assuming Lesson model has a ForeignKey to Course
        print(lesson.video_file)
        # Remove the video file from storage
        if lesson.video_file:  # Assuming 'video' is the field for the uploaded video file
            video_path = lesson.video_file.path  # Get the file path
            print(video_path)
            if os.path.exists(video_path):
                os.remove(video_path)  # Delete the file from storage

        lesson.delete()  # Delete the lesson
        return redirect('course_edit_detail', course_id=course_id)  # Redirect to course edit detail
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


def lesson_update(request, lesson_id):
    if request.method == 'POST':
        lesson = get_object_or_404(Lesson, id=lesson_id)  # Retrieve the lesson or return 404
        course = get_object_or_404(Course, id=lesson.course.id)  # Get the associated course

        # Get form data
        title = request.POST.get('title')
        new_order = int(request.POST.get('order'))  # Convert order to an integer
        is_free = request.POST.get('is_free') == 'true'  # Convert string 'true' to boolean

        # Update lesson fields
        lesson.title = title
        lesson.is_free = is_free
        
        # Check if the new order already exists for another lesson
        if lesson.order != new_order:
            existing_lesson = Lesson.objects.filter(order=new_order, course=course).exclude(id=lesson_id).first()

            if existing_lesson:
                # Swap orders if another lesson with the same order exists
                existing_lesson.order = lesson.order  # Swap the order
                existing_lesson.save()
        
        # Update the current lesson with the new order
        lesson.order = new_order
        lesson.save()

        # Redirect to the course edit detail page
        return redirect('course_edit_detail', course_id=course.id)

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)
    

def create_upload_video(request, course_id):
    if request.method == 'POST':
        title = request.POST.get('title')
        video_file = request.FILES.get('video_file')  # Ensure this matches the form field name
        print(video_file)
        is_free = request.POST.get('is_free') == 'true'  # Convert string to boolean
        order = Lesson.objects.filter(course_id=course_id).count()
        
        if video_file:  # Check if video_file is provided
            # Save the uploaded video file to a temporary location
            video_path = default_storage.save(video_file.name, video_file)
            full_video_path = os.path.join(settings.MEDIA_ROOT, video_path)  # Get full path

            # Use a context manager to ensure the video file is properly closed
            with VideoFileClip(full_video_path) as video_clip:
                duration = video_clip.duration  # Get duration in seconds

                # Convert duration from seconds (float) to timedelta
                duration_timedelta = timedelta(seconds=duration)

                lesson = Lesson(course_id=course_id, title=title, order=order, video_file=video_file, duration=duration_timedelta, is_free=is_free)
                lesson.save()

            # Now it's safe to delete the temporary file
            os.remove(full_video_path)

            return JsonResponse({'success': True, 'message': 'Video uploaded successfully.'})
        
        return JsonResponse({'success': False, 'error': 'No video file provided.'}, status=400)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)



def course_edit_detail(request, course_id):
    categories = Category.objects.all()
    course = get_object_or_404(Course, id=course_id)  # Retrieve the course or return 404
    lessons = course.lessons.all().order_by('order')  # Fetch lessons using course_id
    context = {
        'course': course,
        'categories': categories,
        'lessons': lessons,
    }
    return render(request, 'courses-edit-detail.html', context)

def course_delete(request, course_id):
    course = get_object_or_404(Course, id=course_id)  # Retrieve the course or return 404
    if request.method == 'POST':
        # Remove all lessons related to the course
        for lesson in course.lessons.all():  # Iterate over all lessons
            if lesson.video_file:  # Check if there's a video file
                video_path = lesson.video_file.path  # Get the file path
                if os.path.exists(video_path):
                    os.remove(video_path)  # Delete the file from storage
            lesson.delete()  # Delete the lesson

        # Remove the course thumbnail
        if course.thumbnail:  # Assuming 'thumbnail' is the field for the course image
            thumbnail_path = course.thumbnail.path  # Get the file path
            if os.path.exists(thumbnail_path):
                os.remove(thumbnail_path)  # Delete the thumbnail file

        course.delete()  # Delete the course
        return redirect('courses_admin')

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

@login_required
def create_course(request, user_id):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        level = request.POST.get('level')
        language = request.POST.get('language')
        certificate = request.POST.get('certificate') == 'true'  # Convert string to boolean
        thumbnail = request.FILES.get('thumbnail')  # Ensure this is handled correctly
        print("Files being saved:", thumbnail)
        category_id = request.POST.get('category')

        instructor = Instructor.objects.filter(user_id=user_id).first()
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
            # Remove the old thumbnail if it exists
            if course.thumbnail:
                default_storage.delete(course.thumbnail.path)
            course.thumbnail = thumbnail

        if category_id:
            category = Category.objects.filter(id=category_id).first()
            course.category = category

        course.save()

        return JsonResponse({'success': True, 'message': 'Course updated successfully!'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)