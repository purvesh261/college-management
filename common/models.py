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
                            verbose_name="Account Id",
                            default='')

    date = models.DateTimeField(default=datetime.now,
                            blank=True)

class Course(models.Model):
    type_choice = (('Mandatory', 'Mandatory'),
                ('Elective', 'Elective'))

    course_id = models.CharField(max_length=20,
                            primary_key=True)

    course_name = models.CharField(max_length=100,
                            verbose_name="Course Name",
                            blank=False)
    
    subject_code = models.CharField(max_length=15,
                            verbose_name="Subject Code",
                            blank=False)
    
    description = models.TextField(max_length=300,
                            verbose_name='Description',
                            default = '')

    semester = models.CharField(max_length=2,
                            verbose_name='Semester')

    branch = models.CharField(max_length=70,
                            default='',
                            verbose_name='Branch')
    
    course_credits = models.CharField(max_length=3,
                            default=0,
                            verbose_name='Course Credits')
    
    course_type = models.CharField(max_length=20, 
                            choices=type_choice,
                            default='Mandatory')
    
    start_date = models.DateField(verbose_name="Start Date")

    end_date = models.DateField(verbose_name="End Date")

    active = models.BooleanField(verbose_name="Active",
                            default=True)

    completed = models.BooleanField(verbose_name="Completed",
                            default=False)
    
class CourseFaculty(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    faculty_id = models.CharField(max_length=30, default='', verbose_name='Faculty ID')



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
