from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password, UserAttributeSimilarityValidator
from django.contrib.auth import authenticate, login, logout
from students.forms import StudentForm
from staff.forms import StaffForm
from .forms import LoginForm
from students.models import Student
from staff.models import Staff
# from common.models import AppUser
from .methods import id_generator

#announcements
from common.models import Announcement
# Create your views here.



def login_view(request, *args, **kwargs):
    if not request.user.is_anonymous:
        userEmail = request.user.email
        print(userEmail,"2")
        user = Staff.objects.filter(email=userEmail, isPending=False)
        if user:
            print(user)
            if user[0].isAdmin:
                print(user,"2")
                return redirect('../college-admin/home/')
            else:
                return redirect('../staff/home/')
        else:
            user = Student.objects.filter(email=userEmail, isPending=False)
            if user:
                return redirect('../students/home/')
            else:
                print(user,"3")
                return render(request, "common/no_permission.html")
        
    next_url = request.POST.get('next')

    #announcement
    announcement_data=reversed(Announcement.objects.all())

    if request.method == 'POST':
        form = LoginForm(request.POST or None)
        if form.is_valid():
            details = form.cleaned_data
            username_input = details['username']
            passwd_input = details['passwd']

            try:
                user = authenticate(request,username=username_input,
                            password=passwd_input)
                if user is None:
                    raise ValidationError("Incorrect username or password")
            except ValidationError as e:
                form.add_error('passwd',e)
                return render(request, 'common/home.html', {'form': form, 'announcement_data':announcement_data})

            if user is not None:
                staffMember = Staff.objects.filter(username=username_input).first()
                if staffMember:
                    pending = getattr(staffMember,'isPending')
                    if pending:
                        return redirect('../pending-account')

                    category = getattr(staffMember,'category')
                    request.session['category'] = category
                    login(request,user)
                    if staffMember.isAdmin:
                        if next_url:
                            return redirect(next_url)
                            
                        return redirect("../college-admin/home")
                    elif category in ['Faculty', 'Staff', 'Head of Department']:
                        return redirect("../staff/home")
                
                studentMember = Student.objects.filter(username=username_input).first()
                if studentMember:
                    pending = getattr(studentMember,'isPending')
                    if pending:
                        return redirect('../pending-account')

                    request.session['category'] = 'Student'
                    login(request,user)
                    return redirect("../students/home")
                
            else:
                return render(request, 'common/home.html', {'form': form,'announcement_data':announcement_data})

        else:
            form = LoginForm()
            return render(request, 'common/home.html', {'form': form,'announcement_data':announcement_data})
    else:
        form = LoginForm()
        return render(request, 'common/home.html', {'form': form,'announcement_data':announcement_data})
    #return render(request,'common/home.html',{'announcement_data':announcement_data})

    
def admin_login(request,*args,**kwargs):
    return render(request,"admins/home.html")

def registration_view(request,*args,**kwargs):
    if not request.user.is_anonymous:
        
        userEmail = request.user.email
        user = Staff.objects.filter(email=userEmail, isPending=False)
        if user:
            if user[0].isAdmin:
                return redirect('../college-admin/home/')
            else:
                return redirect('../staff/home/')
        else:
            user = Student.objects.filter(email=userEmail, isPending=False)
            if user:
                return redirect('../students/home/')
            else:
                return render(request, "common/no_permission.html")
    return render(request,"common/register.html")

def account_created_view(request,*args,**kwargs):
    if not request.user.is_anonymous:
        print('whatt')
        userEmail = request.user.email
        user = Staff.objects.filter(email=userEmail, isPending=False)
        if user:
            if user[0].isAdmin:
                return redirect('../college-admin/home/')
            else:
                return redirect('../staff/home/')
        else:
            user = Student.objects.filter(email=userEmail, isPending=False)
            if user:
                return redirect('../students/home/')
            else:
                return render(request, "common/no_permission.html")
    return render(request,"common/account_created.html")

def student_registration(request,*args,**kwargs):
    if not request.user.is_anonymous:
        userEmail = request.user.email
        user = Staff.objects.filter(email=userEmail, isPending=False)
        if user:
            if user[0].isAdmin:
                return redirect('../college-admin/home/')
            else:
                return redirect('../staff/home/')
        else:
            user = Student.objects.filter(email=userEmail, isPending=False)
            if user:
                return redirect('../students/home/')
            else:
                return render(request, "common/no_permission.html")
    if request.method == "POST":
        form = StudentForm(request.POST or None)
        if form.is_valid():
            details = form.cleaned_data
            new_passwd = details['passwd']
            new_username = details['username']
            new_fName = details['firstName']
            new_mName = details['middleName']
            new_lName = details['lastName']
            new_email = details['email']
            new_enrolment = details['enrolment']
            new_dob = details['date']
            new_gender = details['gender']
            new_mobile = details['mobile']
            new_branch = details['branch']
            new_sem = details['sem']
            new_account_id = id_generator()
            
            try:
                validate_password(new_passwd, form)
            except ValidationError as e:
                form.add_error('passwd', e)
                return render(request, "common/studentregistration.html", {'form': form})

            # try:
            #     user_credentials = [new_username, new_fName, new_lName, new_mName, new_mobile, new_enrolment]
            #     for item in user_credentials:
            #         if item.lower() in new_passwd.lower():
            #             raise ValidationError('Password too similar to credentials...')
            # except ValidationError as e:
            #     form.add_error('passwd', e)
            #     return render(request, "common/studentregistration.html", {'form': form})

            newStudent = Student(firstName=str(new_fName.capitalize()),
                        middleName=str(new_mName.capitalize()),
                        lastName=str(new_lName.capitalize()),
                        username=str(new_username),
                        passwd=str(new_passwd),
                        account_id=str(new_account_id),
                        enrolment=str(new_enrolment),
                        date=str(new_dob),
                        mobile=str(new_mobile),
                        branch=str(new_branch),
                        sem=str(new_sem),
                        email=str(new_email.lower()),
                        gender=str(new_gender),
                        isPending=True
                        )

            newUser = User.objects.create_user(
                        username=str(new_username),
                        password=str(new_passwd),
                        first_name=str(new_fName.capitalize()),
                        last_name=str(new_lName.capitalize()),
                        email=str(new_email.lower()),
            )

            newUser.save()
            newStudent.save()
            return redirect("../pending-account")
    else:
        form = StudentForm(request.POST or None)
        for field in form.errors:
                form[field].field.widget.attrs['class'] += 'error'


    return render(request,"common/studentregistration.html",{'form':form})

def pending_account_view(request,*args,**kwargs):
    if not request.user.is_anonymous:
        userEmail = request.user.email
        user = Staff.objects.filter(email=userEmail, isPending=False)
        if user:
            if user[0].isAdmin:
                return redirect('../college-admin/home/')
            else:
                return redirect('../staff/home/')
        else:
            user = Student.objects.filter(email=userEmail, isPending=False)
            if user:
                return redirect('../students/home/')
            else:
                return render(request, "common/no_permission.html")
    logout(request)
    return render(request,"common/pending_account.html")

def staff_registration(request,*args,**kwargs):
    if not request.user.is_anonymous:
        userEmail = request.user.email
        user = Staff.objects.filter(email=userEmail, isPending=False)
        if user:
            if user[0].isAdmin:
                return redirect('../college-admin/home/')
            else:
                return redirect('../staff/home/')
        else:
            user = Student.objects.filter(email=userEmail, isPending=False)
            if user:
                return redirect('../students/home/')
            else:
                return render(request, "common/no_permission.html")
                
    if request.method == "POST":
        form = StaffForm(request.POST or None)
        if form.is_valid():
            details = form.cleaned_data
            new_username = details['username']
            new_fName = details['firstName']
            new_mName = details['middleName']
            new_lName = details['lastName']
            new_empId = details['employeeId']
            new_passwd = details['passwd']
            new_email = details['email']
            new_dob = details['date']
            new_gender = details['gender']
            new_mobile = details['mobile']
            new_branch = details['branch']
            new_designation = details['designation']
            new_isAdmin = False
            new_isPending = True
            new_account_id = id_generator()

            #sets category of user
            new_category = ''
            if new_designation in ['Professor', 'Assistant Professor']:
                new_category = 'Faculty'
            elif new_designation == 'Head of Department':
                new_category = 'Head of Department'
            elif new_designation in ['Lab Instructor','Lab Assistant']:
                new_category = 'Staff'
            

            # find the number of users in staff
            staff_count = int(Staff.objects.count())

            # if there are no staff members, the first created user will be admin
            if staff_count < 1:
                new_isAdmin = True
                new_category = 'Admin'
                new_isPending = False

            try:
                validate_password(new_passwd, form)
            except ValidationError as e:
                form.add_error('passwd', e)
                return render(request, "common/staffregistration.html", {'form': form})
            

            newStaff = Staff(
                        firstName=str(new_fName.capitalize()),
                        middleName=str(new_mName.capitalize()),
                        lastName=str(new_lName.capitalize()),
                        username=str(new_username),
                        employee_id=str(new_empId),
                        passwd=str(new_passwd),
                        account_id=str(new_account_id),
                        date=str(new_dob),
                        mobile=str(new_mobile),
                        branch=str(new_branch),
                        email=str(new_email.lower()),
                        gender=str(new_gender),
                        designation=str(new_designation),
                        isAdmin=new_isAdmin,
                        isPending=new_isPending,
                        category=str(new_category)
                        )
            
            # newUser = AppUser(
            #             firstName=str(new_fName.capitalize()),
            #             lastName=str(new_lName.capitalize()),
            #             username=str(new_username),
            #             passwd=str(new_passwd),
            #             email=str(new_email.lower()),
            #             category=str(new_category),
            #             isAdmin=new_isAdmin,
            #             isPending=new_isPending
            # )

            newUser = User.objects.create_user(
                        username=str(new_username),
                        password=str(new_passwd),
                        first_name=str(new_fName.capitalize()),
                        last_name=str(new_lName.capitalize()),
                        email=str(new_email.lower()),
            )

            # newDjangoUser.save()
            newStaff.save()
            newUser.save()

            if new_isPending:
                return redirect("../pending-account")
            else:
                return redirect("../account-created")
    else:
        form = StaffForm(request.POST or None)
        for field in form.errors:
                form[field].field.widget.attrs['class'] += 'error'

    return render(request,"common/staffregistration.html",{'form':form})

