from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Course, Enrollment
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# 成績管理系統功能
def get_student():
    return Student.objects.first()

def index(request):
    student = get_student()
    student_id = student.id if student else None
    return render(request, 'index.html', {'student_id': student_id})

def score_main(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    enrollments = Enrollment.objects.filter(student=student)
    average = sum([e.average for e in enrollments]) / (enrollments.count() or 1)
    return render(request, 'score_main.html', {
        'student': student,
        'enrollments': enrollments,
        'average': average,
        'student_id': student_id,
    })

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrollments = Enrollment.objects.filter(course=course)
    student = get_student()
    return render(request, 'course_detail.html', {
        'course': course,
        'course_id': course.id,
        'enrollments': enrollments,
        'student_id': student.id if student else None,
    })

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'teacher']

def course_add(request):
    student = get_student()
    form = CourseForm(request.POST or None)
    msg = ""
    if request.method == 'POST' and form.is_valid():
        name = form.cleaned_data['name']
        code = form.cleaned_data['code']
        if Course.objects.filter(name=name).exists():
            msg = "課名已存在，不能重複！"
        elif Course.objects.filter(code=code).exists():
            msg = "課號已存在，不能重複！"
        else:
            form.save()
            return redirect('score_main', student_id=student.id)
    return render(request, 'course_add.html', {
        'form': form,
        'student_id': student.id if student else None,
        'msg': msg,
    })

class EnrollmentForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all())

def enroll_ops(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    enrolled_courses = Enrollment.objects.filter(student=student).values_list('course__id', flat=True)
    msg = ""
    if request.method == 'POST':
        if 'add_course' in request.POST:
            form = EnrollmentForm(request.POST)
            if form.is_valid():
                course = form.cleaned_data['course']
                if Enrollment.objects.filter(student=student, course=course).exists():
                    msg = "不能重複加選這門課程！"
                else:
                    Enrollment.objects.create(student=student, course=course, midterm_score=0, final_score=0)
                    return redirect('enroll_ops', student_id=student.id)
        elif 'drop_course' in request.POST:
            course_id = request.POST.get('drop_course')
            Enrollment.objects.filter(student=student, course_id=course_id).delete()
            return redirect('enroll_ops', student_id=student.id)
        else:
            form = EnrollmentForm()
    else:
        form = EnrollmentForm()
    addable_courses = Course.objects.exclude(id__in=enrolled_courses)
    form.fields['course'].queryset = addable_courses
    enrollments = Enrollment.objects.filter(student=student)
    return render(request, 'enroll_ops.html', {
        'student': student,
        'enrollments': enrollments,
        'form': form,
        'student_id': student.id,
        'msg': msg,
    })

# 用戶註冊
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "註冊成功！請登入。")
            return redirect('login')
        else:
            messages.error(request, "註冊失敗，請確認帳號及密碼格式。")
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# 用戶登入
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "帳號或密碼錯誤！")
    return render(request, 'login.html')

# 用戶登出
def logout_view(request):
    logout(request)
    messages.success(request, "已成功登出！")
    return redirect('login')
