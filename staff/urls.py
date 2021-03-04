from django.urls import path,re_path
from .views import *

app_name = 'staff'
urlpatterns = [
    path('home/', staff_home_view, name="home"),
    path('courses/',staff_courses_view, name="courses"),
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



    re_path(r'^results/(?P<branch_code>[0-9]{2})/$', result_view, name="sem-details"),
    #re_path(r'courses/(?P<branch_code>[0-9]{2})/edit/$', edit_branch_view, name="edit-branch"),
    #re_path(r'courses/(?P<course_code>[0-9]{2})/add-course/$', add_course_view, name="add-course"),
]
