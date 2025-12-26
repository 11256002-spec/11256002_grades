from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import StudentRegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q

from .models import (
    Course,
    Enrollment,
    StudentAccount,
    Student,
    TeacherAccount,
    Profile,
    Comment,
)

# ========= 首頁 =========
def home(request):
    return render(request, "home.html")

# 登出後導回首頁
def logout_view(request): 
    logout(request) 
    return redirect("home") 

# ========= 登入相關 =========
def login_view(request, user_type=None):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # 判斷使用者類型導向
            if user_type == "staff":
                return redirect("teacher_dashboard")
            elif user_type == "student":
                return redirect("student_dashboard")
            else:
                return redirect("index")
        else:
            return render(request, "login.html", {
                "form": form,
                "error": "帳號或密碼錯誤",
                "user_type": user_type
            })
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form, "user_type": user_type})


# 包裝成不同入口
def student_login(request):
    return login_view(request, user_type="student")

def staff_login(request):
    return login_view(request, user_type="staff")


# ========= 學生註冊 =========
def register(request):
    if request.method == "POST":
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            full_name = form.cleaned_data['full_name']
            student_id = form.cleaned_data['student_id']

            # 檢查帳號是否存在
            if User.objects.filter(username=username).exists():
                return render(request, "register.html", {"form": form, "error": "帳號已存在"})

            # 檢查學號是否已註冊
            if Student.objects.filter(student_id=student_id).exists():
                return render(request, "register.html", {"form": form, "error": "學號已被註冊"})

            # 建立 User
            user = User.objects.create_user(username=username, password=password)

            # 建立 Student、StudentAccount、Profile
            Student.objects.create(name=full_name, student_id=student_id)
            StudentAccount.objects.create(user=user, student_id=student_id)
            Profile.objects.create(user=user, full_name=full_name)

            # ✅ 註冊完成後自動登入 
            login(request, user)

            return redirect("student_login")
    else:
        form = StudentRegisterForm()

    return render(request, "register.html", {"form": form})

# ========= 學生首頁 =========
@login_required
def index(request):
    student = None
    enrollments = []
    avg_score = None

    try:
        student_account = StudentAccount.objects.get(user=request.user)
        student = Student.objects.get(student_id=student_account.student_id)
        enrollments = Enrollment.objects.filter(student=student)

        scores = [e.average for e in enrollments if e.average is not None]
        if scores:
            avg_score = round(sum(scores) / len(scores), 1)

    except StudentAccount.DoesNotExist:
        pass

    return render(request, "student_dashboard.html", {
        "student": student,
        "enrollments": enrollments,
        "avg_score": avg_score,
    })

@login_required
def student_dashboard(request):
    student = None
    enrollments = []
    avg_score = None

    try:
        student_account = StudentAccount.objects.get(user=request.user)
        student = Student.objects.get(student_id=student_account.student_id)
        enrollments = Enrollment.objects.filter(student=student)

        scores = [e.average for e in enrollments if e.average is not None]
        if scores:
            avg_score = round(sum(scores) / len(scores), 1)

    except StudentAccount.DoesNotExist:
        pass

    return render(request, "student_dashboard.html", {
        "student": student,
        "enrollments": enrollments,
        "avg_score": avg_score,
    })

# ========= 加選 / 退選 =========
@login_required
def enroll_ops(request):
    try:
        student_account = StudentAccount.objects.get(user=request.user)
        student = Student.objects.get(student_id=student_account.student_id)
    except StudentAccount.DoesNotExist:
        return render(request, "enroll_ops.html", {
            "student": None,
            "enrolled": [],
            "available": [],
        })

    if request.method == "POST":
        action = request.POST.get("action")
        course_id = request.POST.get("course_id")
        course = get_object_or_404(Course, id=course_id)

        if action == "add":
            Enrollment.objects.get_or_create(student=student, course=course)
        elif action == "drop":
            Enrollment.objects.filter(student=student, course=course).delete()

        return redirect("enroll_ops")

    enrolled_qs = Enrollment.objects.filter(student=student).select_related("course")
    enrolled_courses = [e.course.id for e in enrolled_qs]
    available_qs = Course.objects.exclude(id__in=enrolled_courses)

    return render(request, "enroll_ops.html", {
        "student": student,
        "enrolled": enrolled_qs,
        "available": available_qs,
    })

# ========= 老師首頁 =========
@login_required
def teacher_dashboard(request):
    teacher = get_object_or_404(TeacherAccount, user=request.user)
    courses = Course.objects.filter(teacher_account=teacher)
    return render(request, "teacher_dashboard.html", {
        "teacher": teacher,
        "courses": courses,
    })

@login_required
def teacher_course_detail(request, course_id):
    teacher = get_object_or_404(TeacherAccount, user=request.user)
    course = get_object_or_404(Course, id=course_id, teacher_account=teacher)
    enrollments = Enrollment.objects.filter(course=course).select_related("student")

    # 查詢功能：GET 參數 query
    query = request.GET.get("query")
    if query:
        enrollments = enrollments.filter(
            Q(student__student_id__icontains=query) |
            Q(student__name__icontains=query)
        )

    # 成績更新：POST
    if request.method == "POST":
        for e in enrollments:
            mid = request.POST.get(f"mid_{e.id}")
            final = request.POST.get(f"final_{e.id}")
            e.midterm_score = int(mid) if mid else None
            e.final_score = int(final) if final else None
            e.save()
        return redirect("teacher_course_detail", course_id=course.id)

    # 頁面渲染
    return render(request, "teacher_course_detail.html", {
        "course": course,
        "enrollments": enrollments,
    })

    def teacher_course_students(request, course_id):
        teacher = get_object_or_404(TeacherAccount, user=request.user)
        course = get_object_or_404(Course, id=course_id, teacher_account=teacher)
        enrollments = Enrollment.objects.filter(course=course).select_related("student")

        return render(request, "teacher_course_students.html", {
            "course": course,
            "enrollments": enrollments,
        })






# ========= 佔位頁（防 URL 爆炸） =========
@login_required
def score_detail(request, score_id):
    return render(request, "score_detail.html", {"score_id": score_id})

@login_required
def course_detail(request, course_id):
    return render(request, "course_detail.html", {"course_id": course_id})

@login_required
def teacher_course_students(request, course_id):
    teacher = get_object_or_404(TeacherAccount, user=request.user)
    course = get_object_or_404(Course, id=course_id, teacher_account=teacher)
    enrollments = Enrollment.objects.filter(course=course).select_related("student")
    return render(request, "teacher_course_students.html", {
        "course": course,
        "enrollments": enrollments,
    })

# ========= 編輯個人資料 =========
@login_required
def edit_profile(request):
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)

    if request.method == "POST":
        username = request.POST.get("username")
        full_name = request.POST.get("full_name")
        avatar = request.FILES.get("avatar")

        if not username or not full_name:
            return render(request, "edit_profile.html", {"profile": profile, "error": "請填寫所有欄位"})

        # 更新 username
        if user.username != username:
            if User.objects.filter(username=username).exclude(pk=user.pk).exists():
                return render(request, "edit_profile.html", {"profile": profile, "error": "帳號已存在"})
            user.username = username
            user.save()

        # 更新 profile
        profile.full_name = full_name
        if avatar:
            profile.avatar = avatar
        profile.save()

        # 更新 Student name（如果有）
        try:
            student_account = StudentAccount.objects.get(user=user)
            student = Student.objects.get(student_id=student_account.student_id)
            student.name = full_name
            student.save()
        except StudentAccount.DoesNotExist:
            pass

        return render(request, "edit_profile.html", {"profile": profile, "success": "更新成功"})

    return render(request, "edit_profile.html", {"profile": profile})

# ========= 課程留言板 =========


#=========課程資訊=========
@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrollments = Enrollment.objects.filter(course=course)
    comments = Comment.objects.filter(course=course).order_by('-created_at')

    # 取得該名學生的成績（如果是學生登入）
    grade = None
    try:
        student_account = StudentAccount.objects.get(user=request.user)
        student = Student.objects.get(student_id=student_account.student_id)
        grade = Enrollment.objects.filter(course=course, student=student).first()
    except StudentAccount.DoesNotExist:
        pass

    # 處理留言送出
    if request.method == 'POST':
        content = request.POST.get('content')
        if content and len(content) <= 300:
            Comment.objects.create(course=course, user=request.user, content=content)
            return redirect(f"/catalog/course/{course_id}?tab=comments")


    return render(request, 'course_detail.html', {
        'course': course,
        'enrollments': enrollments,
        'comments': comments,
        'grade': grade,
    })



# ========= 編輯留言 =========
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    comment.delete()
    # 刪除後回到留言板
    return redirect(f"{request.META.get('HTTP_REFERER', '/')}?tab=comments")

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    if request.method == "POST":
        new_content = request.POST.get("content")
        if new_content:
            comment.content = new_content
            comment.save()
        return redirect(f"{request.META.get('HTTP_REFERER', '/')}?tab=comments")
    return render(request, "edit_comment.html", {"comment": comment})

