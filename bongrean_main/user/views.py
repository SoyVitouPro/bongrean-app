from django.shortcuts import render, redirect
from django.contrib.auth import logout
from allauth.socialaccount.models import SocialAccount
from .models import Profile
from courses.models import Category
from django.contrib.auth.decorators import login_required

@login_required
def user_profile(request):
    user = request.user
    profile_picture_url = None
    last_login = None
    email = None

    if user.is_authenticated:
        # Ensure the user has a profile
        profile, created = Profile.objects.get_or_create(user=user)

        # Get user information
        email = profile.email or user.email  # fallback to user's email if profile email is not set
        last_login = user.last_login  # User's last login time

        try:
            # Get social account profile picture (Google)
            social_account = SocialAccount.objects.get(user=user, provider='google')
            extra_data = social_account.extra_data
            profile_picture_url = extra_data.get('picture')
        except SocialAccount.DoesNotExist:
            # Fallback to profile picture from Profile model
            profile_picture_url = profile.profile_picture if profile.profile_picture else None

        # Save profile picture URL to Profile model if fetched
        if profile_picture_url:
            profile.profile_picture = profile_picture_url
            profile.save()

    # Pass the information to the template
    return render(request, 'profile.html', {
        'email': email,
        'last_login': last_login,
        'profile_picture_url': profile_picture_url,
        'full_name': user.get_full_name(),  # Get user's full name
    })

def login(request):
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('/')




def courses_admin(request):
    categories = Category.objects.all()  # Fetch all categories
    return render(request, 'courses-admin.html', {'categories': categories})  # Pass categories to the template
