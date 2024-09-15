from django.shortcuts import render, redirect
from django.contrib.auth import logout
from allauth.socialaccount.models import SocialAccount
from .models import Profile

# Create your views here.
def login(request):
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('/')

def profile(request):
    user = request.user
    profile_picture_url = None

    if user.is_authenticated:
        try:
            social_account = SocialAccount.objects.get(user=user, provider='google')
            extra_data = social_account.extra_data
            profile_picture_url = extra_data.get('picture')
        except SocialAccount.DoesNotExist:
            # Fallback to profile picture from Profile model
            profile_picture_url = user.profile.profile_picture.url if user.profile.profile_picture else None

    return render(request, 'profile.html', {'profile_picture_url': profile_picture_url})
