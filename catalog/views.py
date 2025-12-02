from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Course, Enrollment

def home(request):
    return render(request, "home.html")

def index(request):
    return render(request, "index.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "login.html", {"error": "帳號或密碼錯誤"})
    return render(request, "login.html")

def course_detail(request, course_id):
    course = Course.objects.get(id=course_id)
    enrollments = Enrollment.objects.filter(course=course)
    return render(request, "course_detail.html", {
        "course": course,
        "enrollments": enrollments
    })
