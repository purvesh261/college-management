from django.shortcuts import render, redirect
from students.models import Student
from admins.forms import editforms
from admins.forms1 import editforms1
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import common
from staff.models import Staff
from  . import forms
from datetime import datetime
from common.forms import LoginForm

from common.methods import id_generator
from common.announcementform import announcementform
from common.models import Announcement
from admins.forms2 import editforms2


#admin announcement

#@login_required(login_url=common.views.login_view)
def admin_announcement(request,*args,**kwargs):
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




# Create your views here.
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
def admins_courses_view(request, *args, **kwargs):
    return render(request, "admins/courses.html")

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
def admins_student_approved_detail_view(request,*args,**kwargs):
    obj=Student.objects.filter(isPending=False)
    return render(request,"admins/studentapproved.html",{'student':obj})


#approve page will be called to to approve accounts
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
def admins_staff_pending_detail_view(request,*args,**kwargs):
    obj=Staff.objects.filter(isPending=True)
    print(obj)
    return render(request,"admins/staff.html",{'staff':obj})

def admins_staff_approved_detail_view(request,*args,**kwargs):
    obj=Staff.objects.filter(isPending=False)
    return render(request,"admins/staffapproved.html",{'staff':obj})

#to approve staff accounts
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

#edit staff details
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
def logout_view(request, *args, **kwargs):
    logout(request)
    # form = LoginForm(request.post or None)
    # context = {
    #     'form':form,
    # }
    return redirect(common.views.login_view)


   

    