from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from login import views

urlpatterns = [
    path('forgotPassword',views.forgotPassword, name='forgotPassword'),
    path('lockscreen',views.lockscreen, name='lockscreen'),
    path('recoverPassword',views.recoverPassword, name='recoverPassword'),
    path('',views.Login, name='login'),
    path('validate',views.validate, name='validate'),
    
]