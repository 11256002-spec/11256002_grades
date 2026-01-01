from django.db import models
from django.contrib.auth.models import User


# ======================
# 帳號相關
# ======================

# 學生帳號：連到 Django 內建 User
class StudentAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.student_id} - {self.user.username}"


# 教職員帳號（老師）
class TeacherAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teacher_name = models.CharField(max_length=50)

    def __str__(self):
        return self.teacher_name


# ======================
# 個人資料（頭像＋姓名）
# ======================

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50, blank=True)  # 姓名可選填
    avatar = models.ImageField(
        upload_to='avatars/', blank=True, null=True,
        default='avatars/default.png'
    )

    def __str__(self):
        return self.full_name if self.full_name else self.user.username

    # 方便 template 直接取圖片 URL
    @property
    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        return '/media/avatars/default.png'


# ======================
# 學生 / 課程 / 修課
# ======================

class Student(models.Model):
    name = models.CharField(max_length=50)
    student_id = models.CharField(max_length=20, unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.student_id})"


class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    teacher_account = models.ForeignKey(
        TeacherAccount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses'
    )
    teacher = models.CharField(max_length=50, null=True, blank=True)  # 顯示用

    def __str__(self):
        return f"{self.code} - {self.name}"


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    midterm_score = models.IntegerField(null=True, blank=True)
    final_score = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ("student", "course")

    def __str__(self):
        return f"{self.student.name} 修習 {self.course.name}"

    @property
    def average(self):
        if self.midterm_score is None or self.final_score is None:
            return None
        return round((self.midterm_score + self.final_score) / 2, 1)


# ======================
# 課程留言系統
# ======================
class Comment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


# ======================
# （可保留）分數表
# ======================
class Score(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self):
        return f"{self.enrollment.student} - {self.value}"
