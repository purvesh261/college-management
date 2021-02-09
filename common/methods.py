from students.models import Student
from staff.models import Staff
from common.models import Announcement, Course
import datetime
import random
import string

def id_generator():
    today = datetime.datetime.now()
    year = str(today.year)
    year = year[2:]
    while True:
        new_account_id = ''.join([str(random.choice(string.digits)) for n in range(8)])
        new_account_id = year + new_account_id
        if Student.objects.filter(account_id=new_account_id).exists() or Staff.objects.filter(account_id=new_account_id).exists() or Announcement.objects.filter(account_id=new_account_id).exists() or Course.objects.filter(course_id=new_account_id).exists():
            pass
        else:
            break
    return new_account_id

def course_id_generator(branch_code):
    today = datetime.datetime.now()
    year = str(today.year)
    year = year[2:]
    base = year + branch_code 
    while True:
        new_course_id = ''.join([str(random.choice(string.digits)) for n in range(6)])
        new_course_id = base + new_course_id
        if Student.objects.filter(account_id=new_course_id).exists() or Staff.objects.filter(account_id=new_course_id).exists() or Announcement.objects.filter(account_id=new_course_id).exists() or Course.objects.filter(course_id=new_course_id).exists():
            pass
        else:
            break
    return new_course_id
# def is_logged_in(category):
#     if request.user.is_authenticated:

#     else: