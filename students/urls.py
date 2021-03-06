from django.urls import path,re_path
from .views import *

app_name = 'students'
urlpatterns = [
    path('home/', student_home_view, name="home"),
    path('courses/', courses_redirect_view, name="courses_redirect_view"),
    path('courses/mt/', no_course_view, name="no_course_view"),
    re_path(r'^courses/(?P<course_code>[0-9]{10})/$', student_courses_view, name="courses_view"),
    re_path(r'^courses/(?P<course_code>[0-9]{10})/assignments/$', all_assignments_view, name="all_assignments"),
    re_path(r'^assignments/(?P<course_code>[0-9]{10})/(?P<assignment_id>[0-9]{10})/$', assignment_details_view, name="assignment-details"),
    # path('results/',student_results_view, name="results"),
    path('attendance/', attendance_redirect_view, name="attendance_redirect_view"),
    re_path(r'^attendance/(?P<course_code>[0-9]{10})/$',student_attendance_view, name="attendance"),
    path('profile/',student_profile_view, name="profile"),
    path('edit-profile/<int:account_id>',student_profile_edit,name='profile-edit'),
    path('results/', courses_redirect_view, name="courses_redirect_view"),
    path('results/mt/', no_course_view, name="no_course_view"),
 
    re_path(r'^results/(?P<course_code>[0-9]{10})/$', student_results_view, name="courses_view"),
    path('logout/',logout_view, name='logout'),


    re_path(r'^courses/(?P<course_code>[0-9]{10})/doubts$', student_courses_doubt, name="doubt"),


]