from django.shortcuts import render, redirect
from django.contrib.auth import logout

# Create your views here.
def login(request):
    return render(request, 'login.html')
# Create your views here.
def logout_view(request):
    logout(request)
    return redirect('/')

def profile(request):
    return render(request, 'profile.html')


# in your view, e.g., user/views.py
from allauth.socialaccount.models import SocialAccount

def profile(request):
    user = request.user
    profile_picture_url = None

    if user.is_authenticated:
        try:
            social_account = SocialAccount.objects.get(user=user, provider='google')
            extra_data = social_account.extra_data
            profile_picture_url = extra_data.get('picture')
        except SocialAccount.DoesNotExist:
            pass

    return render(request, 'profile.html', {'profile_picture_url': profile_picture_url})
