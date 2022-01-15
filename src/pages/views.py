from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import auth
from django.views.generic.base import RedirectView
from pages.models import Student , Attendance,AttendanceDetail,MarksDetail,Marks
from django.contrib.auth.decorators import login_required
from django.http import *
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout

Dict={'student': None }

# Create your views here.
@login_required(login_url='login')
def homeView(request,*args,**kwargs): 
    return render(request,"dashboard/index.html", {})

def login_user(request):
    if request.method == 'POST':
        # Process the request if posted data are available
        username = request.POST['username']
        password = request.POST['password']
        # Check username and password combination if correct
        user = authenticate(username=username, password=password)
        if user is not None:
            # Save session as cookie to login the user
            login(request, user)
            # Success, now let's login the user.
            return redirect(request, '/')
        else:
            # Incorrect credentials, let's throw an error to the screen.
            return render(request, 'loginform.html', {'error_message': 'Incorrect username and / or password.'})
    else:
        # No post data availabe, let's just show the page to the user.
        return render(request, 'loginform.html')         


@login_required(login_url='login')
def AttendanceView(request):
    studentobj=AttendanceDetail.objects.filter(student_id=request.user.id)
    totatt=studentobj.count()
    student=studentobj[0]
    presentatt=0
    absentatt=0
    for item in studentobj:
        if item.status == True:
            presentatt += 1
        absentatt=totatt-presentatt
    totalcourseatt=AttendanceDetail.objects.filter(student_id=request.user.id).filter(attendance__course_id='DC101')
    totalcat=totalcourseatt.count()
    coursep =0
    coursea=0
    for item in totalcourseatt:
        if item.status == True:
            coursep += 1
        coursea=totalcat-coursep
       
    context={
    'objs':studentobj,
    'obj':student,
    'total':totatt,
    'present':presentatt,
    'absent':absentatt,
    'totcourse':totalcat,
    'coursep':coursep,
    'coursea':coursea,
    'queryset':totalcourseatt
    }
    return render (request,'attendance.html',context)

@login_required(login_url='login')
def Marksview(request):
    studentobj=MarksDetail.objects.filter(student_id=request.user.id)
    markscour=MarksDetail.objects.filter(student_id=request.user.id).filter(marks__course_id='DC101')[0]
    totalscored=markscour.mst1+markscour.mst2+markscour.end_sem
    context={
        'stobj':studentobj[0],
        'obj':studentobj,
        'coursemst1':markscour,
        'total':totalscored
    }
    return render(request,'marks.html',context)

@login_required(login_url='login')
def Studentview(request):
    st=Student.objects.get(user_id=request.user.id)
    context={
        'student':st
    }
    return render(request,"student.html",context)



