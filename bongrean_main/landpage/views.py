from django.shortcuts import render
from django.http import HttpResponse
import os
from dotenv import load_dotenv # type: ignore

# Load environment variables
load_dotenv()

# Create your views here.
def home(request):
    db_name = os.getenv('DB_NAME')
    print(f"DB_NAME: {db_name}")
    
    return render(request, 'home.html')