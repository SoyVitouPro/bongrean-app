from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Course Model
class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_pic = models.ImageField(upload_to='static/instructor', null=True, blank=True)

    def __str__(self):
        return self.user.username


class Course(models.Model):
    LEVEL_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    thumbnail = models.ImageField(upload_to='static/thumbnials', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    language = models.CharField(max_length=50)
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES)
    certificate = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='static/videos/', null=True, blank=True)  # Ensure this matches the view
    duration = models.DurationField()
    order = models.PositiveIntegerField()
    is_free = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)  # Added date field with default to now

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class LessonRating(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='ratings', on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('lesson', 'student')

    def __str__(self):
        return f"{self.student.username} - {self.rating}"


class LessonComment(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='comments', on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.student.username} on {self.lesson.title}"


class LessonQnA(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='questions', on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField(null=True, blank=True)
    is_answered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    answered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Question by {self.student.username} on {self.lesson.title}"