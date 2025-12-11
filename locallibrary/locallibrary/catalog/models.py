from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Student(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=50, unique=True)      # 課名不可重複
    code = models.CharField(max_length=10, unique=True)      # 課號不可重複
    teacher = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    midterm_score = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    final_score = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:
        unique_together = ['student', 'course']      # 同一學生同一課不可重複

    @property
    def average(self):
        return (self.midterm_score + self.final_score) / 2

    def __str__(self):
        return f"{self.student.name}－{self.course.name} 修課紀錄"
