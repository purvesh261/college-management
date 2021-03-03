from django.shortcuts import render, redirect, get_object_or_404, reverse
from students.models import Student
from admins.forms1 import editforms1
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import common
from staff.models import Staff
from  . import forms
from .forms import editforms, AddBranchForm, EditBranchForm, AddCourseForm, AddFacultyForm
from .models import Branch
from datetime import datetime
from common.forms import LoginForm
from common.methods import id_generator, course_id_generator
from common.announcementform import announcementform
from common.models import Announcement, Course, CourseFaculty
from admins.forms2 import editforms2

'''
TODO:
Wherever storing branch information, change from branch name to branch code.
'''

#admin announcement

#@login_required(login_url=common.views.login_view)
def admin_announcement(request,*args,**kwargs):
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
            #messages.success(request,"Announcement Added")
            return redirect("../announcement/")
        else:
            return HttpResponse(messages)
    return render(request,"common/announcement.html",{'announcementform1':announcementform1})



#@login_required(login_url=common.views.login_view)
def admin_add_announcement(request,*args,**kwargs):
    obj=Announcement.objects.all()
    return render(request,"common/allannouncement.html",{'announcementform1':obj})

#@login_required(login_url=common.views.login_view)
def announcement_done(request,*args,**kwargs):
    announcementform1 = announcementform(request.POST or None)
    return render(request,"common/announcement.html",{'announcementform1':announcementform1})

#admin announcement edit 

#@login_required(login_url=common.views.login_view)
def admins_announcement_edit(request,account_id):
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
            #return render(request,'common/announcement_updated.html')
        else:
            return HttpResponse(messages)
    return render(request,'common/announcementedit.html',{'editdata':displaydata})

#@login_required(login_url=common.views.login_view)
#def edit_announcement(request,account_id):
        #return render(request,'common/announcemet_updated.html')

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
#             #return redirect("../edit-announcement/")
#             #return render(request,'common/announcement_updated.html',{'editdata':updatedata})
#             return render(request,'common/announcement_updated.html')
#         else:
#             return HttpResponse(messages)

    
#announcement delete
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

#@login_required(login_url=common.views.login_view)
def admins_home_view(request, *args, **kwargs):
    time = datetime.now()
    announcement_data=reversed(Announcement.objects.all())
    currentTime = time.strftime("%d/%m/%Y %I:%M %p")
    context = {
        'timestamp': currentTime,
    }
    return render(request, "admins/home.html",{'context':context,'announcement_data':announcement_data})

#@login_required(login_url=common.views.login_view)
def admins_students_view(request, *args, **kwargs):
    return render(request, "admins/students.html")

#@login_required(login_url=common.views.login_view)
def admins_staff_view(request, *args, **kwargs):
    return render(request, "admins/staff.html")

#@login_required(login_url=common.views.login_view)
# admin profile edit
def admins_profile_view(request, *args, **kwargs):
    obj=Staff.objects.filter(isAdmin=True)
    print(obj)
    return render(request, "admins/profile.html",{'admin':obj})

#@login_required(login_url=common.views.login_view)
def admins_profile_edit(request,account_id):
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
    return render(request,'admins/adminprofileedit.html',{'editdata':displaydata})

# def edit_profile(request,account_id):
#     updatedata=Staff.objects.get(account_id=account_id)
#     print(account_id)
#     if request.method == "POST":
#         print('post')
#         form=editforms1(request.POST or None,instance=updatedata)
#         #error here
#         if form.is_valid():
#             form.save()
#             messages.success(request,"Your Profile updated")
#             return render(request,'admins/adminprofileedit.html',{'editdata':updatedata})
#         else:
#             return HttpResponse(messages)
#     print(form.errors)


# for data extraction for student
#@login_required(login_url=common.views.login_view)
def admins_student_pending_detail_view(request,*args,**kwargs):
    obj=Student.objects.filter(isPending=True)
    print(obj)
    return render(request,"admins/students.html",{'student':obj})
    
# load approved acounts
# @login_required(login_url=common.views.login_view)  
def admins_student_approved_detail_view(request,*args,**kwargs):
    obj=Student.objects.filter(isPending=False)
    return render(request,"admins/studentapproved.html",{'student':obj})


#approve page will be called to to approve accounts
#@login_required(login_url=common.views.login_view)
def admins_student_approve(request,account_id):
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
            #messages.success(request,"Student Approved")
            #return render(request,'admins/studentapprove.html',{'editdata':updatedata})
            return redirect("../student-account-pending-details")
        else:
            return HttpResponse(messages)
    return render(request,'admins/studentapprove.html',{'editdata':displaydata})


#edit approved details will be validated
# def approve_student(request,account_id):
#     updatedata=Student.objects.get(account_id=account_id)
#     print(account_id)
#     if request.method == "POST":
#         print('post')
#         form=editforms(request.POST or None,instance=updatedata)
#         #error here
#         if form.is_valid():
#             form.save()
#             messages.success(request,"Student Approved")
#             return render(request,'admins/studentapprove.html',{'editdata':updatedata})
#         else:
#             return HttpResponse(messages)
#     print(form.errors)

#edit page will be called for unapproved details of students

#edit student details
#@login_required(login_url=common.views.login_view)
def admins_student_detail_view(request,*args,**kwargs):
    return render(request,"admins/students.html")
  
#@login_required(login_url=common.views.login_view)
def admins_student_edit(request,account_id):
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
            #messages.success(request,"student data updated")
            #return render(request,'admins/studentedit.html',{'editdata':updatedata})
            return redirect("../students")
        else:
            return HttpResponse(messages)
    #print(form.errors)
    return render(request,'admins/studentedit.html',{'editdata':displaydata})

#to edit unapproved students
#@login_required(login_url=common.views.login_view)
# def edit_student(request,account_id):
#     updatedata=Student.objects.get(account_id=account_id)
#     print(account_id)
#     if request.method == "POST":
#         print('post')
#         form=editforms(request.POST or None,instance=updatedata)
#         #error here
#         if form.is_valid():
#             form.save()
#             messages.success(request,"student data updated")
#             return render(request,'admins/studentedit.html',{'editdata':updatedata})
#         else:
#             return HttpResponse(messages)
#     print(form.errors)



#for extraction of staff
#@login_required(login_url=common.views.login_view)
def admins_staff_pending_detail_view(request,*args,**kwargs):
    obj=Staff.objects.filter(isPending=True)
    print(obj)
    return render(request,"admins/staff.html",{'staff':obj})

#@login_required(login_url=common.views.login_view)
def admins_staff_approved_detail_view(request,*args,**kwargs):
    obj=Staff.objects.filter(isPending=False)
    return render(request,"admins/staffapproved.html",{'staff':obj})

#to approve staff accounts
#@login_required(login_url=common.views.login_view)
def admins_staff_approve(request,account_id):
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
            #messages.success(request,"Staff Member Approved")
            #return render(request,'admins/staffapprove.html',{'editdata':updatedata})
            return redirect("../staff-account-pending-details")
        else:
            return HttpResponse(messages)
    return render(request,'admins/staffapprove.html',{'editdata':displaydata})

# def approve_staff(request,account_id):
#     updatedata=Staff.objects.get(account_id=account_id)
#     print(account_id)
#     if request.method == "POST":
#         print('post')
#         form=editforms1(request.POST or None,instance=updatedata)
#         #error here
#         if form.is_valid():
#             form.save()
#             messages.success(request,"Staff Member Approved")
#             return render(request,'admins/staffapprove.html',{'editdata':updatedata})
#         else:
#             return HttpResponse(messages)
#     print(form.errors)

# edit staff details
#@login_required(login_url=common.views.login_view)
def admins_staff_edit(request,account_id):
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
            #messages.success(request,"Staff Member data updated")
            #return render(request,'admins/staffedit.html',{'editdata':updatedata})
            return redirect("../staff")
        else:
            return HttpResponse(messages)
    return render(request,'admins/staffedit.html',{'editdata':displaydata})

# def edit_staff(request,account_id):
#     updatedata=Staff.objects.get(account_id=account_id)
#     print(account_id)
#     if request.method == "POST":
#         print('post')
#         form=editforms1(request.POST or None,instance=updatedata)
#         #error here
#         if form.is_valid():
#             form.save()
#             messages.success(request,"Staff Member data updated")
#             return render(request,'admins/staffedit.html',{'editdata':updatedata})
#         else:
#             return HttpResponse(messages)
#     print(form.errors)

#@login_required(login_url=common.views.login_view)
def admins_courses_view(request, *args, **kwargs):
    branches = Branch.objects.all().order_by('branch_name')
    branch_info = {}
    for branch in branches:
        branch_info[branch.branch_name] = {}
        branch_info[branch.branch_name]["staff"] = len(Staff.objects.filter(branch=branch.branch_name, isPending=False))
        hod = Staff.objects.filter(designation="Head Of Department", branch=branch.branch_name, isPending=False)

        if hod:
            branch_info[branch.branch_name]["hod"] = hod[0].firstName + " " + hod[0].lastName
        else:
            branch_info[branch.branch_name]["hod"] = "Unspecified"
        courses = Course.objects.filter(branch=branch.branch_name)
        branch_info[branch.branch_name]["number"] = len(courses)
    context = {
        'branches' : branches,
        'branch_info': branch_info,
    }
    return render(request, "admins/courses.html", context)

#@login_required(login_url=common.views.login_view)
def create_branch_view(request, *args, **kwargs):
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
    else:
        form = AddBranchForm(request.POST or None)
        for field in form.errors:
            form[field].field.widget.attrs['class'] += 'error'

    context = {
        'form': form,
    }
    return render(request, "admins/add_branch.html", context)

#@login_required(login_url=common.views.login_view)
def branch_view(request, branch_code, *args, **kwargs):
    selectedBranch = get_object_or_404(Branch,code=branch_code)
    staffOfBranch = Staff.objects.filter(branch=selectedBranch.branch_name, isPending=False)
    coursesInBranch = Course.objects.filter(branch=branch_code).order_by('semester')
    context = {
        "branch":selectedBranch,
        "staff":staffOfBranch,
        "courses":coursesInBranch,
    }
    return render(request, "admins/branch_page.html",context)

#@login_required(login_url=common.views.login_view)
def edit_branch_view(request, branch_code, *args, **kwargs):
    selectedBranch = get_object_or_404(Branch,code=branch_code)
    print("ok",selectedBranch)
    print(selectedBranch)
    intial_data = {
        'branchName':selectedBranch.branch_name,
        'branchCode':selectedBranch.code,
        'description':selectedBranch.description
    }
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

#@login_required(login_url=common.views.login_view)
def add_course_view(request, *args, **kwargs):
    '''
    TODO: 
    change the branch field from branch name to branch code
    '''
    if request.method == "POST":
        form = AddCourseForm(request.POST or None)
        if form.is_valid():
            details = form.cleaned_data
            newBranch = details['branch']
            print("hellollooooo",newBranch)
            # newBranchCode =  Branch.objects.filter(branch_name=newBranch)[0].code
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

def manage_course_view(request,course_code, *args, **kwargs):
    selectedCourse = get_object_or_404(Course,course_id=course_code)
    courseBranch = Branch.objects.get(code=selectedCourse.branch)
    CourseFacultySet = CourseFaculty.objects.filter(course_id=selectedCourse)

    assignedFaculties = []
    for faculty in CourseFacultySet:
        currentFaculty = Staff.objects.get(employee_id=faculty.faculty_id)
        assignedFaculties.append([faculty.faculty_id, currentFaculty.firstName + " " + currentFaculty.lastName])
    
    facultyList = Staff.objects.filter(branch=courseBranch.branch_name, isPending=False).order_by('firstName')

    for faculty in facultyList:
        add = True
        for assfac in assignedFaculties:
            print(assfac[0], faculty.employee_id)
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

def remove_faculty_view(request,course_code,emp_id, *args, **kwargs):
    deleteObj = CourseFaculty.objects.get(faculty_id=emp_id)
    deleteObj.delete()
    return redirect('/college-admin/courses/' + course_code)

#@login_required(login_url=common.views.login_view)
def logout_view(request, *args, **kwargs):
    logout(request)
    # form = LoginForm(request.post or None)
    # context = {
    #     'form':form,
    # }
    return redirect(common.views.login_view)


   

    