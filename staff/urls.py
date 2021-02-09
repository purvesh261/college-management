from django.urls import path
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

]