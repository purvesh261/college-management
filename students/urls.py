from django.urls import path,re_path
from .views import *

app_name = 'students'
urlpatterns = [
    path('home/', student_home_view, name="home"),
    path('courses/',student_courses_view, name="courses"),
    path('attendance/',student_attendance_view, name="attendance"),
    path('profile/',student_profile_view, name="profile"),
    path('edit-profile/<int:account_id>',student_profile_edit,name='profile-edit'),





    path('results/', courses_redirect_view, name="courses_redirect_view"),
    path('results/mt/', no_course_view, name="no_course_view"),
 
    re_path(r'^results/(?P<course_code>[0-9]{10})/$', student_results_view, name="courses_view"),

]