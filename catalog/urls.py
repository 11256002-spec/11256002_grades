from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
]
