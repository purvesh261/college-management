from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse, resolve
import collections
from datetime import datetime
from common.announcementform import announcementform
from common.models import Announcement, Assignment, Course, CourseFaculty, Submission
from staff.forms2 import editforms2
from common.methods import id_generator, assignment_id_generator
from  . import forms
from .models import Branch
import common
from staff.models import Staff
from staff.forms import resultform, CreateAssignmentForm, EditAssignmentForm, editforms1, editresultform
from students.models import Student, Attendance, Result
from staff.forms import doubtform
from students.models import Doubt


# Create your views here.

def staff_home_view(request, *args, **kwargs):
    time = datetime.now()
    doubts=Doubt.objects.filter(answer='')
    print(len(doubts))
    announcement_data=reversed(Announcement.objects.all())
    print(announcement_data)
    #for i in announcement_data:
        #print(i.title)
    currentTime = time.strftime("%d/%m/%Y %I:%M %p")
    context = {
        'timestamp': currentTime,
        
        
    }
    return render(request, "staff/home.html",{'context':context,'announcement_data':announcement_data,'doubts':len(doubts)})

#staff announcement
def staff_announcement(request,*args,**kwargs):
    announcementform1 = announcementform(request.POST or None)
    if request.method == 'POST':
        print('post1')
        announcementform1 = announcementform(request.POST or None)
        if announcementform1.is_valid():
            print('post')
            details = announcementform1.cleaned_data
            new_title=details['title']
            new_description=details['description']
            new_account_id = id_generator()
            print(new_title)
            print(new_description)
            newannouncement = Announcement(title=str(new_title.capitalize()),
                                           description=str(new_description.capitalize()),
                                           account_id=str(new_account_id))
            print(newannouncement)
            newannouncement.save()
            #messages.success(request,"Announcement Added")
            return redirect("../announcement/")
        else:
            return HttpResponse(messages)
    return render(request,"common/announcement.html",{'announcementform1':announcementform1})



#@login_required(login_url=common.views.login_view)
def staff_add_announcement(request,*args,**kwargs):
    obj=Announcement.objects.all()
    return render(request,"common/allannouncement.html",{'announcementform1':obj})

#@login_required(login_url=common.views.login_view)
def staff_announcement_done(request,*args,**kwargs):
    announcementform1 = announcementform(request.POST or None)
    return render(request,"common/announcement.html",{'announcementform1':announcementform1})



#admin announcement edit 

#@login_required(login_url=common.views.login_view)
def staff_announcement_edit(request,account_id):
    print(account_id)
    displaydata=Announcement.objects.get(account_id=account_id)
    print(displaydata)
    updatedata=Announcement.objects.get(account_id=account_id)
    print(updatedata)
    print(account_id)
    if request.method == "POST":
        print('post')
        form=editforms2(request.POST or None,instance=updatedata)
        #error here
        if form.is_valid():
            print('inform')
            form.save()
            #messages.success(request,"Announcement updated")
            return redirect("../all-announcement")
            #return render(request,'common/announcementedit.html',{'editdata':updatedata})
        else:
            return HttpResponse(messages)    
    return render(request,'common/announcementedit.html',{'editdata':displaydata})



#@login_required(login_url=common.views.login_view)
# def edit_announcement(request,account_id):
#     updatedata=Announcement.objects.get(account_id=account_id)
#     print(updatedata)
#     print(account_id)
#     if request.method == "POST":
#         print('post')
#         form=editforms2(request.POST or None,instance=updatedata)
#         #error here
#         if form.is_valid():
#             print('inform')
#             form.save()
#             messages.success(request,"Announcement updated")
#             return render(request,'common/announcementedit.html',{'editdata':updatedata})
#         else:
#             return HttpResponse(messages)
#     print(form.errors)

# staff announcement end

#delete announcement 
#@login_required(login_url=common.views.login_view)
def staff_delete_view(request, account_id):
    obj=Announcement.objects.get(account_id=account_id)
    print(obj)
    print(request.method)
    if request.method=="GET":
        print('get')
        obj.delete()
        return redirect("../all-announcement")
    else:
        return HttpResponse(messages)
    return render(request,'common/allannouncement.html',{'announcementform1':obj}) 

# @login_required(login_url=common.views.login_view)
def courses_redirect_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        if not request.session.get('userId'):
            userEmail = request.user.email
            user = Staff.objects.get(email=userEmail)
            request.session['userId'] = user.employee_id

        courses = CourseFaculty.objects.filter(faculty_id=request.session['userId'])
        courseList = {}
        for course in courses:
            if courseList.get(course.course_id.semester):
                courseList[course.course_id.semester].append((course.course_id.course_id,course.course_id.course_name))
            else:
                courseList[course.course_id.semester] = [(course.course_id.course_id,course.course_id.course_name)]
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
    return render(request, "staff/courses.html", context)

# @login_required(login_url=common.views.login_view)
def staff_courses_view(request,course_code, *args, **kwargs):
    if request.user.is_authenticated:
        if not request.session.get('userId'):
            userEmail = request.user.email
            user = Staff.objects.get(email=userEmail)
            request.session['userId'] = user.employee_id
                    
        doubts=Doubt.objects.filter(course_id=course_code,answer='')


        selectedCourse = Course.objects.get(course_id=course_code)
        selectedObj = get_object_or_404(CourseFaculty, faculty_id=request.session['userId'],course_id=selectedCourse)
        courseList = {}
        assignments = None
        if selectedObj:
            courses = CourseFaculty.objects.filter(faculty_id=request.session['userId'])
            for course in courses:
                if courseList.get(course.course_id.semester):
                    courseList[course.course_id.semester].append((course.course_id.course_id,course.course_id.course_name))
                else:
                    courseList[course.course_id.semester] = [(course.course_id.course_id,course.course_id.course_name)]
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

        context = {
            'courses' : courseList,
            'selectedCourse' : selectedCourse,
            'assignments' : ongoingAssignments,
            'doubts':doubts
        }
    return render(request, "staff/courses.html", context)

def staff_doubt_answer(request,id,course_code):
    doubts_data=Doubt.objects.filter(id=id)
    print(doubts_data)
    for i in doubts_data:
        enrol=i.enrolment
        doubt=i.doubt
        course_id=i.course_id
        i_d=i.id
    initial_dict={
        'id':i_d
    }
    doubtform1=doubtform(request.POST,initial=initial_dict)
    if request.method == 'POST':
        print('post1')
        doubtform1 = doubtform(request.POST)
        if doubtform1.is_valid():
            print('post')
            details = doubtform1.cleaned_data
            new_enrolment=enrol
            new_doubt=doubt
            new_answer=details['answer']
            new_course=course_id
           
            new_id=i_d
            print(new_answer)
            newdoubt = Doubt(enrolment=str(new_enrolment),
                             doubt=str(new_doubt),
                             answer=str(new_answer.capitalize()),
                             course_id=str(new_course),
                             id=new_id)              
            print(newdoubt)
            newdoubt.save()
            #messages.success(request,"Announcement Added")
            return redirect("../")
        else:
            return HttpResponse(messages)


    context={
            'doubtform1':doubtform1
            }
    return render(request,'staff/doubts.html',context)


# @login_required(login_url=common.views.login_view)
def create_assignment_view(request,course_code, *args, **kwargs):
    if request.user.is_authenticated:
        userEmail = request.user.email
        user = Staff.objects.get(email=userEmail)
        if not request.session.get('userId'):
            request.session['userId'] = user.employee_id


        selectedCourse = Course.objects.get(course_id=course_code)
        if request.method == 'POST':
            form = CreateAssignmentForm(request.POST or None,request.FILES)
            if form.is_valid():
                details = form.cleaned_data
                assignmentID = assignment_id_generator(course_code)
                title = details['title']
                description = details['description']
                startDate = details['start_date']
                endDate = details['end_date']
                if not startDate:
                    startDate = datetime.today()
                new_assignment = Assignment(assignment_id=str(assignmentID),
                                    course=selectedCourse,
                                    faculty=user,
                                    title=title,
                                    description=description,
                                    start_date=startDate,
                                    end_date=endDate,
                                    assignment_file=request.FILES['assignment_file'] if request.FILES.get('assignment_file') else None, 
                                    )
                new_assignment.save()
                return redirect(reverse('staff:courses_view', kwargs={'course_code':course_code}))
            else:
                form = CreateAssignmentForm(request.POST or None)
                return render(request, 'staff/create_assignment.html', {'form': form})
        else:
            form = CreateAssignmentForm(request.POST or None)
            return render(request, 'staff/create_assignment.html', {'form': form})

def view_assignments_view(request, course_code, *args, **kwargs):
    context = {}
    if request.user.is_authenticated:
        if not request.session.get('userId'):
            userEmail = request.user.email
            user = Staff.objects.get(email=userEmail)
            request.session['userId'] = user.employee_id

        selectedCourse = Course.objects.get(course_id=course_code)
        selectedObj = get_object_or_404(CourseFaculty, faculty_id=request.session['userId'],course_id=selectedCourse)
        courseList = {}
        assignments = None
        if selectedObj:
            courses = CourseFaculty.objects.filter(faculty_id=request.session['userId'])
            for course in courses:
                if courseList.get(course.course_id.semester):
                    courseList[course.course_id.semester].append((course.course_id.course_id,course.course_id.course_name))
                else:
                    courseList[course.course_id.semester] = [(course.course_id.course_id,course.course_id.course_name)]
            courseList = collections.OrderedDict(sorted(courseList.items()))
            # assignments = Assignment.objects.filter(course=selectedCourse, end_date__gte=datetime.today()).order_by('start_date').reverse()
            # completedAssignments = Assignment.objects.filter(course=selectedCourse, end_date__lt=datetime.today()).order_by('start_date').reverse()
            assignments = []
            completedAssignments = []
            upcomingAssignments = []
            assTemp = Assignment.objects.filter(course=selectedCourse).order_by('start_date').reverse()
            for assignment in assTemp:
                if assignment.start_date > datetime.date(datetime.today()):
                    upcomingAssignments.append(assignment)
                elif assignment.end_date == None:
                    assignments.append(assignment)
                elif assignment.end_date > datetime.date(datetime.today()):
                    assignments.append(assignment)
                else:
                    completedAssignments.append(assignment)
            context = {
            'courses' : courseList,
            'selectedCourse' : selectedCourse,
            'assignments' : assignments,
            'completedAssignments' : completedAssignments,
            'upcomingAssignments' : upcomingAssignments,
            }
    return render(request, 'staff/assignments.html', context)
    
def manage_assignment_view(request, course_code, assignment_id, *args, **kwargs):
    context = {}
    if request.user.is_authenticated:
        if not request.session.get('userId'):
            userEmail = request.user.email
            user = Staff.objects.get(email=userEmail)
            request.session['userId'] = user.employee_id

        selectedCourse = Course.objects.get(course_id=course_code)
        selectedObj = get_object_or_404(CourseFaculty, faculty_id=request.session['userId'],course_id=selectedCourse)
        courseList = {} 
        if selectedObj:
            courses = CourseFaculty.objects.filter(faculty_id=request.session['userId'])
            
            for course in courses:
                if courseList.get(course.course_id.semester):
                    courseList[course.course_id.semester].append((course.course_id.course_id,course.course_id.course_name))
                else:
                    courseList[course.course_id.semester] = [(course.course_id.course_id,course.course_id.course_name)]
            courseList = collections.OrderedDict(sorted(courseList.items()))
            selectedAssignment = Assignment.objects.get(assignment_id=assignment_id)
            students = Student.objects.filter(branch=selectedCourse.branch,sem=selectedCourse.semester,isPending=False).order_by('enrolment')

            submissions = Submission.objects.filter(assignment=selectedAssignment)

            submittedStudents = [sub.student.enrolment for sub in submissions]
            submissionDict = {}
            for student in students:
                if student.enrolment in submittedStudents:
                    status = ''
                    sub = Submission.objects.get(student=student, assignment=selectedAssignment)
                    print(sub.submission_time.year)
                    if selectedAssignment.end_date and datetime.date(sub.submission_time) > selectedAssignment.end_date:
                        status = 'Submitted Late'
                    else:
                        status = 'Submitted'

                    submissionDict[student.enrolment] = [sub, status]
                else:
                    status = ''
                    if selectedAssignment.end_date and datetime.date(datetime.today()) > selectedAssignment.end_date:
                        status = 'Overdue'
                    else:
                        status = 'Not Submitted'
                    submissionDict[student.enrolment] = [None, status]
            print(submissionDict)

        context = {
            'courses' : courseList,
            'selectedCourse' : selectedCourse,
            'selectedAssignment' : selectedAssignment,
            'students': students,
            'submittedStudents': submittedStudents,
            'submissions': submissionDict,
        }
    return render(request, 'staff/manage_assignment.html', context)

def edit_assignment_view(request,assignment_id, *args, **kwargs):
    selectedAssignment = Assignment.objects.get(assignment_id=assignment_id)
    if not request.session.get('userId'):
            userEmail = request.user.email
            user = Staff.objects.get(email=userEmail)
            request.session['userId'] = user.employee_id
    course = selectedAssignment.course
    if CourseFaculty.objects.filter(course_id=course, faculty_id=request.session['userId']):
        if request.method == "POST":
            form = EditAssignmentForm(request.POST, request.FILES, instance=selectedAssignment)
            if form.is_valid():
                form.save()
                return redirect('..')
        else:
            form = EditAssignmentForm(request.POST or None, instance=selectedAssignment)
            for field in form.errors:
                form[field].field.widget.attrs['class'] += 'error'

    context = {
        'form': form,
    }
    
    return render(request, "staff/edit_assignment.html",context)

def delete_assignment_view(request,assignment_id, *args, **kwargs):
    selectedAssignment = Assignment.objects.get(assignment_id=assignment_id)
    if not request.session.get('userId'):
            userEmail = request.user.email
            user = Staff.objects.get(email=userEmail)
            request.session['userId'] = user.employee_id
    course = selectedAssignment.course
    if CourseFaculty.objects.filter(course_id=course, faculty_id=request.session['userId']):
        selectedAssignment.assignment_file.delete()
        selectedAssignment.delete()
        return redirect(reverse('staff:courses_view', kwargs={'course_code':course.course_id}))
    else:
        return redirect("..../courses/" + course.course_id)

# @login_required(login_url=common.views.login_view)
def staff_attendance_view(request, course_code, *args, **kwargs):
    if request.user.is_authenticated:
        if not request.session.get('userId'):
            userEmail = request.user.email
            user = Staff.objects.get(email=userEmail)
            request.session['userId'] = user.employee_id

        selectedCourse = Course.objects.get(course_id=course_code)
        selectedObj = get_object_or_404(CourseFaculty, faculty_id=request.session['userId'],course_id=selectedCourse)
        courseList = {}
        assignments = None
        if selectedObj:
            courses = CourseFaculty.objects.filter(faculty_id=request.session['userId'])
            for course in courses:
                if courseList.get(course.course_id.semester):
                    courseList[course.course_id.semester].append((course.course_id.course_id,course.course_id.course_name))
                else:
                    courseList[course.course_id.semester] = [(course.course_id.course_id,course.course_id.course_name)]
            courseList = collections.OrderedDict(sorted(courseList.items()))
           
            attendanceHistory = Attendance.objects.filter(course=selectedCourse)
            dates = set()
            percentage = {}
            for item in attendanceHistory:
                if percentage.get(item.date):
                    percentage[item.date].append(item.status)
                else:
                    percentage[item.date] = [item.status]

                dates.add(item.date)

            for key in percentage.keys():
                percentage[key] = [round((percentage[key].count('P') / len(percentage[key])) * 100, 2), round(100 - (percentage[key].count('P') / len(percentage[key])) * 100, 2), key.strftime('%d%m%Y')]

            dates = list(percentage.keys())

            dateDict = {}

            res = []

            sortedDict = {}
            
            for ele in reversed(sorted(percentage.keys())):
                res.append(ele)

            for date in res:
                sortedDict[date] = percentage[date]
            
            student_list = Student.objects.filter(sem=selectedCourse.semester, branch=selectedCourse.branch, isPending=False)
            
            studentAttendance = {}
            for stud in student_list:

                studentHist = Attendance.objects.filter(course=selectedCourse, student=stud)
                if len(studentHist) > 0:
                    studentPresent = 0
                    for item in studentHist:
                        if item.status == 'P':
                            studentPresent += 1
                    studentAttendance[stud.enrolment] = round((studentPresent / len(studentHist)) * 100, 2)
                else:
                    studentAttendance[stud.enrolment] = 'N.A.'

            print(studentAttendance)

        updated = 0
        att_date = 0
        if request.session.get('attendance_added'):
            updated = request.session['attendance_added']
            att_date = request.session['attendance_date']
            request.session['attendance_added'] = 0
            request.session['attendance_date'] = 0


        context = {
            'courses' : courseList,
            'selectedCourse' : selectedCourse,
            'history': sortedDict,
            'students': student_list,
            'studentPercentage': studentAttendance,
            'updated': updated,
            'date': att_date,
        }
        return render(request, "staff/attendance_course_list.html", context)
    else:
         return redirect(reverse('login'))

# @login_required(login_url=common.views.login_view)
def attendance_redirect_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        if not request.session.get('userId'):
            userEmail = request.user.email
            user = Staff.objects.get(email=userEmail)
            request.session['userId'] = user.employee_id

        courses = CourseFaculty.objects.filter(faculty_id=request.session['userId'])
        courseList = {}
        for course in courses:
            if courseList.get(course.course_id.semester):
                courseList[course.course_id.semester].append((course.course_id.course_id,course.course_id.course_name))
            else:
                courseList[course.course_id.semester] = [(course.course_id.course_id,course.course_id.course_name)]
        if list(courseList):
            course_code = list(courseList.values())[0][0][0]
        else:
            course_code = 'mt'
        return redirect("./" + course_code)
    else:
        return redirect(reverse('login'))

# @login_required(login_url=common.views.login_view)
def enter_attendance_view(request, course_code, *args, **kwargs):
    if request.user.is_authenticated:
        userEmail = request.user.email
        user = Staff.objects.get(email=userEmail)
        request.session['userId'] = user.employee_id

        selectedCourse = Course.objects.get(course_id=course_code)
        selectedObj = get_object_or_404(CourseFaculty, faculty_id=request.session['userId'],course_id=selectedCourse)
        courseList = {}
        assignments = None
        if selectedObj:
            courses = CourseFaculty.objects.filter(faculty_id=request.session['userId'])
            for course in courses:
                if courseList.get(course.course_id.semester):
                    courseList[course.course_id.semester].append((course.course_id.course_id,course.course_id.course_name))
                else:
                    courseList[course.course_id.semester] = [(course.course_id.course_id,course.course_id.course_name)]
            courseList = collections.OrderedDict(sorted(courseList.items()))
            student_list = Student.objects.filter(sem=selectedCourse.semester, branch=selectedCourse.branch, isPending=False)

        if request.method == "POST":
            attendance = list(request.POST.items())
            selectedDate = attendance[1][1]
            print(selectedDate)
            attendanceList = Attendance.objects.filter(course=selectedCourse, date=datetime(int(selectedDate[:4].lstrip('0')), int(selectedDate[5:7].lstrip('0')), int(selectedDate[8:].lstrip('0'))))
            
            if attendanceList:
                request.session['date_already_exists'] = 1
                path = '/staff/attendance/' + course_code + '/enter-attendance/'  
                return redirect(path)

            for i in range(2,len(attendance)):
                item = attendance[i]
                enrol = item[0]
                status = item[1]
                for stud in student_list:
                    if stud.enrolment == enrol:
                        AttendanceObj = Attendance(student=stud, date=selectedDate, course=selectedCourse, faculty=user, status=status)
                        AttendanceObj.save()
                        request.session['attendance_added'] = 1
                        request.session['attendance_date'] = selectedDate
                        break
            return redirect(reverse('staff:attendance', kwargs={'course_code':course_code}))
        exists_error = 0
        if request.session.get('date_already_exists'):
            exists_error = 1
            request.session['date_already_exists'] = 0

        context = {
            'courses' : courseList,
            'selectedCourse' : selectedCourse,
            'students' : student_list,
            'date': datetime.date(datetime.today()),
            'exists_error': exists_error,
        }
        return render(request, 'staff/enter_attendance.html', context)

    else:
         return redirect(reverse('login'))

# @login_required(login_url=common.views.login_view)
def edit_attendance_view(request, course_code, date, *args, **kwargs):
    if request.user.is_authenticated:
        userEmail = request.user.email
        user = Staff.objects.get(email=userEmail)
        request.session['userId'] = user.employee_id
        day = date[0:2]
        month = date[2:4]
        year = date[4:]

        selectedDate = datetime(int(year), int(month), int(day))
        print(selectedDate)
        selectedDate1 = selectedDate.strftime('%Y-%m-%d')
        date = selectedDate.strftime('%A, %d %B %Y')
        selectedCourse = Course.objects.get(course_id=course_code)
        selectedObj = get_object_or_404(CourseFaculty, faculty_id=request.session['userId'],course_id=selectedCourse)
        courseList = {}
        if selectedObj:
            courses = CourseFaculty.objects.filter(faculty_id=request.session['userId'])
            for course in courses:
                if courseList.get(course.course_id.semester):
                    courseList[course.course_id.semester].append((course.course_id.course_id,course.course_id.course_name))
                else:
                    courseList[course.course_id.semester] = [(course.course_id.course_id,course.course_id.course_name)]
            courseList = collections.OrderedDict(sorted(courseList.items()))
            student_list = Student.objects.filter(sem=selectedCourse.semester, branch=selectedCourse.branch, isPending=False)
            attendanceObj = Attendance.objects.filter(date=selectedDate, course=selectedCourse)
        if request.method == "POST":
            attendance = list(request.POST.items())
            print(attendance)
            for i in range(1,len(attendance)):
                item = attendance[i]
                enrol = item[0]
                status = item[1]
                for stud in student_list:
                    if stud.enrolment == enrol:
                        AttendanceObj = Attendance.objects.get(student=stud, date=selectedDate1, course=selectedCourse)
                        AttendanceObj.status = status
                        AttendanceObj.save()
                        request.session['attendance_added'] = 1
                        request.session['attendance_date'] = selectedDate1
                        break
            return redirect(reverse('staff:attendance', kwargs={'course_code':course_code}))

        context = {
            'attendance': attendanceObj,
            'date' : date,
            'courses' : courseList,

        }
        print(selectedDate)

        return render(request,'staff/edit_attendance.html', context)
    else:
         return redirect(reverse('login'))

# @login_required(login_url=common.views.login_view)
def student_attendance_details_view(request, course_code, student_id, *args, **kwargs):
    if request.user.is_authenticated:
        context = {}
        if not request.session.get('userId'):
            userEmail = request.user.email
            user = Staff.objects.get(email=userEmail)
            request.session['userId'] = user.employee_id

        selectedCourse = Course.objects.get(course_id=course_code)
        selectedObj = get_object_or_404(CourseFaculty, faculty_id=request.session['userId'],course_id=selectedCourse)
        courseList = {}
        assignments = None
        if selectedObj:
            courses = CourseFaculty.objects.filter(faculty_id=request.session['userId'])
            for course in courses:
                if courseList.get(course.course_id.semester):
                    courseList[course.course_id.semester].append((course.course_id.course_id,course.course_id.course_name))
                else:
                    courseList[course.course_id.semester] = [(course.course_id.course_id,course.course_id.course_name)]
            courseList = collections.OrderedDict(sorted(courseList.items()))
            selectedStudent = get_object_or_404(Student, account_id=student_id)

            studentAttendance = Attendance.objects.filter(student=selectedStudent, course=selectedCourse)
            attCount = 0

            for att in studentAttendance:
                if att.status == 'P':
                    attCount += 1
            
            totalAtt = len(studentAttendance)
            percentage = 100
            if totalAtt > 0:
                percentage = round((attCount / totalAtt ) * 100,2)
            fpath = request.get_full_path()
            fpath = fpath.split('/')[-1]
            updated = 0
            if request.session.get('student_attendance_updated'):
                updated = request.session['student_attendance_updated']
                request.session['student_attendance_updated'] = 0

            context = {
            'courses' : courseList,
            'selectedCourse' : selectedCourse,
            'student': selectedStudent,
            'studentAttendance': studentAttendance,
            'percentage': percentage,
            'updated' : updated
            }
        
        if request.method == "POST":
            attendance = list(request.POST.items())
            
            for item in range(1,len(attendance)):
                for att in studentAttendance:
                    print(att.date.strftime('%B %#d, %Y'), attendance[item][0])
                    if att.date.strftime('%B %#d, %Y') == attendance[item][0] and att.status != attendance[item][1]:
                        att.status = attendance[item][1]
                        newObj = Attendance.objects.get(date=att.date,course=selectedCourse, student=selectedStudent)
                        newObj.status = attendance[item][1]
                        newObj.save()
                        break
            
            request.session['student_attendance_updated'] = 1
            path = '/staff/attendance/' + course_code + '/' + student_id + '/'
            return redirect(path)

        return render(request, "staff/student_attendance.html", context)

        
    else:
         return redirect(reverse('login'))


# @login_required(login_url=common.views.login_view)
def staff_results_view(request, course_code, *args, **kwargs):
    if request.user.is_authenticated:
        if not request.session.get('userId'):
            userEmail = request.user.email
            user = Staff.objects.get(email=userEmail)
            request.session['userId'] = user.employee_id
        selectedCourse = Course.objects.get(course_id=course_code)
        selectedObj = get_object_or_404(CourseFaculty, faculty_id=request.session['userId'],course_id=selectedCourse)
        courseList = {}
        if selectedObj:
            courses = CourseFaculty.objects.filter(faculty_id=request.session['userId'])
            for course in courses:
                if courseList.get(course.course_id.semester):
                    courseList[course.course_id.semester].append((course.course_id.course_id,course.course_id.course_name))
                else:
                    courseList[course.course_id.semester] = [(course.course_id.course_id,course.course_id.course_name)]
            courseList = collections.OrderedDict(sorted(courseList.items()))

        branches = Branch.objects.all().order_by('branch_name')
        print(selectedCourse.course_name)
        sem=selectedCourse.semester
        br_code=selectedCourse.branch
        b1=get_object_or_404(Branch,code=br_code)
        print(sem)
        print(branches)
        displaydata=Student.objects.filter(sem=sem,branch=br_code)   
        context = {
            'branches' : branches,
            'courses' : courseList,
            'selectedCourse' : selectedCourse,
            'student':displaydata,
            'branch_name':b1.branch_name
            }
    return render(request, "staff/results.html",context)


# @login_required(login_url=common.views.login_view)
def result_view(request, branch_code, *args):
    branches = Branch.objects.all().order_by('branch_name')
    b1=get_object_or_404(Branch,code=branch_code)
    print(b1.branch_name)
    print(branch_code)
    #staffOfBranch = Staff.objects.filter(branch=selectedBranch.branch_name, isPending=False)
    #selectedBranch = get_object_or_404(Branch,code=branch_code)
    context = {
        'branches' : branches,
        'branch':b1
            }
    return render(request,"staff/semresult.html",{'branch':b1.branch_name})


# @login_required(login_url=common.views.login_view)
def sem_result(request,branch_code,*args):
    sem=(request.path.split('/')) #split the whole url /
    s1=sem[4] #to fetch the sem from url
    print('sem',sem[4]) #print the extracted sem from url

    b1=get_object_or_404(Branch,code=branch_code) #get the branch bane using branch code
    b2=b1.branch_name #get the branch name
    print(b2) #print branch name

    branch_info=b2.split(' ') #model acceptes Short form branch name eg(CE)so using split
    print(branch_info) #print splited branch_info

    binfo=branch_info[0][0]+branch_info[1][0] #fetching short form
    print(binfo) #printing short form

    displaydata=Student.objects.filter(sem=s1,branch=branch_code,isPending=False) #fetching the student by filtering the data
    print(displaydata) #print filtered data of students
    return render(request,"staff/result.html",{'student':displaydata,'branch':b1.branch_name,'sem':s1})

# @login_required(login_url=common.views.login_view)
def add_result(request,account_id,course_code,*args):
    branches = Branch.objects.all().order_by('branch_name')
    selectedCourse = Course.objects.get(course_id=course_code)
    print(selectedCourse.course_name)
    s1=selectedCourse.semester
    br_code=selectedCourse.branch
    b1=get_object_or_404(Branch,code=br_code)
    print(branches)
    displaydata=Student.objects.get(account_id=account_id)
    initial_dict={
        'account_id':id_generator,
        'enrolment':displaydata.enrolment,
        'branch':displaydata.branch,
        'sem':s1,
        'course_id':course_code,
        'course_name':selectedCourse.course_name
    }
    resultform1 = resultform(request.POST or None, initial=initial_dict)
    if request.method == 'POST':
        print('post1')
        resultform1 = resultform(request.POST or None)
        if resultform1.is_valid():
            print('post')
            details = resultform1.cleaned_data
            new_account_id = details['account_id']
            new_enrolment=details['enrolment'] #change all default field by using displaydata
            new_branch=details['branch']
            new_sem=details['sem']
            new_course_name=details['course_name']
            new_course_id=details['course_id']
            new_marks=details['marks']
            new_exam=details['exam']
            
            print(new_enrolment)
            print(new_branch)
            print(new_sem)
            newresult = Result(account_id=str(new_account_id),
                                enrolment=str(new_enrolment),
                                branch=str(new_branch),
                                sem=str(new_sem),
                                course_id=str(new_course_id),
                                course_name=str(new_course_name),
                                marks=str(new_marks),
                                exam=str(new_exam))
                                          
            print(newresult)
            newresult.save()
            #messages.success(request,"Announcement Added")
            return redirect("../")
        else:
            print('error')
                
    
    print('post')
    return render(request,"staff/addresult.html",{'resultform1':resultform1,'sem':s1,'displaydata':displaydata})

#staff-student internals result
# @login_required(login_url=common.views.login_view)
def student_internal_results(request,course_code,*args):
    url=(request.path.split('/')) #split the whole url /
    # s1=url[4] #to fetch the sem from url
    # print('sem',url[4]) #print the extracted sem from url

    # b1=get_object_or_404(Branch,code=branch_code) #get the branch bane using branch code
    # b2=b1.branch_name #get the branch name
    # print(b2) #print branch name

    # branch_info=b2.split(' ') #model acceptes Short form branch name eg(CE)so using split
    # print(branch_info) #print splited branch_info

    # binfo=branch_info[0][0]+branch_info[1][0] #fetching short form
    # print(binfo) #printing short form
    branches = Branch.objects.all().order_by('branch_name')
    selectedCourse = Course.objects.get(course_id=course_code)
    print(selectedCourse.course_name)
    s1=selectedCourse.semester
    br_code=selectedCourse.branch
    b1=get_object_or_404(Branch,code=br_code)
    print(branches)
    exam=url[4]
    print('examname',exam)

    displaydata=Result.objects.filter(sem=s1,branch=br_code,exam=exam,course_name=selectedCourse.course_name) #fetching the student by filtering the data
    print(displaydata) #print filtered data of students
    return render(request,"staff/stdresult.html",{'student':displaydata,'branch':b1.branch_name,'examname':exam})

# @login_required(login_url=common.views.login_view)
def student_result_edit(request,course_code,account_id,*args):
    print(account_id)
    displaydata=Result.objects.get(account_id=account_id)
    print(displaydata)
    updatedata=Result.objects.get(account_id=account_id)
    print(updatedata)
    print(account_id)
    if request.method == "POST":
        print('post')
        form=editresultform(request.POST or None,instance=updatedata)
        #error here
        if form.is_valid():
            print('inform')
            form.save()
            #messages.success(request,"Announcement updated")
            return redirect("../")
            #return render(request,'common/announcementedit.html',{'editdata':updatedata})
        else:
            return HttpResponse(messages)    
    return render(request,'staff/editresult.html',{'editdata':displaydata})


def staff_result_delete(request,course_code,account_id):
    obj=Result.objects.get(account_id=account_id)
    print(obj)
    print(request.method)
    if request.method=="GET":
        print('get')
        obj.delete()
        return redirect("../")
    else:
        return HttpResponse(messages)
    return render(request,'staff/stdresult.html',{'student':obj}) 

# @login_required(login_url=common.views.login_view)
def staff_profile_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        if not request.session.get('userId'):
            userEmail = request.user.email
            user = Staff.objects.get(email=userEmail)
            request.session['userId'] = user.employee_id
    obj=Staff.objects.filter(employee_id=request.session['userId'])
    for i in obj:
        br=i.branch
    print(br)
    branch=Branch.objects.filter(code=br)
    print(branch)
    return render(request, "staff/profile.html",{'staff':obj,'branch':branch})

# @login_required(login_url=common.views.login_view)
def staff_profile_edit(request,account_id,*args,**kwargs):
    print(account_id)
    displaydata=Staff.objects.get(account_id=account_id)
    print(displaydata)
    updatedata=Staff.objects.get(account_id=account_id)
    print(account_id)
    if request.method == "POST":
        print('post')
        form=editforms1(request.POST or None,instance=updatedata)
        #error here
        if form.is_valid():
            form.save()
            #messages.success(request,"Your Profile updated")
            #return render(request,'admins/adminprofileedit.html',{'editdata':updatedata})
            return redirect("../profile")
        else:
            return HttpResponse(messages)
    return render(request,'staff/edit_profile.html',{'editdata':displaydata})




