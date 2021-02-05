from django.db import models
from datetime import datetime    



class Announcement(models.Model):
    title=models.CharField(max_length=100,
                            default='',
                            verbose_name="Title")
    description=models.CharField(max_length=100,
                            default='',
                            verbose_name="Description")
    account_id = models.CharField(max_length=20,
                            verbose_name="Account Id", default='')
    date = models.DateTimeField(default=datetime.now, blank=True)

class Course(model.Model):
    course_name = models.CharField(max_length=100, default='',
                            verbose_name="Course Name")
    
    subject_code = models.CharField(max_length=15,
                            verbose_name="Subject Code", primary_key=True)
    
    semester = models.CharField(max_length=2, default='',
                            verbose_name='Semester')

    branch = models.CharField(max_length=70, default='',
                            verbose_name='Branch')
    
    year = models.CharField(verbose_name="Year", default=datetime.now().year)

    ongoing = models.BooleanField(verbose_name="Ongoing", default=True)

    completed = models.BooleanField(verbose_name="Completed", default=False)
    
class CourseFaculty(model.Models):
    subject_code = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    faculty_name = models.CharField(max_length=100, default='', verbose_name='Faculty')


# Create your models here.
# class AppUser(models.Model):
#     categories = (('Student', 'Student'),
#                 ('Faculty','Faculty'),
#                 ('Staff','Staff'),
#                 ('Admin','Admin'),
#                 ('Head of Department','Head of Department'))

#     firstName = models.CharField(max_length=70,
#                      default='',
#                     verbose_name="First Name")

#     lastName = models.CharField(max_length=70,
#                     default='',
#                     verbose_name="Last Name")

#     username=models.CharField(max_length=70,
#                     verbose_name="Username",
#                     primary_key=True, unique=True)

#     passwd = models.CharField(max_length=70,
#                     verbose_name="Password")
    
#     email = models.EmailField(max_length=70,
#                     verbose_name="Email")

#     category = models.CharField(max_length=70,
#                     verbose_name="User Category",
#                     choices=categories)

#     isAdmin=models.BooleanField(max_length=10,
#                     default=False)

#     isPending = models.BooleanField(max_length=10,
#                     default=True)
