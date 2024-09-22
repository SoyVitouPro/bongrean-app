from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from courses.models import Course, Category, Instructor
from django.contrib.auth.decorators import login_required


def user_content(request):
    return render(request, 'content.html')


def course_edit_detail(request, course_id):
    categories = Category.objects.all()
    course = get_object_or_404(Course, id=course_id)  # Retrieve the course or return 404
    context = {'course': course,
               'categories':categories
               }  # Pass the course information to the template
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