from django.shortcuts import render, redirect
from django.contrib.auth import logout

# Create your views here.
def login(request):
    return render(request, 'login.html')
# Create your views here.
def logout(request):
    logout(request)
    return redirect('/')