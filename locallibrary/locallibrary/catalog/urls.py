from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('scores/<int:student_id>/', views.score_main, name='score_main'),  
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('course/add/', views.course_add, name='course_add'),
    path('enroll/<int:student_id>/', views.enroll_ops, name='enroll_ops'),
]
