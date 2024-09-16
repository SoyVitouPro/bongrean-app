from django.shortcuts import render

# Create your views here.
def instructors(request):
    return render(request, 'instructors.html')
