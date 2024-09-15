from django.shortcuts import render
from django.http import HttpResponse
import os
from dotenv import load_dotenv # type: ignore

# Load environment variables
load_dotenv()

# Create your views here.
def home(request):
    return render(request, 'home.html')