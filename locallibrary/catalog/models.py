from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Student(models.Model):
<<<<<<< HEAD
    name = models.CharField('姓名', max_length=20)      
=======
    name = models.CharField(max_length=20)
>>>>>>> c911ab5d0de40ec29bfb2df60f9f3f2b68eb70f8

    def __str__(self):
        return self.name

<<<<<<< HEAD
    class Meta:
        verbose_name = '學生'                           
        verbose_name_plural = '學生'

class Course(models.Model):
    name = models.CharField('課程名稱', max_length=50, unique=True)      
    code = models.CharField('課程代碼', max_length=10, unique=True)      
    teacher = models.CharField('授課教師', max_length=20)               
=======
class Course(models.Model):
    name = models.CharField(max_length=50, unique=True)      # 課名不可重複
    code = models.CharField(max_length=10, unique=True)      # 課號不可重複
    teacher = models.CharField(max_length=20)
>>>>>>> c911ab5d0de40ec29bfb2df60f9f3f2b68eb70f8

    def __str__(self):
        return self.name

<<<<<<< HEAD
    class Meta:
        verbose_name = '課程'
        verbose_name_plural = '課程'

class Enrollment(models.Model):
    student = models.ForeignKey(Student, verbose_name='學生', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name='課程', on_delete=models.CASCADE)
    midterm_score = models.PositiveIntegerField('期中考分數',
        validators=[MinValueValidator(0), MaxValueValidator(100)])
    final_score = models.PositiveIntegerField('期末考分數',
        validators=[MinValueValidator(0), MaxValueValidator(100)])

    class Meta:
        unique_together = ['student', 'course']
        verbose_name = '修課紀錄'
        verbose_name_plural = '修課紀錄'
=======
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
>>>>>>> c911ab5d0de40ec29bfb2df60f9f3f2b68eb70f8

    @property
    def average(self):
        return (self.midterm_score + self.final_score) / 2

    def __str__(self):
<<<<<<< HEAD
        return f"{self.student.name} 在 {self.course.name} 修課紀錄"
=======
        return f"{self.student.name}－{self.course.name} 修課紀錄"
>>>>>>> c911ab5d0de40ec29bfb2df60f9f3f2b68eb70f8
