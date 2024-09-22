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

@register.filter
def split_duration(value):
    """Convert a timedelta to a tuple of (minutes, seconds)."""
    total_seconds = int(value.total_seconds())
    minutes, seconds = divmod(total_seconds, 60)
    return minutes, seconds
