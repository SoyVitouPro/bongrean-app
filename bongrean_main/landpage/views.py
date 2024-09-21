from django.shortcuts import render
from django.http import HttpResponse
import os
from dotenv import load_dotenv # type: ignore
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from user.models import Profile  # Importing Profile from the user app


# Load environment variables
load_dotenv()

def home(request):
    return render(request, 'home.html') 


@login_required
def get_profile(request):
    return render(request, 'profile.html') 

