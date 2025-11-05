from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, "home.html")

def resume(request):
    return render(request, "resume.html")
