
from django.conf import settings
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from courses.models import Category, Course, Instructor, Lesson
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from courses.models import Comment
from user.models import Profile


# Create your views here.
def home(request):
    # Retrieve all courses from the database
    courses = Course.objects.all()
    
    return render(request, 'course.html', {'courses': courses})


def create_comment(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        # Extract content and parent ID from the POST request
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')  # Optional, for replies
        print("parentID", parent_id)
        if content:  # Ensure the content is not empty
            parent = None

            # If this is a reply, find the parent comment
            if parent_id:
                parent = get_object_or_404(Comment, id=parent_id)

            # Create and save the comment
            comment = Comment.objects.create(
                user=request.user,
                content=content,
                course=course,
                parent=parent  # This will be None for root-level comments
            )

            # Redirect to the course details page after comment is added
            return redirect('course_details', course_id=course.id)

    # If not a POST request, redirect back to course details
    return redirect('course_details', course_id=course.id)



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
    # Fetch the specific course
    course = get_object_or_404(Course, id=course_id)

    # Fetch all lessons related to the course
    lessons = Lesson.objects.filter(course=course).values(
        'id', 'video_file', 'title', 'duration', 'views', 'created_at'
    )

    # Fetch the first instructor related to the course
    instructor = Instructor.objects.filter(course=course).first()
    course_thumbnail = course.thumbnail if instructor else None
    print(Comment.objects.filter(course_id=course_id))
    # Fetch comments related to the course
    comments = Comment.objects.filter(course=course).select_related('user__profile').values(
    'id',
    'user__username',
    'user__profile__profile_picture',
    'content',
    'created_at'
)


    context = {
        'courses': lessons,
        'course_id': course_id,
        'MEDIA_URL': settings.MEDIA_URL,
        'instructor_image': instructor.profile_pic if instructor else None,
        'instructor': instructor.bio if instructor else 'Unknown',
        'course_thumbnail': course_thumbnail,
        'video_range': range(1, 7),
        'comments': comments,  # Pass comments with profile pictures to the template
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








