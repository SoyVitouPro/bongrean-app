from django import template
from courses.models import Course, Instructor

register = template.Library()

@register.simple_tag
def course_list_all_by_user(user_id):
    # Retrieve the instructor using the user_id
    instructor = Instructor.objects.filter(user_id=user_id).first()
    # Retrieve courses for the specific instructor
    courses = Course.objects.filter(instructor=instructor) if instructor else []
    return courses