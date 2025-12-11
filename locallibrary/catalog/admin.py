from django.contrib import admin

admin.site.site_header = '成績管理系統'
admin.site.site_title = '成績管理系統'
admin.site.index_title = '歡迎使用成績管理後台'

from .models import Student, Course, Enrollment
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Enrollment)
