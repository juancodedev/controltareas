from django.conf.urls import url
from django.contrib import admin
# from django.contrib.auth import logout
from django.urls import include, path
from dashboard.views import dashboard, tableTask
from login.views import logout

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('tableTask/', tableTask, name='tableTask'),
    path('logout/',logout, name='logout'),
]