from django.shortcuts import render,redirect,get_object_or_404
from django.shortcuts import render,redirect, get_object_or_404
from datetime import datetime
from common.announcementform import announcementform
from common.models import Announcement, Assignment
from staff.forms2 import editforms2
from common.methods import id_generator, assignment_id_generator
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from  . import forms
from django.contrib import messages
from .models import Branch
from staff.models import Staff
from staff.forms import CreateAssignmentForm
from common.models import  Course, CourseFaculty
from students.models import Student
from staff.forms import resultform
from students.models import Result
from staff.forms import editresultform
import collections
from staff.forms import editforms1


# Create your views here.

def staff_home_view(request, *args, **kwargs):
    time = datetime.now()
    announcement_data=reversed(Announcement.objects.all())
    print(announcement_data)
    #for i in announcement_data:
        #print(i.title)
    currentTime = time.strftime("%d/%m/%Y %I:%M %p")
    context = {
        'timestamp': currentTime,
        
    }
    return render(request, "staff/home.html",{'context':context,'announcement_data':announcement_data})

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
def staff_courses_view(request, course_code, *args, **kwargs):
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
    return render(request, "staff/courses.html", context)

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
                print(dict(request.FILES))
                if not startDate:
                    startDate = c
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

        context = {
            'courses' : courseList,
            'selectedCourse' : selectedCourse,
            'selectedAssignment' : selectedAssignment,
            'students': students,
        }
    return render(request, 'staff/manage_assignment.html', context)

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
def staff_attendance_view(request, *args, **kwargs):
    return render(request, "staff/attendance.html")

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
def result_view(request, *args,branch_code):
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
            new_marks=details['marks']
            new_exam=details['exam']
            
            print(new_enrolment)
            print(new_branch)
            print(new_sem)
            newresult = Result(account_id=str(new_account_id),
                                enrolment=str(new_enrolment),
                                branch=str(new_branch),
                                sem=str(new_sem),
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


