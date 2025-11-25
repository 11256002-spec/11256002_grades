from django.contrib import admin
<<<<<<< HEAD

admin.site.site_header = '成績管理系統'
admin.site.site_title = '成績管理系統'
admin.site.index_title = '歡迎使用成績管理後台'

from .models import Student, Course, Enrollment
=======
from .models import Student, Course, Enrollment

>>>>>>> c911ab5d0de40ec29bfb2df60f9f3f2b68eb70f8
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Enrollment)
