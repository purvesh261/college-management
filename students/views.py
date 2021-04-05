from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from common.models import Course, Assignment
from datetime import datetime
import collections
from django.shortcuts import render
from students.models import Student, Attendance
from students.models import Result
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from  . import forms
from django.contrib import messages
from .models import Branch
from staff.models import Staff
from common.models import Announcement, Assignment
from django.shortcuts import render,redirect,get_object_or_404
from django.shortcuts import render,redirect, get_object_or_404
from common.models import  Course, CourseFaculty,Announcement
import collections
from datetime import datetime
from django.urls import reverse
from students.forms import editforms


# Create your views here.

def student_home_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        if not request.session.get('userId'):
            userEmail = request.user.email
            user = Student.objects.get(email=userEmail)
            request.session['userBranch']=user.branch
            request.session['userEnrolment']=user.enrolment
        result=Result.objects.filter(enrolment=request.session['userEnrolment'],branch=request.session['userBranch'])
        res=[]
        for i in result:
            res.append(i)
        print(res)
    time = datetime.now()
    announcement_data=reversed(Announcement.objects.all())
    currentTime = time.strftime("%d/%m/%Y %I:%M %p")
    context = {
        'timestamp': currentTime,
        'announcement_data':announcement_data,
        'res':res
    }
   
    return render(request, "students/home.html",context)


def courses_redirect_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        if not request.session.get('enrolment'):
            username = request.user.username
            user = Student.objects.get(username=username)
            request.session['enrolment'] = user.enrolment
            print(username, user)

        user = Student.objects.get(enrolment=request.session['enrolment'])
        courses = Course.objects.filter(branch=user.branch, semester=user.sem)
        courseList = {}
        for course in courses:
            if courseList.get(course.semester):
                courseList[course.semester].append((course.course_id,course.course_name))
            else:
                courseList[course.semester] = [(course.course_id,course.course_name)]
        if list(courseList):
            course_code = list(courseList.values())[0][0][0]
        else:
            course_code = 'mt'

        return redirect("./" + course_code)
    else:
        print("OK!!!!!")

def no_course_view(request, *args,**kwargs):
    context = {
        'courses': []
    }
    return render(request, "students/courses.html", context)

def student_courses_view(request, course_code, *args, **kwargs):
    if request.user.is_authenticated:
        if not request.session.get('enrolment'):
            username = request.user.username
            user = Student.objects.get(username=username)
            request.session['enrolment'] = user.enrolment

        user = Student.objects.get(enrolment=request.session['enrolment'])
        selectedCourse = get_object_or_404(Course, course_id=course_code)

        if user.branch == selectedCourse.branch and user.sem == selectedCourse.semester:
            courses = Course.objects.filter(branch=user.branch, semester=user.sem)
            courseList = {}
            for course in courses:
                if courseList.get(course.semester):
                    courseList[course.semester].append((course.course_id,course.course_name))
                else:
                    courseList[course.semester] = [(course.course_id,course.course_name)]
            courseList = collections.OrderedDict(sorted(courseList.items()))
            assignments = Assignment.objects.filter(course=selectedCourse).order_by('start_date').reverse()
            ongoingAssignments = []
            for assignment in assignments:
                if assignment.start_date > datetime.date(datetime.today()):
                    continue
                elif assignment.start_date <= datetime.date(datetime.today()) and assignment.end_date == None:
                    ongoingAssignments.append(assignment)
                elif assignment.start_date <= datetime.date(datetime.today()) and assignment.end_date >= datetime.date(datetime.today()):
                    ongoingAssignments.append(assignment)
                elif assignment.start_date < datetime.date(datetime.today()) and assignment.end_date < datetime.date(datetime.today()):
                    break

            context = {
            'courses' : courseList,
            'selectedCourse' : selectedCourse,
            'assignments' : ongoingAssignments,
            }
            return render(request, "students/courses.html", context)
        else:
            return render(request, "students/no_permission.html")

    return render(request, "students/courses.html")

def student_attendance_view(request, *args, **kwargs):
    return render(request, "students/attendance.html")


def courses_redirect_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        if not request.session.get('userId'):
            userEmail = request.user.email
            user = Student.objects.get(email=userEmail)
            request.session['userSem'] = user.sem
            request.session['userBranch']=user.branch

        courses = Course.objects.filter(semester=request.session['userSem'],branch=request.session['userBranch'])
        courseList = {}
        for course in courses:
            if courseList.get(course.semester):
                courseList[course.semester].append((course.course_id,course.course_name))
            else:
                courseList[course.semester] = [(course.course_id,course.course_name)]
        if list(courseList):
            course_code = list(courseList.values())[0][0][0]
        else:
            course_code = 'mt'
        print('code',course_code)

        return redirect("./" + course_code)
    else:
        print("OK!!!!!")


def student_results_view(request,course_code, *args, **kwargs):
    if request.user.is_authenticated:
        if not request.session.get('userId'):
            userEmail = request.user.email
            user = Student.objects.get(email=userEmail)
            request.session['userSem'] = user.sem
            request.session['userBranch']=user.branch
            request.session['userEnrolment']=user.enrolment
            request.session['userName']=user.username
        selectedCourse = Course.objects.get(course_id=course_code)
        courses = Course.objects.filter(semester=request.session['userSem'],branch=request.session['userBranch'])
        result=Result.objects.filter(enrolment=request.session['userEnrolment'],branch=request.session['userBranch'],course_id=course_code)
        print(reversed(result))
        print(result)
        for i in reversed(result):
            print(i.marks,i.exam,i.course_name)
        courseList = {}
        for course in courses:
            if courseList.get(course.semester):
                courseList[course.semester].append((course.course_id,course.course_name))
            else:
                courseList[course.semester] = [(course.course_id,course.course_name)]
        courseList = collections.OrderedDict(sorted(courseList.items()))     
       
        std=Student.objects.filter(username=request.session['userName'])
        for i in std:
            print(i.firstName)

        grades=[]
        for g in result:
            print((int(g.marks)/20)*100)
            grade=(int(g.marks)/20)*100
            grades.append(grade)
        print(grades)
        context={
        'selectedCourse':selectedCourse,
        'courses':courseList,
        'result':(result),
        'student':std,
        'grades':grades,
        'zip':zip(result,grades)
        }

    return render(request, "students/results.html",context)
def no_course_view(request, *args,**kwargs):
    context = {
        'courses': []
    }
    return render(request, "staff/results.html", context)
def student_profile_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        if not request.session.get('userId'):
            userEmail = request.user.email
            user = Student.objects.get(email=userEmail)
            request.session['userName'] = user.username
    obj=Student.objects.filter(username=request.session['userName'])
    for i in obj:
        br=i.branch
    print(br)
    branch=Branch.objects.filter(code=br)
    print(branch)
    context={
        'student':obj,
        'branch':branch
    }
    return render(request, "students/profile.html",context)

def student_profile_edit(request,account_id):
    print(account_id)
    displaydata=Student.objects.get(account_id=account_id)
    print(displaydata)
    updatedata=Student.objects.get(account_id=account_id)
    print(account_id)
    if request.method == "POST":
        print('post')
        form=editforms(request.POST or None,instance=updatedata)
        #error here
        if form.is_valid():
            form.save()
            #messages.success(request,"Your Profile updated")
            #return render(request,'admins/adminprofileedit.html',{'editdata':updatedata})
            return redirect("../profile")
        else:
            return HttpResponse(messages)
    return render(request,'students/edit_profile.html',{'editdata':displaydata})