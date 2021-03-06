from django.db import models
from staff.models import Staff
from datetime import datetime    
from .validators import validate_file_extension

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
                            default = '',
                            blank=True)

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

class Assignment(models.Model):
    assignment_id = models.CharField(max_length=20,
                            primary_key=True)

    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    start_date = models.DateField(verbose_name="Start Date", blank=True)

    end_date = models.DateField(verbose_name="End Date", blank=True, null=True)

    faculty = models.ForeignKey(Staff, on_delete=models.CASCADE)

    title = models.CharField(max_length=160, verbose_name="Title")

    description = models.TextField(max_length=300,
                            verbose_name='Description',
                            default = '',
                            blank=True)

    assignment_file = models.FileField(verbose_name="Assignment File", blank=True, upload_to='assignments', validators=[validate_file_extension])

class Submission(models.Model):
    submission_id = models.CharField(max_length=20, verbose_name="Submission ID",
                            primary_key=True)
    
    course = models.ForeignKey('Course', on_delete=models.CASCADE, verbose_name="Course")

    assignment = models.ForeignKey('Assignment', on_delete=models.CASCADE, verbose_name="Assignment")

    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, verbose_name="Student")

    submission_time = models.DateTimeField(default=datetime.now, verbose_name= "Submission Time")

    submission_file = models.FileField(verbose_name="Submission File", blank=True, upload_to="submissions", validators=[validate_file_extension])

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
