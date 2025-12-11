from django.contrib import admin
from .models import StudentAccount, Student, TeacherAccount, Course, Enrollment


@admin.register(StudentAccount)
class StudentAccountAdmin(admin.ModelAdmin):
    list_display = ("student_id", "user")


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("student_id", "name")


@admin.register(TeacherAccount)
class TeacherAccountAdmin(admin.ModelAdmin):
    list_display = ("teacher_name", "user")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "teacher")


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "midterm_score", "final_score")
