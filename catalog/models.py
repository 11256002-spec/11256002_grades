from django.db import models
from django.contrib.auth.models import User


# 學生帳號：連到 Django 內建 User，之後用來登入
class StudentAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.student_id} - {self.user.username}"


# 教職員帳號（老師）：一樣連到 User
class TeacherAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teacher_name = models.CharField(max_length=50)

    def __str__(self):
        return self.teacher_name


# 學生基本資料（之後也可以直接拿 StudentAccount 取代）
class Student(models.Model):
    name = models.CharField(max_length=50)
    student_id = models.CharField(max_length=20, unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.student_id})"


# 課程：連到老師帳號
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

# 修課紀錄：一筆代表「某學生選了某課」
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    midterm_score = models.IntegerField(null=True, blank=True)
    final_score = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ("student", "course")  # 同一學生同一課只會有一筆

    def __str__(self):
        return f"{self.student.name} 修習 {self.course.name}"

    @property
    def average(self):
        if self.midterm_score is None or self.final_score is None:
            return None
        return (self.midterm_score + self.final_score) / 2


# 如不特別需要額外分數表，可以先不用 Score 這個 model；
# 先保留但之後可能會拿掉
class Score(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self):
        return f"{self.enrollment.student} - {self.value}"
