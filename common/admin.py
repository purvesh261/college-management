from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Announcement)
admin.site.register(Course)
admin.site.register(CourseFaculty)