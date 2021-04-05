from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from common.models import Course, Assignment
from datetime import datetime
import collections

# Create your views here.

def student_home_view(request, *args, **kwargs):
    return render(request, "students/home.html")


def courses_redirect_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        if not request.session.get('enrolment'):
            username = request.user.username
            user = Student.objects.get(username=username)
            request.session['enrolment'] = user.enrolment
            print(username, user)

        user = Student.objects.get(enrolment=request.session['enrolment'])
        courses = Course.objects.filter(branch=user.branch, semester=user.sem)
        courseList = {}
        for course in courses:
            if courseList.get(course.semester):
                courseList[course.semester].append((course.course_id,course.course_name))
            else:
                courseList[course.semester] = [(course.course_id,course.course_name)]
        if list(courseList):
            course_code = list(courseList.values())[0][0][0]
        else:
            course_code = 'mt'

        return redirect("./" + course_code)
    else:
        print("OK!!!!!")

def no_course_view(request, *args,**kwargs):
    context = {
        'courses': []
    }
    return render(request, "students/courses.html", context)

def student_courses_view(request, course_code, *args, **kwargs):
    if request.user.is_authenticated:
        if not request.session.get('enrolment'):
            username = request.user.username
            user = Student.objects.get(username=username)
            request.session['enrolment'] = user.enrolment

        user = Student.objects.get(enrolment=request.session['enrolment'])
        selectedCourse = get_object_or_404(Course, course_id=course_code)

        if user.branch == selectedCourse.branch and user.sem == selectedCourse.semester:
            courses = Course.objects.filter(branch=user.branch, semester=user.sem)
            courseList = {}
            for course in courses:
                if courseList.get(course.semester):
                    courseList[course.semester].append((course.course_id,course.course_name))
                else:
                    courseList[course.semester] = [(course.course_id,course.course_name)]
            courseList = collections.OrderedDict(sorted(courseList.items()))
            assignments = Assignment.objects.filter(course=selectedCourse).order_by('start_date').reverse()
            ongoingAssignments = []
            for assignment in assignments:
                if assignment.start_date > datetime.date(datetime.today()):
                    continue
                elif assignment.start_date <= datetime.date(datetime.today()) and assignment.end_date == None:
                    ongoingAssignments.append(assignment)
                elif assignment.start_date <= datetime.date(datetime.today()) and assignment.end_date >= datetime.date(datetime.today()):
                    ongoingAssignments.append(assignment)
                elif assignment.start_date < datetime.date(datetime.today()) and assignment.end_date < datetime.date(datetime.today()):
                    break

            context = {
            'courses' : courseList,
            'selectedCourse' : selectedCourse,
            'assignments' : ongoingAssignments,
            }
            return render(request, "students/courses.html", context)
        else:
            return render(request, "students/no_permission.html")

    return render(request, "students/courses.html")

def student_attendance_view(request, *args, **kwargs):
    return render(request, "students/attendance.html")

def student_results_view(request, *args, **kwargs):
    return render(request, "students/results.html")

def student_profile_view(request, *args, **kwargs):
    return render(request, "students/profile.html")