from django.conf.urls import url
from django.contrib import admin
# from django.contrib.auth import logout
from django.urls import include, path
from dashboard.views import dashboard, tasklist, teamwork,admin,workload, taskdetails, tasknew,newuser,newunits,newrole
from login.views import logout

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('tasklist/', tasklist, name='tasklist'),
    path('teamwork/', teamwork, name='teamwork'),
    path('workload/', workload, name='workload'),
    path('taskdetails/', taskdetails, name='taskdetails'),
    path('tasknew/', tasknew, name='tasknew'),
    path('newuser/', newuser, name='newuser'),    
    path('newunits/', newunits, name='newunits'),
    path('newrole/', newrole, name='newrole'),
    path('admin/', admin, name='admin'),
    path('logout/',logout, name='logout'),
    
    
]