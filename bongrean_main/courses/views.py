from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from courses.models import Category, Course, Instructor
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def home(request):
    # Retrieve all courses from the database
    courses = Course.objects.all()
    
    return render(request, 'course.html', {'courses': courses})

def user_content(request):
    return render(request, 'content.html')


def course_details(request, course_id):
    # Create a sample course
    sample_course = {
        'id': course_id,
        'title': 'Introduction to Python Programming',
        'description': 'Learn the basics of Python programming language, including syntax, data types, control structures, and functions.',
        'instructor': 'John Doe',
        'instructor_image': 'https://149357281.v2.pressablecdn.com/wp-content/uploads/2023/12/Coursera-expands-AI-powered-translations-to-17-popular-languages-V2.png',  # Add path to instructor image
        'duration': '8 weeks',
        'price': 99.99,
        'level': 'Beginner',
        'language': 'English',
        'certificate': 'Yes',
        'video_hours': 10,
        'articles': 5,
        'downloadable_resources': 3,
        'sections': [
            {
                'title': 'Getting Started',
                'lessons': [
                    {'title': 'Introduction', 'duration': '5:00'},
                    {'title': 'Setup', 'duration': '10:00'}
                ]
            },
            {
                'title': 'Basic Concepts',
                'lessons': [
                    {'title': 'Variables', 'duration': '15:00'},
                    {'title': 'Data Types', 'duration': '20:00'}
                ]
            }
        ]
    }
    
    context = {
        'course': sample_course,
        'video_range': range(1, 7)  # Pass the range to the template
    }
    
    return render(request, 'course-details.html', context)


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

def course_list_all(request):
    # Logic to list all courses
    courses = Course.objects.all()  # Retrieve all courses from the database
    context = {'courses': courses}
    return render(request, 'course-list.html', context)

def course_edit_detail(request, course_id):
    categories = Category.objects.all()
    course = get_object_or_404(Course, id=course_id)  # Retrieve the course or return 404
    context = {'course': course,
               'categories':categories
               }  # Pass the course information to the template
    return render(request, 'courses-edit-detail.html', context)

def course_list_all_by_user(request):
    return render(request, 'courses-edit-detail.html')

def course_list_by_id(request, course_id):
    # Logic to retrieve a course by its ID
    course = get_object_or_404(Course, id=course_id)  # Retrieve the course or return 404
    context = {'course': course}
    return render(request, 'course-detail.html', context)

def course_list_all_by_category(request, category):
    # Logic to list courses by category
    category_courses = Course.objects.filter(category=category)  # Retrieve courses by category
    context = {'courses': category_courses}
    return render(request, 'course-list-by-category.html', context)

def course_delete(request, course_id):
    # Logic to delete a course
    course = get_object_or_404(Course, id=course_id)  # Retrieve the course or return 404
    if request.method == 'POST':
        course.delete()  # Delete the course
        return redirect('courses_admin')  # Redirect to the course list after deletion


