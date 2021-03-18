from django.db import models
from admins.models import Branch


class Student(models.Model):
     gender_choices=(('M','Male'),('F','Female'),('O','Other'),)
     # branch_choices=(('CE','Computer Engineering'),
     #                   ('IT','Information Technology'),
     #                   ('EC','Electronics and Comm. Engineering'),
     #                   ('BME','Bio-Medical Engineering'),
     #                   ('MC','Mechantronics Engineering'),
     #                   ('ME','Mechanical Engineering'),
     #                   ('CE','Civil Engineering'),
     #                   ('EE','Electrical Engineering'),
     #                   ('ME','Marine Engineering'),
     #                   ('AE','Automobile Engineering'),
     #                   ('PE','Petrochemical Engineering'))
     
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
     branch_choices=(('CE','Computer Engineering'),
                       ('IT','Information Technology'),
                       ('EC','Electronics and Comm. Engineering'),
                       ('BME','Bio-Medical Engineering'),
                       ('MC','Mechantronics Engineering'),
                       ('ME','Mechanical Engineering'),
                       ('CE','Civil Engineering'),
                       ('EE','Electrical Engineering'),
                       ('ME','Marine Engineering'),
                       ('AE','Automobile Engineering'),
                       ('PE','Petrochemical Engineering'))

     sem_choices=(('1','I'),
                    ('2','II'),
                    ('3','III'),
                    ('4','IV'),
                    ('5','V'),
                    ('6','VI'),
                    ('7','VII'),
                    ('8','VIII'))
     exam_choices=(('Internal-1','I1'),
                    ('Internal-2','I2'),
                    ('Internal','I'))

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
     


