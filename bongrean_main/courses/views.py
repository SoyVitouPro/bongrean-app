from django.shortcuts import render, get_object_or_404

# Create your views here.
def home(request):
    return render(request, 'course.html')

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

