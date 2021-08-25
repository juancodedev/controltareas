from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from login import views

urlpatterns = [
    # path('dashboard/', include('dashboard.urls')),
    path('',views.login, name='login'),
    path('forgotPassword',views.forgotPassword, name='forgotPassword'),
    path('lockscreen',views.lockscreen, name='lockscreen'),
    path('recoverPassword',views.recoverPassword, name='recoverPassword'),
]