from django.shortcuts import render,redirect
from datetime import datetime
from common.announcementform import announcementform
from common.models import Announcement
from staff.forms2 import editforms2
from common.methods import id_generator
from django.http import HttpResponse
from  . import forms
from django.contrib import messages
from .models import Branch
from staff.models import Staff
from common.models import  Course
from students.models import Student



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

    
    


def staff_courses_view(request, *args, **kwargs):
    return render(request, "staff/courses.html")

def staff_attendance_view(request, *args, **kwargs):
    return render(request, "staff/attendance.html")

def staff_results_view(request, *args, **kwargs):
    branches = Branch.objects.all().order_by('branch_name')
    context = {
        'branches' : branches,
            }
    return render(request, "staff/results.html",context)

def result_view(request, *args,**kwargs):
    branches = Branch.objects.all().order_by('branch_name')
    
    context = {
        'branches' : branches,
            }
    return render(request,"staff/semresult.html")

def staff_profile_view(request, *args, **kwargs):
    return render(request, "staff/profile.html")


