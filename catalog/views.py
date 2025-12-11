from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import (
    Course,
    Enrollment,
    Score,
    StudentAccount,
    Student,
    TeacherAccount,
)

# ========= 首頁與登入相關 =========

# 首頁：兩顆按鈕「學生」「教職員」
def home(request):
    print("=== HOME VIEW RENDERED ===")
    return render(request, "home.html")


# 學生登入
def student_login(request):
    return login_view(request, user_type="student")


# 教職員登入（老師 / 管理者）
def staff_login(request):
    return login_view(request, user_type="staff")


# 共用的登入處理函式
def login_view(request, user_type=None):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # 依入口分流：學生 → index，教職員 → teacher_dashboard
            if user_type == "staff":
                return redirect("teacher_dashboard")
            else:
                return redirect("index")
        else:
            return render(
                request,
                "login.html",
                {"error": "帳號或密碼錯誤", "user_type": user_type},
            )

    # GET：顯示登入頁
    return render(request, "login.html", {"user_type": user_type})


def register(request):
    """
    學生註冊帳號：
    - 建立 User
    - 建立 Student
    - 建立 StudentAccount（User ↔ 學號）
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        full_name = request.POST.get("full_name")
        student_id = request.POST.get("student_id")

        # 基本檢查
        if not (username and password and full_name and student_id):
            return render(
                request,
                "register.html",
                {"error": "請填寫所有欄位"},
            )

        # 帳號或學號是否已被使用
        if User.objects.filter(username=username).exists():
            return render(
                request,
                "register.html",
                {"error": "這個帳號已被使用，請換一個。"},
            )
        if Student.objects.filter(student_id=student_id).exists():
            return render(
                request,
                "register.html",
                {"error": "這個學號已經註冊過。"},
            )

        # 建立 User
        user = User.objects.create_user(username=username, password=password)

        # 建立 Student
        student = Student.objects.create(
            name=full_name,
            student_id=student_id,
        )

        # 建立 StudentAccount（用學號連結）
        StudentAccount.objects.create(
            user=user,
            student_id=student_id,
        )

        # 建好後導到學生登入頁
        return redirect("student_login")

    # GET：顯示註冊表單
    return render(request, "register.html")


# ========= 學生首頁（成績總覽） =========

@login_required
def index(request):
    """
    學生登入後的首頁：顯示基本資料、修課清單與成績與平均。
    目前假設登入的是學生；之後可再分流老師/學生。
    """
    user = request.user

    # 找對應的學生帳號 & 學生資料
    try:
        student_account = StudentAccount.objects.get(user=user)
        student = Student.objects.filter(
            student_id=student_account.student_id
        ).first()
    except StudentAccount.DoesNotExist:
        student_account = None
        student = None

    enrollments = []
    avg_score = None

    if student is not None:
        enrollments = Enrollment.objects.filter(student=student)

        # 計算學期平均（只算有成績的課）
        scores = [
            e.average
            for e in enrollments
            if e.average is not None
        ]
        if scores:
            avg_score = sum(scores) / len(scores)

    context = {
        "student_account": student_account,
        "student": student,
        "enrollments": enrollments,
        "avg_score": avg_score,
    }
    return render(request, "student_dashboard.html", context)


# ========= 學生加選 / 退選 =========

@login_required
def enroll_ops(request):
    """
    學生加選 / 退選課程頁：
    - 上半部：已選課程，可退選
    - 下半部：可選課程，可加選
    """
    user = request.user

    # 找出對應學生
    try:
        student_account = StudentAccount.objects.get(user=user)
        student = Student.objects.filter(
            student_id=student_account.student_id
        ).first()
    except StudentAccount.DoesNotExist:
        student_account = None
        student = None

    if student is None:
        # 沒學生資料，就只顯示提示訊息
        return render(request, "enroll_ops.html", {
            "student": None,
            "enrolled": [],
            "available": [],
        })

    if request.method == "POST":
        action = request.POST.get("action")
        course_id = request.POST.get("course_id")

        if action and course_id:
            course = get_object_or_404(Course, id=course_id)

            if action == "add":
                # 加選：如果尚未有這筆修課紀錄才新增
                Enrollment.objects.get_or_create(
                    student=student,
                    course=course,
                )
            elif action == "drop":
                # 退選：刪除這筆 Enrollment
                Enrollment.objects.filter(
                    student=student,
                    course=course,
                ).delete()

        # 操作完重新整理頁面，避免重複送出
        return redirect("enroll_ops")

    # GET：準備畫面要用的資料
    enrolled_qs = Enrollment.objects.filter(student=student).select_related("course")
    enrolled_courses = [e.course for e in enrolled_qs]

    # 可選課程 = 所有課程 - 已選課程
    available_qs = Course.objects.exclude(id__in=[c.id for c in enrolled_courses])

    context = {
        "student": student,
        "enrolled": enrolled_qs,
        "available": available_qs,
    }
    return render(request, "enroll_ops.html", context)


# ========= 其他原本頁面（先保留） =========

def score_detail(request, score_id):
    return render(request, "score_detail.html", {"score_id": score_id})


def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrollments = Enrollment.objects.filter(course=course)
    return render(
        request,
        "course_detail.html",
        {
            "course": course,
            "enrollments": enrollments,
        },
    )


# ========= 老師相關頁面 =========

@login_required
def teacher_dashboard(request):
    """
    老師首頁：列出這位老師所開的課程。
    需要 Course 有外鍵指到 TeacherAccount（teacher_account）。
    """
    teacher_account = get_object_or_404(TeacherAccount, user=request.user)
    courses = Course.objects.filter(teacher_account=teacher_account)

    return render(
        request,
        "teacher_dashboard.html",
        {
            "teacher": teacher_account,
            "courses": courses,
        },
    )


@login_required
def teacher_course_detail(request, course_id):
    """
    老師管理單一課程成績的頁面：
    - 顯示修課學生
    - 可以修改期中、期末成績
    """
    teacher_account = get_object_or_404(TeacherAccount, user=request.user)
    course = get_object_or_404(
        Course,
        id=course_id,
        teacher_account=teacher_account,
    )

    enrollments = (
        Enrollment.objects
        .filter(course=course)
        .select_related("student")
    )

    if request.method == "POST":
        # 根據表單更新分數
        for enrollment in enrollments:
            mid_key = f"mid_{enrollment.id}"
            final_key = f"final_{enrollment.id}"

            mid = request.POST.get(mid_key)
            final = request.POST.get(final_key)

            if mid is not None:
                enrollment.midterm_score = int(mid) if mid != "" else None
            if final is not None:
                enrollment.final_score = int(final) if final != "" else None

            enrollment.save()

        return redirect("teacher_course_detail", course_id=course.id)

    return render(
        request,
        "teacher_course_detail.html",
        {
            "course": course,
            "enrollments": enrollments,
        },
    )
