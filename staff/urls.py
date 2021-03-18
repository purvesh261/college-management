from django.urls import path,re_path
from .views import *

app_name = 'staff'
urlpatterns = [
    path('home/', staff_home_view, name="home"),
    # path('courses/',staff_courses_view, name="courses"),
    path('results/',staff_results_view, name="results"),
    path('attendance/',staff_attendance_view, name="attendance"),
    path('profile/',staff_profile_view, name="profile"),


    path('announcement/',staff_announcement,name='adminannoucement'),
    #path('announcement-done/',staff_announcement_done,name='annoucementdone'),
    
    path('all-announcement/',staff_add_announcement,name='adminannoucement'),
    
    #path('home/', admins_home_announcement, name="home"),

    path('edit-announcement/<int:account_id>',staff_announcement_edit,name='announcemenedit'),
    #path('update-announcement/<int:account_id>/',edit_announcement,name='announcementupdate'),

    path('delete-announcement/<int:account_id>',staff_delete_view,name='staffannouncementdelete'),


    #path('add-result/<int:account_id>',add_result,name='addresult'),

    re_path(r'^results/(?P<branch_code>[0-9]{2})/$', result_view, name="sem-details"),
    re_path(r'results/(?P<branch_code>[0-9]{2})/(1|2|3|4|5|6|7|8)/add-result/$', sem_result, name="sem-result"),
    re_path(r'results/(?P<branch_code>[0-9]{2})/(1|2|3|4|5|6|7|8)/add-result/(?P<account_id>[0-9]{10})/$', add_result, name="add-result"),
    re_path(r'results/(?P<branch_code>[0-9]{2})/(1|2|3|4|5|6|7|8)/add-result/(Internal-1|Internal-2|Internal)', student_internal_results, name="sem-result"),
    re_path(r'results/(?P<branch_code>[0-9]{2})/(1|2|3|4|5|6|7|8)/edit-result/(?P<account_id>[0-9]{10})', student_result_edit, name="sem-result"),

    #re_path(r'courses/(?P<course_code>[0-9]{2})/add-course/$', add_course_view, name="add-course"),

    path('courses/', courses_redirect_view, name="courses_redirect_view"),
    path('courses/mt/', no_course_view, name="no_course_view"),
    re_path(r'^courses/(?P<course_code>[0-9]{10})/$', staff_courses_view, name="courses_view"),
    re_path(r'^courses/(?P<course_code>[0-9]{10})/create-assignment$', create_assignment_view, name="create-assignment"),
    re_path(r'^assignments/(?P<course_code>[0-9]{10})/(?P<assignment_id>[0-9]{10})/$', manage_assignment_view, name="manage_assignment"),
    re_path(r'^courses/(?P<course_code>[0-9]{10})/assignments/$', view_assignments_view, name="assignments-view"),
    re_path(r'^assignments/delete/(?P<assignment_id>[0-9]{10})/$', delete_assignment_view, name="delete_assignment"),
]
