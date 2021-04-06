from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import Student
from common.models import Course, Assignment
from datetime import datetime
from students.models import Student, Attendance, Result
from  . import forms
from admins.models import Branch
from staff.models import Staff
from common.models import Announcement, Assignment, Course, CourseFaculty, Submission
from common.methods import submission_id_generator
from students.forms import editforms
from datetime import datetime
import collections


# Create your views here.

def student_home_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        if not request.session.get('userEnrolment'):
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
    else:
        return redirect(reverse('login'))


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
        return redirect(reverse('login'))

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
            assignments = Assignment.objects.filter(course=selectedCourse) #.order_by('start_date').reverse()
            ongoingAssignments = []
            completedAssignments = []
            for assignment in assignments:
                if assignment.start_date > datetime.date(datetime.today()):
                    continue
                elif assignment.start_date <= datetime.date(datetime.today()) and assignment.end_date == None:
                    ongoingAssignments.append(assignment)
                elif assignment.start_date <= datetime.date(datetime.today()) and assignment.end_date >= datetime.date(datetime.today()):
                    ongoingAssignments.append(assignment)
                elif assignment.end_date and assignment.end_date < datetime.date(datetime.today()):
                    completedAssignments.append(assignment)

            studentSubmissions = Submission.objects.filter(student=user, course=selectedCourse)
            submittedAssignments = [sub.assignment for sub in studentSubmissions]

            submittedDict = {}

            for assignment in ongoingAssignments:
                if assignment in submittedAssignments:
                    submittedDict[assignment.assignment_id] = "Submitted"
                else:
                    submittedDict[assignment.assignment_id] = "Not submitted"
                
            overdue = []
            for assignment in completedAssignments:
                if assignment not in submittedAssignments:
                    overdue.append(assignment)
        
            context = {
            'courses' : courseList,
            'selectedCourse' : selectedCourse,
            'assignments' : ongoingAssignments,
            'submissions': studentSubmissions,
            'submittedAssignments' : submittedDict,
            'overdue': overdue
            }

            return render(request, "students/courses.html", context)
        else:
            return render(request, "students/no_permission.html")
    else:
        return redirect(reverse('login'))

def assignment_details_view(request, course_code, assignment_id, *args, **kwargs):
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
            selectedAssignment = get_object_or_404(Assignment, assignment_id=assignment_id)

            if request.method == 'POST':
                u_file = str(request.FILES['submission-file'])
                extension = u_file.split(".")[1].lower()
                path = "/students/assignments/" + course_code + "/" + assignment_id + "/"
                if extension != 'pdf':
                    request.session['file_type_error'] = 1
                    return redirect(path)

                new_submission = Submission(submission_id=submission_id_generator(course_code, assignment_id),
                                course=selectedCourse,
                                assignment=selectedAssignment,
                                student=user,
                                submission_file=request.FILES['submission-file'] if request.FILES.get('submission-file') else None )
                new_submission.save()

                request.session["assignmentSubmitted"] = 1
                return redirect(path)

            if selectedAssignment.course != selectedCourse or selectedAssignment.course.branch != user.branch or selectedAssignment.course.semester != user.sem:
                return render(request, "students/no_permission.html")

            studentSubmission = Submission.objects.filter(student=user, assignment=selectedAssignment)
            
            submittedLate = False
            overdue = False
            timeRemaining = None
            if studentSubmission:
                studentSubmission = studentSubmission[0]
                if selectedAssignment.end_date and datetime.date(studentSubmission.submission_time) > selectedAssignment.end_date:
                    submittedLate = True
            else:
                if selectedAssignment.end_date:
                    if selectedAssignment.end_date < datetime.date(datetime.now()):
                        overdue = True
                        timeRemaining = datetime.date(datetime.now()) - selectedAssignment.end_date
                    else:
                        timeRemaining = selectedAssignment.end_date - datetime.date(datetime.now())
                        
                    timeRemaining = str(timeRemaining).split(',')[0]
                    if timeRemaining == '0:00:00':
                        timeRemaining = '0 days' 

            uploadSuccess = '0'
            if request.session.get("assignmentSubmitted") and request.session["assignmentSubmitted"] == 1:
                uploadSuccess = '1'
                request.session["assignmentSubmitted"] = 0

            if request.session.get("file_type_error") and request.session["file_type_error"] == 1:
                uploadSuccess = 'file_error'
                request.session["file_type_error"] = 0

            context = {
                'courses': courseList,
                'selectedCourse' : selectedCourse,
                'selectedAssignment': selectedAssignment,
                'submission': studentSubmission,
                'submitLate': submittedLate,
                'overdue': overdue,
                'timeRemaining': timeRemaining,
                'uploadSuccess': uploadSuccess,
            }

            return render(request, "students/assignment_details.html", context)

        else:
            return render(request, "students/no_permission.html")
    else:
        return redirect(reverse('login'))
    
def all_assignments_view(request, course_code, *args, **kwargs):
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
            assignments = Assignment.objects.filter(course=selectedCourse) #.order_by('start_date').reverse()
            ongoingAssignments = []
            completedAssignments = []
            for assignment in assignments:
                if assignment.start_date > datetime.date(datetime.today()):
                    continue
                elif assignment.start_date <= datetime.date(datetime.today()) and assignment.end_date == None:
                    ongoingAssignments.append(assignment)
                elif assignment.start_date <= datetime.date(datetime.today()) and assignment.end_date >= datetime.date(datetime.today()):
                    ongoingAssignments.append(assignment)
                elif assignment.end_date and assignment.end_date < datetime.date(datetime.today()):
                    completedAssignments.append(assignment)
            
            studentSubmissions = Submission.objects.filter(student=user, course=selectedCourse)
            studentAssignments = [sub.assignment for sub in studentSubmissions]
            ongoingStatus = {}
            for assignment in ongoingAssignments:
                if assignment in studentAssignments:
                    ongoingStatus[assignment] = 'Submitted'
                else:
                    ongoingStatus[assignment] = 'Not Submitted'

            completedStatus = {}
            
            for assignment in completedAssignments:
                if assignment in studentAssignments:
                    completedStatus[assignment] = 'Submitted'
                else:
                    completedStatus[assignment] = 'Overdue'

            print(ongoingStatus, completedStatus)
            context = {
                'courses': courseList,
                'selectedCourse' : selectedCourse,
                'ongoingAssignments': ongoingAssignments,
                'completedAssignments': completedAssignments,
                'ongoingStatus': ongoingStatus,
                'completedStatus': completedStatus,
            }

            return render(request, "students/all_assignments.html", context)

        else:
            return render(request, "students/no_permission.html")
    else:
        return redirect(reverse('login'))
    

def attendance_redirect_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        if not request.session.get('enrolment'):
            username = request.user.username
            user = Student.objects.get(username=username)
            request.session['enrolment'] = user.enrolment

        user = Student.objects.get(enrolment=request.session['enrolment'])
        courses = Course.objects.filter(branch=user.branch, semester=user.sem)
        courseList = {}
        for course in courses:
            if courseList.get(course.semester):
                courseList[course.semester].append((course.course_id,course.course_name))
            else:
                courseList[course.semester] = [(course.course_id,course.course_name)]
        courseList = collections.OrderedDict(sorted(courseList.items()))
        if list(courseList):
            course_code = list(courseList.values())[0][0][0]
        else:
            course_code = 'mt'
        return redirect("./" + course_code)
    else:
        return redirect(reverse('login'))

    
def student_attendance_view(request, course_code, *args, **kwargs):
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
            studentAttendance = Attendance.objects.filter(student=user, course=selectedCourse)

            total = 0
            present = 0
            absent = 0
            if len(studentAttendance) > 0:
                total = len(studentAttendance)
                for att in studentAttendance:
                    if att.status == 'P':
                        present += 1

                attendancePercentage = round((present / total) * 100, 2)
                absent = total - present
            else:
                attendancePercentage = 'N.A.'

            context = {
                'courses': courseList,
                'selectedCourse': selectedCourse,
                'studentAttendance': studentAttendance,
                'attendanceStats': [total, present, absent, attendancePercentage]
            }
            return render(request, "students/attendance.html", context)

def courses_redirect_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        if not request.session.get('userSem'):
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
        if not request.session.get('userName'):
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