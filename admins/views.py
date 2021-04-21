from django.shortcuts import render, redirect, get_object_or_404, reverse
from students.models import Student
from admins.forms1 import editforms1
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django import forms as djforms
import common
from django.contrib.auth.models import User
from staff.models import Staff
from  . import forms
from .forms import editforms, AddBranchForm, EditBranchForm, AddCourseForm, AddFacultyForm,EditCourseForm
from .models import Branch
from datetime import datetime
from common.forms import LoginForm
from common.methods import id_generator, course_id_generator
from common.announcementform import announcementform
from common.models import Announcement, Course, CourseFaculty
from admins.forms2 import editforms2
from django.template.defaulttags import register


#admin announcement

@login_required(login_url=common.views.login_view)
def admin_announcement(request,*args,**kwargs):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    userEmail = request.user.email
    user = Staff.objects.filter(email=userEmail)
    if not user:
        return render(request, "common/no_permission.html")
    else:
        if not user[0].isAdmin:
            return render(request, "common/no_permission.html")

    announcementform1 = announcementform(request.POST or None)
    if request.method == 'POST':
        announcementform1 = announcementform(request.POST or None)
        if announcementform1.is_valid():
            details = announcementform1.cleaned_data
            new_title=details['title']
            new_description=details['description']
            new_account_id = id_generator()
            newannouncement = Announcement(title=str(new_title.capitalize()),
                                           description=str(new_description.capitalize()),
                                           account_id=str(new_account_id))
            print(newannouncement)
            newannouncement.save()
            return redirect("../announcement/")
        else:
            return HttpResponse(messages)
    return render(request,"common/announcement.html",{'announcementform1':announcementform1})



@login_required(login_url=common.views.login_view)
def admin_add_announcement(request,*args,**kwargs):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    userEmail = request.user.email
    user = Staff.objects.filter(email=userEmail)
    if not user:
        return render(request, "common/no_permission.html")
    else:
        if not user[0].isAdmin:
            return render(request, "common/no_permission.html")
    obj=Announcement.objects.all()
    return render(request,"common/allannouncement.html",{'announcementform1':obj})

@login_required(login_url=common.views.login_view)
def announcement_done(request,*args,**kwargs):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    userEmail = request.user.email
    user = Staff.objects.filter(email=userEmail)
    if not user:
        return render(request, "common/no_permission.html")
    else:
        if not user[0].isAdmin:
            return render(request, "common/no_permission.html")

    announcementform1 = announcementform(request.POST or None)
    return render(request,"common/announcement.html",{'announcementform1':announcementform1})

#admin announcement edit 

@login_required(login_url=common.views.login_view)
def admins_announcement_edit(request,account_id):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    userEmail = request.user.email
    user = Staff.objects.filter(email=userEmail)
    if not user:
        return render(request, "common/no_permission.html")
    else:
        if not user[0].isAdmin:
            return render(request, "common/no_permission.html")

    displaydata=Announcement.objects.get(account_id=account_id)
    updatedata=Announcement.objects.get(account_id=account_id)
    if request.method == "POST":
        form=editforms2(request.POST or None,instance=updatedata)
        #error here
        if form.is_valid():
            form.save()
            return redirect("../all-announcement")
        else:
            return HttpResponse(messages)
    return render(request,'common/announcementedit.html',{'editdata':displaydata})


#announcement delete
@login_required(login_url=common.views.login_view)
def staff_delete_view(request, account_id):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    userEmail = request.user.email
    user = Staff.objects.filter(email=userEmail)
    if not user:
        return render(request, "common/no_permission.html")
    else:
        if not user[0].isAdmin:
            return render(request, "common/no_permission.html")

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

@login_required(login_url=common.views.login_view)
def admins_home_view(request, *args, **kwargs):
    
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    userEmail = request.user.email
    user = Staff.objects.filter(email=userEmail)
    if not user:
        return render(request, "common/no_permission.html")
    else:
        if not user[0].isAdmin:
            return render(request, "common/no_permission.html")
    time = datetime.now()
    announcement_data=reversed(Announcement.objects.all())
    currentTime = time.strftime("%d/%m/%Y %I:%M %p")
    obj1=Student.objects.filter(isPending=True)
    obj2=Staff.objects.filter(isPending=True)
    s1=len(obj1)
    s2=len(obj2)
    print(s1)
    context = {
        'timestamp': currentTime,
    }

    return render(request, "admins/home.html",{'context':context,'announcement_data':announcement_data,'student':s1,'staff':s2})

@login_required(login_url=common.views.login_view)
def admins_students_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    userEmail = request.user.email
    user = Staff.objects.filter(email=userEmail)
    if not user:
        return render(request, "common/no_permission.html")
    else:
        if not user[0].isAdmin:
            return render(request, "common/no_permission.html")

    branches = Branch.objects.all().order_by('branch_name')
    print(branches)
    context = {
        'branches' : branches,
            }
    return render(request, "admins/students.html",context)

@login_required(login_url=common.views.login_view)
def admins_student_sem_view(request,branch_code,*args):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    userEmail = request.user.email
    user = Staff.objects.filter(email=userEmail)
    if not user:
        return render(request, "common/no_permission.html")
    else:
        if not user[0].isAdmin:
            return render(request, "common/no_permission.html")

    branches = Branch.objects.all().order_by('branch_name')
    b1=get_object_or_404(Branch,code=branch_code)
    print(b1.branch_name)
    print(branch_code)
    return render(request,'admins/student_sem.html',{'branch':b1.branch_name})


@login_required(login_url=common.views.login_view)
def admins_profile_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    userEmail = request.user.email
    user = Staff.objects.filter(email=userEmail)
    if not user:
        return render(request, "common/no_permission.html")
    else:
        if not user[0].isAdmin:
            return render(request, "common/no_permission.html")

    obj = Staff.objects.filter(email=userEmail)[0]
    branch = obj.branch
    branch = Branch.objects.get(code=branch)
    branch = branch.branch_name
    # obj=Staff.objects.filter(isAdmin=True)
    print(obj)
    return render(request, "admins/profile.html",{'admin':obj, 'branch':branch})

@login_required(login_url=common.views.login_view)
def admins_profile_edit(request,account_id):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    userEmail = request.user.email
    user = Staff.objects.filter(email=userEmail)
    if not user:
        return render(request, "common/no_permission.html")
    else:
        if not user[0].isAdmin:
            return render(request, "common/no_permission.html")

    displaydata=Staff.objects.get(account_id=account_id)
    updatedata=Staff.objects.get(account_id=account_id)
    if request.method == "POST":
        form=editforms1(request.POST or None,instance=updatedata)
        #error here
        if form.is_valid():
            details = form.cleaned_data
            fName = details['firstName']
            lName = details['lastName']
            email = details['email']
            form.save()
            user = User.objects.get(email=request.user.email)
            user.first_name = fName
            user.last_name = lName
            user.email = email
            user.save()

            return redirect("../profile")
        else:
            return HttpResponse(messages)
    return render(request,'admins/adminprofileedit.html',{'editdata':displaydata})

# for data extraction for student
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@login_required(login_url=common.views.login_view)
def admins_student_detail_view(request,branch_code, *args):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    userEmail = request.user.email
    user = Staff.objects.filter(email=userEmail)
    if not user:
        return render(request, "common/no_permission.html")
    else:
        if not user[0].isAdmin:
            return render(request, "common/no_permission.html")
    sem=(request.path.split('/')) #split the whole url /
    s1=sem[4] #to fetch the sem from url
    print('sem',sem[4])
    b1=get_object_or_404(Branch,code=branch_code) #get the branch bane using branch code
    b2=b1.branch_name #get the branch name
    print(b2) #print branch name
    obj=Student.objects.filter(sem=s1,branch=branch_code,isPending=False)
    branch_dict={}
    for student in obj:
        branch_dict[student.enrolment] = Branch.objects.get(code=student.branch).branch_name
    return render(request,"admins/students_list.html",{'student':obj,'branch_name':branch_dict})


@login_required(login_url=common.views.login_view)
def admins_student_pending_detail_view(request,branch_code,*args,**kwargs):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    userEmail = request.user.email
    user = Staff.objects.filter(email=userEmail)
    if not user:
        return render(request, "common/no_permission.html")
    else:
        if not user[0].isAdmin:
            return render(request, "common/no_permission.html")

    sem=(request.path.split('/')) #split the whole url /
    s1=sem[4] #to fetch the sem from url
    print('sem',sem[4])
    b1=get_object_or_404(Branch,code=branch_code) #get the branch bane using branch code
    b2=b1.branch_name #get the branch name
    print(b2) #print branch name
    obj=Student.objects.filter(sem=s1,branch=branch_code,isPending=True)
    branch_dict={}
    for student in obj:
        branch_dict[student.enrolment] = Branch.objects.get(code=student.branch).branch_name
    print(obj)
    print(branch_dict)
    return render(request,"admins/student_pending.html",{'student':obj,'branch_name':branch_dict})
    

# approve page will be called to to approve accounts
@login_required(login_url=common.views.login_view)
def admins_student_approve(request,account_id,branch_code):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    userEmail = request.user.email
    user = Staff.objects.filter(email=userEmail)
    if not user:
        return render(request, "common/no_permission.html")
    else:
        if not user[0].isAdmin:
            return render(request, "common/no_permission.html")

    print(account_id)
    displaydata=Student.objects.get(account_id=account_id)
    print(displaydata)
    updatedata=Student.objects.get(account_id=account_id)
    print(account_id)
    branch_name=Branch.objects.all()
    if request.method == "POST":
        form=editforms(request.POST or None,instance=updatedata)
        #error here
        if form.is_valid():
            form.save()
            return redirect("../student-account-pending-details")
        else:
            return HttpResponse(messages)
    return render(request,'admins/studentapprove.html',{'editdata':displaydata,'branch_name':branch_name})
  
@login_required(login_url=common.views.login_view)
def admins_student_edit(request,account_id,branch_code):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    userEmail = request.user.email
    user = Staff.objects.filter(email=userEmail)
    if not user:
        return render(request, "common/no_permission.html")
    else:
        if not user[0].isAdmin:
            return render(request, "common/no_permission.html")

    displaydata=Student.objects.get(account_id=account_id)
    updatedata=Student.objects.get(account_id=account_id)
    branch_name=Branch.objects.all()
    if request.method == "POST":
        form=editforms(request.POST or None,instance=updatedata)
        #error here
        if form.is_valid():
            form.save()
            return redirect("../")
        else:
            return HttpResponse(messages)
    #print(form.errors)
    return render(request,'admins/studentedit.html',{'editdata':displaydata,'branch_name':branch_name})

@login_required(login_url=common.views.login_view)
def admins_staff_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    userEmail = request.user.email
    user = Staff.objects.filter(email=userEmail)
    if not user:
        return render(request, "common/no_permission.html")
    else:
        if not user[0].isAdmin:
            return render(request, "common/no_permission.html")

    branches = Branch.objects.all().order_by('branch_name')
    print(branches)
    context = {
        'branches' : branches,
            }
    return render(request, "admins/staff.html",context)

@login_required(login_url=common.views.login_view)
def admins_staff_detail_view(request,branch_code,*args):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    userEmail = request.user.email
    user = Staff.objects.filter(email=userEmail)
    if not user:
        return render(request, "common/no_permission.html")
    else:
        if not user[0].isAdmin:
            return render(request, "common/no_permission.html")

    obj=Staff.objects.filter(isPending=False,branch=branch_code)
    branch_dict={}
    for staff in obj:
        branch_dict[staff.employee_id] = Branch.objects.get(code=staff.branch).branch_name
    return render(request,"admins/staff_list.html",{'staff':obj,'branch_name':branch_dict})


@login_required(login_url=common.views.login_view)
def admins_staff_pending_detail_view(request,*args,**kwargs):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    userEmail = request.user.email
    user = Staff.objects.filter(email=userEmail)
    if not user:
        return render(request, "common/no_permission.html")
    else:
        if not user[0].isAdmin:
            return render(request, "common/no_permission.html")

    obj=Staff.objects.filter(isPending=True)
    print(obj)
    branch_dict={}
    for staff in obj:
        branch_dict[staff.employee_id] = Branch.objects.get(code=staff.branch).branch_name
    return render(request,"admins/staff_pending.html",{'staff':obj,'branch_name':branch_dict})

#to approve staff accounts
@login_required(login_url=common.views.login_view)
def admins_staff_approve(request,account_id,branch_code):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    userEmail = request.user.email
    user = Staff.objects.filter(email=userEmail)
    if not user:
        return render(request, "common/no_permission.html")
    else:
        if not user[0].isAdmin:
            return render(request, "common/no_permission.html")

    displaydata=Staff.objects.get(account_id=account_id)
    updatedata=Staff.objects.get(account_id=account_id)
    branch_name=Branch.objects.all()

    if request.method == "POST":
        form=editforms1(request.POST or None,instance=updatedata)
        if form.is_valid():
            
            form.save()
            return redirect("../staff-account-pending-details")
        else:
            return HttpResponse(messages)
    return render(request,'admins/staffapprove.html',{'editdata':displaydata,'branch_name':branch_name})

# edit staff details
@login_required(login_url=common.views.login_view)
def admins_staff_edit(request,account_id,branch_code):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    userEmail = request.user.email
    user = Staff.objects.filter(email=userEmail)
    if not user:
        return render(request, "common/no_permission.html")
    else:
        if not user[0].isAdmin:
            return render(request, "common/no_permission.html")

    displaydata=Staff.objects.get(account_id=account_id)
    updatedata=Staff.objects.get(account_id=account_id)
    branch_name=Branch.objects.all()
    if request.method == "POST":
        form=editforms1(request.POST or None,instance=updatedata)
        #error here
        if form.is_valid():
            form.save()
            return redirect("../")
        else:
            return HttpResponse(messages)
    return render(request,'admins/staffedit.html',{'editdata':displaydata,'branch_name':branch_name})


@login_required(login_url=common.views.login_view)
def admins_courses_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    userEmail = request.user.email
    user = Staff.objects.filter(email=userEmail)
    if not user:
        return render(request, "common/no_permission.html")
    else:
        if not user[0].isAdmin:
            return render(request, "common/no_permission.html")

    branches = Branch.objects.all().order_by('branch_name')
    branch_info = {}
    for branch in branches:
        branch_info[branch.branch_name] = {}
        branch_info[branch.branch_name]["staff"] = len(Staff.objects.filter(branch=branch.branch_name, isPending=False))
        hod = Staff.objects.filter(designation="Head Of Department", branch=branch.branch_name, isPending=False)
        # print(branch_info)
        if hod:
            branch_info[branch.branch_name]["hod"] = hod[0].firstName + " " + hod[0].lastName
        else:
            branch_info[branch.branch_name]["hod"] = "Unspecified"
        courses = Course.objects.filter(branch=branch.code)
        print(courses)
        branch_info[branch.branch_name]["number"] = len(courses)
    context = {
        'branches' : branches,
        'branch_info': branch_info,
    }
    return render(request, "admins/courses.html", context)

@login_required(login_url=common.views.login_view)
def create_branch_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    userEmail = request.user.email
    user = Staff.objects.filter(email=userEmail)
    if not user:
        return render(request, "common/no_permission.html")
    else:
        if not user[0].isAdmin:
            return render(request, "common/no_permission.html")

    if request.method == "POST":
        form = AddBranchForm(request.POST or None)
        if form.is_valid():
            details = form.cleaned_data
            newBranchName = details['branch_name']
            newCode = details['code']
            newDescription = details['description']

            newBranch = Branch(
                branch_name=str(newBranchName.capitalize()),
                code=str(newCode),
                description=str(newDescription)
            )
            newBranch.save()
            return redirect('../courses')
    else:
        form = AddBranchForm(request.POST or None)
        for field in form.errors:
            form[field].field.widget.attrs['class'] += 'error'

    context = {
        'form': form,
    }
    return render(request, "admins/add_branch.html", context)

@login_required(login_url=common.views.login_view)
def branch_view(request, branch_code, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    userEmail = request.user.email
    user = Staff.objects.filter(email=userEmail)
    if not user:
        return render(request, "common/no_permission.html")
    else:
        if not user[0].isAdmin:
            return render(request, "common/no_permission.html")

    selectedBranch = get_object_or_404(Branch,code=branch_code)
    print(selectedBranch.branch_name)
    staffOfBranch = Staff.objects.filter(branch=selectedBranch.code, isPending=False)
    coursesInBranch = Course.objects.filter(branch=branch_code).order_by('semester')
    print(staffOfBranch)
    context = {
        "branch":selectedBranch,
        "staff":staffOfBranch,
        "courses":coursesInBranch,
    }
    return render(request, "admins/branch_page.html",context)

@login_required(login_url=common.views.login_view)
def edit_branch_view(request, branch_code, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    userEmail = request.user.email
    user = Staff.objects.filter(email=userEmail)
    if not user:
        return render(request, "common/no_permission.html")
    else:
        if not user[0].isAdmin:
            return render(request, "common/no_permission.html")

    selectedBranch = get_object_or_404(Branch,code=branch_code)
    if request.method == "POST":
        form = EditBranchForm(request.POST, instance=selectedBranch)
        if form.is_valid():
            form.save()
            return redirect('..')
    else:
        form = EditBranchForm(request.POST or None, instance=selectedBranch)
        for field in form.errors:
            form[field].field.widget.attrs['class'] += 'error'

    context = {
        'form': form,
    }
    
    return render(request,'admins/edit_branch.html',context)

@login_required(login_url=common.views.login_view)
def add_course_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    userEmail = request.user.email
    user = Staff.objects.filter(email=userEmail)
    if not user:
        return render(request, "common/no_permission.html")
    else:
        if not user[0].isAdmin:
            return render(request, "common/no_permission.html")

    if request.method == "POST":
        form = AddCourseForm(request.POST or None)
        if form.is_valid():
            details = form.cleaned_data
            newBranch = details['branch']
            newCourseId = course_id_generator(newBranch)
            newCourse = details['course_name']
            newSubjectCode = details['subject_code']
            newDescription = details['description']
            newSemester = details['semester']
            newCourseCredits = details['course_credits']
            newCourseType = details['course_type']
            newStartDate = details['start_date']
            newEndDate = details['end_date']
            newActive = True
            if details['active'] == 'No':
                newActive = False

            newCourse = Course(
                course_id=newCourseId,
                course_name=newCourse,
                description=newDescription,
                subject_code=newSubjectCode,
                branch=newBranch,
                semester=newSemester,
                course_credits=newCourseCredits,
                course_type=newCourseType,
                start_date=newStartDate,
                end_date=newEndDate,
                active=newActive
            )
            newCourse.save()
            path = "college-admin/courses/" + newBranch + "/"
            return redirect('..')
    else:
        form = AddCourseForm(request.POST or None)
        for field in form.errors:
            form[field].field.widget.attrs['class'] += 'error'
    context = {
        'form': form,
    }

    return render(request,'admins/add_course.html',context)

@login_required(login_url=common.views.login_view)
def manage_course_view(request,course_code, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    userEmail = request.user.email
    user = Staff.objects.filter(email=userEmail)
    if not user:
        return render(request, "common/no_permission.html")
    else:
        if not user[0].isAdmin:
            return render(request, "common/no_permission.html")

    selectedCourse = get_object_or_404(Course,course_id=course_code)
    courseBranch = Branch.objects.get(code=selectedCourse.branch)
    CourseFacultySet = CourseFaculty.objects.filter(course_id=selectedCourse)

    assignedFaculties = []
    for faculty in CourseFacultySet:
        currentFaculty = Staff.objects.get(employee_id=faculty.faculty_id)
        assignedFaculties.append([faculty.faculty_id, currentFaculty.firstName + " " + currentFaculty.lastName])
    
    facultyList = Staff.objects.filter(branch=courseBranch.code, isPending=False).order_by('firstName')

    for faculty in facultyList:
        add = True
        for assfac in assignedFaculties:
            if assfac[0] == faculty.employee_id:
                add = False
        if add:
            facultyChoiceList = ((faculty.employee_id,faculty.firstName + " " + faculty.lastName))
    if request.method == "POST":
        form = AddFacultyForm(facultyList,assignedFaculties, request.POST or None)
        if form.is_valid():
            details = form.cleaned_data
            faculty = details['faculty']
            course = selectedCourse
            NewFaculty = CourseFaculty(course_id=course,
                            faculty_id=faculty)
            NewFaculty.save()
            return redirect('.')
    else:
        form = AddFacultyForm(facultyList, assignedFaculties)
        for field in form.errors:
            form[field].field.widget.attrs['class'] += 'error'
    context = {
        'course': selectedCourse,
        'branch': courseBranch,
        'form': form,
        'faculties': assignedFaculties
    }

    return render(request,"admins/manage_course.html", context)

@login_required(login_url=common.views.login_view)
def edit_course_view(request, course_code, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    userEmail = request.user.email
    user = Staff.objects.filter(email=userEmail)
    if not user:
        return render(request, "common/no_permission.html")
    else:
        if not user[0].isAdmin:
            return render(request, "common/no_permission.html")

    selectedCourse = get_object_or_404(Course,course_id=course_code)
    initialSubCode = selectedCourse.subject_code
    if request.method == 'POST':
        editForm = EditCourseForm(request.POST or None, instance=selectedCourse)
        if editForm.is_valid():
            details = editForm.cleaned_data
            newSubCode = details['subject_code']
            if initialSubCode != newSubCode:
                try:
                    if Course.objects.filter(subject_code=newSubCode):
                        raise djforms.ValidationError("Subject code already exists.")
                except djforms.ValidationError as e:
                    editForm.add_error('subject_code', e)
                    return render(request,"admins/edit_course.html", {'form': editForm})
                
            editForm.save()
            return redirect('..')
    else:
        editForm = EditCourseForm(instance=selectedCourse)
        for field in editForm.errors:
            editForm[field].field.widget.attrs['class'] += 'error'

    context = {
        'form': editForm,
    }
    return render(request,"admins/edit_course.html", context)

@login_required(login_url=common.views.login_view)
def remove_faculty_view(request,course_code,emp_id, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    userEmail = request.user.email
    user = Staff.objects.filter(email=userEmail)
    if not user:
        return render(request, "common/no_permission.html")
    else:
        if not user[0].isAdmin:
            return render(request, "common/no_permission.html")

    DeleteCourse = Course.objects.get(course_id=course_code)
    deleteObj = CourseFaculty.objects.get(faculty_id=emp_id,course_id=DeleteCourse)
    deleteObj.delete()
    return redirect('/college-admin/courses/' + course_code)

@login_required(login_url=common.views.login_view)
def logout_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    userEmail = request.user.email
    user = Staff.objects.filter(email=userEmail)
    if not user:
        return render(request, "common/no_permission.html")
    else:
        if not user[0].isAdmin:
            return render(request, "common/no_permission.html")

    logout(request)
    return redirect(common.views.login_view)


   

    