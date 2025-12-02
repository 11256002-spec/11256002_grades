from django.db import models
from django.contrib.auth.models import User

# 學生帳號，連結到 Django 內建的 User
class StudentAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.student_id} - {self.user.username}"


# 學生基本資料
class Student(models.Model):
    name = models.CharField(max_length=50)
    student_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.name} ({self.student_id})"


# 課程
class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    teacher = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.code} - {self.name}"


# 修課紀錄
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    midterm_score = models.IntegerField(null=True, blank=True)
    final_score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.name} 修習 {self.course.name}"
