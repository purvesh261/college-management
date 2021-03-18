from django import forms
from students.models import Student
from django.contrib.auth.password_validation import validate_password
from staff.models import Staff
from common.models import Assignment
from admins.models import Branch
from django.utils.safestring import mark_safe
import re
import pandas as pd
from students.models import Result


class StaffForm(forms.ModelForm):
    gender_choice=Staff.gender_choices

    designation_choices=Staff.designation_choices

    # branch_choices= Staff.branch_choices
    branches = Branch.objects.values_list('branch_name','code')
    # branch_choices = []
    # for i in branches:
    #     branch_choices.append((i[0],i[0]))

    branch_choices = ((branch[1],branch[0]) for branch in branches)
    # branch_choices = tuple(branch_choices)
    print(branch_choices)

  
    firstName = forms.CharField(label='First Name:',
                widget=forms.TextInput(attrs={"placeholder":"Your first name",
                                             "size":"40",
                                            "class":"text"}))
    middleName = forms.CharField(label='Middle Name:', required=False,
                widget=forms.TextInput(attrs={"placeholder":"Your middle name (optional)",
                                             "size":"40",
                                            "class":"text"}))
    lastName = forms.CharField(label='Last Name:',
                widget=forms.TextInput(attrs={"placeholder":"Your last name",
                                             "size":"40",
                                            "class":"text"}))
    username = forms.CharField(label='Username:', min_length=6, max_length=40,
                widget=forms.TextInput(attrs={"placeholder":"Your Username",
                                             "size":"40",
                                             "class":"text"}))
    employeeId = forms.CharField(label='Employee Id:',min_length=8,max_length=30, 
                widget=forms.TextInput(attrs={"placeholder":"Your employee id",
                                            "size":"30",
                                            "class":"text"}))
    passwd = forms.CharField(label='Password:', min_length=8, max_length=40,
                widget=forms.PasswordInput(attrs={"placeholder":"Create a password",
                                             "size":"40",
                                             "class":"text"}))
    confirm_passwd = forms.CharField(label='Confirm Password:', min_length=8, max_length=40,
                widget=forms.PasswordInput(attrs={"placeholder":"Re-enter your password",
                                             "size":"40",
                                             "class":"text"}))
    mobile=forms.CharField(label='Mobile:', min_length=10, max_length=10,
                widget=forms.TextInput(attrs={"placeholder":"Your mobile number",
                                             "size":"40",
                                             "class":"text"}))
   
    gender=forms.ChoiceField(label="Gender:",choices=gender_choice,
                         widget=forms.Select(attrs={
                             "class":"choice1"})) 

    designation=forms.ChoiceField(label="Designation:",choices=designation_choices,
                          widget=forms.Select(attrs={
                              "class":"choice2",})) 
    branch=forms.ChoiceField(label="Branch:",choices=branch_choices,
                         widget=forms.Select(attrs={
                             "class":"choice3",})) 
    
    # branch = forms.ModelChoiceField(label="Branch:",queryset=Student.objects.values_list('firstName',flat=True),
    #                         widget=forms.Select(attrs={
    #                          "class":"choice3",})) 
                          
    date = forms.DateField(label="Date of Birth:",
                widget=forms.TextInput(attrs={
                    "placeholder":"dd/mm/yyyy",
                    "class":"datefield",
                    'type':"date"
                }))
    email = forms.EmailField(label="Email:",
                widget=forms.EmailInput(attrs={"placeholder":"Your email",
                                             "size":"40",
                                             'type':"email",
                                             "class":"text"}))
    class Meta:
        model = Staff
        fields= [
            'firstName',
            'middleName',
            'lastName',
            'username',
            'employeeId',
            'date',
            'gender',
            'passwd',
            'confirm_passwd',
            'email',
            'mobile',
            'branch',
            'designation',
        ]

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean()
        firstName = str(self.cleaned_data.get("firstName"))
        middleName = str(self.cleaned_data.get("middleName"))
        lastName = str(self.cleaned_data.get("lastName"))
        passwd = str(self.cleaned_data.get("passwd"))
        confirm_passwd = str(self.cleaned_data.get("confirm_passwd"))
        date = str(self.cleaned_data.get("date"))
        username = str(self.cleaned_data.get("username"))
        employee_id = str(self.cleaned_data.get("employeeId"))
        mobile = str(self.cleaned_data.get("mobile"))
        email = str(self.cleaned_data.get("email"))
        branch = str(self.cleaned_data.get("branch"))
        designation = str(self.cleaned_data.get("designation"))
        print(branch,designation)
        # validates first name
        try:
            if not re.search("^[A-Za-z]+$", firstName):
                fn_error = "Not a valid first name."
                raise forms.ValidationError(fn_error)
        except forms.ValidationError as e:
            self.add_error('firstName', e)
        
        # validates middle name
        try:
            if middleName != '' and middleName != None:
                if not re.search("^[A-Za-z]+$", middleName):
                    mn_error = "Not a valid middle name."
                    raise forms.ValidationError(mn_error)
        except forms.ValidationError as e:
            if middleName != '' or middleName != None:
                self.add_error('middleName', e)

        # validates last name
        try:
            if not re.search("^[A-Za-z]+$", lastName):
                ln_error = "Not a valid last name"
                raise forms.ValidationError(ln_error)
            else:
                pass
        except forms.ValidationError as e:
            self.add_error('lastName', e)

        #validates employee id
        try:
            patt = re.match("^(?P<code>[0-9]{2})(?P<year>[0-9]{2})([0-9]{6})$", employee_id)
            if not patt:
                id_error = "Not a valid id"
                raise forms.ValidationError(id_error)
            else:
                branch_id = patt.group('code')
                corrBranch = Branch.objects.filter(code=branch_id)
                if corrBranch:
                    corrBranchName = corrBranch[0].branch_name
                    if corrBranchName != branch:
                        id_error = "Id does not belong to selected branch"
                        raise forms.ValidationError(id_error)
                else:
                    id_error = "Not a valid id"
                    raise forms.ValidationError(id_error)
        except forms.ValidationError as e:
            self.add_error('employeeId',e)

        # validates date of birth
        try:
            timestamp = pd.to_datetime(date,dayfirst=True)
            today = pd.to_datetime('today').normalize()
            difference = today - timestamp
            age = difference.days / 365
            if age < 16:
                date_error = "You must be at least 16 years</br>old to create an account."
                date_error = mark_safe(date_error)
                raise forms.ValidationError(date_error)
        except forms.ValidationError as e:
            self.add_error('date', e)

        # validates password strength
        try:
            if not re.search('^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$',passwd):
                errormsg = mark_safe('Password must contain at least</br>1 upper case letter,</br>1 lower case letter,</br>1 digit and 1 special symbol.')
                raise forms.ValidationError(errormsg)
        except forms.ValidationError as e:
            self.add_error('passwd', e)

        # checks if password and confirm password are same
        try:
            if passwd != confirm_passwd:
                raise forms.ValidationError('Passwords do not match')
        except forms.ValidationError as e:
            self.add_error('confirm_passwd', e)

        # validates username
        try:
            username_not_valid = False
            if not re.search(r'^\w+$', username):
                username_error = mark_safe("Username can only contain alphanumeric</br>characters and underscore.")
                username_not_valid = True
                raise forms.ValidationError(username_error)
        except forms.ValidationError as e:
            self.add_error('username', e)

        # If username is valid, checks if username already exists
        if username_not_valid == False:
            try:
                if Student.objects.filter(username=username).exists() or Staff.objects.filter(username=username).exists():
                    username_exists_error = username + ' is already taken.</br>Select a different username.'
                    username_exists_error = mark_safe(username_exists_error)
                    raise forms.ValidationError(username_exists_error)
            except forms.ValidationError as e:
                self.add_error('username', e)
        
         # validates mobile number
        try:
            mobile_not_valid = False
            if not re.search("^[0-9]{10}$",mobile):
                mobile_error = "Not a valid phone number"
                mobile_not_valid = True
                raise forms.ValidationError("Not a valid phone number")
        except forms.ValidationError as e:
            self.add_error('mobile', e)
        
        # if mobile is valid, checks if mobile is already used
        if mobile_not_valid == False:
            try:
                if Student.objects.filter(mobile=mobile).exists() or Staff.objects.filter(mobile=mobile).exists():
                    mobile_exists_error = 'This mobile number is already</br>associated with an account.'
                    mobile_exists_error = mark_safe(mobile_exists_error)
                    raise forms.ValidationError(mobile_exists_error)
            except forms.ValidationError as e:
                self.add_error('mobile', e)
        
        # checks if there is already a head for selected department
        if designation == "Head of Department":
            print('entered')
            try:
                print("tried")
                if Staff.objects.filter(designation="Head of Department",branch=branch).exists():
                    hod_exists_error = branch + ' already has a</br>Head of Department.'
                    hod_exists_error = mark_safe(hod_exists_error)
                    print("raising error")
                    raise forms.ValidationError(hod_exists_error)
            except forms.ValidationError as e:
                print("adding error")
                self.add_error('designation', e)

        # validates email
        try:
            email_not_valid = False
            if not re.search('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', email):
                email_error = "Not a valid email"
                email_not_valid = True
                raise forms.ValidationError(email_error)
        except forms.ValidationError as e:
            self.add_error('email', e)
        
        # if email is valid, checks if email is already used

        if email_not_valid == False:
            try:
                if Student.objects.filter(email=email).exists() or Staff.objects.filter(email=email).exists():
                    email_exists_error = 'This email is already associated</br>with an account'
                    email_exists_error = mark_safe(email_exists_error)
                    raise forms.ValidationError(email_exists_error)
            except forms.ValidationError as e:
                self.add_error('email', e)
            else:
                return cleaned_data
        else:
            return cleaned_data


#for student result
class resultform(forms.ModelForm):
    class Meta:
        model=Result
        fields= [
            'account_id',
            'enrolment',
            'branch',
            'sem',
            'course_name',
            'marks',
            'exam',
            ]

class editresultform(forms.ModelForm):
    class Meta:
        model=Result
        fields=[
            'account_id',
            'enrolment',
            'sem',
            'course_name',
            'marks',
        ]
class CreateAssignmentForm(forms.ModelForm):
    title = forms.CharField(label='Title:', min_length=3, max_length=160,
                widget=forms.TextInput(attrs={"placeholder":"Enter a title",
                                             "size":"40",
                                             "class":"text"}))
    
    description = forms.CharField(label='Description:',max_length=500,required=False,
                widget=forms.Textarea(attrs={"placeholder":"Enter Description",
                                             "size":"40",
                                             "class":"text desc-box",
                                             "height":"5",
                                             "width":"100",
                                             "name":"description"}))
                                             
    start_date = forms.DateField(label="Start Date:",required=False,
                widget=forms.TextInput(attrs={
                    "placeholder":"dd/mm/yyyy",
                    "class":"datefield",
                    'type':"date"
                }))
    
    end_date = forms.DateField(label="End Date:",required=False,
                widget=forms.TextInput(attrs={
                    "placeholder":"dd/mm/yyyy",
                    "class":"datefield",
                    'type':"date"
                }))

    assignment_file = forms.FileField(label="Attachment:",required=False,
                widget=forms.FileInput(attrs={
                    'type':'file',
                    'class':'file',
                    'name':'file',
                }))

    class Meta:
        model = Assignment
        fields = [
            'title',
            'description',
            'start_date',
            'end_date',
            'assignment_file',
        ]

    def clean(self,*args,**kwargs):
        cleaned_data = super().clean()
        title = str(self.cleaned_data.get('title'))
        startDate = self.cleaned_data.get('start_date')
        endDate = self.cleaned_data.get('end_date')

        try:
            if not re.search('^[A-Za-z0-9\s]+$',title):
                raise forms.ValidationError("Not a valid title")
        except forms.ValidationError as e:
            self.add_error('title', e)

        try:
            if (startDate and endDate) and (startDate > endDate):
                raise forms.ValidationError("Start date is greater than end date")
        except forms.ValidationError as e:
            self.add_error('end_date', e)
        
        return cleaned_data

    #     if assignment_file:
    #         ext = os.path.splitext(assignment_file.name)[1]  # [0] returns path+filename
    #         valid_extensions = ['.pdf']
    #         try:
    #             if not ext.lower() in valid_extensions:
    #                 raise forms.ValidationError('Unsupported file extension.')
    #         except forms.ValidationError as e:
    #             self.add_error('assignment_file',e)

    #     return cleaned_data
