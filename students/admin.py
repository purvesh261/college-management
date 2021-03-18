from django.contrib import admin

# Register your models here.
from .models import Student
from .models import Result
admin.site.register(Student)
admin.site.register(Result)