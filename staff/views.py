from django.shortcuts import render,redirect,get_object_or_404
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
from staff.forms import resultform
from students.models import Result
from staff.forms import editresultform

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

    displaydata=Student.objects.filter(sem=s1,branch=binfo,isPending=False) #fetching the student by filtering the data
    print(displaydata) #print filtered data of students
    return render(request,"staff/result.html",{'student':displaydata,'branch':b1.branch_name,'sem':s1})


def add_result(request,account_id,branch_code):
    b1=get_object_or_404(Branch,code=branch_code)
    sem=(request.path.split('/')) #split the whole url /
    s1=sem[4] #fetching semester
    # cd=sem[3] #fetching branch code
    # cname=Course.objects.filter(semester=s1,branch=cd)
    # print(cname)
    # subname=[]
    # for i in cname:
    #     subname.append(i.course_name)
    #     print(i.course_name)
    # #subname=cname.course_name
    # #print('cname',cname.course_name)
    # print('subname',subname[0]) #subject name
    # #print(b2)
    # #print('s1',s1)
    # sname="h1,h2"
    displaydata=Student.objects.get(account_id=account_id)
    initial_dict={
        'account_id':id_generator,
        'enrolment':displaydata.enrolment,
        'branch':displaydata.branch,
        'sem':s1,
        
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
            return HttpResponse(messages)
    
    print('post')
    return render(request,"staff/addresult.html",{'resultform1':resultform1,'sem':s1,'displaydata':displaydata})

#staff-student internals result
def student_internal_results(request,branch_code,*args):
    url=(request.path.split('/')) #split the whole url /
    s1=url[4] #to fetch the sem from url
    print('sem',url[4]) #print the extracted sem from url

    b1=get_object_or_404(Branch,code=branch_code) #get the branch bane using branch code
    b2=b1.branch_name #get the branch name
    print(b2) #print branch name

    branch_info=b2.split(' ') #model acceptes Short form branch name eg(CE)so using split
    print(branch_info) #print splited branch_info

    binfo=branch_info[0][0]+branch_info[1][0] #fetching short form
    print(binfo) #printing short form

    exam=url[6]
    print('examname',exam)

    displaydata=Result.objects.filter(sem=s1,branch=binfo,exam=exam) #fetching the student by filtering the data
    print(displaydata) #print filtered data of students
    return render(request,"staff/stdresult.html",{'student':displaydata,'branch':b1.branch_name,'examname':exam})


def student_result_edit(request,branch_code,account_id,*args):
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
            return redirect("../add-result")
            #return render(request,'common/announcementedit.html',{'editdata':updatedata})
        else:
            return HttpResponse(messages)    
    return render(request,'staff/editresult.html',{'editdata':displaydata})



def staff_profile_view(request, *args, **kwargs):
    return render(request, "staff/profile.html")


