from django.db import models
from admins.models import Branch

class Staff(models.Model):
     gender_choices=(('M','Male'),('F','Female'),('O','Other'),)
     # branch_choices=(('Computer Engineering','Computer Engineering'),
     #                   ('Information Technology','Information Technology'),
     #                   ('Electronics and Comm. Engineering','Electronics and Comm. Engineering'),
     #                   ('Bio-Medical Engineering','Bio-Medical Engineering'),
     #                   ('Mechantronics Engineering','Mechantronics Engineering'),
     #                   ('Mechanical Engineering','Mechanical Engineering'),
     #                   ('Civil Engineering','Civil Engineering'),
     #                   ('Electrical Engineering','Electrical Engineering'),
     #                   ('Marine Engineering','Marine Engineering'),
     #                   ('Automobile Engineering','Automobile Engineering'),
     #                   ('Petrochemical Engineering','Petrochemical Engineering'))  

     branches = Branch.objects.values_list('branch_name')
     branch_choices = ((branch[0],branch[0]) for branch in branches)

     designation_choices=(('Head of Department','Head of Department'),
                    ('Professor','Professor'),
                    ('Assistant Professor','Assistant Professor'),
                    ('Lab Instructor', 'Lab Instructor'),
                    ('Lab Assistant','Lab Assistant'))
               
     categories = (('Faculty','Faculty'),
                ('Staff','Staff'),
                ('Admin','Admin'),
                ('Head of Department','Head of Department'))

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
     
     employee_id = models.CharField(max_length=70,
                    verbose_name='Employee Id', unique=True)

     account_id = models.CharField(max_length=20,
                    verbose_name="Account Id", default='', primary_key=True)

     date = models.DateField(max_length=70,
                    verbose_name="Date of Birth")

     mobile = models.CharField(max_length=10,
               verbose_name="Mobile Number")

     branch = models.CharField(max_length=70,
                    verbose_name="Branch", choices=branch_choices)

     email = models.EmailField(max_length=70,
                    verbose_name="Email")
     
     gender = models.CharField(max_length=7,
                    verbose_name="Gender",
                    choices=gender_choices)

     designation = models.CharField(max_length=20,
                    verbose_name="Designation",
                    choices=designation_choices)

     category = models.CharField(max_length=70,
                    verbose_name="Category",
                    default='Faculty',
                    choices=categories)

     isAdmin=models.BooleanField(max_length=10,
                    default=False)
     
     isPending = models.BooleanField(max_length=10,
                    default=True,
                    )
     


