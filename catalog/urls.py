from django.urls import path
from . import views

urlpatterns = [
    # 首頁
    path("", views.home, name="home"),

    # 首頁按鈕用的兩個登入網址
    path("student/login/", views.student_login, name="student_login"),
    path("staff/login/", views.staff_login, name="staff_login"),

    # 登入後的學生首頁（成績總覽）
    path("index/", views.index, name="index"),

    # 學生加選 / 退選頁面
    path("enroll_ops/", views.enroll_ops, name="enroll_ops"),

    # 共用登入 / 註冊
    path("login/", views.login_view, name="login"),   # 先保留舊網址，以防別處用到
    path("register/", views.register, name="register"),

    # 其他原本頁面
    path("scores/<int:score_id>/", views.score_detail, name="score_detail"),
    path("course/<int:course_id>/", views.course_detail, name="course_detail"),

    # 老師相關頁面
    path("teacher/", views.teacher_dashboard, name="teacher_dashboard"),
    path(
        "teacher/course/<int:course_id>/",
        views.teacher_course_detail,
        name="teacher_course_detail",
    ),
]
