# locallibrary/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from catalog import views   

urlpatterns = [
    # Django admin
    #path('admin/', admin.site.urls),

    # 首頁
    path('', views.home, name='home'),

    # 登入相關
    path('student/login/', views.student_login, name='student_login'),
    path('staff/login/', views.staff_login, name='staff_login'),
    path('login/', views.login_view, name='login'),

    # 註冊
    path('register/', views.register, name='register'),

    #登出
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),

    # 學生首頁與操作
    #path('index/', views.index, name='index'),
    path('enroll_ops/', views.enroll_ops, name='enroll_ops'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),

    # 課程與留言
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    #修改留言
    path("comment/<int:comment_id>/delete/", views.delete_comment, name="delete_comment"),
    path("comment/<int:comment_id>/edit/", views.edit_comment, name="edit_comment"),
    
    # 老師首頁與課程管理
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/course/<int:course_id>/', views.teacher_course_detail, name='teacher_course_detail'),
    path('teacher/course/<int:course_id>/students/', views.teacher_course_students, name='teacher_course_students'),

    # 分數詳細（佔位）
    path('scores/<int:score_id>/', views.score_detail, name='score_detail'),
]

# 靜態檔案 + Media 支援（頭像上傳等）
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
