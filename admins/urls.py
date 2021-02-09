from django.urls import path, re_path
from .views import *

app_name = 'college-admin'
urlpatterns = [
    path('home/', admins_home_view, name="home"),
    path('students/', admins_students_view, name="students"),
    path('staff/', admins_staff_view, name="staff"),
    path('courses/', admins_courses_view, name="courses"),
    path('profile/', admins_profile_view, name="profile"),

    path('logout/',logout_view, name='logout'),

    path('announcement/',admin_announcement,name='adminannoucement'),
    #path('announcement-done/',announcement_done,name='annoucementdone'),
    
    path('all-announcement/',admin_add_announcement,name='adminannoucement'),
    
    #path('home/', admins_home_announcement, name="home"),

    path('edit-announcement/<int:account_id>',admins_announcement_edit,name='announcemenedit'),
    #path('update-announcement/<int:account_id>/',edit_announcement,name='announcementupdate'),

    path('delete-announcement/<int:account_id>',staff_delete_view,name='staffannouncementdelete'),




    path('student-account-pending-details/',admins_student_pending_detail_view,name='studentsdetails'),
    path('student-account-approved-details/',admins_student_approved_detail_view,name='studentsdetails2'),

    #for edit
    path('approve-student/<int:account_id>',admins_student_approve,name='studentapprove'),
    #path('approved-student/<int:account_id>/',approve_student,name='studentapproved'),

    path('edit-student/<int:account_id>',admins_student_edit,name='studentedit'),
    #path('update-student/<int:account_id>/',edit_student,name='studentupdate'),


    #for staff
    path('staff-account-pending-details/',admins_staff_pending_detail_view,name='staffdetails'),
    path('staff-account-approved-details/',admins_staff_approved_detail_view,name='staffdetails2'),

    #for edit
    path('approve-staff/<int:account_id>/',admins_staff_approve,name='staffapprove'),
    #path('approved-staff/<int:account_id>/',approve_staff,name='staffapproved'),

    path('edit-staff/<int:account_id>/',admins_staff_edit,name='staffedit'),
    #path('update-staff/<int:account_id>/',edit_staff,name='staffupdate'),


    # for admin profile edit
    path('edit-profile/<int:account_id>/',admins_profile_edit,name='adminedit'),
    #path('update-profile/<int:account_id>/',edit_profile,name='adminupdate'),

    # to create a new branch
    path('create-branch/', create_branch_view, name="create-branch"),

    re_path(r'^courses/(?P<branch_code>[0-9]{2})/$', branch_view, name="branch-details"),
    re_path(r'courses/(?P<branch_code>[0-9]{2})/edit/$', edit_branch_view, name="edit-branch"),
    re_path(r'courses/(?P<course_code>[0-9]{2})/add-course/$', add_course_view, name="add-course"),


]
