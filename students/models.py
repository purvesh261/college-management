from django.db import models
from common.models import Course
from admins.models import Branch
from staff.models import Staff
from datetime import datetime

class Student(models.Model):
     gender_choices=(('M','Male'),('F','Female'),('O','Other'),)
     
     branches = Branch.objects.values_list('branch_name','code')
     branch_choices = ((branch[1],branch[0]) for branch in branches)

     sem_choices=(('1','I'),
                    ('2','II'),
                    ('3','III'),
                    ('4','IV'),
                    ('5','V'),
                    ('6','VI'),
                    ('7','VII'),
                    ('8','VIII'))  

     categories = (
          ('Student','Student'),
          )            

     firstName = models.CharField(max_length=70,
                    default='',
                    verbose_name="First Name")

     middleName = models.CharField(max_length=70,
                    default='',
                    verbose_name="Middle Name",
                    blank=True)

     lastName = models.CharField(max_length=70,
                    default='',
                    verbose_name="Last Name")

     username=models.CharField(max_length=70,
                    verbose_name="Username")

     passwd = models.CharField(max_length=70,
                    verbose_name="Password")
     
     account_id = models.CharField(max_length=20,
                    verbose_name="Account Id", default='')
                    
     enrolment = models.CharField(max_length=70,
                    primary_key=True,
                    verbose_name="Enrolment Number")

     date = models.DateField(max_length=70,
                    verbose_name="Date of Birth")

     mobile=models.CharField(max_length=10,
               verbose_name="Mobile Number")

     branch=models.CharField(max_length=70,
                    verbose_name="Branch",
                    choices=branch_choices)

     sem=models.CharField(max_length=5,
                    verbose_name="Semester",
                    choices=sem_choices)

     email = models.EmailField(max_length=70,
                    verbose_name="Email")
     
     gender=models.CharField(max_length=7,
                    verbose_name="Gender",
                    choices=gender_choices)

     isPending = models.BooleanField(max_length=10,
                    default=True)
     
     category = models.CharField(max_length=70,
                    verbose_name="Category",
                    default="Student",
                    choices=categories)
               
class Result(models.Model):
     branches = Branch.objects.values_list('branch_name','code')
     branch_choices = ((branch[1],branch[0]) for branch in branches)
    
     sem_choices=(('1','I'),
                    ('2','II'),
                    ('3','III'),
                    ('4','IV'),
                    ('5','V'),
                    ('6','VI'),
                    ('7','VII'),
                    ('8','VIII'))
     exam_choices=(('Internal-1','Internal-1'),
                    ('Internal-2','Internal-2'),
                    ('Internal','Internal'))

     # courses = Course.objects.values_list('course_name')
     # courses_choices = ((course[0],course[0]) for course in courses) 

     # sub=Course.objects.values_list('subject_code')
     # subcode=((subject[0],subject[0]) for subject in sub)

     # courseid=Course.objects.values_list('course_id')

     account_id = models.CharField(max_length=20,
                    verbose_name="Account Id", default='', primary_key=True)
     branch=models.CharField(max_length=70,
                    verbose_name="Branch",
                    choices=branch_choices)
     sem=models.CharField(max_length=5,
                    verbose_name="Semester",
                    choices=sem_choices)
     course_id = models.CharField(max_length=20,default='')

     course_name = models.CharField(max_length=100,
                            verbose_name="Course Name",
                            blank=True)
    
     enrolment = models.CharField(max_length=70,
                    verbose_name="Enrolment Number")

     marks=models.CharField(max_length=5,
                            verbose_name="Marks",
                            blank=True)
     exam=models.CharField(max_length=25,
                            verbose_name="Exam Name",
                            choices=exam_choices)
     

class Attendance(models.Model):
     attendance_choices = (('P','Present'), ('A', 'Absent'))
     student = models.ForeignKey(Student, on_delete=models.CASCADE)
     course = models.ForeignKey(Course, on_delete=models.CASCADE)
     faculty = models.ForeignKey(Staff, on_delete=models.CASCADE)
     date = models.DateField(verbose_name="Date")
     status = models.CharField(max_length=10, verbose_name="Status", choices=attendance_choices)


class Doubt(models.Model):
     enrolment=models.CharField(max_length=70,
                    verbose_name="Enrolment Number")
     doubt=models.CharField(max_length=500,verbose_name='Doubt')
     answer=models.CharField(max_length=500,blank=True,verbose_name='Answer')
     course_id=models.CharField(max_length=20,blank=True)
