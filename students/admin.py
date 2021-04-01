from django.contrib import admin

# Register your models here.
from .models import Student, Result, Attendance

admin.site.register(Student)
admin.site.register(Result)
admin.site.register(Attendance)