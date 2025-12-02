from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("index/", views.index, name="index"),
    path('login/', views.login_view, name='login'),
    path("register/", views.register, name="register"),
    path("scores/<int:score_id>/", views.score_detail, name="score_detail"),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
]
