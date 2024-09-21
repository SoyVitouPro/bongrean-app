from django.contrib import admin

# Register your models here.
from .models import Category
from .models import Instructor  # Assuming Instructor model is in instructors app
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Instructor)  # Registering the Instructor model
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_username', 'get_bio')  # Changed to use callable methods
    search_fields = ('user__username', 'bio')  # Adjust fields as necessary

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'  # Optional: set a short description for the column

    def get_bio(self, obj):
        return obj.bio
    get_bio.short_description = 'Bio'  # Optional: set a short description for the column
